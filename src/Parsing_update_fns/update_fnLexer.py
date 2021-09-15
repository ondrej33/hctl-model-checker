# Generated from update_fn.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\17")
        buf.write("e\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\5\4(\n\4")
        buf.write("\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5\61\n\5\3\6\3\6\3\7\3")
        buf.write("\7\3\7\5\78\n\7\3\b\3\b\3\b\5\b=\n\b\3\t\3\t\3\t\3\n\3")
        buf.write("\n\3\n\3\n\3\13\6\13G\n\13\r\13\16\13H\3\f\5\fL\n\f\3")
        buf.write("\f\3\f\3\r\6\rQ\n\r\r\r\16\rR\3\r\3\r\3\16\3\16\3\16\3")
        buf.write("\16\3\16\7\16\\\n\16\f\16\16\16_\13\16\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3]\2\17\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n")
        buf.write("\23\13\25\f\27\r\31\16\33\17\3\2\7\4\2VVvv\4\2HHhh\4\2")
        buf.write("##\u0080\u0080\6\2\62;C\\aac|\4\2\13\13\"\"\2m\2\3\3\2")
        buf.write("\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2")
        buf.write("\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2")
        buf.write("\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\3\35")
        buf.write("\3\2\2\2\5\37\3\2\2\2\7\'\3\2\2\2\t\60\3\2\2\2\13\62\3")
        buf.write("\2\2\2\r\67\3\2\2\2\17<\3\2\2\2\21>\3\2\2\2\23A\3\2\2")
        buf.write("\2\25F\3\2\2\2\27K\3\2\2\2\31P\3\2\2\2\33V\3\2\2\2\35")
        buf.write("\36\7*\2\2\36\4\3\2\2\2\37 \7+\2\2 \6\3\2\2\2!\"\t\2\2")
        buf.write("\2\"#\7t\2\2#$\7w\2\2$(\7g\2\2%&\7v\2\2&(\7v\2\2\'!\3")
        buf.write("\2\2\2\'%\3\2\2\2(\b\3\2\2\2)*\t\3\2\2*+\7c\2\2+,\7n\2")
        buf.write("\2,-\7u\2\2-\61\7g\2\2./\7h\2\2/\61\7h\2\2\60)\3\2\2\2")
        buf.write("\60.\3\2\2\2\61\n\3\2\2\2\62\63\t\4\2\2\63\f\3\2\2\2\64")
        buf.write("\65\7(\2\2\658\7(\2\2\668\7(\2\2\67\64\3\2\2\2\67\66\3")
        buf.write("\2\2\28\16\3\2\2\29:\7~\2\2:=\7~\2\2;=\7~\2\2<9\3\2\2")
        buf.write("\2<;\3\2\2\2=\20\3\2\2\2>?\7/\2\2?@\7@\2\2@\22\3\2\2\2")
        buf.write("AB\7>\2\2BC\7/\2\2CD\7@\2\2D\24\3\2\2\2EG\t\5\2\2FE\3")
        buf.write("\2\2\2GH\3\2\2\2HF\3\2\2\2HI\3\2\2\2I\26\3\2\2\2JL\7\17")
        buf.write("\2\2KJ\3\2\2\2KL\3\2\2\2LM\3\2\2\2MN\7\f\2\2N\30\3\2\2")
        buf.write("\2OQ\t\6\2\2PO\3\2\2\2QR\3\2\2\2RP\3\2\2\2RS\3\2\2\2S")
        buf.write("T\3\2\2\2TU\b\r\2\2U\32\3\2\2\2VW\7\61\2\2WX\7,\2\2X]")
        buf.write("\3\2\2\2Y\\\5\33\16\2Z\\\13\2\2\2[Y\3\2\2\2[Z\3\2\2\2")
        buf.write("\\_\3\2\2\2]^\3\2\2\2][\3\2\2\2^`\3\2\2\2_]\3\2\2\2`a")
        buf.write("\7,\2\2ab\7\61\2\2bc\3\2\2\2cd\b\16\2\2d\34\3\2\2\2\f")
        buf.write("\2\'\60\67<HKR[]\3\b\2\2")
        return buf.getvalue()


class update_fnLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    TRUE = 3
    FALSE = 4
    NEG = 5
    CON = 6
    DIS = 7
    IMPL = 8
    EQIV = 9
    PROP_NAME = 10
    NEWLINE = 11
    WS = 12
    Block_comment = 13

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'->'", "'<->'" ]

    symbolicNames = [ "<INVALID>",
            "TRUE", "FALSE", "NEG", "CON", "DIS", "IMPL", "EQIV", "PROP_NAME", 
            "NEWLINE", "WS", "Block_comment" ]

    ruleNames = [ "T__0", "T__1", "TRUE", "FALSE", "NEG", "CON", "DIS", 
                  "IMPL", "EQIV", "PROP_NAME", "NEWLINE", "WS", "Block_comment" ]

    grammarFileName = "update_fn.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


