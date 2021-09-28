# Generated from HCTL.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3 ")
        buf.write("R\4\2\t\2\4\3\t\3\4\4\t\4\3\2\6\2\n\n\2\r\2\16\2\13\5")
        buf.write("\2\16\n\2\3\2\3\2\3\2\3\3\6\3\24\n\3\r\3\16\3\25\3\3\5")
        buf.write("\3\31\n\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5")
        buf.write("\4\63\n\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\7")
        buf.write("\4M\n\4\f\4\16\4P\13\4\3\4\2\3\6\5\2\4\6\2\3\3\2\6\7\2")
        buf.write("b\2\r\3\2\2\2\4\30\3\2\2\2\6\62\3\2\2\2\b\n\7\36\2\2\t")
        buf.write("\b\3\2\2\2\n\13\3\2\2\2\13\t\3\2\2\2\13\f\3\2\2\2\f\16")
        buf.write("\3\2\2\2\r\t\3\2\2\2\r\16\3\2\2\2\16\17\3\2\2\2\17\20")
        buf.write("\5\6\4\2\20\21\5\4\3\2\21\3\3\2\2\2\22\24\7\36\2\2\23")
        buf.write("\22\3\2\2\2\24\25\3\2\2\2\25\23\3\2\2\2\25\26\3\2\2\2")
        buf.write("\26\31\3\2\2\2\27\31\7\2\2\3\30\23\3\2\2\2\30\27\3\2\2")
        buf.write("\2\31\5\3\2\2\2\32\33\b\4\1\2\33\63\7\35\2\2\34\63\7\34")
        buf.write("\2\2\35\63\t\2\2\2\36\37\7\3\2\2\37 \5\6\4\2 !\7\4\2\2")
        buf.write("!\63\3\2\2\2\"#\7\b\2\2#\63\5\6\4\17$%\7\24\2\2%\63\5")
        buf.write("\6\4\16&\'\7\31\2\2\'(\7\34\2\2()\7\5\2\2)\63\5\6\4\5")
        buf.write("*+\7\32\2\2+,\7\34\2\2,-\7\5\2\2-\63\5\6\4\4./\7\33\2")
        buf.write("\2/\60\7\34\2\2\60\61\7\5\2\2\61\63\5\6\4\3\62\32\3\2")
        buf.write("\2\2\62\34\3\2\2\2\62\35\3\2\2\2\62\36\3\2\2\2\62\"\3")
        buf.write("\2\2\2\62$\3\2\2\2\62&\3\2\2\2\62*\3\2\2\2\62.\3\2\2\2")
        buf.write("\63N\3\2\2\2\64\65\f\r\2\2\65\66\7\t\2\2\66M\5\6\4\16")
        buf.write("\678\f\f\2\289\7\n\2\29M\5\6\4\r:;\f\13\2\2;<\7\13\2\2")
        buf.write("<M\5\6\4\13=>\f\n\2\2>?\7\f\2\2?M\5\6\4\13@A\f\t\2\2A")
        buf.write("B\7\25\2\2BM\5\6\4\nCD\f\b\2\2DE\7\26\2\2EM\5\6\4\tFG")
        buf.write("\f\7\2\2GH\7\27\2\2HM\5\6\4\7IJ\f\6\2\2JK\7\30\2\2KM\5")
        buf.write("\6\4\6L\64\3\2\2\2L\67\3\2\2\2L:\3\2\2\2L=\3\2\2\2L@\3")
        buf.write("\2\2\2LC\3\2\2\2LF\3\2\2\2LI\3\2\2\2MP\3\2\2\2NL\3\2\2")
        buf.write("\2NO\3\2\2\2O\7\3\2\2\2PN\3\2\2\2\t\13\r\25\30\62LN")
        return buf.getvalue()


class HCTLParser ( Parser ):

    grammarFileName = "HCTL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "':'", "<INVALID>", "<INVALID>", 
                     "'~'", "<INVALID>", "<INVALID>", "'->'", "'<->'", "'A'", 
                     "'E'", "<INVALID>", "'X'", "'Y'", "'F'", "'G'", "<INVALID>", 
                     "'EU'", "'AU'", "'EW'", "'AW'", "'!'", "'@'", "'3'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "TRUE", "FALSE", "NEG", "CON", "DIS", "IMPL", "EQIV", 
                      "A", "E", "PATH", "X", "Y", "F", "G", "TEMPORAL_UNARY", 
                      "E_U", "A_U", "E_W", "A_W", "BIND", "JUMP", "EXISTS", 
                      "VAR_NAME", "PROP_NAME", "NEWLINE", "WS", "Block_comment" ]

    RULE_root = 0
    RULE_fullStop = 1
    RULE_formula = 2

    ruleNames =  [ "root", "fullStop", "formula" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    TRUE=4
    FALSE=5
    NEG=6
    CON=7
    DIS=8
    IMPL=9
    EQIV=10
    A=11
    E=12
    PATH=13
    X=14
    Y=15
    F=16
    G=17
    TEMPORAL_UNARY=18
    E_U=19
    A_U=20
    E_W=21
    A_W=22
    BIND=23
    JUMP=24
    EXISTS=25
    VAR_NAME=26
    PROP_NAME=27
    NEWLINE=28
    WS=29
    Block_comment=30

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def formula(self):
            return self.getTypedRuleContext(HCTLParser.FormulaContext,0)


        def fullStop(self):
            return self.getTypedRuleContext(HCTLParser.FullStopContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(HCTLParser.NEWLINE)
            else:
                return self.getToken(HCTLParser.NEWLINE, i)

        def getRuleIndex(self):
            return HCTLParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = HCTLParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==HCTLParser.NEWLINE:
                self.state = 7 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 6
                    self.match(HCTLParser.NEWLINE)
                    self.state = 9 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==HCTLParser.NEWLINE):
                        break



            self.state = 13
            self.formula(0)
            self.state = 14
            self.fullStop()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FullStopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(HCTLParser.NEWLINE)
            else:
                return self.getToken(HCTLParser.NEWLINE, i)

        def EOF(self):
            return self.getToken(HCTLParser.EOF, 0)

        def getRuleIndex(self):
            return HCTLParser.RULE_fullStop

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFullStop" ):
                listener.enterFullStop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFullStop" ):
                listener.exitFullStop(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFullStop" ):
                return visitor.visitFullStop(self)
            else:
                return visitor.visitChildren(self)




    def fullStop(self):

        localctx = HCTLParser.FullStopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_fullStop)
        self._la = 0 # Token type
        try:
            self.state = 22
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [HCTLParser.NEWLINE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 17 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 16
                    self.match(HCTLParser.NEWLINE)
                    self.state = 19 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==HCTLParser.NEWLINE):
                        break

                pass
            elif token in [HCTLParser.EOF]:
                self.enterOuterAlt(localctx, 2)
                self.state = 21
                self.match(HCTLParser.EOF)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormulaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return HCTLParser.RULE_formula

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class HybridContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a HCTLParser.FormulaContext
            super().__init__(parser)
            self.value = None # Token
            self.var = None # Token
            self.child = None # FormulaContext
            self.copyFrom(ctx)

        def BIND(self):
            return self.getToken(HCTLParser.BIND, 0)
        def VAR_NAME(self):
            return self.getToken(HCTLParser.VAR_NAME, 0)
        def formula(self):
            return self.getTypedRuleContext(HCTLParser.FormulaContext,0)

        def JUMP(self):
            return self.getToken(HCTLParser.JUMP, 0)
        def EXISTS(self):
            return self.getToken(HCTLParser.EXISTS, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHybrid" ):
                listener.enterHybrid(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHybrid" ):
                listener.exitHybrid(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitHybrid" ):
                return visitor.visitHybrid(self)
            else:
                return visitor.visitChildren(self)


    class BinaryContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a HCTLParser.FormulaContext
            super().__init__(parser)
            self.left = None # FormulaContext
            self.value = None # Token
            self.right = None # FormulaContext
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(HCTLParser.FormulaContext)
            else:
                return self.getTypedRuleContext(HCTLParser.FormulaContext,i)

        def CON(self):
            return self.getToken(HCTLParser.CON, 0)
        def DIS(self):
            return self.getToken(HCTLParser.DIS, 0)
        def IMPL(self):
            return self.getToken(HCTLParser.IMPL, 0)
        def EQIV(self):
            return self.getToken(HCTLParser.EQIV, 0)
        def E_U(self):
            return self.getToken(HCTLParser.E_U, 0)
        def A_U(self):
            return self.getToken(HCTLParser.A_U, 0)
        def E_W(self):
            return self.getToken(HCTLParser.E_W, 0)
        def A_W(self):
            return self.getToken(HCTLParser.A_W, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinary" ):
                listener.enterBinary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinary" ):
                listener.exitBinary(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinary" ):
                return visitor.visitBinary(self)
            else:
                return visitor.visitChildren(self)


    class TerminalNodeContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a HCTLParser.FormulaContext
            super().__init__(parser)
            self.value = None # Token
            self.copyFrom(ctx)

        def PROP_NAME(self):
            return self.getToken(HCTLParser.PROP_NAME, 0)
        def VAR_NAME(self):
            return self.getToken(HCTLParser.VAR_NAME, 0)
        def TRUE(self):
            return self.getToken(HCTLParser.TRUE, 0)
        def FALSE(self):
            return self.getToken(HCTLParser.FALSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerminalNode" ):
                listener.enterTerminalNode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerminalNode" ):
                listener.exitTerminalNode(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerminalNode" ):
                return visitor.visitTerminalNode(self)
            else:
                return visitor.visitChildren(self)


    class UnaryContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a HCTLParser.FormulaContext
            super().__init__(parser)
            self.value = None # Token
            self.child = None # FormulaContext
            self.copyFrom(ctx)

        def NEG(self):
            return self.getToken(HCTLParser.NEG, 0)
        def formula(self):
            return self.getTypedRuleContext(HCTLParser.FormulaContext,0)

        def TEMPORAL_UNARY(self):
            return self.getToken(HCTLParser.TEMPORAL_UNARY, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnary" ):
                listener.enterUnary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnary" ):
                listener.exitUnary(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnary" ):
                return visitor.visitUnary(self)
            else:
                return visitor.visitChildren(self)


    class SkipNodeContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a HCTLParser.FormulaContext
            super().__init__(parser)
            self.value = None # Token
            self.child = None # FormulaContext
            self.copyFrom(ctx)

        def formula(self):
            return self.getTypedRuleContext(HCTLParser.FormulaContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSkipNode" ):
                listener.enterSkipNode(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSkipNode" ):
                listener.exitSkipNode(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSkipNode" ):
                return visitor.visitSkipNode(self)
            else:
                return visitor.visitChildren(self)



    def formula(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = HCTLParser.FormulaContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_formula, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 48
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [HCTLParser.PROP_NAME]:
                localctx = HCTLParser.TerminalNodeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 25
                localctx.value = self.match(HCTLParser.PROP_NAME)
                pass
            elif token in [HCTLParser.VAR_NAME]:
                localctx = HCTLParser.TerminalNodeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 26
                localctx.value = self.match(HCTLParser.VAR_NAME)
                pass
            elif token in [HCTLParser.TRUE, HCTLParser.FALSE]:
                localctx = HCTLParser.TerminalNodeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 27
                localctx.value = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==HCTLParser.TRUE or _la==HCTLParser.FALSE):
                    localctx.value = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [HCTLParser.T__0]:
                localctx = HCTLParser.SkipNodeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 28
                localctx.value = self.match(HCTLParser.T__0)
                self.state = 29
                localctx.child = self.formula(0)
                self.state = 30
                self.match(HCTLParser.T__1)
                pass
            elif token in [HCTLParser.NEG]:
                localctx = HCTLParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 32
                localctx.value = self.match(HCTLParser.NEG)
                self.state = 33
                localctx.child = self.formula(13)
                pass
            elif token in [HCTLParser.TEMPORAL_UNARY]:
                localctx = HCTLParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 34
                localctx.value = self.match(HCTLParser.TEMPORAL_UNARY)
                self.state = 35
                localctx.child = self.formula(12)
                pass
            elif token in [HCTLParser.BIND]:
                localctx = HCTLParser.HybridContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 36
                localctx.value = self.match(HCTLParser.BIND)
                self.state = 37
                localctx.var = self.match(HCTLParser.VAR_NAME)
                self.state = 38
                self.match(HCTLParser.T__2)
                self.state = 39
                localctx.child = self.formula(3)
                pass
            elif token in [HCTLParser.JUMP]:
                localctx = HCTLParser.HybridContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 40
                localctx.value = self.match(HCTLParser.JUMP)
                self.state = 41
                localctx.var = self.match(HCTLParser.VAR_NAME)
                self.state = 42
                self.match(HCTLParser.T__2)
                self.state = 43
                localctx.child = self.formula(2)
                pass
            elif token in [HCTLParser.EXISTS]:
                localctx = HCTLParser.HybridContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 44
                localctx.value = self.match(HCTLParser.EXISTS)
                self.state = 45
                localctx.var = self.match(HCTLParser.VAR_NAME)
                self.state = 46
                self.match(HCTLParser.T__2)
                self.state = 47
                localctx.child = self.formula(1)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 76
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 74
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
                    if la_ == 1:
                        localctx = HCTLParser.BinaryContext(self, HCTLParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 50
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 51
                        localctx.value = self.match(HCTLParser.CON)
                        self.state = 52
                        localctx.right = self.formula(12)
                        pass

                    elif la_ == 2:
                        localctx = HCTLParser.BinaryContext(self, HCTLParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 53
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 54
                        localctx.value = self.match(HCTLParser.DIS)
                        self.state = 55
                        localctx.right = self.formula(11)
                        pass

                    elif la_ == 3:
                        localctx = HCTLParser.BinaryContext(self, HCTLParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 56
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 57
                        localctx.value = self.match(HCTLParser.IMPL)
                        self.state = 58
                        localctx.right = self.formula(9)
                        pass

                    elif la_ == 4:
                        localctx = HCTLParser.BinaryContext(self, HCTLParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 59
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 60
                        localctx.value = self.match(HCTLParser.EQIV)
                        self.state = 61
                        localctx.right = self.formula(9)
                        pass

                    elif la_ == 5:
                        localctx = HCTLParser.BinaryContext(self, HCTLParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 62
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 63
                        localctx.value = self.match(HCTLParser.E_U)
                        self.state = 64
                        localctx.right = self.formula(8)
                        pass

                    elif la_ == 6:
                        localctx = HCTLParser.BinaryContext(self, HCTLParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 65
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 66
                        localctx.value = self.match(HCTLParser.A_U)
                        self.state = 67
                        localctx.right = self.formula(7)
                        pass

                    elif la_ == 7:
                        localctx = HCTLParser.BinaryContext(self, HCTLParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 68
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 69
                        localctx.value = self.match(HCTLParser.E_W)
                        self.state = 70
                        localctx.right = self.formula(5)
                        pass

                    elif la_ == 8:
                        localctx = HCTLParser.BinaryContext(self, HCTLParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 71
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 72
                        localctx.value = self.match(HCTLParser.A_W)
                        self.state = 73
                        localctx.right = self.formula(4)
                        pass

             
                self.state = 78
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.formula_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def formula_sempred(self, localctx:FormulaContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 4)
         




