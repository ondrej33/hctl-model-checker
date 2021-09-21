from src.model import *
from src.implementation import *


# computes the set of states which can make transition ONLY into the initial set and nowhere else
# applying ALL of the update functions
def pre_A_all_vars(model: Model, initial: Function) -> Function:
    current_set = model.bdd.add_expr("True")
    for i in range(model.num_props):
        current_set = current_set & pre_A_one_var(model, f"s__{i}", initial)

    # TODO: add same thing as for pre_E_all_vars - create explicit self loops
    return current_set


# AX computed through small update BDDs using pre_A_all_vars
def AX_v2(model: Model, phi: Function) -> Function:
    return pre_A_all_vars(model, phi)


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
