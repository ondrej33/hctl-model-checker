# Generated from update_fn.g4 by ANTLR 4.9.2
from antlr4 import *
from src.abstract_syntax_tree import *
if __name__ is not None and "." in __name__:
    from .update_fn_parser import update_fnParser
else:
    from update_fn_parser import update_fnParser

# This class defines a complete generic visitor for a parse tree produced by update_fnParser.

class update_fnVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by HCTLParser#root.
    def visitRoot(self, ctx: update_fnParser.RootContext):
        return self.visit(ctx.formula())

    # Visit a parse tree produced by HCTLParser#fullStop.
    # We should never arrive here!!
    def visitFullStop(self, ctx: update_fnParser.FullStopContext):
        return self.visitChildren(ctx)

    # This is a node of "parentheses", we just dive one more level
    def visitSkipNode(self, ctx: update_fnParser.SkipNodeContext):
        return self.visit(ctx.child)

    def visitTerminalNode(self, ctx: update_fnParser.TerminalNodeContext):
        # unify all possibilities for true/false nodes into one option
        if ctx.value.text in {"True", "true", "tt"}:
            return TerminalNode(value="True", category=NodeType.TRUE)
        elif ctx.value.text in {"False", "false", "ff"}:
            return TerminalNode(value="False", category=NodeType.FALSE)

        # only other possible way for item in update fn is a proposition
        return TerminalNode(value=ctx.value.text, category=NodeType.PROP)

    def visitUnary(self, ctx: update_fnParser.UnaryContext):
        # we have slight inconsistency here - "!" means negation in context of update functions,
        # but it is considered as binder otherwise
        # this is caused due to the compatibility with AEON or BNET format
        if ctx.value.text == "!":
            ctx.value.text = "~"
        return UnaryNode(child=self.visit(ctx.child), category=OP_DICT[ctx.value.text])

    def visitBinary(self, ctx: update_fnParser.BinaryContext):
        return BinaryNode(left=self.visit(ctx.left), right=self.visit(ctx.right), category=OP_DICT[ctx.value.text])



del update_fnParser