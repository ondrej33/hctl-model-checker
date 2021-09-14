from update_fnLexer import update_fnLexer
from update_fnParser import update_fnParser
from update_fnVisitor import update_fnVisitor

from antlr4 import *
from src.abstract_syntax_tree import *
from src.implementation import *

from heapq import heappush, heappop

# To create update_fnParser and other files from grammar:
#    $ java -jar "/usr/local/lib/antlr-4.9.2-complete.jar" -Dlanguage=Python3 -visitor update_fn.g4
# or $ antlr4 -Dlanguage=Python3 -visitor update_fn.g4
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

    # Visits node and depending on its type and operation, evaluates the subformula which it represents
    # Uses results from children, combines them until whole thing is done
    def visit(self, node, bdd):
        result = bdd.add_expr("False")
        if type(node) == TerminalNode:
            # TODO: differentiate between true/false OR prop/param node
            result = bdd.add_expr(node.value)
        elif type(node) == UnaryNode:
            # we have only the negation here
            result = ~self.visit(node.child, bdd)
        elif type(node) == BinaryNode:
            if node.value == '&&':
                result = self.visit(node.left, bdd) & self.visit(node.right, bdd)
            elif node.value == '||':
                result = self.visit(node.left, bdd) | self.visit(node.right, bdd)
            elif node.value == '->':
                result = self.visit(node.left, bdd).implies(self.visit(node.right, bdd))
            elif node.value == '<->':
                result = self.visit(node.left, bdd).equiv(self.visit(node.right, bdd))
        return result


def parse(formula, model: Model) -> Function:
    lexer = update_fnLexer(InputStream(formula))
    stream = CommonTokenStream(lexer)
    parser = update_fnParser(stream)
    tree = parser.root()

    ast = update_fnVisitor().visitRoot(tree)
    bdd = BDD()
    # TODO make a BDD at this point
    result = EvaluateExpressionVisitor().visit(ast, bdd)
    return result


if __name__ == '__main__':
    # TODO: change path
    bnet_path = "bnet_examples/023.bnet"
