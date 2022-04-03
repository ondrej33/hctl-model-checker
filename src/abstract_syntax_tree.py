from src.node_type_enum import NodeType, OP_DICT, OP_TO_STRING

"""
This file includes essential classes used for the syntax tree of the HCTL formula
"""

# base class for syntax trees of HCTL formulas and also update functions in BN
class Node:
    def __init__(self, category):
        self.category = category
        self.height = None
        self.subform_string = None

    # just define something so that heapq can be used on nodes
    def __lt__(self, other):
        return self.height < other.height


# specialized node for variables/propositions/params/booleans
class TerminalNode(Node):
    def __init__(self, value, category):
        super().__init__(category)
        self.value = value
        self.subform_string = value
        self.height = 1


# specialized node for unary operators
class UnaryNode(Node):
    def __init__(self, child, category):
        super().__init__(category)
        self.child = child
        self.subform_string = "(" + OP_TO_STRING[category] + child.subform_string + ")"
        self.height = child.height + 1


# specialized node for binary operators
class BinaryNode(Node):
    def __init__(self, left, right, category):
        super().__init__(category)
        self.left = left
        self.right = right
        self.subform_string = "(" + left.subform_string + OP_TO_STRING[category] + right.subform_string + ")"
        self.height = left.height + 1 if left.height > right.height else right.height + 1


# specialized node for hybrid operators
class HybridNode(Node):
    def __init__(self, var, child, category):
        super().__init__(category)
        self.var = var
        self.child = child
        self.subform_string = "(" + OP_TO_STRING[category] + var + ":" + child.subform_string + ")"
        self.height = child.height + 1
