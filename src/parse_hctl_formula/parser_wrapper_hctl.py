from src.parse_hctl_formula.hctl_lexer import HCTLLexer
from src.parse_hctl_formula.hctl_parser import HCTLParser
from src.parse_hctl_formula.hctl_visitor import HCTLVisitor

from antlr4 import *
from src.abstract_syntax_tree import *

# To create HCTLParser and other files from grammar:
#    $ java -jar "/usr/local/lib/antlr-4.9.2-complete.jar" -Dlanguage=Python3 -visitor HCTL.g4
# or $ antlr4 -Dlanguage=Python3 -visitor HCTL.g4
# then change HCTLVisitor to this: (and add import of structures)


def parse_to_tree(formula: str) -> Node:
    """Parse given HCTL formula into the syntax tree."""
    lexer = HCTLLexer(InputStream(formula))
    stream = CommonTokenStream(lexer)
    parser = HCTLParser(stream)
    tree = parser.root()

    as_tree = HCTLVisitor().visitRoot(tree)
    return as_tree
