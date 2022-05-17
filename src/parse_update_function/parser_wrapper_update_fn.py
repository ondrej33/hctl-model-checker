from src.parse_update_function.update_fn_lexer import update_fnLexer
from src.parse_update_function.update_fn_parser import update_fnParser
from src.parse_update_function.update_fn_visitor import update_fnVisitor

from antlr4 import *
from src.abstract_syntax_tree import *


# To create update_fnParser and other files from grammar:
#    $ java -jar "/usr/local/lib/antlr-4.9.2-complete.jar" -Dlanguage=Python3 -visitor update_fn.g4
# or $ antlr4 -Dlanguage=Python3 -visitor update_fn.g4
# BEWARE! - backup update_fnVisitor file, it would be be rewritten


def parse_update_fn_to_tree(formula) -> Node:
    """Parse given update function's formula into an abstract syntax tree."""
    lexer = update_fnLexer(InputStream(formula))
    stream = CommonTokenStream(lexer)
    parser = update_fnParser(stream)
    tree = parser.root()

    as_tree = update_fnVisitor().visitRoot(tree)
    return as_tree
