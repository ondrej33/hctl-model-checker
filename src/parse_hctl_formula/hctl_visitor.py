# Generated from HCTL.g4 by ANTLR 4.9.2
from antlr4 import *
from src.abstract_syntax_tree import *
if __name__ is not None and "." in __name__:
    from .hctl_parser import HCTLParser
else:
    from hctl_parser import HCTLParser


class HCTLVisitor(ParseTreeVisitor):
    """Class wrapping the construction of the HCTL abstract syntax tree."""

    def visitRoot(self, ctx: HCTLParser.RootContext):
        """Visit a parse tree produced by HCTLParser#root."""
        return self.visit(ctx.formula())

    def visitFullStop(self, ctx: HCTLParser.FullStopContext):
        """Visit a parse tree produced by HCTLParser#fullStop."""
        # We should never arrive here
        return self.visitChildren(ctx)

    def visitSkipNode(self, ctx: HCTLParser.SkipNodeContext):
        """Skip the node for "parentheses"."""
        return self.visit(ctx.child)

    def visitTerminalNode(self, ctx: HCTLParser.TerminalNodeContext):
        """Process terminal nodes."""
        # unify all possibilities for true/false nodes into one option
        if ctx.value.text in {"True", "true", "tt"}:
            return TerminalNode(value="True", category=NodeType.TRUE)
        elif ctx.value.text in {"False", "false", "ff"}:
            return TerminalNode(value="False", category=NodeType.FALSE)
        # variable names have are in a form of {var_name}
        elif '{' in ctx.value.text:
            return TerminalNode(value=ctx.value.text, category=NodeType.VAR)
        else:
            return TerminalNode(value=ctx.value.text, category=NodeType.PROP)

    def visitUnary(self, ctx: HCTLParser.UnaryContext):
        """Process unary nodes."""
        return UnaryNode(child=self.visit(ctx.child), category=OP_DICT[ctx.value.text])

    def visitBinary(self, ctx: HCTLParser.BinaryContext):
        """Process binary nodes."""
        # special case: "(EX phi1) || (EX phi2)", will be transformed into "EX (phi1 || phi2)"
        # THERE MIGHT BE PARENTHESIS NODE ON THE WAY (lets handle one layer of parentheses)
        if ctx.value.text == "||":
            if ctx.left.value.text == "EX" and ctx.right.value.text == "EX":
                child_or = BinaryNode(
                    left=self.visit(ctx.left.child),
                    right=self.visit(ctx.right.child),
                    category=NodeType.OR
                )
                return UnaryNode(child=child_or, category=NodeType.EX)
            elif ctx.left.value.text == "(" and ctx.left.child.value.text == "EX" and \
                    ctx.right.value.text == "EX":
                child_or = BinaryNode(
                    left=self.visit(ctx.left.child.child),
                    right=self.visit(ctx.right.child),
                    category=NodeType.OR
                )
                return UnaryNode(child=child_or, category=NodeType.EX)
            elif ctx.left.value.text == "EX" and \
                    ctx.right.value.text == "(" and ctx.right.child.value.text == "EX":
                child_or = BinaryNode(
                    left=self.visit(ctx.left.child),
                    right=self.visit(ctx.right.child.child),
                    category=NodeType.OR
                )
                return UnaryNode(child=child_or, category=NodeType.EX)
            elif ctx.left.value.text == "(" and ctx.left.child.value.text == "EX" and \
                    ctx.right.value.text == "(" and ctx.right.child.value.text == "EX":
                child_or = BinaryNode(
                    left=self.visit(ctx.left.child.child),
                    right=self.visit(ctx.right.child.child),
                    category=NodeType.OR
                )
                return UnaryNode(child=child_or, category=NodeType.EX)

        # same thing for "(AX phi1) && (AX phi2)" == "AX (phi1 && phi2)"
        if ctx.value.text == "&&":
            if ctx.left.value.text == "AX" and ctx.right.value.text == "AX":
                child_and = BinaryNode(
                    left=self.visit(ctx.left.child),
                    right=self.visit(ctx.right.child),
                    category=NodeType.AND
                )
                return UnaryNode(child=child_and, category=NodeType.AX)
            elif ctx.left.value.text == "(" and ctx.left.child.value.text == "AX" and \
                    ctx.right.value.text == "AX":
                child_and = BinaryNode(
                    left=self.visit(ctx.left.child.child),
                    right=self.visit(ctx.right.child),
                    category=NodeType.AND
                )
                return UnaryNode(child=child_and, category=NodeType.AX)
            elif ctx.left.value.text == "AX" and \
                    ctx.right.value.text == "(" and ctx.right.child.value.text == "AX":
                child_and = BinaryNode(
                    left=self.visit(ctx.left.child),
                    right=self.visit(ctx.right.child.child),
                    category=NodeType.AND
                )
                return UnaryNode(child=child_and, category=NodeType.AX)
            elif ctx.left.value.text == "(" and ctx.left.child.value.text == "AX" and \
                    ctx.right.value.text == "(" and ctx.right.child.value.text == "AX":
                # both children have parentheses
                child_and = BinaryNode(
                    left=self.visit(ctx.left.child.child),
                    right=self.visit(ctx.right.child.child),
                    category=NodeType.AND
                )
                return UnaryNode(child=child_and, category=NodeType.AX)

        return BinaryNode(
            left=self.visit(ctx.left),
            right=self.visit(ctx.right),
            category=OP_DICT[ctx.value.text]
        )

    def visitHybrid(self, ctx: HCTLParser.HybridContext):
        """Process hybrid nodes."""
        return HybridNode(
            var=ctx.var.text,
            child=self.visit(ctx.child),
            category=OP_DICT[ctx.value.text]
        )


del HCTLParser