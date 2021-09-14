# Generated from update_fn.g4 by ANTLR 4.7.2
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\17")
        buf.write("a\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16")
        buf.write("\t\16\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\5\4(\n\4")
        buf.write("\3\5\3\5\3\5\3\5\3\5\3\5\3\5\5\5\61\n\5\3\6\3\6\3\7\3")
        buf.write("\7\3\7\3\b\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\n\3\n\3\13\6")
        buf.write("\13C\n\13\r\13\16\13D\3\f\5\fH\n\f\3\f\3\f\3\r\6\rM\n")
        buf.write("\r\r\r\16\rN\3\r\3\r\3\16\3\16\3\16\3\16\3\16\7\16X\n")
        buf.write("\16\f\16\16\16[\13\16\3\16\3\16\3\16\3\16\3\16\3Y\2\17")
        buf.write("\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31")
        buf.write("\16\33\17\3\2\6\4\2VVvv\4\2HHhh\6\2\62;C\\aac|\4\2\13")
        buf.write("\13\"\"\2g\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2")
        buf.write("\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2")
        buf.write("\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2")
        buf.write("\2\33\3\2\2\2\3\35\3\2\2\2\5\37\3\2\2\2\7\'\3\2\2\2\t")
        buf.write("\60\3\2\2\2\13\62\3\2\2\2\r\64\3\2\2\2\17\67\3\2\2\2\21")
        buf.write(":\3\2\2\2\23=\3\2\2\2\25B\3\2\2\2\27G\3\2\2\2\31L\3\2")
        buf.write("\2\2\33R\3\2\2\2\35\36\7*\2\2\36\4\3\2\2\2\37 \7+\2\2")
        buf.write(" \6\3\2\2\2!\"\t\2\2\2\"#\7t\2\2#$\7w\2\2$(\7g\2\2%&\7")
        buf.write("v\2\2&(\7v\2\2\'!\3\2\2\2\'%\3\2\2\2(\b\3\2\2\2)*\t\3")
        buf.write("\2\2*+\7c\2\2+,\7n\2\2,-\7u\2\2-\61\7g\2\2./\7h\2\2/\61")
        buf.write("\7h\2\2\60)\3\2\2\2\60.\3\2\2\2\61\n\3\2\2\2\62\63\7\u0080")
        buf.write("\2\2\63\f\3\2\2\2\64\65\7(\2\2\65\66\7(\2\2\66\16\3\2")
        buf.write("\2\2\678\7~\2\289\7~\2\29\20\3\2\2\2:;\7/\2\2;<\7@\2\2")
        buf.write("<\22\3\2\2\2=>\7>\2\2>?\7/\2\2?@\7@\2\2@\24\3\2\2\2AC")
        buf.write("\t\4\2\2BA\3\2\2\2CD\3\2\2\2DB\3\2\2\2DE\3\2\2\2E\26\3")
        buf.write("\2\2\2FH\7\17\2\2GF\3\2\2\2GH\3\2\2\2HI\3\2\2\2IJ\7\f")
        buf.write("\2\2J\30\3\2\2\2KM\t\5\2\2LK\3\2\2\2MN\3\2\2\2NL\3\2\2")
        buf.write("\2NO\3\2\2\2OP\3\2\2\2PQ\b\r\2\2Q\32\3\2\2\2RS\7\61\2")
        buf.write("\2ST\7,\2\2TY\3\2\2\2UX\5\33\16\2VX\13\2\2\2WU\3\2\2\2")
        buf.write("WV\3\2\2\2X[\3\2\2\2YZ\3\2\2\2YW\3\2\2\2Z\\\3\2\2\2[Y")
        buf.write("\3\2\2\2\\]\7,\2\2]^\7\61\2\2^_\3\2\2\2_`\b\16\2\2`\34")
        buf.write("\3\2\2\2\n\2\'\60DGNWY\3\b\2\2")
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
            "'('", "')'", "'~'", "'&&'", "'||'", "'->'", "'<->'" ]

    symbolicNames = [ "<INVALID>",
            "TRUE", "FALSE", "NEG", "CON", "DIS", "IMPL", "EQIV", "PROP_NAME", 
            "NEWLINE", "WS", "Block_comment" ]

    ruleNames = [ "T__0", "T__1", "TRUE", "FALSE", "NEG", "CON", "DIS", 
                  "IMPL", "EQIV", "PROP_NAME", "NEWLINE", "WS", "Block_comment" ]

    grammarFileName = "update_fn.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


