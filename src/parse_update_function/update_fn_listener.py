# Generated from update_fn.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .update_fn_parser import update_fnParser
else:
    from update_fn_parser import update_fnParser

# This class defines a complete listener for a parse tree produced by update_fnParser.
class update_fnListener(ParseTreeListener):

    # Enter a parse tree produced by update_fnParser#root.
    def enterRoot(self, ctx:update_fnParser.RootContext):
        pass

    # Exit a parse tree produced by update_fnParser#root.
    def exitRoot(self, ctx:update_fnParser.RootContext):
        pass


    # Enter a parse tree produced by update_fnParser#fullStop.
    def enterFullStop(self, ctx:update_fnParser.FullStopContext):
        pass

    # Exit a parse tree produced by update_fnParser#fullStop.
    def exitFullStop(self, ctx:update_fnParser.FullStopContext):
        pass


    # Enter a parse tree produced by update_fnParser#binary.
    def enterBinary(self, ctx:update_fnParser.BinaryContext):
        pass

    # Exit a parse tree produced by update_fnParser#binary.
    def exitBinary(self, ctx:update_fnParser.BinaryContext):
        pass


    # Enter a parse tree produced by update_fnParser#terminalNode.
    def enterTerminalNode(self, ctx:update_fnParser.TerminalNodeContext):
        pass

    # Exit a parse tree produced by update_fnParser#terminalNode.
    def exitTerminalNode(self, ctx:update_fnParser.TerminalNodeContext):
        pass


    # Enter a parse tree produced by update_fnParser#unary.
    def enterUnary(self, ctx:update_fnParser.UnaryContext):
        pass

    # Exit a parse tree produced by update_fnParser#unary.
    def exitUnary(self, ctx:update_fnParser.UnaryContext):
        pass


    # Enter a parse tree produced by update_fnParser#skipNode.
    def enterSkipNode(self, ctx:update_fnParser.SkipNodeContext):
        pass

    # Exit a parse tree produced by update_fnParser#skipNode.
    def exitSkipNode(self, ctx:update_fnParser.SkipNodeContext):
        pass



del update_fnParser