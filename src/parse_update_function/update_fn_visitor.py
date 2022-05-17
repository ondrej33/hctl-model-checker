# Generated from update_fn.g4 by ANTLR 4.9.2
from antlr4 import *
from src.abstract_syntax_tree import *
if __name__ is not None and "." in __name__:
    from .update_fn_parser import update_fnParser
else:
    from update_fn_parser import update_fnParser


class update_fnVisitor(ParseTreeVisitor):
    """This class defines a generic visitor for a parse tree produced by update_fnParser."""

    def visitRoot(self, ctx: update_fnParser.RootContext):
        """Visit a parse tree produced by HCTLParser#root."""
        return self.visit(ctx.formula())

    def visitFullStop(self, ctx: update_fnParser.FullStopContext):
        """Visit a parse tree produced by HCTLParser#fullStop."""
        # We should never arrive here
        return self.visitChildren(ctx)

    def visitSkipNode(self, ctx: update_fnParser.SkipNodeContext):
        """Skip the node for "parentheses"."""
        return self.visit(ctx.child)

    def visitTerminalNode(self, ctx: update_fnParser.TerminalNodeContext):
        """Process terminal nodes."""
        # unify all possibilities for true/false nodes into one option
        if ctx.value.text in {"True", "true", "tt"}:
            return TerminalNode(value="True", category=NodeType.TRUE)
        elif ctx.value.text in {"False", "false", "ff"}:
            return TerminalNode(value="False", category=NodeType.FALSE)

        # only other possible way for item in update fn is a proposition
        return TerminalNode(value=ctx.value.text, category=NodeType.PROP)

    def visitUnary(self, ctx: update_fnParser.UnaryContext):
        """Process unary nodes."""

        # there is slight inconsistency: "!" means negation in context of update functions,
        # but it is considered as binder otherwise (in HCTL formula)
        if ctx.value.text == "!":
            ctx.value.text = "~"
        return UnaryNode(child=self.visit(ctx.child), category=OP_DICT[ctx.value.text])

    def visitBinary(self, ctx: update_fnParser.BinaryContext):
        """Process binary nodes."""
        return BinaryNode(
            left=self.visit(ctx.left),
            right=self.visit(ctx.right),
            category=OP_DICT[ctx.value.text]
        )



del update_fnParser