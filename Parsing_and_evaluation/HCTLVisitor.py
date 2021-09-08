# Generated from HCTL.g4 by ANTLR 4.9.2
from antlr4 import *
from abstract_syntax_tree import *
if __name__ is not None and "." in __name__:
    from .HCTLParser import HCTLParser
else:
    from HCTLParser import HCTLParser


# This class defines a complete generic visitor for a parse tree produced by HCTLParser.

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


del HCTLParser