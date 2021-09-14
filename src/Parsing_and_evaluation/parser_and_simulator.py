from HCTLLexer import HCTLLexer
from HCTLParser import HCTLParser
from HCTLVisitor import HCTLVisitor

from antlr4 import *
from abstract_syntax_tree import *
from src.implementation import *

from heapq import heappush, heappop

# to create HCTLParser and all from grammar:
# java -jar "C:\Program Files\Java\antlr-4.9.2-complete.jar" -Dlanguage=Python3 -visitor HCTL.g4
# then change HCTLVisitor to this: (and add import of structures)

"""
# code changed in HCTLVisitor follows (this is backup, it might disappear when creating new parser):

class HCTLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HCTLParser#root.
    def visitRoot(self, ctx: HCTLParser.RootContext):
        return self.visit(ctx.formula())

    # Visit a parse tree produced by HCTLParser#fullStop.
    # We should never arrive here!!
    def visitFullStop(self, ctx: HCTLParser.FullStopContext):
        return self.visitChildren(ctx)

    # This is a node of "parentheses", we just dive one more level
    def visitSkipNode(self, ctx: HCTLParser.SkipNodeContext):
        return self.visit(ctx.child)

    def visitTerminalNode(self, ctx: HCTLParser.TerminalNodeContext):
        return TerminalNode(value=ctx.value.text)

    def visitUnary(self, ctx: HCTLParser.UnaryContext):
        return UnaryNode(value=ctx.value.text, child=self.visit(ctx.child))

    def visitBinary(self, ctx: HCTLParser.BinaryContext):
        return BinaryNode(value=ctx.value.text, left=self.visit(ctx.left), right=self.visit(ctx.right))

    def visitHybrid(self, ctx: HCTLParser.HybridContext):
        return HybridNode(value=ctx.value.text, var=ctx.var.text, child=self.visit(ctx.child))
"""

NUM_PROPS_AT_LEAST_TO_OPTIMIZE = 20


class EvaluateExpressionVisitor:

    # TODO: test parser on many many propositional formulas + construct more tests for CTL/HCTL formulas

    # TODO: FINISH and TEST CACHE

    # TODO: !bring ALL optimizations in!, (add NESTED through union, now we have just the three basic)
    # TODO: JUMP might not need x in the subformula

    # TODO: adding state-variables to the model DIRECTLY FROM FORMULA

    # TODO: translating variables in formula to s__1...

    # Visits node and depending on its type and operation, evaluates the subformula which it represents
    # Uses results from children, combines them until whole thing is done
    # if optimize=True, then parent was some hybrid operation and we can push it inside for example EX...
    def visit(self, node, model: Model, dupl, cache, optim=False, optim_op=None, optim_var=None):
        # first check for if this node does not belong in the duplicates
        save_to_cache = False
        if node.subform_string in dupl:
            if node.subform_string in cache:
                # one duplicate less now, if we already got all of them, lets delete the cached value
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
            # we must differentiate between propositions (params) VS state-variables
            # if we have a state-variable, node.value has form of {var_name}
            if '{' in node.value:
                result = create_comparator(model, node.value[1:-1])
            # TODO: instead of propositions/params return their translated name (anything -> s__n ...)
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
        else:
            # if we have EX directly after this hybrid node and its subformula contains 'var',
            # we can use optimized path - however we use it only for bigger models, because it works better
            if type(node.child) == UnaryNode and node.child.value == "EX" and \
                    node.var in node.child.subform_string and model.num_props > NUM_PROPS_AT_LEAST_TO_OPTIMIZE:
                result = self.visit(node.child, model, dupl, cache, optim=True, optim_op=node.value, optim_var=node.var[1:-1])
            elif node.value == '!':
                result = bind(model, node.var[1:-1], self.visit(node.child, model, dupl, cache))
            elif node.value == '@':
                result = jump(model, node.var[1:-1], self.visit(node.child, model, dupl, cache))
            elif node.value == 'Q':
                result = existential(model, node.var[1:-1], self.visit(node.child, model, dupl, cache))

        if save_to_cache:
            cache[node.subform_string] = result
        return result


# find out if we have some duplicate nodes in our parse tree
# if so - mark them and then when evaluating, save result to some cache (and delete after the last usage)
def mark_duplicates(root_node):
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


def parse_and_eval(formula, model: Model) -> Function:
    lexer = HCTLLexer(InputStream(formula))
    stream = CommonTokenStream(lexer)
    parser = HCTLParser(stream)
    tree = parser.root()

    ast = HCTLVisitor().visitRoot(tree)
    duplicates = mark_duplicates(ast)
    result = EvaluateExpressionVisitor().visit(ast, model, duplicates, {})
    return result


if __name__ == '__main__':
    # TODO: change path
    bnet_path = "bnet_examples/023.bnet"
    m = bnet_parser(bnet_path)
    f = "!{x}: (AG EF {x})"
    res = parse_and_eval(f, m)
    print_results(res, m, f"model: {m.name}, formula: {f}", True)
