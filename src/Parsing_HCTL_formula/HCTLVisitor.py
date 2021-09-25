# Generated from HCTL.g4 by ANTLR 4.9.2
from antlr4 import *
from src.abstract_syntax_tree import *
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
        # unify all possibilities for true/false nodes into one option
        if ctx.value.text in {"True", "true", "tt"}:
            return TerminalNode(value="True")
        elif ctx.value.text in {"False", "false", "ff"}:
            return TerminalNode(value="False")

        return TerminalNode(value=ctx.value.text)

    def visitUnary(self, ctx: HCTLParser.UnaryContext):
        return UnaryNode(value=ctx.value.text, child=self.visit(ctx.child))

    def visitBinary(self, ctx: HCTLParser.BinaryContext):
        # special case: if we have "(EX phi1) || (EX phi2)", we will make it instead as "EX (phi1 || phi2)"
        # THERE MIGHT BE PARENTHESIS NODE ON THE WAY (lets care about one layer of parentheses)
        if ctx.value.text == "||":
            if ctx.left.value.text == "EX" and ctx.right.value.text == "EX":
                child_or = BinaryNode(value="||", left=self.visit(ctx.left.child), right=self.visit(ctx.right.child))
                return UnaryNode(value="EX", child=child_or)
            elif ctx.left.value.text == "(" and ctx.left.child.value.text == "EX" and \
                    ctx.right.value.text == "EX":
                child_or = BinaryNode(value="||", left=self.visit(ctx.left.child.child), right=self.visit(ctx.right.child))
                return UnaryNode(value="EX", child=child_or)
            elif ctx.left.value.text == "EX" and \
                    ctx.right.value.text == "(" and ctx.right.child.value.text == "EX":
                child_or = BinaryNode(value="||", left=self.visit(ctx.left.child), right=self.visit(ctx.right.child.child))
                return UnaryNode(value="EX", child=child_or)
            elif ctx.left.value.text == "(" and ctx.left.child.value.text == "EX" and \
                    ctx.right.value.text == "(" and ctx.right.child.value.text == "EX":
                child_or = BinaryNode(value="||", left=self.visit(ctx.left.child.child), right=self.visit(ctx.right.child.child))
                return UnaryNode(value="EX", child=child_or)

        # same thing for "(AX phi1) && (AX phi2)" == "AX (phi1 && phi2)"
        if ctx.value.text == "&&":
            if ctx.left.value.text == "AX" and ctx.right.value.text == "AX":
                child_and = BinaryNode(value="&&", left=self.visit(ctx.left.child), right=self.visit(ctx.right.child))
                return UnaryNode(value="AX", child=child_and)
            elif ctx.left.value.text == "(" and ctx.left.child.value.text == "AX" and \
                    ctx.right.value.text == "AX":
                child_and = BinaryNode(value="&&", left=self.visit(ctx.left.child.child), right=self.visit(ctx.right.child))
                return UnaryNode(value="AX", child=child_and)
            elif ctx.left.value.text == "AX" and \
                    ctx.right.value.text == "(" and ctx.right.child.value.text == "AX":
                child_and = BinaryNode(value="&&", left=self.visit(ctx.left.child), right=self.visit(ctx.right.child.child))
                return UnaryNode(value="AX", child=child_and)
            elif ctx.left.value.text == "(" and ctx.left.child.value.text == "AX" and \
                    ctx.right.value.text == "(" and ctx.right.child.value.text == "AX":
                # both children have parentheses
                child_and = BinaryNode(value="&&", left=self.visit(ctx.left.child.child), right=self.visit(ctx.right.child.child))
                return UnaryNode(value="AX", child=child_and)

        return BinaryNode(value=ctx.value.text, left=self.visit(ctx.left), right=self.visit(ctx.right))

    def visitHybrid(self, ctx: HCTLParser.HybridContext):
        return HybridNode(value=ctx.value.text, var=ctx.var.text, child=self.visit(ctx.child))


del HCTLParser