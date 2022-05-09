from antlr4 import *
from heapq import heappush, heappop
from typing import Dict, Tuple

from src.abstract_syntax_tree import *
from src.implementation_components import *
from src.parse_hctl_formula.parser_wrapper_hctl import parse_to_tree


# minimal number of propositions in a model to activate certain optimisations
MIN_NUM_PROPS_TO_OPTIMIZE = 25


# check whether given node corresponds to EX operation
def is_node_ex_to_optimize(node, var: str) -> bool:
    return type(node) == UnaryNode and node.category == NodeType.EX and var in node.subform_string


# check whether given node corresponds to OR operation
def is_node_union(node) -> bool:
    return type(node) == BinaryNode and node.category == NodeType.OR


# checks if we can get to some EX node if we travel only through the union nodes
# this is for optimizing inner EX in hybrid formulas (var is variable bound by hybrid operator)
def check_descendants_for_ex(node, var: str) -> bool:
    # if we came to EX node (whose subformula includes the var), we are done
    if is_node_ex_to_optimize(node, var):
        return True

    # another chance is to find the goal in at least one child of an Union node
    if is_node_union(node):
        return check_descendants_for_ex(node.left, var) or check_descendants_for_ex(node.right, var)

    # otherwise there is no point in optimizing
    return False


"""
returns string representing the same subformula, but with canonical var names (var0, var1...)
We suppose the subform is:
    1) syntactically VALID hctl formula, minimized by minimize_number_of_state_vars function
    2) with NO EXCESS SPACES and includes all PARENTHESES
for example "(3{x}:(3{xx}:((@{x}:((~{xx})&&(AX{x})))&&(@{xx}:(AX{xx})))))" is valid input
any node.subform_string field should be OK to use
"""
def canonize_subform(subform, idx, translate_dict, canonical, stack_len=0) -> int:
    while idx < len(subform):
        char = subform[idx]
        if char == '(':
            canonical.append(char)
            idx = canonize_subform(subform, idx + 1, translate_dict, canonical, stack_len)
        elif char == ')':
            canonical.append(char)
            return idx + 1
        # we ust distinguish situations when 3 is existential and when it is part of some prop name
        elif char == '!' or (char == '3' and idx + 1 < len(subform) and subform[idx + 1] == '{'):
            idx += 2  # move to the beginning of the var name
            var_name = []
            while subform[idx] != '}':
                var_name.append(subform[idx])
                idx += 1
            idx += 2
            translate_dict[''.join(var_name)] = f"var{stack_len}"
            canonical.extend([char, '{'] + list(translate_dict[''.join(var_name)]) + ['}', ':'])
            stack_len += 1
        elif char == '{':
            idx += 1  # move to the beginning of the var name
            var_name = []
            while subform[idx] != '}':
                var_name.append(subform[idx])
                idx += 1
            idx += 1
            var_name_str = ''.join(var_name)

            # WE MUST BE PREPARED FOR THE CASE WHEN FREE VARS APPEAR - bcs we are canonizing all subformulas in tree
            if var_name_str not in translate_dict:
                translate_dict[var_name_str] = f"var{stack_len}"
                stack_len += 1

            canonical.extend(['{'] + list(translate_dict[var_name_str]) + ['}'])
        else:
            canonical.append(char)
            idx += 1

    return idx


# returns semantically same subformula, but with "canonized" var names
def get_canonical(subform) -> str:
    canonical = []
    canonize_subform(subform, 0, {}, canonical)
    return ''.join(canonical)


# returns subformula with "canonized" var names and the dictionary with renamings
def get_canonical_and_dict(subform) -> Tuple[str, Dict[str, str]]:
    canonical = []
    rename_dict = {}
    canonize_subform(subform, 0, rename_dict, canonical)
    return ''.join(canonical), rename_dict


class EvaluateExpressionVisitor:
    """
    Visits node and depending on its type and operation, evaluates the subformula which it represents
    @:param node:  node in abstract syntax tree of HCTL formula, it represents a subformula
    @:param model: model containing var/param/prop names, bdds for update fns and so on
    @:param dupl:  dict of CANONIZED subformulas present more times in the formula (val is how many are left)
    @:param cache: dict of solved CANONIZED subformulas from dupl and <their results, renaming vars>
    @:param optim_h: if optim=True, then parent was some hybrid operation and we can push it inside for example EX...
    @:param optim_op and @:param optim_var holds info about what hybrid op we are optimizing
    """
    def visit(self, node, model: Model, dupl: Dict[str, int], cache,
              optim_h=False, optim_op=None, optim_var=None) -> Function:
        # first check for if this node does not belong in the duplicates
        save_to_cache = False
        canonized_subform, renaming = get_canonical_and_dict(node.subform_string)
        if canonized_subform in dupl:
            if canonized_subform in cache:
                # one duplicate less now, if we already visited all of them, lets delete the cached value
                dupl[canonized_subform] -= 1
                result, result_renaming = cache[canonized_subform]
                if dupl[canonized_subform] == 0:
                    dupl.pop(canonized_subform)
                    cache.pop(canonized_subform)

                # we can only return cached value if we are not in the middle of optimizing
                if not optim_h:
                    # since we are working with canonical cache, we must rename vars in result bdd
                    result_renaming = {val: key for key, val in result_renaming.items()}
                    combined_renaming = {result_renaming[val] : key for key, val in renaming.items()}
                    renaming_vectors = {f"{key}__{i}": f"{val}__{i}" for key, val in combined_renaming.items() for i in range(model.num_props)}
                    renamed_res = model.bdd.let(renaming_vectors, result)
                    #print(f"finished : {node.subform_string} : total_nodes = {len(model.bdd)} : this_bdd_nodes = {len(renamed_res)}")
                    return renamed_res
            else:
                # we want to save the result of this subformula unless we are in the middle of optimizing
                save_to_cache = not optim_h

        result = model.mk_empty_colored_set()
        if type(node) == TerminalNode:
            # we must differentiate between atomic props VS state-variables VS constants
            if node.category == NodeType.VAR:
                # if we have a state-variable, node.value has form of {var_name}
                result = create_comparator(model, node.value[1:-1])
            elif node.category == NodeType.TRUE:
                result = model.mk_unit_colored_set()
            elif node.category == NodeType.FALSE:
                result = model.mk_empty_colored_set()
            else:
                result = labeled_by(model, node.value)
        elif type(node) == UnaryNode:
            child_result = self.visit(node.child, model, dupl, cache)
            if node.category == NodeType.NEG:
                result = negate(model, child_result)
            elif node.category == NodeType.EX:
                # if predecessor was a hybrid node, we use optimize the process (distribute hybrid ops inside)
                if optim_h:
                    result = optimized_hybrid_EX(model, child_result, optim_var, optim_op)
                else:
                    result = EX(model, child_result)
            elif node.category == NodeType.AX:
                result = AX(model, child_result)
            elif node.category == NodeType.EF:
                result = EF_saturated(model, child_result)
            elif node.category == NodeType.AF:
                result = AF(model, child_result)
            elif node.category == NodeType.EG:
                result = EG(model, child_result)
            elif node.category == NodeType.AG:
                result = AG(model, child_result)
        elif type(node) == BinaryNode:
            # first lets check if we can optimise - if the predecessor was a hybrid node,
            # we can distribute it through the OR operators and optimize some future EX operator
            if optim_h and node.category == NodeType.OR:
                # if we have enabled optim, procedure depends on what types of children we have
                optimize_left = is_node_ex_to_optimize(node.left, optim_var) or is_node_union(node.left)
                optimize_right = is_node_ex_to_optimize(node.right, optim_var) or is_node_union(node.right)
                if optimize_left:
                    if optimize_right:
                        result = self.visit(node.left, model, dupl, cache, optim_h, optim_op, optim_var) | \
                                 self.visit(node.right, model, dupl, cache, optim_h, optim_op, optim_var)
                    else:
                        result = self.visit(node.left, model, dupl, cache, optim_h, optim_op, optim_var) | \
                                 self.visit_with_hybrid_op(optim_var, optim_op, node.right, model, dupl, cache)
                else:
                    if optimize_right:
                        result = self.visit_with_hybrid_op(optim_var, optim_op, node.left, model, dupl, cache) | \
                                 self.visit(node.right, model, dupl, cache, optim_h, optim_op, optim_var)
                    else:
                        result = self.visit_with_hybrid_op(optim_var, optim_op, node, model, dupl, cache)
            else:
                # we save the results for children and then combine them using the given operation
                left_result = self.visit(node.left, model, dupl, cache)
                right_result = self.visit(node.right, model, dupl, cache)

                if node.category == NodeType.AND:
                    result = left_result & right_result
                if node.category == NodeType.OR:
                    result = left_result | right_result
                elif node.category == NodeType.IMP:
                    # P -> Q == ~P | Q
                    result = negate(model, left_result) | right_result
                elif node.category == NodeType.IFF:
                    # P <=> Q == (P & Q) | (~P & ~Q)
                    result = (left_result & right_result) | (negate(model, left_result) & negate(model, right_result))
                elif node.category == NodeType.XOR:
                    # P ^ Q == (P & ~Q) | (~P & Q)
                    result = (left_result & negate(model, right_result)) | (negate(model, left_result) & right_result)
                elif node.category == NodeType.EU:
                    result = EU_saturated(model, left_result, right_result)
                elif node.category == NodeType.AU:
                    result = AU_v2(model, left_result, right_result)
                elif node.category == NodeType.EW:
                    result = EW(model, left_result, right_result)
                elif node.category == NodeType.AW:
                    result = AW(model, left_result, right_result)

        elif type(node) == HybridNode:
            """
            # Decide if there is a chance to optimize something - our goal is to optimize EX in some descendant node,
            # and we can distribute hybrid ops through the union.
            # We optimize only for bigger models - for smaller ones this is not much effective.
            """
            if model.num_props > MIN_NUM_PROPS_TO_OPTIMIZE and check_descendants_for_ex(node.child, node.var):
                result = self.visit(node.child, model, dupl, cache, optim_h=True, optim_op=node.category,
                                    optim_var=node.var[1:-1])
            else:
                child_result = self.visit(node.child, model, dupl, cache)
                if node.category == NodeType.BIND:
                    result = bind(model, child_result, node.var[1:-1])
                elif node.category == NodeType.JUMP:
                    result = jump(model, child_result, node.var[1:-1])
                elif node.category == NodeType.EXIST:
                    result = existential(model, child_result, node.var[1:-1])

        # do not forget to save the result for potential future re-use
        if save_to_cache:
            cache[canonized_subform] = (result, renaming)

        return result

    # gets the result of evaluated node, but applies hybrid op on it in the end
    # this is useful when optimisations happen somewhere during the eval
    def visit_with_hybrid_op(self, var: str, op: NodeType, node, model: Model,
                             dupl: Dict[str, int], cache: Dict[str, Function]) -> Function:
        child_result = self.visit(node, model, dupl, cache)
        if op == NodeType.BIND:
            return bind(model, child_result, var)
        elif op == NodeType.JUMP:
            return jump(model, child_result, var)
        elif op == NodeType.EXIST:
            return existential(model, child_result, var)


# find out if we have some duplicate nodes in our parse tree
# if so - mark them and then when evaluating, save result to some cache (and delete after the last usage)
# uses some kind of canonization - EX{x} and EX{y} are recognized as duplicates
def mark_duplicates(root_node) -> Dict[str, int]:
    # go through the nodes from top, use height to compare only those with the same level
    # once we find duplicate, do not continue traversing its branch (it will be skipped during eval)
    queue = []
    heappush(queue, (-root_node.height, root_node))
    duplicates = {}

    # because we are traversing a tree, we dont care if we visited some nodes or not
    last_height = root_node.height
    same_height_nodes = set()
    while queue:
        skip = False
        _, node = heappop(queue)
        node_canonical_subform = get_canonical(node.subform_string)

        # if we have saved some nodes of the same height, lets compare them
        if last_height == node.height:
            for n, n_canonic_subform in same_height_nodes:
                if node_canonical_subform == n_canonic_subform:
                    if n_canonic_subform in duplicates:
                        duplicates[n_canonic_subform] += 1
                        skip = True  # we wont be traversing subtree of this node (cache will be used)
                    else:
                        duplicates[n_canonic_subform] = 1
                    break
            # do not include subtree of the duplicate in the traversing (will be cached during eval)
            if skip:
                continue
            same_height_nodes.add((node, get_canonical(node.subform_string)))
        else:
            # change the saved height and empty the set
            last_height = node.height
            same_height_nodes.clear()
            same_height_nodes.add((node, node_canonical_subform))

        # add children to the queue
        if type(node) == UnaryNode or type(node) == HybridNode:
            heappush(queue, (-node.child.height, node.child))
        elif type(node) == BinaryNode:
            heappush(queue, (-node.left.height, node.left))
            heappush(queue, (-node.right.height, node.right))

    return duplicates


def eval_tree(as_tree: Node, model: Model) -> Function:
    duplicates = mark_duplicates(as_tree)
    result = EvaluateExpressionVisitor().visit(as_tree, model, duplicates, {})
    return result


def parse_and_eval(formula: str, model: Model) -> Function:
    as_tree = parse_to_tree(formula)
    return eval_tree(as_tree, model)
