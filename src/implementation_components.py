from src.model import *

"""
This file includes the implementation for evaluating all components of HCTL formula.
It is build so that we can combine them into the bottom-up algorithm.
"""

# ============================================================================================= #
# ============================= SUBFORMULAS EVALUATION PART =================================== #
# ============================================================================================= #


def labeled_by(model: Model, prop: str) -> Function:
    """Create a bdd-representation of all states labeled by given proposition"""
    return model.bdd.add_expr(prop) & model.mk_unit_colored_set()


def negate(model: Model, phi: Function) -> Function:
    return ~phi & model.mk_unit_colored_set()


def create_comparator(model: Model, var: str) -> Function:
    """
    Create equalizer of the state and a state variable
    It is essentially a bdd for "bit-comparator" in form (s1 <=> x1) & (s2 <=> x2)...
    """
    expr_parts = [f"(s__{i} <=> {var}__{i})" for i in range(model.num_props())]
    expr = " & ".join(expr_parts)
    comparator = model.bdd.add_expr(expr) & model.mk_unit_colored_set()
    return comparator


def bind(model: Model, phi: Function, var: str) -> Function:
    """Evaluate bind quantifier."""
    comparator = create_comparator(model, var)
    intersection = comparator & phi

    # now lets use existential quantification to get rid of the bdd vars coding VAR
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props())]
    result = model.bdd.quantify(intersection, vars_to_get_rid)
    return result


def jump(model: Model, phi: Function, var: str) -> Function:
    """Evaluate jump operator."""
    comparator = create_comparator(model, var)
    intersection = comparator & phi

    # now lets use existential quantification to get rid of the bdd vars coding STATE
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props())]
    result = model.bdd.quantify(intersection, vars_to_get_rid)
    return result


def existential(model: Model, phi: Function, var: str) -> Function:
    """Evaluate existential quantifier."""
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props())]
    result = model.bdd.quantify(phi, vars_to_get_rid)
    return result


def pre_E_one_var(model: Model, initial_set: Function, var: str) -> Function:
    """
    Compute the set of states which can make a transition into the initial set by
    applying the update function of the given BN variable.

    Pseudocode:
    NEGATIVE_PREDECESSOR = !X & Exists(SET & X, 'X') & B_X  
    POSITIVE_PREDECESSOR = X & Exists(SET & !X, 'X') & !B_X
    PREDECESSORS_IN_X = NEGATIVE_PREDECESSOR | POSITIVE_PREDECESSOR
    """
    var_bdd = labeled_by(model, var)
    not_var_bdd = negate(model, var_bdd)
    neg_pred = not_var_bdd & model.bdd.quantify(initial_set & var_bdd, [var]) & model.update_fns[var]
    pos_pred = var_bdd & model.bdd.quantify(initial_set & not_var_bdd, [var]) & negate(model, model.update_fns[var])
    return neg_pred | pos_pred


def pre_E_all_vars(model: Model, initial_set: Function) -> Function:
    """
    Compute the set of states which can make transition into the initial set
    applying ANY of the update functions.
    """
    current_set = model.mk_empty_colored_set()
    for i in range(model.num_props()):
        current_set = current_set | pre_E_one_var(model, initial_set, f"s__{i}")
    return current_set | (initial_set & model.stable)


def EX(model: Model, phi: Function) -> Function:
    return pre_E_all_vars(model, phi)


def EU_saturated(model: Model, phi1: Function, phi2: Function) -> Function:
    """Evaluate EU using saturation (which is faster than fixed-point algorithm)"""
    result = phi2
    done = False
    while not done:
        done = True
        for i in range(model.num_props(), 0, -1):
            update = (phi1 & pre_E_one_var(model, result, f"s__{i - 1}")) & negate(model, result)
            if update != model.bdd.false:
                result = result | update
                done = False
                break
    return result


def EF_saturated(model: Model, phi: Function) -> Function:
    """Evaluate EF operator via EU with saturation."""
    # EF f == [true EU f]
    return EU_saturated(model, model.mk_unit_colored_set(), phi)


def EG(model: Model, phi: Function) -> Function:
    """Evaluate EG using classical fixed-point algorithm."""
    old = phi
    new = model.mk_empty_colored_set()
    while old != new:
        new = old
        old = old & EX(model, old)
    return old


def AX(model: Model, phi: Function) -> Function:
    """Compute AX through the EX."""
    # AX f = ~EX (~f)
    return negate(model, EX(model, negate(model, phi)))


def AF(model: Model, phi1: Function) -> Function:
    """Compute AF through the EG."""
    # AF f = ~EG (~f)
    return negate(model, EG(model, negate(model, phi1)))


def AG(model: Model, phi1: Function) -> Function:
    """Compute AG through the EF."""
    # AG f = ~EF (~f)
    return negate(model, EF_saturated(model, negate(model,phi1)))


def AU(model: Model, phi1: Function, phi2: Function) -> Function:
    """Compute AU through the combination of EU and EG."""
    # A[f U g] = ~E[~g U (~f & ~g)] & ~EG ~g
    not_phi1 = negate(model, phi1)
    not_phi2 = negate(model, phi2)
    and_inner = not_phi1 & not_phi2
    not_eu = negate(model, EU_saturated(model, not_phi2, and_inner))
    not_eg = negate(model, EG(model, not_phi1))
    return not_eu & not_eg


def AU_v2(model: Model, phi1: Function, phi2: Function) -> Function:
    """Compute AU using fixed-point algorithm, should be faster."""
    old = phi2
    new = model.mk_empty_colored_set()
    while old != new:
        new = old
        old = old | (phi1 & AX(model, old))
    return old


def EW(model: Model, phi1: Function, phi2: Function):
    """Compute EW through the AU."""
    # E[f W g] = ¬A[¬f U ¬g]
    not_phi1 = negate(model, phi1)
    not_phi2 = negate(model, phi2)
    return negate(model, AU(model, not_phi1, not_phi2))


def AW(model: Model, phi1: Function, phi2: Function):
    """Compute AW through the EU."""
    # A[f W g] = ¬E[¬f U ¬g]
    not_phi1 = negate(model, phi1)
    not_phi2 = negate(model, phi2)
    return negate(model, EU_saturated(model, not_phi1, not_phi2))


# ============================================================================================= #
# ============================ OPTIMIZED FORMULAE EVALUATION PART ============================= #
# ============================================================================================= #


def optimized_bind_EX(model: Model, phi: Function, var: str) -> Function:
    """Compute combination of binder and EX using optimized approach.

    For example used for formula ↓var. (EX phi).

    Args:
        model: model structure with symbolic representation
        phi: BDD-representation of the evaluated inner subformula
        var: hybrid variable quantified by the binder
    """
    current_set = model.mk_empty_colored_set()
    comparator = create_comparator(model, var)
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props())]

    for i in range(model.num_props()):
        intersection = comparator & pre_E_one_var(model, phi, f"s__{i}")
        current_set = current_set | model.bdd.quantify(intersection, vars_to_get_rid)

    # return current_set
    stable_binded = model.bdd.quantify(comparator & (phi & model.stable), vars_to_get_rid)
    return current_set | stable_binded


def optimized_jump_EX(model: Model, phi: Function, var: str) -> Function:
    """
    Compute combination of jump and EX using optimized approach.
    For example used for formula @var. (EX phi).
    """
    current_set = model.mk_empty_colored_set()
    comparator = create_comparator(model, var)
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props())]

    for i in range(model.num_props()):
        intersection = comparator & pre_E_one_var(model, phi, f"s__{i}")
        current_set = current_set | model.bdd.quantify(intersection, vars_to_get_rid)

    # return current_set
    stable_jumped = model.bdd.quantify(comparator & (phi & model.stable), vars_to_get_rid)
    return current_set | stable_jumped


def optimized_exist_EX(model: Model, phi: Function, var: str) -> Function:
    """
    Compute combination of existential quantifier and EX using optimized approach.
    For example used for formula ∃var. (EX phi).
    """
    current_set = model.mk_empty_colored_set()
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props())]

    for i in range(model.num_props()):
        pred = pre_E_one_var(model, phi, f"s__{i}")
        current_set = current_set | model.bdd.quantify(pred, vars_to_get_rid)

    # return current_set
    stable_exist = model.bdd.quantify(phi & model.stable, vars_to_get_rid)
    return current_set | stable_exist


def optimized_hybrid_EX(model: Model, phi: Function, var: str, operation: str) -> Function:
    """Compute combination of hybrid operator and EX using optimized approach"""
    if operation == "!":
        return optimized_bind_EX(model, phi, var)
    elif operation == "@":
        return optimized_jump_EX(model, phi, var)
    elif operation == "3":
        return optimized_exist_EX(model, phi, var)
