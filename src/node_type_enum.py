from enum import Enum, auto


# enum for categories of nodes in formula syntax tree
class NodeType(Enum):
    PROP = auto()
    VAR = auto()
    TRUE = auto()
    FALSE = auto()

    NEG = auto()
    OR = auto()
    AND = auto()
    IMP = auto()
    IFF = auto()
    XOR = auto()

    EX = auto()
    AX = auto()
    EF = auto()
    AF = auto()
    EU = auto()
    AU = auto()
    EG = auto()
    AG = auto()
    EW = auto()
    AW = auto()

    BIND = auto()
    JUMP = auto()
    EXIST = auto()


# mapping from string representation of operators to the enum representation
OP_DICT = {
    "~": NodeType.NEG,
    "||": NodeType.OR,
    "|": NodeType.OR,
    "&&": NodeType.AND,
    "&": NodeType.AND,
    "->": NodeType.IMP,
    "<->": NodeType.IFF,
    "^": NodeType.XOR,

    "EX": NodeType.EX,
    "AX": NodeType.AX,
    "EF": NodeType.EF,
    "AF": NodeType.AF,
    "EG": NodeType.EG,
    "AG": NodeType.AG,
    "EU": NodeType.EU,
    "AU": NodeType.AU,
    "EW": NodeType.EW,
    "AW": NodeType.AW,

    "!": NodeType.BIND,
    "@": NodeType.JUMP,
    "3": NodeType.EXIST,
}

# mapping from enum representation of operators to the string
OP_TO_STRING = {op: op_string for (op_string, op) in OP_DICT.items()}