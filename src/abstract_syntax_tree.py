# TODO: use some inheritance and merge some code

from NodeTypeEnum import NodeType, OP_DICT


class Node:
    def __init__(self, value):
        self.value = value
        self.height = None
        self.subform_string = None
        self.category = None

    # just define something so that heapq can be used on nodes
    def __lt__(self, other):
        return self.value < other.value


class TerminalNode(Node):
    def __init__(self, value):
        super().__init__(value)
        self.subform_string = value
        self.height = 1
        self.category = self.classify_terminal()

    def classify_terminal(self):
        if self.value in {"True", "true", "tt"}:
            return NodeType.TRUE
        elif self.value in {"False", "false", "ff"}:
            return NodeType.FALSE
        elif '{' in self.value:
            return NodeType.VAR
        else:
            return NodeType.PROP


class UnaryNode(Node):
    def __init__(self, child, value):
        super().__init__(value)
        self.child = child
        self.subform_string = "(" + value + child.subform_string + ")"
        self.height = child.height + 1
        self.category = OP_DICT[value]


class BinaryNode(Node):
    def __init__(self, left, right, value):
        super().__init__(value)
        self.left = left
        self.right = right
        self.subform_string = "(" + left.subform_string + value + right.subform_string + ")"
        self.height = left.height + 1 if left.height > right.height else right.height + 1
        self.category = OP_DICT[value]


class HybridNode(Node):
    def __init__(self, var, child, value):
        super().__init__(value)
        self.var = var
        self.child = child
        self.subform_string = "(" + value + var + ":" + child.subform_string + ")"
        self.height = child.height + 1
        self.category = OP_DICT[value]
