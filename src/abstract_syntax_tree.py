from src.node_type_enum import NodeType, OP_DICT, OP_TO_STRING

"""
This file includes essential classes used for the syntax tree of the HCTL formula
"""


class Node:
    """Base class for syntax trees of HCTL formulas and update functions in BN."""

    def __init__(self, category):
        self.category = category
        self.height = None
        self.subform_string = None

    def __lt__(self, other):
        # We need < so that heapq can be used on nodes.
        return self.height < other.height


class TerminalNode(Node):
    """Specialization of the node for terminals - variables/propositions/params/constants."""

    def __init__(self, value, category):
        super().__init__(category)
        self.value = value
        self.subform_string = value
        self.height = 1


class UnaryNode(Node):
    """Specialized node for unary operators."""

    def __init__(self, child, category):
        super().__init__(category)
        self.child = child
        self.subform_string = "(" + OP_TO_STRING[category] + child.subform_string + ")"
        self.height = child.height + 1


class BinaryNode(Node):
    """Specialized node for binary operators."""

    def __init__(self, left, right, category):
        super().__init__(category)
        self.left = left
        self.right = right
        self.subform_string = "(" + left.subform_string + OP_TO_STRING[category] + right.subform_string + ")"
        self.height = left.height + 1 if left.height > right.height else right.height + 1


class HybridNode(Node):
    """Specialized node for hybrid operators."""

    def __init__(self, var, child, category):
        super().__init__(category)
        self.var = var
        self.child = child
        self.subform_string = "(" + OP_TO_STRING[category] + var + ":" + child.subform_string + ")"
        self.height = child.height + 1
