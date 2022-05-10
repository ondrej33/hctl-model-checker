from antlr4 import *
from src.abstract_syntax_tree import *
from src.exceptions import InvalidUpdateFnOperationError
from src.parse_update_function.parser_wrapper_update_fn import parse_update_fn_to_tree


class EvaluateExpressionVisitor:
    """Class wrapping the evaluation of update function into BDDs."""

    def __init__(self):
        pass

    def visit(self, node, bdd):
        """Visit node and recursively evaluate the subformula which it represents into BDD.

        Compute in bottom-up manner. First evaluate potential children, then combine
        their results depending on the type and operation corresponding to the node.

        Args:
            node: node of the syntax tree of processed subformula
            bdd: bdd manager

        Returns:
            BDD encoding of the given update function (formula).
        """
        result = bdd.add_expr("False")
        if type(node) == TerminalNode:
            # we have either prop/param here (bdd var) or True/False, which is also OK to evaluate
            result = bdd.add_expr(node.value)

        # we have only the negation here at the moment
        elif type(node) == UnaryNode and node.category == NodeType.NEG:
            result = ~self.visit(node.child, bdd)

        elif type(node) == BinaryNode:
            if node.category == NodeType.AND:
                result = self.visit(node.left, bdd) & self.visit(node.right, bdd)
            elif node.category == NodeType.OR:
                result = self.visit(node.left, bdd) | self.visit(node.right, bdd)
            elif node.category == NodeType.IMP:
                result = self.visit(node.left, bdd).implies(self.visit(node.right, bdd))
            elif node.category == NodeType.IFF:
                result = self.visit(node.left, bdd).equiv(self.visit(node.right, bdd))
            elif node.category == NodeType.XOR:
                result = ~ self.visit(node.left, bdd).equiv(self.visit(node.right, bdd))
        else:
            raise InvalidUpdateFnOperationError(node.category)
        return result


def encode_update_fn_tree(as_tree: Node, bdd):  # -> Function:
    """Encode update function represented by a tree into the BDD."""
    result = EvaluateExpressionVisitor().visit(as_tree, bdd)
    return result


def encode_update_fn_string(formula: str, bdd):  # -> Function:
    """Parse update function and encode it into the BDD."""
    as_tree = parse_update_fn_to_tree(formula)
    return encode_update_fn_tree(as_tree, bdd)
