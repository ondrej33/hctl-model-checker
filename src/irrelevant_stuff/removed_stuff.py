from src.model import *
from src.implementation import *


# fixpoint version of AF
def AF_v2(model: Model, phi: Function) -> Function:
    # lfpZ. ( phi OR AX Z )
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = model.bdd.apply("or", new, AX(model, old))
    return old


# fixpoint version of AG
def AG_v2(model: Model, phi: Function) -> Function:
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old & AX(model, old)
    return old
