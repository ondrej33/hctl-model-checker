from src.model import *

"""
This file includes the implementation for evaluating all components of HCTL formula
It is build so that we can combine them into the bottom-up algorithm
"""

# ============================================================================================= #
# ============================= SUBFORMULAS EVALUATION PART =================================== #
# ============================================================================================= #


# creates a bdd representing all states labeled by proposition given
def labeled_by(model: Model, prop: str) -> Function:
    return model.bdd.add_expr(prop) & model.mk_unit_colored_set()


def negate(model: Model, phi: Function) -> Function:
    return ~phi & model.mk_unit_colored_set()


# creates comparator for variables s1, s2,... and var1, var2,...
# it will be bdd for (s1 <=> var1) & (s2 <=> var2)...
def create_comparator(model: Model, var: str) -> Function:
    expr_parts = [f"(s__{i} <=> {var}__{i})" for i in range(model.num_props)]
    expr = " & ".join(expr_parts)
    comparator = model.bdd.add_expr(expr) & model.mk_unit_colored_set()
    return comparator


# Release(x, Comparator(x) & SMC(M, phi))
def bind(model: Model, phi: Function, var: str) -> Function:
    comparator = create_comparator(model, var)
    intersection = comparator & phi

    # now lets use existential quantification to get rid of the bdd vars coding VAR
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]
    result = model.bdd.quantify(intersection, vars_to_get_rid)
    return result


# Release(s, Comparator(x) & SMC(M, phi))
def jump(model: Model, phi: Function, var: str) -> Function:
    comparator = create_comparator(model, var)
    intersection = comparator & phi

    # now lets use existential quantification to get rid of the bdd vars coding STATE
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props)]
    result = model.bdd.quantify(intersection, vars_to_get_rid)
    return result


# Release(x, SMC(M, phi))
def existential(model: Model, phi: Function, var: str) -> Function:
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]
    result = model.bdd.quantify(phi, vars_to_get_rid)
    return result


# computes the set of states which can make transition into the initial set
# applying the update function of the given `var`
# SHOULD BE USED ONLY BY FUNCTIONS IN THIS FILE
def pre_E_one_var(model: Model, initial: Function, var: str) -> Function:
    """
    NEGATIVE_PREDECESSOR = !X & Exists(SET & X, 'X') & B_X  
    POSITIVE_PREDECESSOR = X & Exists(SET & !X, 'X') & !B_X
    PREDECESSORS_IN_X = NEGATIVE_PREDECESSOR | POSITIVE_PREDECESSOR
    """
    var_bdd = labeled_by(model, var)
    not_var_bdd = negate(model, var_bdd)
    neg_pred = not_var_bdd & model.bdd.quantify(initial & var_bdd, [var]) & model.update_fns[var]
    pos_pred = var_bdd & model.bdd.quantify(initial & not_var_bdd, [var]) & negate(model, model.update_fns[var])
    return neg_pred | pos_pred


# computes the set of states which can make transition into the initial set
# applying ALL of the update functions
def pre_E_all_vars(model: Model, initial: Function) -> Function:
    current_set = model.mk_empty_colored_set()
    for i in range(model.num_props):
        current_set = current_set | pre_E_one_var(model, initial, f"s__{i}")
    return current_set | (initial & model.stable)


def EX(model: Model, phi: Function) -> Function:
    return pre_E_all_vars(model, phi)


# compute EU based on saturation, faster than fixed-point version
def EU_saturated(model: Model, phi1: Function, phi2: Function) -> Function:
    result = phi2
    done = False
    while not done:
        done = True
        for i in range(model.num_props, 0, -1):
            update = (phi1 & pre_E_one_var(model, result, f"s__{i-1}")) & negate(model, result)
            if update != model.bdd.false:
                result = result | update
                done = False
                break
    #reorder(model.bdd)
    return result


# EF computed via EU with saturation
# is correct since  EF f == [true EU f]
def EF_saturated(model: Model, phi: Function) -> Function:
    return EU_saturated(model, model.mk_unit_colored_set(), phi)


# classical fixed-point algorithm for EG
def EG(model: Model, phi: Function) -> Function:
    old = phi
    new = model.mk_empty_colored_set()
    while old != new:
        new = old
        old = old & EX(model, old)
    return old


# AX computed through the EX
def AX(model: Model, phi: Function) -> Function:
    # AX f = ~EX (~f)
    return negate(model, EX(model, negate(model, phi)))


# AX computed through the EG
def AF(model: Model, phi1: Function) -> Function:
    # AF f = ~EG (~f)
    return negate(model, EG(model, negate(model, phi1)))


# AG computed through EF
def AG(model: Model, phi1: Function) -> Function:
    # AG f = ~EF (~f)
    return negate(model, EF_saturated(model, negate(model,phi1)))


# AU computed through the combination of EU and EG
def AU(model: Model, phi1: Function, phi2: Function) -> Function:
    # A[f U g] = ~E[~g U (~f & ~g)] & ~EG ~g
    not_phi1 = negate(model, phi1)
    not_phi2 = negate(model, phi2)
    and_inner = not_phi1 & not_phi2
    not_eu = negate(model, EU_saturated(model, not_phi2, and_inner))
    not_eg = negate(model, EG(model, not_phi1))
    return not_eu & not_eg


# fixpoint version for AU, should usually be faster
def AU_v2(model: Model, phi1: Function, phi2: Function) -> Function:
    old = phi2
    new = model.mk_empty_colored_set()
    while old != new:
        new = old
        old = old | (phi1 & AX(model, old))
    return old


# EW computed through the AU
def EW(model: Model, phi1: Function, phi2: Function):
    # E[f R g] = ¬A[¬f U ¬g]
    not_phi1 = negate(model, phi1)
    not_phi2 = negate(model, phi2)
    return negate(model, AU(model, not_phi1, not_phi2))


# AW computed through the EU
def AW(model: Model, phi1: Function, phi2: Function):
    # A[f R g] = ¬E[¬f U ¬g]
    not_phi1 = negate(model, phi1)
    not_phi2 = negate(model, phi2)
    return negate(model, EU_saturated(model, not_phi1, not_phi2))


# ============================================================================================= #
# ============================ OPTIMIZED FORMULAE EVALUATION PART ============================= #
# ============================================================================================= #


# binder EX:   ↓var. (EX PHI)
# var should be something like "x"
def optimized_bind_EX(model: Model, phi: Function, var: str) -> Function:
    current_set = model.mk_empty_colored_set()
    comparator = create_comparator(model, var)
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        intersection = comparator & pre_E_one_var(model, phi, f"s__{i}")
        current_set = current_set | model.bdd.quantify(intersection, vars_to_get_rid)

    # return current_set
    stable_binded = model.bdd.quantify(comparator & (phi & model.stable), vars_to_get_rid)
    return current_set | stable_binded


# jump EX:   @x. (EX PHI)
# var should be something like "x"
def optimized_jump_EX(model: Model, phi: Function, var: str) -> Function:
    current_set = model.mk_empty_colored_set()
    comparator = create_comparator(model, var)
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        intersection = comparator & pre_E_one_var(model, phi, f"s__{i}")
        current_set = current_set | model.bdd.quantify(intersection, vars_to_get_rid)

    # return current_set
    stable_jumped = model.bdd.quantify(comparator & (phi & model.stable), vars_to_get_rid)
    return current_set | stable_jumped


# existential EX:   ∃x. (EX SET1)
def optimized_exist_EX(model: Model, phi: Function, var: str) -> Function:
    current_set = model.mk_empty_colored_set()
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        pred = pre_E_one_var(model, phi, f"s__{i}")
        current_set = current_set | model.bdd.quantify(pred, vars_to_get_rid)

    # return current_set
    stable_exist = model.bdd.quantify(phi & model.stable, vars_to_get_rid)
    return current_set | stable_exist


# wrapper for all 3 functions above
def optimized_hybrid_EX(model: Model, phi: Function, var: str, operation: str) -> Function:
    if operation == "!":
        return optimized_bind_EX(model, phi, var)
    elif operation == "@":
        return optimized_jump_EX(model, phi, var)
    elif operation == "3":
        return optimized_exist_EX(model, phi, var)
