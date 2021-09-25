from collections import OrderedDict
from termcolor import colored
from src.parse_all import parse_all

from src.model import *


# ============================================================================================= #
# ============================= SUBFORMULAS EVALUATION PART =================================== #
# ============================================================================================= #


# creates a bdd representing all states labeled by proposition given
def labeled_by(prop: str, model: Model) -> Function:
    return model.bdd.add_expr(prop)


# creates comparator for variables s1, s2,... and var1, var2,...
# it will be bdd for (s1 <=> var1) & (s2 <=> var2)...
def create_comparator(model: Model, var: str) -> Function:
    expr_parts = [f"(s__{i} <=> {var}__{i})" for i in range(model.num_props)]
    expr = " & ".join(expr_parts)
    comparator = model.bdd.add_expr(expr)
    return comparator


# Release(x, Comparator(x) & SMC(M, phi))
def bind(model: Model, var: str, phi: Function) -> Function:
    comparator = create_comparator(model, var)
    intersection = comparator & phi

    # now lets use existential quantification to get rid of the bdd vars coding VAR
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]
    result = model.bdd.quantify(intersection, vars_to_get_rid)
    return result


# Release(s, Comparator(x) & SMC(M, phi))
def jump(model: Model, var: str, phi: Function) -> Function:
    comparator = create_comparator(model, var)
    intersection = comparator & phi

    # now lets use existential quantification to get rid of the bdd vars coding STATE
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props)]
    result = model.bdd.quantify(intersection, vars_to_get_rid)
    return result


# Release(x, SMC(M, phi))
def existential(model: Model, var: str, phi: Function) -> Function:
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]
    result = model.bdd.quantify(phi, vars_to_get_rid)
    return result


# computes the set of states which can make transition into the initial set
# applying the update function of the given `var`
# SHOULD BE USED ONLY BY FUNCTIONS IN THIS FILE
def pre_E_one_var(model: Model, var: str, initial: Function) -> Function:
    """
    NEGATIVE_PREDECESSOR = !X & Exists(SET & X, 'X') & B_X  
    POSITIVE_PREDECESSOR = X & Exists(SET & !X, 'X') & !B_X
    PREDECESSORS_IN_X = NEGATIVE_PREDECESSOR | POSITIVE_PREDECESSOR
    """

    var_bdd = labeled_by(var, model)
    neg_pred = ~var_bdd & model.bdd.quantify(initial & var_bdd, [var]) & model.update_fns[var]
    pos_pred = var_bdd & model.bdd.quantify(initial & ~var_bdd, [var]) & ~model.update_fns[var]
    return neg_pred | pos_pred


# computes the set of states which can make transition into the initial set
# applying ALL of the update functions
def pre_E_all_vars(model: Model, initial: Function) -> Function:
    current_set = model.bdd.add_expr("False")
    for i in range(model.num_props):
        current_set = current_set | pre_E_one_var(model, f"s__{i}", initial)

    # TODO: change back?? - now it artificially creates self-loops for stable states with no successor
    # return current_set
    return current_set | (initial & model.stable)


# computes the set of states which can make transition ONLY into the initial set and nowhere else
# applying the update function of the given `var`
# SHOULD BE USED ONLY BY FUNCTIONS IN THIS FILE
def pre_A_one_var(model: Model, var: str, initial: Function) -> Function:
    return ~pre_E_one_var(model, var, ~initial)


# computes the set of successors for the given set
# by applying the update function of the given `var`
# SHOULD BE USED ONLY BY FUNCTIONS IN THIS FILE
# TODO: test if right
def post_E_one_var(model: Model, var: str, given_set: Function) -> Function:
    """
    GO_DOWN = !X & Exists((SET & X & !B_X), 'X')
    GO_UP = X & Exists((SET & !X & B_X), 'X')
    """

    var_bdd = labeled_by(var, model)
    go_down = ~var_bdd & model.bdd.quantify(given_set & var_bdd & ~model.update_fns[var], [var])
    go_up = var_bdd & model.bdd.quantify(given_set & ~var_bdd & model.update_fns[var], [var])
    return go_down | go_up


# computes the set of successors for the given set
# by applying ALL of the update functions
def post_E_all_vars(model: Model, given_set: Function) -> Function:
    current_set = model.bdd.add_expr("False")
    for i in range(model.num_props):
        current_set = current_set | post_E_one_var(model, f"s__{i}", given_set)

    # TODO: add same thing as for pre_E_all_vars - create self loops - this helps for "bind x: EY x"
    # TODO: problem with self-loops might arrise again, but this time in sources - we have reversed graph
    return current_set


def EX(model: Model, phi: Function) -> Function:
    return pre_E_all_vars(model, phi)


def EY(model: Model, phi: Function) -> Function:
    return post_E_all_vars(model, phi)


def EU(model: Model, phi1: Function, phi2: Function) -> Function:
    old = phi2
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old | (phi1 & EX(model, old))
    return old


# computed via EU
def EF(model: Model, phi: Function) -> Function:
    true_bdd = model.bdd.add_expr("True")
    return EU(model, true_bdd, phi)


# fixpoint version without excess computing
def EF_v2(model: Model, phi: Function) -> Function:
    # lfpZ. ( phi OR EX Z )
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old | EX(model, old)
    return old


def EG(model: Model, phi: Function) -> Function:
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old & EX(model, old)
    return old


# computed through pure EX
def AX(model: Model, phi: Function) -> Function:
    # AX f = ~EX (~f)
    return ~EX(model, ~phi)


# computed through pure EY
# TODO: check if this is right
def AY(model: Model, phi: Function) -> Function:
    return ~EY(model, ~phi)


def AF(model: Model, phi1: Function) -> Function:
    # AF f = ~EG (~f)
    return ~EG(model, ~phi1)


# computed through EF
def AG(model: Model, phi1: Function) -> Function:
    # AG f = ~EF (~f)
    return ~EF(model, ~phi1)


def AU(model: Model, phi1: Function, phi2: Function) -> Function:
    # A[f U g] = ~E[~g U (~f & ~g)] & ~EG ~g
    and_inner = ~phi1 & ~phi2
    not_eu = ~EU(model, ~phi2, and_inner)
    not_eg = ~EG(model, ~phi1)
    return not_eu & not_eg


# fixpoint version for AU, should be faster
def AU_v2(model: Model, phi1: Function, phi2: Function) -> Function:
    old = phi2
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old | (phi1 & AX(model, old))
    return old


def EW(model: Model, phi1: Function, phi2: Function):
    # E[f R g] = ¬A[¬f U ¬g]
    return ~AU(model, ~phi1, ~phi2)


def AW(model: Model, phi1: Function, phi2: Function):
    # A[f R g] = ¬E[¬f U ¬g]
    return ~EU(model, ~phi1, ~phi2)


# ============================================================================================= #
# ============================ OPTIMIZED FORMULAE EVALUATION PART ============================= #
# ============================================================================================= #


# binder EX:   ↓var. (EX PHI)
# var should be something like "x"
def optimized_bind_EX(model: Model, phi: Function, var: str) -> Function:
    current_set = model.bdd.add_expr("False")
    comparator = create_comparator(model, var)
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        intersection = comparator & pre_E_one_var(model, f"s__{i}", phi)
        current_set = current_set | model.bdd.quantify(intersection, vars_to_get_rid)

    # TODO: change back?? - now it artificially creates self-loops for stable states with no successor
    # return current_set
    stable_binded = model.bdd.quantify(comparator & (phi & model.stable), vars_to_get_rid)
    return current_set | stable_binded


# jump EX:   @x. (EX PHI)
# var should be something like "x"
def optimized_jump_EX(model: Model, phi: Function, var: str) -> Function:
    current_set = model.bdd.add_expr("False")
    comparator = create_comparator(model, var)
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        intersection = comparator & pre_E_one_var(model, f"s__{i}", phi)
        current_set = current_set | model.bdd.quantify(intersection, vars_to_get_rid)

    # TODO: change back?? - now it artificially creates self-loops for stable states with no successor
    # return current_set
    stable_jumped = model.bdd.quantify(comparator & (phi & model.stable), vars_to_get_rid)
    return current_set | stable_jumped


# existential EX:   ∃x. (EX SET1)
def optimized_exist_EX(model: Model, phi: Function, var: str) -> Function:
    current_set = model.bdd.add_expr("False")
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        pred = pre_E_one_var(model, f"s__{i}", phi)
        current_set = current_set | model.bdd.quantify(pred, vars_to_get_rid)

    # TODO: change back?? - now it artificially creates self-loops for stable states with no successor
    # return current_set
    stable_exist = model.bdd.quantify(phi & model.stable, vars_to_get_rid)
    return current_set | stable_exist


# wrapper for all 3 functions above
def optimized_hybrid_EX(model: Model, phi: Function, var: str, operation: str) -> Function:
    if operation == "!":
        return optimized_bind_EX(model, phi, var)
    elif operation == "@":
        return optimized_jump_EX(model, phi, var)
    elif operation == "Q":
        return optimized_exist_EX(model, phi, var)


# ============================================================================================= #
# ======================================= PARSING PART ======================================== #
# ============================================================================================= #


# parses a file with a boolean network, creates model from it - BUT STATE VARIABLES ARE ADDED MANUALLY atm
# only testing version, can break quickly...
# TODO: remake this, implicitly add vars from formula
# TODO: better handle the renaming of variables (now vars cant be 'number', 's', 'x'...)
"""
version of bnet files that is used:
    all lines except first one are in the form: "variable_name, update_fn"
    BUT to handle params, we will add lines in form: "param_name," (there is no update fn) - those will be params
"""


def bnet_parser(file_name: str):
    # first preprocess the file content
    file = open(file_name, "r")
    content = file.read()
    # TODO: maybe clean the content (no need atm, because test examples are clean)
    
    lines = content.split("\n")[1:]  # first line does not contain data
    if not lines[-1]:
        lines.pop()  # last item might be just empty string after last newline
    lines_ordered = sorted(lines, key=lambda x: x.split(",")[0])

    # collect all the variable names and their update functions and reorder them
    # order will be alphabetical, uppercase first, lowercase later (like ASCII)
    update_dict = OrderedDict()
    prop_names = []
    param_names = []
    for line in lines_ordered:
        var_func_pair = line.split(",")
        if var_func_pair[1]:  # if this is not empty, we have var and its update fn
            prop_names.append(var_func_pair[0])
            update_dict[var_func_pair[0]] = var_func_pair[1]
        else:  # otherwise we have parameter with no update fn
            param_names.append(var_func_pair[0])
    num_props = len(prop_names)
    num_params = len(param_names)

    # rename props/params in update functions, as we will be using only the short versions (s0,s1... or p0...)
    # we will start renaming the longest ones, so that we dont overwrite them with some substring
    name_dict = dict()
    for i in range(num_props):
        name_dict[prop_names[i]] = f"s__{i}"
    for i in range(num_params):
        name_dict[param_names[i]] = f"p__{i}"
    for prop in prop_names:
        for p in sorted((prop_names+param_names), key=lambda x: len(x), reverse=True):
            update_dict[prop] = update_dict[prop].replace(p, name_dict[p])

    # define a BDD vars will be named s0,s1... and we will store full names elsewhere, also add 2 HCTL vars
    bdd = BDD()
    vrs = [f"s__{i}" for i in range(num_props)]       # state describing vars
    vrs.extend(f"p__{i}" for i in range(num_params))  # params
    vrs.extend(f"x__{i}" for i in range(num_props))   # state-variable x (for HCTL MC)
    vrs.extend(f"y__{i}" for i in range(num_props))   # state-variable y (for HCTL MC)
    bdd.declare(*vrs)

    # reordering to some desired order (now it is s0,x0,y0,s1...,p0,p1...)
    # TODO: try different orders
    my_order = dict()
    for i in range(num_props):
        my_order[f"s__{i}"] = i * 3
        my_order[f"x__{i}"] = i * 3 + 1
        my_order[f"y__{i}"] = i * 3 + 2
    for i in range(num_params):
        my_order[f"p__{i}"] = i + 3 * num_props
    bdd.reorder(my_order)
    # bdd.configure(reordering=False)  # auto reorder disabled (probably)? - it is slower when disabled

    # go through update function strings one by one and create dict of BDDs (update functions) from them
    list_update_fns = [bdd.add_expr(update_dict[prop]) for prop in update_dict]
    real_update_dict = OrderedDict()
    for i in range(num_props):
        real_update_dict[f"s__{i}"] = list_update_fns[i]

    update_dict_renamed = OrderedDict()
    for i in range(num_props):
        update_dict_renamed[f"s__{i}"] = update_dict[prop_names[i]]

    # pack it all into a whole model and return it
    name_dict_reversed = {y: x for x, y in name_dict.items()}
    model_name = file_name.split("\\")[-1]
    model = Model(model_name, bdd, prop_names, param_names, ['x', 'y'], real_update_dict, name_dict_reversed)
    return model


# ================================================================================================= #
# ================================ BODY AND DEALING WITH RESULTS ================================== #
# ================================================================================================= #


# returns decimal value of binary vector s0,s1,s2...
# is used for sorting assignments
def eval_assignment(assignment, num_props) -> int:
    result_val = 0
    for i in range(num_props):
        result_val += assignment[len(assignment) - 1 - i][1] * 2 ** i
    return result_val


# returns decimal value of binary vector p0,p1,p2... - BUT uses inverted values
# is used for sorting as a addition to previous function
def eval_color(assignment, num_cols) -> float:
    result_val = 0
    for i in range(num_cols):
        result_val += assignment[len(assignment) - 1 - i][1] * (1 / 2 ** i)
    return result_val


def print_results(result: Function, model: Model, message: str = "", show_all: bool = False) -> None:
    if message:
        print(message)

    vars_to_show = [f"s__{i}" for i in range(model.num_props)]+[f"p__{i}" for i in range(model.num_params)]
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)
    print(f"{len(list(assignments))} RESULTS FOUND IN TOTAL")

    if not show_all:
        return
    """
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)  # assigning a generator again, was depleted
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (x[0][0], len(x[0]), x[0])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (eval_assignment(x, model.num_props) + eval_color(x, model.num_params)))

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
    
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)  # assigning a generator again, was depleted
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (model.name_dict[x[0]])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (eval_assignment(x, model.num_props + model.num_params)))

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
    vars_to_show = [f"s__{i}" for i in range(model.num_props)]+[f"p__{i}" for i in range(model.num_params)]+[f"x__{i}" for i in range(model.num_props)]
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)
    print(f"{len(list(assignments))} RESULTS FOUND IN TOTAL")

    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)
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
    """

