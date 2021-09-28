from enum import Enum, auto


# enum for categories of nodes in formula syntax tree
class NodeType(Enum):
    PROP = auto()
    VAR = auto()
    TRUE = auto()
    FALSE = auto()

    NEG = auto()
    DIS = auto()
    CON = auto()
    IMPL = auto()
    EQIV = auto()

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
    EY = auto()
    AY = auto()

    BIND = auto()
    JUMP = auto()
    EXIST = auto()


OP_DICT = {
    "~": NodeType.NEG,
    "||": NodeType.DIS,
    "|": NodeType.DIS,
    "&&": NodeType.CON,
    "&": NodeType.CON,
    "->": NodeType.IMPL,
    "<->": NodeType.EQIV,

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
    "EY": NodeType.EY,
    "AY": NodeType.AY,

    "!": NodeType.BIND,
    "@": NodeType.JUMP,
    "3": NodeType.EXIST,
}