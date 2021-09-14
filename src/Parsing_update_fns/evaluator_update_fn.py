from antlr4 import *
from src.abstract_syntax_tree import *
from src.implementation import *
from parser_update_fn import parse_to_tree


class EvaluateExpressionVisitor:

    # Visits node and depending on its type and operation, evaluates the subformula which it represents
    # Uses results from children, combines them until whole thing is done
    def visit(self, node, bdd):
        result = bdd.add_expr("False")
        if type(node) == TerminalNode:
            # TODO: differentiate between true/false OR prop/param node
            result = bdd.add_expr(node.value)
        elif type(node) == UnaryNode:
            # we have only the negation here
            result = ~self.visit(node.child, bdd)
        elif type(node) == BinaryNode:
            if node.value == '&&':
                result = self.visit(node.left, bdd) & self.visit(node.right, bdd)
            elif node.value == '||':
                result = self.visit(node.left, bdd) | self.visit(node.right, bdd)
            elif node.value == '->':
                result = self.visit(node.left, bdd).implies(self.visit(node.right, bdd))
            elif node.value == '<->':
                result = self.visit(node.left, bdd).equiv(self.visit(node.right, bdd))
        return result


def eval_tree(as_tree: Node, bdd: BDD) -> Function:
    result = EvaluateExpressionVisitor().visit(as_tree, bdd)
    return result


def parse_and_eval(formula: str, bdd: BDD) -> Function:
    as_tree = parse_to_tree(formula)
    return eval_tree(as_tree, bdd)


if __name__ == '__main__':
    # TODO: change path
    bnet_path = "bnet_examples/023.bnet"
