from antlr4 import *
from src.abstract_syntax_tree import *
from src.implementation import *
from src.Parsing_HCTL_formula.parser_hctl import parse_to_tree
from src.parse_all import parse_all

from heapq import heappush, heappop
from typing import Dict

NUM_PROPS_AT_LEAST_TO_OPTIMIZE = 20


class EvaluateExpressionVisitor:

    # TODO: test parser and evaluator on more CTL/HCTL formulas

    # TODO: FINISH and TEST CACHE

    # TODO: >>bring ALL optimizations in <<, (add NESTED through union, now we have just the three basic)
    # TODO: JUMP might not need x in the subformula

    # TODO: optimize also through the intersection ? and maybe even do something with AX ?

    # TODO: solve the possible problem with future (self-loops again, but in sources??)

    # TODO: maybe change all operators in the tree to just EX, EU, EG - so that we can use cache sometimes??

    # TODO: sometimes its possible to eval thing once and then just rename vars, instead of counting twice
    # TODO: for example (AG EF var) in formula: 3x.3y.(@x. AG¬y & AG EFx) & (@y. AG EFy)

    """
    Visits node and depending on its type and operation, evaluates the subformula which it represents
    @:param node:  node in abstract syntax tree of HCTL formula, it represents a subformula
    @:param model: model containing var/param/prop names, bdds for update fns and so on
    @:param dupl:  dict of subformulas (str) being present more times in the formula (val is how many are left)
    @:param cache: dict of solved subformulas from dupl and their results
    @:param optim: if optim=True, then parent was some hybrid operation and we can push it inside for example EX...
    @:param optim_op and @:param optim_var holds info about what hybrid op we are optimizing
    """
    def visit(self, node, model: Model, dupl: Dict[str, int], cache: Dict[str, Function],
              optim=False, optim_op=None, optim_var=None) -> Function:
        # TODO : subform_string problem
        # first check for if this node does not belong in the duplicates
        save_to_cache = False
        if node.subform_string in dupl:
            if node.subform_string in cache:
                # one duplicate less now, if we already visited all of them, lets delete the cached value
                dupl[node.subform_string] -= 1
                result = cache[node.subform_string]
                if dupl[node.subform_string] == 0:
                    dupl.pop(node.subform_string)
                    cache.pop(node.subform_string)
                return result
            else:
                save_to_cache = True

        result = model.bdd.add_expr("False")
        if type(node) == TerminalNode:
            # we must differentiate between atomic props VS state-variables
            # if we have a state-variable, node.value has form of {var_name}
            if '{' in node.value:
                result = create_comparator(model, node.value[1:-1])
            else:
                result = model.bdd.add_expr(node.value)
        elif type(node) == UnaryNode:
            if node.value == '~':
                result = ~self.visit(node.child, model, dupl, cache)
            elif node.value == 'EX':
                if optim:
                    result = optimized_hybrid_EX(model, self.visit(node.child, model, dupl, cache), optim_var, optim_op)
                else:
                    result = EX(model, self.visit(node.child, model, dupl, cache))
            elif node.value == 'AX':
                result = AX(model, self.visit(node.child, model, dupl, cache))
            elif node.value == 'EY':
                result = EY(model, self.visit(node.child, model, dupl, cache))
            elif node.value == 'AY':
                result = AY(model, self.visit(node.child, model, dupl, cache))
            elif node.value == 'EF':
                result = EF(model, self.visit(node.child, model, dupl, cache))
            elif node.value == 'AF':
                result = AF(model, self.visit(node.child, model, dupl, cache))
            elif node.value == 'EG':
                result = EG(model, self.visit(node.child, model, dupl, cache))
            elif node.value == 'AG':
                result = AG(model, self.visit(node.child, model, dupl, cache))
        elif type(node) == BinaryNode:
            if node.value == '&&':
                result = self.visit(node.left, model, dupl, cache) & self.visit(node.right, model, dupl, cache)
            elif node.value == '||':
                result = self.visit(node.left, model, dupl, cache) | self.visit(node.right, model, dupl, cache)
            elif node.value == '->':
                result = self.visit(node.left, model, dupl, cache).implies(self.visit(node.right, model, dupl, cache))
            elif node.value == '<->':
                result = self.visit(node.left, model, dupl, cache).equiv(self.visit(node.right, model, dupl, cache))
            elif node.value == 'EU':
                result = EU(model, self.visit(node.left, model, dupl, cache), self.visit(node.right, model, dupl, cache))
            elif node.value == 'AU':
                result = AU(model, self.visit(node.left, model, dupl, cache), self.visit(node.right, model, dupl, cache))
            elif node.value == 'EW':
                result = EW(model, self.visit(node.left, model, dupl, cache), self.visit(node.right, model, dupl, cache))
            elif node.value == 'AW':
                result = AW(model, self.visit(node.left, model, dupl, cache), self.visit(node.right, model, dupl, cache))
        elif type(node) == HybridNode:
            # if we have EX directly after this hybrid node and its subformula contains 'var',
            # we can use optimized path - however we use it only for bigger models, because it works better
            if type(node.child) == UnaryNode and node.child.value == "EX" and \
                    node.var in node.child.subform_string and model.num_props > NUM_PROPS_AT_LEAST_TO_OPTIMIZE:
                result = self.visit(node.child, model, dupl, cache, optim=True, optim_op=node.value, optim_var=node.var[1:-1])
            elif node.value == '!':
                result = bind(model, self.visit(node.child, model, dupl, cache), node.var[1:-1])
            elif node.value == '@':
                result = jump(model, self.visit(node.child, model, dupl, cache), node.var[1:-1])
            elif node.value == '3':
                result = existential(model, self.visit(node.child, model, dupl, cache), node.var[1:-1])

        if save_to_cache:
            cache[node.subform_string] = result
        return result


# find out if we have some duplicate nodes in our parse tree
# if so - mark them and then when evaluating, save result to some cache (and delete after the last usage)
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

        # if we have saved some nodes of the same height, lets compare them
        if last_height == node.height:
            for n in same_height_nodes:
                if node.subform_string == n.subform_string:
                    # TODO : subform_string string problem?
                    duplicates[n.subform_string] = duplicates.get(n.subform_string, 0) + 1
                    skip = True
                    break
            # do not include subtree of the duplicate in the traversing (will be cached during eval)
            if skip:
                continue
            same_height_nodes.add(node)
        else:
            # change the saved height and empty the set
            last_height = node.height
            same_height_nodes.clear()
            same_height_nodes.add(node)

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


if __name__ == '__main__':
    # TODO: change path
    bnet_path = "bnet_examples/064_free.bnet"
    f = "!{x}: (AG EF {x})"

    m, tree = parse_all(bnet_path, f)
    res = eval_tree(tree, m)
    print_results(res, m, f"model: {m.name}, formula: {f}", True)
