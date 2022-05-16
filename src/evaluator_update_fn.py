from antlr4 import *
from src.abstract_syntax_tree import *
from src.exceptions import InvalidUpdateFnOperationError
from src.parse_update_function.parser_wrapper_update_fn import parse_update_fn_to_tree


def eval_uf_tree_rec(node, bdd):
    """Recursively evaluate the update fn' subformula represented by tree into BDD.

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
        # there is either prop/param (bdd var) or true/false
        result = bdd.add_expr(node.value)

    # there is only the negation at the moment
    elif type(node) == UnaryNode and node.category == NodeType.NEG:
        result = ~eval_uf_tree_rec(node.child, bdd)

    elif type(node) == BinaryNode:
        if node.category == NodeType.AND:
            result = eval_uf_tree_rec(node.left, bdd) & eval_uf_tree_rec(node.right, bdd)
        elif node.category == NodeType.OR:
            result = eval_uf_tree_rec(node.left, bdd) | eval_uf_tree_rec(node.right, bdd)
        elif node.category == NodeType.IMP:
            result = eval_uf_tree_rec(node.left, bdd).implies(eval_uf_tree_rec(node.right, bdd))
        elif node.category == NodeType.IFF:
            result = eval_uf_tree_rec(node.left, bdd).equiv(eval_uf_tree_rec(node.right, bdd))
        elif node.category == NodeType.XOR:
            result = ~ eval_uf_tree_rec(node.left, bdd).equiv(eval_uf_tree_rec(node.right, bdd))
    else:
        raise InvalidUpdateFnOperationError(node.category)
    return result


def eval_update_fn_tree(as_tree: Node, bdd):  # -> Function:
    """Encode update function represented by a tree into a BDD instance."""
    result = eval_uf_tree_rec(as_tree, bdd)
    return result


def eval_update_fn_string(formula: str, bdd):  # -> Function:
    """Parse update function and encode it into a BDD instance."""
    as_tree = parse_update_fn_to_tree(formula)
    return eval_update_fn_tree(as_tree, bdd)
