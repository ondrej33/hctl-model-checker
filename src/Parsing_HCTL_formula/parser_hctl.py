from HCTLLexer import HCTLLexer
from HCTLParser import HCTLParser
from HCTLVisitor import HCTLVisitor

from antlr4 import *
from src.abstract_syntax_tree import *

# To create HCTLParser and other files from grammar:
#    $ java -jar "/usr/local/lib/antlr-4.9.2-complete.jar" -Dlanguage=Python3 -visitor HCTL.g4
# or $ antlr4 -Dlanguage=Python3 -visitor HCTL.g4
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


def parse_to_tree(formula: str) -> Node:
    lexer = HCTLLexer(InputStream(formula))
    stream = CommonTokenStream(lexer)
    parser = HCTLParser(stream)
    tree = parser.root()

    as_tree = HCTLVisitor().visitRoot(tree)
    return as_tree
