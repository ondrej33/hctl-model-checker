# Generated from HCTL.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .hctl_parser import HCTLParser
else:
    from hctl_parser import HCTLParser

# This class defines a complete listener for a parse tree produced by HCTLParser.
class HCTLListener(ParseTreeListener):

    # Enter a parse tree produced by HCTLParser#root.
    def enterRoot(self, ctx:HCTLParser.RootContext):
        pass

    # Exit a parse tree produced by HCTLParser#root.
    def exitRoot(self, ctx:HCTLParser.RootContext):
        pass


    # Enter a parse tree produced by HCTLParser#fullStop.
    def enterFullStop(self, ctx:HCTLParser.FullStopContext):
        pass

    # Exit a parse tree produced by HCTLParser#fullStop.
    def exitFullStop(self, ctx:HCTLParser.FullStopContext):
        pass


    # Enter a parse tree produced by HCTLParser#hybrid.
    def enterHybrid(self, ctx:HCTLParser.HybridContext):
        pass

    # Exit a parse tree produced by HCTLParser#hybrid.
    def exitHybrid(self, ctx:HCTLParser.HybridContext):
        pass


    # Enter a parse tree produced by HCTLParser#binary.
    def enterBinary(self, ctx:HCTLParser.BinaryContext):
        pass

    # Exit a parse tree produced by HCTLParser#binary.
    def exitBinary(self, ctx:HCTLParser.BinaryContext):
        pass


    # Enter a parse tree produced by HCTLParser#terminalNode.
    def enterTerminalNode(self, ctx:HCTLParser.TerminalNodeContext):
        pass

    # Exit a parse tree produced by HCTLParser#terminalNode.
    def exitTerminalNode(self, ctx:HCTLParser.TerminalNodeContext):
        pass


    # Enter a parse tree produced by HCTLParser#unary.
    def enterUnary(self, ctx:HCTLParser.UnaryContext):
        pass

    # Exit a parse tree produced by HCTLParser#unary.
    def exitUnary(self, ctx:HCTLParser.UnaryContext):
        pass


    # Enter a parse tree produced by HCTLParser#skipNode.
    def enterSkipNode(self, ctx:HCTLParser.SkipNodeContext):
        pass

    # Exit a parse tree produced by HCTLParser#skipNode.
    def exitSkipNode(self, ctx:HCTLParser.SkipNodeContext):
        pass



del HCTLParser