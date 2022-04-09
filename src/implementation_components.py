from termcolor import colored

from src.model import *
import gc

"""
This file includes the implementation of evaluator for all components of HCTL formula
It is build so that we can combine them into the bottom-up algorithm

Also has the functions for result printing
"""

# ============================================================================================= #
# ============================= SUBFORMULAS EVALUATION PART =================================== #
# ============================================================================================= #


NODE_LIMIT_FOR_GARBAGE = 1_000_000


# runs garbage collectors for both python and bdd.autoref implementation
# CAN NOT BE USED WHEN CUDD VERSION OF DD LIBRARY IS USED
def collect_garbage_if_needed(bdd: BDD) -> None:
    if len(bdd) > NODE_LIMIT_FOR_GARBAGE:
        gc.collect()
        bdd.collect_garbage()


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


"""
# fixpoint version
def EU(model: Model, phi1: Function, phi2: Function) -> Function:
    old = phi2
    new = model.mk_empty_colored_set()
    while old != new:
        new = old
        old = old | (phi1 & EX(model, old))
        # collect_garbage_if_needed(model.bdd)
    return old
"""

# version based on saturation
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

"""
# fixpoint version without excess computing
def EF_v2(model: Model, phi: Function) -> Function:
    # lfpZ. ( phi OR EX Z )
    old = phi
    new = model.mk_empty_colored_set()
    while old != new:
        new = old
        old = old | EX(model, old)
        # collect_garbage_if_needed(model.bdd)
    return old


# version based on saturation
def EF_saturated(model: Model, phi: Function) -> Function:
    result = phi
    done = False
    while not done:
        done = True
        for i in range(model.num_props, 0, -1):
            update = pre_E_one_var(model, result, f"s__{i-1}") & negate(model, result)
            if update != model.bdd.false:
                result = result | update
                done = False
                break
    #reorder(model.bdd)
    return result
"""

# computed via EU with saturation
def EF_saturated(model: Model, phi: Function) -> Function:
    return EU_saturated(model, model.mk_unit_colored_set(), phi)


def EG(model: Model, phi: Function) -> Function:
    old = phi
    new = model.mk_empty_colored_set()
    while old != new:
        new = old
        old = old & EX(model, old)
        # collect_garbage_if_needed(model.bdd)
    return old


# computed through pure EX
def AX(model: Model, phi: Function) -> Function:
    # AX f = ~EX (~f)
    return negate(model, EX(model, negate(model, phi)))


def AF(model: Model, phi1: Function) -> Function:
    # AF f = ~EG (~f)
    return negate(model, EG(model, negate(model, phi1)))


# computed through EF
def AG(model: Model, phi1: Function) -> Function:
    # AG f = ~EF (~f)
    return negate(model, EF_saturated(model, negate(model,phi1)))


def AU(model: Model, phi1: Function, phi2: Function) -> Function:
    # A[f U g] = ~E[~g U (~f & ~g)] & ~EG ~g
    not_phi1 = negate(model, phi1)
    not_phi2 = negate(model, phi2)
    and_inner = not_phi1 & not_phi2
    not_eu = negate(model, EU_saturated(model, not_phi2, and_inner))
    not_eg = negate(model, EG(model, not_phi1))
    return not_eu & not_eg


# fixpoint version for AU, should be faster
def AU_v2(model: Model, phi1: Function, phi2: Function) -> Function:
    old = phi2
    new = model.mk_empty_colored_set()
    while old != new:
        new = old
        old = old | (phi1 & AX(model, old))
        # collect_garbage_if_needed(model.bdd)
    return old


def EW(model: Model, phi1: Function, phi2: Function):
    # E[f R g] = ¬A[¬f U ¬g]
    not_phi1 = negate(model, phi1)
    not_phi2 = negate(model, phi2)
    return negate(model, AU(model, not_phi1, not_phi2))


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


# ================================================================================================= #
# ================================ BODY AND DEALING WITH RESULTS ================================== #
# ================================================================================================= #


# returns decimal value of binary vector s0,s1,s2...
# is used for sorting assignments
def encode_assignment(assignment, num_props) -> int:
    result_val = 0
    for i in range(num_props):
        result_val += assignment[len(assignment) - 1 - i][1] * 2 ** i
    return result_val


# returns decimal value of binary vector p0,p1,p2... - BUT uses inverted values
# is used for sorting as a addition to previous function
def encode_color(assignment, num_cols) -> float:
    result_val = 0
    for i in range(num_cols):
        result_val += assignment[len(assignment) - 1 - i][1] * (1 / 2 ** i)
    return result_val


# using projection gets rid of all parameters from BDD
# bdd must support only props and params, no state-variables
def get_states_only(phi: Function, model: Model):
    vars_to_get_rid = [f"p__{i}" for i in range(model.num_params)]
    return model.bdd.quantify(phi, vars_to_get_rid)


# using projection gets rid of all propositions from BDD
# bdd must support only props and params, no state-variables
def get_colors_only(phi: Function, model: Model):
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props)]
    return model.bdd.quantify(phi, vars_to_get_rid)


# Print number of computed results in the final BDD (number of state-color pairs),
# and then numbers of colors & states alone
def print_results_fast(result: Function, model: Model, message: str = ""):
    if message:
        print(message)

    assignments = model.bdd.count(result, nvars=model.num_props + model.num_params)
    print(f"{assignments} RESULTS FOUND IN TOTAL")

    result_colors = get_colors_only(result, model)
    assignments = model.bdd.count(result_colors, nvars=model.num_params)
    print(f"{assignments} COLORS FOUND IN TOTAL")

    result_states = get_states_only(result, model)
    assignments = model.bdd.count(result_states, nvars=model.num_props)
    print(f"{assignments} STATES FOUND IN TOTAL")

    print(f"props: {model.num_props}, params: {model.num_params}")


def print_results(result: Function, model: Model, message: str = "", show_all: bool = False) -> None:
    print_results_fast(result, model, message)

    if not show_all:
        return

    """
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)  # assigning a generator again, was depleted
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (x[0][0], len(x[0]), x[0])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (encode_assignment(x, model.num_props) + encode_color(x, model.num_params)))

    # we will print params first, then proposition values
    for assignment in assignments_sorted:
        # we will print only 0/1 instead True/False
        transformed_params = [int(item[1]) for item in assignment[0:model.num_params]]
        print(transformed_params, end="  ")
        transformed_props = [int(item[1]) for item in assignment[len(assignment) - model.num_props:]]
        print(transformed_props)
    print()
    """

    # -----------------------------------------------------------------------------------

    # printing all variables in alphabetical order, colored, like in AEON
    """
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)  # assigning a generator again, was depleted
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (model.name_dict[x[0]])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (encode_assignment(x, model.num_props + model.num_params)))

    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)
    for assignment in assignments_sorted:
        # we will print only 0/1 instead True/False
        transformed = [(model.name_dict[item[0]], int(item[1])) for item in assignment]
        for var, val in transformed:
            text = ""
            if val == 0:
                text = colored('!' + var, 'red')
            else:
                text = colored(var, "green")
            print(text, end=" ")
        print()
    print()
    """

    assignments = model.bdd.pick_iter(result)
    print(f"{len(list(assignments))} RESULTS FOUND IN TOTAL")

    assignments = model.bdd.pick_iter(result)
    sorted_inside = [sorted(assignment.items(), key=lambda x: x[0]) for assignment in assignments]

    for assignment in sorted_inside:
        # we will print only 0/1 instead True/False
        transformed = [(item[0], int(item[1])) for item in assignment]
        for var, val in transformed:
            text = ""
            if val == 0:
                text = colored('!' + var, 'red')
            else:
                text = colored(var, "green")
            print(text, end=" ")
        print()
    print()


