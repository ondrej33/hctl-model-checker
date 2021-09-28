from src.Parsing_update_fns.update_fnLexer import update_fnLexer
from src.Parsing_update_fns.update_fnParser import update_fnParser
from src.Parsing_update_fns.update_fnVisitor import update_fnVisitor

from antlr4 import *
from src.abstract_syntax_tree import *


# To create update_fnParser and other files from grammar:
#    $ java -jar "/usr/local/lib/antlr-4.9.2-complete.jar" -Dlanguage=Python3 -visitor update_fn.g4
# or $ antlr4 -Dlanguage=Python3 -visitor update_fn.g4
# then change update_fnVisitor to this: (and add import of structures)

"""
# code changed in update_fnVisitor follows (this is backup, it might disappear when creating new parser):

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
            return TerminalNode(value="True")
        elif ctx.value.text in {"False", "false", "ff"}:
            return TerminalNode(value="False")

        return TerminalNode(value=ctx.value.text)

    def visitUnary(self, ctx: update_fnParser.UnaryContext):
        return UnaryNode(value=ctx.value.text, child=self.visit(ctx.child))

    def visitBinary(self, ctx: update_fnParser.BinaryContext):
        return BinaryNode(value=ctx.value.text, left=self.visit(ctx.left), right=self.visit(ctx.right))
"""


# parses given formula of update function into the syntax tree
def parse_to_tree(formula) -> Node:
    lexer = update_fnLexer(InputStream(formula))
    stream = CommonTokenStream(lexer)
    parser = update_fnParser(stream)
    tree = parser.root()

    as_tree = update_fnVisitor().visitRoot(tree)
    return as_tree
