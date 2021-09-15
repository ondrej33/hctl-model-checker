# Generated from update_fn.g4 by ANTLR 4.9.2
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
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\17")
        buf.write("\67\4\2\t\2\4\3\t\3\4\4\t\4\3\2\6\2\n\n\2\r\2\16\2\13")
        buf.write("\5\2\16\n\2\3\2\3\2\3\2\3\3\6\3\24\n\3\r\3\16\3\25\3\3")
        buf.write("\5\3\31\n\3\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4$\n")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\7\4")
        buf.write("\62\n\4\f\4\16\4\65\13\4\3\4\2\3\6\5\2\4\6\2\3\3\2\5\6")
        buf.write("\2>\2\r\3\2\2\2\4\30\3\2\2\2\6#\3\2\2\2\b\n\7\r\2\2\t")
        buf.write("\b\3\2\2\2\n\13\3\2\2\2\13\t\3\2\2\2\13\f\3\2\2\2\f\16")
        buf.write("\3\2\2\2\r\t\3\2\2\2\r\16\3\2\2\2\16\17\3\2\2\2\17\20")
        buf.write("\5\6\4\2\20\21\5\4\3\2\21\3\3\2\2\2\22\24\7\r\2\2\23\22")
        buf.write("\3\2\2\2\24\25\3\2\2\2\25\23\3\2\2\2\25\26\3\2\2\2\26")
        buf.write("\31\3\2\2\2\27\31\7\2\2\3\30\23\3\2\2\2\30\27\3\2\2\2")
        buf.write("\31\5\3\2\2\2\32\33\b\4\1\2\33$\7\f\2\2\34$\t\2\2\2\35")
        buf.write("\36\7\3\2\2\36\37\5\6\4\2\37 \7\4\2\2 $\3\2\2\2!\"\7\7")
        buf.write("\2\2\"$\5\6\4\7#\32\3\2\2\2#\34\3\2\2\2#\35\3\2\2\2#!")
        buf.write("\3\2\2\2$\63\3\2\2\2%&\f\6\2\2&\'\7\b\2\2\'\62\5\6\4\7")
        buf.write("()\f\5\2\2)*\7\t\2\2*\62\5\6\4\6+,\f\4\2\2,-\7\n\2\2-")
        buf.write("\62\5\6\4\4./\f\3\2\2/\60\7\13\2\2\60\62\5\6\4\4\61%\3")
        buf.write("\2\2\2\61(\3\2\2\2\61+\3\2\2\2\61.\3\2\2\2\62\65\3\2\2")
        buf.write("\2\63\61\3\2\2\2\63\64\3\2\2\2\64\7\3\2\2\2\65\63\3\2")
        buf.write("\2\2\t\13\r\25\30#\61\63")
        return buf.getvalue()


class update_fnParser ( Parser ):

    grammarFileName = "update_fn.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'->'", "'<->'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "TRUE", "FALSE", 
                      "NEG", "CON", "DIS", "IMPL", "EQIV", "PROP_NAME", 
                      "NEWLINE", "WS", "Block_comment" ]

    RULE_root = 0
    RULE_fullStop = 1
    RULE_formula = 2

    ruleNames =  [ "root", "fullStop", "formula" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    TRUE=3
    FALSE=4
    NEG=5
    CON=6
    DIS=7
    IMPL=8
    EQIV=9
    PROP_NAME=10
    NEWLINE=11
    WS=12
    Block_comment=13

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
            return self.getTypedRuleContext(update_fnParser.FormulaContext,0)


        def fullStop(self):
            return self.getTypedRuleContext(update_fnParser.FullStopContext,0)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(update_fnParser.NEWLINE)
            else:
                return self.getToken(update_fnParser.NEWLINE, i)

        def getRuleIndex(self):
            return update_fnParser.RULE_root

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

        localctx = update_fnParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==update_fnParser.NEWLINE:
                self.state = 7 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 6
                    self.match(update_fnParser.NEWLINE)
                    self.state = 9 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==update_fnParser.NEWLINE):
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
                return self.getTokens(update_fnParser.NEWLINE)
            else:
                return self.getToken(update_fnParser.NEWLINE, i)

        def EOF(self):
            return self.getToken(update_fnParser.EOF, 0)

        def getRuleIndex(self):
            return update_fnParser.RULE_fullStop

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

        localctx = update_fnParser.FullStopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_fullStop)
        self._la = 0 # Token type
        try:
            self.state = 22
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [update_fnParser.NEWLINE]:
                self.enterOuterAlt(localctx, 1)
                self.state = 17 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 16
                    self.match(update_fnParser.NEWLINE)
                    self.state = 19 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==update_fnParser.NEWLINE):
                        break

                pass
            elif token in [update_fnParser.EOF]:
                self.enterOuterAlt(localctx, 2)
                self.state = 21
                self.match(update_fnParser.EOF)
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
            return update_fnParser.RULE_formula

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class BinaryContext(FormulaContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a update_fnParser.FormulaContext
            super().__init__(parser)
            self.left = None # FormulaContext
            self.value = None # Token
            self.right = None # FormulaContext
            self.copyFrom(ctx)

        def formula(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(update_fnParser.FormulaContext)
            else:
                return self.getTypedRuleContext(update_fnParser.FormulaContext,i)

        def CON(self):
            return self.getToken(update_fnParser.CON, 0)
        def DIS(self):
            return self.getToken(update_fnParser.DIS, 0)
        def IMPL(self):
            return self.getToken(update_fnParser.IMPL, 0)
        def EQIV(self):
            return self.getToken(update_fnParser.EQIV, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a update_fnParser.FormulaContext
            super().__init__(parser)
            self.value = None # Token
            self.copyFrom(ctx)

        def PROP_NAME(self):
            return self.getToken(update_fnParser.PROP_NAME, 0)
        def TRUE(self):
            return self.getToken(update_fnParser.TRUE, 0)
        def FALSE(self):
            return self.getToken(update_fnParser.FALSE, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a update_fnParser.FormulaContext
            super().__init__(parser)
            self.value = None # Token
            self.child = None # FormulaContext
            self.copyFrom(ctx)

        def NEG(self):
            return self.getToken(update_fnParser.NEG, 0)
        def formula(self):
            return self.getTypedRuleContext(update_fnParser.FormulaContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a update_fnParser.FormulaContext
            super().__init__(parser)
            self.value = None # Token
            self.child = None # FormulaContext
            self.copyFrom(ctx)

        def formula(self):
            return self.getTypedRuleContext(update_fnParser.FormulaContext,0)


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
        localctx = update_fnParser.FormulaContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_formula, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [update_fnParser.PROP_NAME]:
                localctx = update_fnParser.TerminalNodeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 25
                localctx.value = self.match(update_fnParser.PROP_NAME)
                pass
            elif token in [update_fnParser.TRUE, update_fnParser.FALSE]:
                localctx = update_fnParser.TerminalNodeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 26
                localctx.value = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==update_fnParser.TRUE or _la==update_fnParser.FALSE):
                    localctx.value = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [update_fnParser.T__0]:
                localctx = update_fnParser.SkipNodeContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 27
                localctx.value = self.match(update_fnParser.T__0)
                self.state = 28
                localctx.child = self.formula(0)
                self.state = 29
                self.match(update_fnParser.T__1)
                pass
            elif token in [update_fnParser.NEG]:
                localctx = update_fnParser.UnaryContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 31
                localctx.value = self.match(update_fnParser.NEG)
                self.state = 32
                localctx.child = self.formula(5)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 49
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 47
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
                    if la_ == 1:
                        localctx = update_fnParser.BinaryContext(self, update_fnParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 35
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 36
                        localctx.value = self.match(update_fnParser.CON)
                        self.state = 37
                        localctx.right = self.formula(5)
                        pass

                    elif la_ == 2:
                        localctx = update_fnParser.BinaryContext(self, update_fnParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 38
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 39
                        localctx.value = self.match(update_fnParser.DIS)
                        self.state = 40
                        localctx.right = self.formula(4)
                        pass

                    elif la_ == 3:
                        localctx = update_fnParser.BinaryContext(self, update_fnParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 41
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 42
                        localctx.value = self.match(update_fnParser.IMPL)
                        self.state = 43
                        localctx.right = self.formula(2)
                        pass

                    elif la_ == 4:
                        localctx = update_fnParser.BinaryContext(self, update_fnParser.FormulaContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_formula)
                        self.state = 44
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 45
                        localctx.value = self.match(update_fnParser.EQIV)
                        self.state = 46
                        localctx.right = self.formula(2)
                        pass

             
                self.state = 51
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
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 1)
         




