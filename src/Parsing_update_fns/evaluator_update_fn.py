from antlr4 import *
from src.abstract_syntax_tree import *
from src.Parsing_update_fns.parser_update_fn import parse_to_tree


class EvaluateExpressionVisitor:

    # Visits node and depending on its type and operation, evaluates the subformula which it represents
    # Uses results from children, combines them until whole thing is done
    def visit(self, node, bdd):
        result = bdd.add_expr("False")
        if type(node) == TerminalNode:
            # we have either prop/param here (bdd var) or True/False, which is also OK
            result = bdd.add_expr(node.value)
        elif type(node) == UnaryNode:
            # we have only the negation here at the moment
            result = ~self.visit(node.child, bdd)
        elif type(node) == BinaryNode:
            if node.value == '&&' or node.value == '&':
                result = self.visit(node.left, bdd) & self.visit(node.right, bdd)
            elif node.value == '||' or node.value == '|':
                result = self.visit(node.left, bdd) | self.visit(node.right, bdd)
            elif node.value == '->':
                result = self.visit(node.left, bdd).implies(self.visit(node.right, bdd))
            elif node.value == '<->':
                result = self.visit(node.left, bdd).equiv(self.visit(node.right, bdd))
        return result


def eval_tree(as_tree: Node, bdd):  # -> Function:
    result = EvaluateExpressionVisitor().visit(as_tree, bdd)
    return result


def parse_and_eval(formula: str, bdd):  # -> Function:
    as_tree = parse_to_tree(formula)
    return eval_tree(as_tree, bdd)
