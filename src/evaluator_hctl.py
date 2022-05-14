from antlr4 import *
from heapq import heappush, heappop
from typing import Dict, Tuple

from src.abstract_syntax_tree import *
from src.exceptions import InvalidHctlOperationError
from src.implementation_components import *
from src.parse_hctl_formula.parser_wrapper_hctl import parse_to_tree


"""Minimal number of propositions in a model to activate certain optimisations."""
MIN_PROPS_TO_OPTIMIZE = 25


def is_node_ex_to_optimize(node, var: str) -> bool:
    """Check whether node corresponds to EX and contains var in its subtree."""
    return type(node) == UnaryNode and node.category == NodeType.EX and var in node.subform_string


def is_node_union(node) -> bool:
    """Check whether node corresponds to OR operation."""
    return type(node) == BinaryNode and node.category == NodeType.OR


def check_tree_for_ex(node, var: str) -> bool:
    """
    Checks whether there is path from given node to some EX node (contains var
    in its subtree). The path must only contain union nodes.
    This is useful for optimizing the combination of EX and hybrid operators.
    """

    # if we came to EX node (whose subformula includes the var), we are done
    if is_node_ex_to_optimize(node, var):
        return True
    # another chance is to find the goal in at least one child of an Union node
    if is_node_union(node):
        return check_tree_for_ex(node.left, var) or check_tree_for_ex(node.right, var)
    # otherwise there is no point in optimizing
    return False


def canonize_subform(subform: str, idx: int, translate_dict,
                     canonical: List[str], stack_len=0) -> int:
    """Canonize names of the state-variables in given subformula.

    Works recursively, each nesting (parentheses) result in recursive call.

    Args:
        subform: Valid subformula of a hctl formula, minimized by the minimize_number_of_state_vars
            must include all PARENTHESES, must not contain EXCESS SPACES
            "(3{x}:(3{xx}:((@{x}:((~{xx})&&(AX{x})))&&(@{xx}:(AX{xx})))))" is valid input
            any node.subform_string field should be OK to use
        idx: An index to the current character of the subformula to process
        translate_dict: A dictionary mapping the encountered variable names to
            their new canonical forms
        canonical: List of characters of the new canonical form of the subformula
            This is where the result is accumulated.
        stack_len: Number of currently nested variables (represents kind of stack)

    Returns:
        Index in formula where the process stopped (and thus should continue in the parent).
        (the resulting canonical formula is collected in the param canonical)
    """

    while idx < len(subform):
        char = subform[idx]
        if char == '(':
            canonical.append(char)
            idx = canonize_subform(subform, idx + 1, translate_dict, canonical, stack_len)
        elif char == ')':
            canonical.append(char)
            return idx + 1
        # we must distinguish situations when 3 is existential and when it is part of some prop name
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

            # we must take in account free variables (since we usually canonize all subformulas)
            if var_name_str not in translate_dict:
                translate_dict[var_name_str] = f"var{stack_len}"
                stack_len += 1

            canonical.extend(['{'] + list(translate_dict[var_name_str]) + ['}'])
        else:
            canonical.append(char)
            idx += 1

    return idx


def get_canonical(subform: str) -> str:
    """Returns equivalent subformula, but with canonized var names."""
    canonical = []
    canonize_subform(subform, 0, {}, canonical)
    return ''.join(canonical)


def get_canonical_and_dict(subform: str) -> Tuple[str, Dict[str, str]]:
    """Returns subformula with "canonized" var names together with name mappings."""
    canonical = []
    rename_dict = {}
    canonize_subform(subform, 0, rename_dict, canonical)
    return ''.join(canonical), rename_dict


def mark_duplicates(root_node) -> Dict[str, int]:
    """Collect duplicate subformulas in the formula represented by a tree.

    We compare canonized subformulas, so 'EX{x}' and 'EX{y}' are recognized as duplicates.
    This is especially useful for the caching during the evaluation.

    Args:
        root_node: Root of the tree representing the formula

    Returns:
        Dictionary mapping duplicate subformulas to the number of their occurrences
    """

    queue = []
    heappush(queue, (-root_node.height, root_node))
    duplicates = {}
    last_height = root_node.height
    same_height_nodes = set()

    # go through the nodes from top, compare only those with the same height
    # once a duplicate is found, stop traversing its branch (it will be skipped during eval)
    while queue:
        skip = False
        _, node = heappop(queue)
        node_canonical_subform = get_canonical(node.subform_string)

        # if we have saved some nodes of the same height, compare them
        if last_height == node.height:
            for n, n_canonic_subform in same_height_nodes:
                if node_canonical_subform == n_canonic_subform:
                    if n_canonic_subform in duplicates:
                        duplicates[n_canonic_subform] += 1
                        skip = True  # don't traverse subtree of a duplicate node
                    else:
                        duplicates[n_canonic_subform] = 1
                    break
            if skip:
                continue
            same_height_nodes.add((node, get_canonical(node.subform_string)))
        else:
            # change the saved height and empty the set of nodes for comparison
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


def get_and_update_cache(model: Model, canonized_form: str, renaming: Dict[str, str],
                         duplicates: Dict[str, int], cache) -> Function:
    """Get cached value and decrement the number of remaining duplicates.

    If no duplicates of this formula remain, delete cached value to save memory.

    Args:
        model: Model object containing symbolic representation
        canonized_form: Formula string with canonized variable names
        renaming: Dictionary mapping original var names to canonized
        duplicates: Dictionary mapping duplicate formulas to the number of occurrences left
        cache: Dictionary mapping solved subformulas to <result, name_mapping>

    Returns:
         Correctly renamed BDD-result for given formula taken from cache.
    """
    duplicates[canonized_form] -= 1  # one less duplicate remains
    result, result_renaming = cache[canonized_form]
    # if we already found all formula's duplicates, delete the cached value
    if duplicates[canonized_form] == 0:
        duplicates.pop(canonized_form)
        cache.pop(canonized_form)

    # rename vars in result bdd (since cache uses canonized var names)
    result_renaming = {val: key for key, val in result_renaming.items()}
    combined_renaming = {result_renaming[val] : key for key, val in renaming.items()}
    renaming_vectors = {f"{key}__{i}": f"{val}__{i}" for key, val in combined_renaming.items()
                        for i in range(model.num_props())}
    renamed_res = model.bdd.let(renaming_vectors, result)
    return renamed_res


def eval_terminal(node, model: Model) -> Function:
    """Evaluate terminal node of formula tree based on its type."""
    # we have several types of terminals: atomic props, state-variables, constants
    if node.category == NodeType.VAR:
        # if we have a state-variable, node.value has form of '{var_name}'
        return create_comparator(model, node.value[1:-1])
    elif node.category == NodeType.TRUE:
        return model.mk_unit_colored_set()
    elif node.category == NodeType.FALSE:
        return model.mk_empty_colored_set()
    elif node.category == NodeType.PROP:
        return labeled_by(model, node.value)
    else:
        raise InvalidHctlOperationError(node.category)


def apply_unary_op(operation: NodeType, model: Model, child_result: Function,
                   optimize_ex: bool, optim_op: NodeType, optim_var: str) -> Function:
    """Apply unary operation corresponding to a node to the result of its child."""
    if operation == NodeType.NEG:
        return negate(model, child_result)
    elif operation == NodeType.EX:
        # if predecessor was a hybrid node, we optimize (distribute hybrid ops inside EX)
        if optimize_ex:
            return optimized_hybrid_EX(model, child_result, optim_var, optim_op)
        else:
            return EX(model, child_result)
    elif operation == NodeType.AX:
        return AX(model, child_result)
    elif operation == NodeType.EF:
        return EF_saturated(model, child_result)
    elif operation == NodeType.AF:
        return AF(model, child_result)
    elif operation == NodeType.EG:
        return EG(model, child_result)
    elif operation == NodeType.AG:
        return AG(model, child_result)
    else:
        raise InvalidHctlOperationError(operation)


def apply_binary_op(operation: NodeType, model: Model,
                    left_result: Function, right_result: Function) -> Function:
    """Apply binary operation corresponding to a node to the results of its children"""
    if operation == NodeType.AND:
        return left_result & right_result
    elif operation == NodeType.OR:
        return left_result | right_result
    elif operation == NodeType.IMP:
        # P -> Q == ~P | Q
        return negate(model, left_result) | right_result
    elif operation == NodeType.IFF:
        # P <=> Q == (P & Q) | (~P & ~Q)
        return (left_result & right_result) | (negate(model, left_result) & negate(model, right_result))
    elif operation == NodeType.XOR:
        # P ^ Q == (P & ~Q) | (~P & Q)
        return (left_result & negate(model, right_result)) | (negate(model, left_result) & right_result)
    elif operation == NodeType.EU:
        return  EU_saturated(model, left_result, right_result)
    elif operation == NodeType.AU:
        return  AU_v2(model, left_result, right_result)
    elif operation == NodeType.EW:
        return  EW(model, left_result, right_result)
    elif operation == NodeType.AW:
        return  AW(model, left_result, right_result)
    else:
        raise InvalidHctlOperationError(operation)


def apply_hybrid_op(operation: NodeType, model: Model,
                    child_result: Function, hybrid_var: str) -> Function:
    """Apply hybrid operation corresponding to a node to the result of its child"""
    if operation == NodeType.BIND:
        return bind(model, child_result, hybrid_var)
    elif operation == NodeType.JUMP:
        return jump(model, child_result, hybrid_var)
    elif operation == NodeType.EXIST:
        return existential(model, child_result, hybrid_var)
    else:
        raise InvalidHctlOperationError(operation)


def eval_tree_recursive(node, model: Model, dupl: Dict[str, int], cache,
                        optim_h=False, optim_op=None, optim_var=None) -> Function:
    """Visit node and recursively evaluate the subformula which it represents.

    Compute in bottom-up manner. First evaluate potential children, then combine
    their results depending on the type and operation corresponding to the node.
    Make use of cached results, optimize computation of several patterns.

    Args:
        node: A node in abstract syntax tree of HCTL formula, it represents a subformula
        model: Model structure containing symbolic representation and metadata
        dupl: Dictionary mapping duplicate (CANONIZED) subformulas to the number occurrences left
        cache: Dictionary mapping solved (CANONIZED) duplicate subformulas
            to the pair in form <result, variable_names_mapping>
        optim_h: If True, then use optimisations - predecessor was a hybrid operator node
            and we can push it inside (for example) some EX operator
        optim_op: NodeType representing hybrid operation being optimized
        optim_var: Name of the variable bound to hybrid operation being optimized

    Returns:
        A BDD-encoded result of the evaluated formula on the given model.
    """

    save_to_cache = False
    # get canonized form of this subformula, and name mapping for renamed vars
    canonized_form, renaming = get_canonical_and_dict(node.subform_string)
    if canonized_form in dupl:
        if canonized_form in cache:
            cached_result = get_and_update_cache(model, canonized_form, renaming, dupl, cache)
            # return cached value if not in the middle of optimizing
            if not optim_h:
                return cached_result
        else:
            # save the result for this subformula later, unless in the middle of optimizing
            save_to_cache = not optim_h

    result = model.mk_empty_colored_set()
    if type(node) == TerminalNode:
        result = eval_terminal(node, model)
    elif type(node) == UnaryNode:
        child_result = eval_tree_recursive(node.child, model, dupl, cache)
        result = apply_unary_op(node.category, model, child_result, optim_h, optim_op, optim_var)
    elif type(node) == BinaryNode:
        # check if we can apply optimisation - if the predecessor was a hybrid quantifier,
        # we can distribute it through the OR operators and later optimize some EX operator
        if optim_h and node.category == NodeType.OR:
            # if optim is enabled, procedure depends on the types of children
            optimize_left = is_node_ex_to_optimize(node.left, optim_var) or is_node_union(node.left)
            optimize_right = is_node_ex_to_optimize(node.right, optim_var) or is_node_union(node.right)
            if optimize_left:
                if optimize_right:
                    result = eval_tree_recursive(node.left, model, dupl, cache, optim_h, optim_op, optim_var) | \
                             eval_tree_recursive(node.right, model, dupl, cache, optim_h, optim_op, optim_var)
                else:
                    result = eval_tree_recursive(node.left, model, dupl, cache, optim_h, optim_op, optim_var) | \
                             eval_with_hybrid(optim_var, optim_op, node.right, model, dupl, cache)
            else:
                if optimize_right:
                    result = eval_with_hybrid(optim_var, optim_op, node.left, model, dupl, cache) | \
                             eval_tree_recursive(node.right, model, dupl, cache, optim_h, optim_op, optim_var)
                else:
                    result = eval_with_hybrid(optim_var, optim_op, node, model, dupl, cache)
        else:
            left_result = eval_tree_recursive(node.left, model, dupl, cache)
            right_result = eval_tree_recursive(node.right, model, dupl, cache)
            result = apply_binary_op(node.category, model, left_result, right_result)
    elif type(node) == HybridNode:
        # Check if there is some suited descendant (EX) node for optimization
        # Optimize only for larger models - for smaller ones this is not much effective.
        if model.num_props() > MIN_PROPS_TO_OPTIMIZE and check_tree_for_ex(node.child, node.var):
            result = eval_tree_recursive(node.child, model, dupl, cache, optim_h=True,
                                         optim_op=node.category, optim_var=node.var[1:-1])
        else:
            child_result = eval_tree_recursive(node.child, model, dupl, cache)
            result = apply_hybrid_op(node.category, model, child_result, node.var[1:-1])

    # do not forget to save the result for potential future re-use
    if save_to_cache:
        cache[canonized_form] = (result, renaming)

    return result


def eval_with_hybrid(variable: str, op: NodeType, node, model: Model,
                     dupl: Dict[str, int], cache: Dict[str, Function]) -> Function:
    """
    Evaluate the formula corresponding to the node and apply hybrid operation on the result.
    This is useful when optimisations happen somewhere during the evaluation.
    """
    child_result = eval_tree_recursive(node, model, dupl, cache)
    if op == NodeType.BIND:
        return bind(model, child_result, variable)
    elif op == NodeType.JUMP:
        return jump(model, child_result, variable)
    elif op == NodeType.EXIST:
        return existential(model, child_result, variable)


def eval_tree(syntax_tree: Node, model: Model) -> Function:
    """Evaluate formula represented by a tree on a given model."""
    duplicates = mark_duplicates(syntax_tree)
    result = eval_tree_recursive(syntax_tree, model, duplicates, {})
    return result


def parse_and_eval(formula: str, model: Model) -> Function:
    """Parse the formula and evaluate it on a given model."""
    as_tree = parse_to_tree(formula)
    return eval_tree(as_tree, model)
