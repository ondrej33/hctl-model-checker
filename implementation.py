from collections import OrderedDict
from termcolor import colored

from typing import List

from dd.autoref import BDD, Function


# ============================================================================================= #
# ======================================= MODEL PART ========================================== #
# ============================================================================================= #


class Model:
    def __init__(self, name: str, bdd: BDD, num_props: int, names_props: List[str],
                 num_params: int, names_params: List[str], update_fns, update_strings, name_dict):
        self.name = name
        self.bdd = bdd
        self.num_props = num_props
        self.names_props = names_props        # full names for props s0, s1 ... (ASCII alphabetical order)
        self.num_params = num_params
        self.names_params = names_params      # full names for params p0, p1 ... (ASCII alphabetical order)
        self.update_fns = update_fns          # dict with vars + their update funcs, starts with F_s0, F_s1 ...
        self.update_strings = update_strings  # dict with vars + string for their update fns (experimenting)
        self.name_dict = name_dict            # dict with short var names + long var names


# ============================================================================================= #
# ============================= SUBFORMULAS EVALUATION PART =================================== #
# ============================================================================================= #


# creates a bdd representing all states labeled by proposition given
def labeled_by(prop: str, model: Model):
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
def pre_E_one_var(model: Model, var: str, initial: Function) -> Function:
    """
    NEGATIVE_PREDECESSOR = !X & Exists(SET & X, 'X') & B_X   - prvky v množine set také že platí X=1 a pokiaľ
                            zmením na x=0, bude mať f_X hodnotu 1 (teda bude možný prechod do X=1)
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
    return current_set


# computes the set of states which can make transition ONLY into the initial set and nowhere else
# applying the update function of the given `var`
def pre_A_one_var(model: Model, var: str, initial: Function) -> Function:
    return ~pre_E_one_var(model, var, ~initial)


# computes the set of states which can make transition ONLY into the initial set and nowhere else
# applying ALL of the update functions
def pre_A_all_vars(model: Model, initial: Function) -> Function:
    current_set = model.bdd.add_expr("True")
    for i in range(model.num_props):
        current_set = current_set & pre_A_one_var(model, f"s__{i}", initial)
    return current_set


# computes the set of successors for the given set
# by applying the update function of the given `var`
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


# true fixpoint version without excess computing
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


# computed through small update BDDs during pre_A_all_vars
def AX_v2(model: Model, phi: Function) -> Function:
    return pre_A_all_vars(model, phi)


# computed through pure EY
# TODO: check if it is right
def AY(model: Model, phi: Function) -> Function:
    return ~EY(model, ~phi)


def AF(model: Model, phi1: Function) -> Function:
    # AF f = ~EG (~f)
    return ~EG(model, ~phi1)


# fixpoint through AX
def AF_v2(model: Model, phi: Function) -> Function:
    # lfpZ. ( phi OR EX Z )
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old | AX(model, old)
    return old


# computed through EF
def AG(model: Model, phi1: Function) -> Function:
    # AG f = ~EF (~f)
    return ~EF(model, ~phi1)


# fixpoint
def AG_v2(model: Model, phi: Function) -> Function:
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old & AX(model, old)
    return old


# fixpoint, uses different version for AX
def AG_v3(model: Model, phi: Function) -> Function:
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old & AX_v2(model, old)
    return old


def AU(model: Model, phi1: Function, phi2: Function) -> Function:
    # A[f U g] = ~E[~g U (~f & ~g)] & ~EG ~g
    and_inner = ~phi1 & ~phi2
    not_eu = ~EU(model, ~phi2, and_inner)
    not_eg = ~EG(model, ~phi1)
    return not_eu & not_eg

# fixpoint
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
    return current_set


# jump EX:   @x. (EX PHI)
# var should be something like "x"
def optimized_jump_EX(model: Model, phi: Function, var: str) -> Function:
    current_set = model.bdd.add_expr("False")
    comparator = create_comparator(model, var)
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        intersection = comparator & pre_E_one_var(model, f"s__{i}", phi)
        current_set = current_set | model.bdd.quantify(intersection, vars_to_get_rid)
    return current_set


# existential EX:   ∃x. (EX SET1)
def optimized_exist_EX(model: Model, phi: Function, var: str) -> Function:
    current_set = model.bdd.add_expr("False")
    vars_to_get_rid = [f"{var}__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        pred = pre_E_one_var(model, f"s__{i}", phi)
        current_set = current_set | model.bdd.quantify(pred, vars_to_get_rid)
    return current_set


# wrapper for all 3 functions above
def optimized_hybrid_EX(model: Model, phi: Function, var: str, operation: str) -> Function:
    if operation == "!":
        return optimized_bind_EX(model, phi, var)
    elif operation == "@":
        return optimized_jump_EX(model, phi, var)
    elif operation == "Q":
        return optimized_exist_EX(model, phi, var)

# ============================================================================================= #
# ============================== FIXED FORMULAE EVALUATION PART =============================== #
# ======================v====================================================================== #


# formula: ↓x (EX x)
# unstable steady state (self loop)
def model_check_fixed1(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ex = EX(model, x)
    return bind(model, 'x', ex)


# formula: ↓x (EX x)
# FASTEST version using BINDER, uses binder already during computing the EX, with smaller BDDs
def model_check_fixed1_v2(model: Model) -> Function:
    x = create_comparator(model, 'x')
    current_set = model.bdd.add_expr("False")
    for i in range(model.num_props):
        current_set = current_set | bind(model, 'x', pre_E_one_var(model, f"s__{i}", x))
    return current_set


# formula: ↓x (AX x)
# stable steady states - sink states
def model_check_fixed2(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ax = AX(model, x)
    return bind(model, 'x', ax)


# formula: ↓x (AX x), stable steady states (self loop only, sink)
# FASTEST version using BINDER, uses binder already during computing the AX, with smaller BDDs
def model_check_fixed2_v2(model: Model) -> Function:
    x = create_comparator(model, 'x')

    current_set = model.bdd.add_expr("True")
    for i in range(model.num_props):
        current_set = current_set & bind(model, 'x', pre_A_one_var(model, f"s__{i}", x))
    return current_set


# formula: ↓x (AX x), stable steady states (self loop only, sink)
# FAST, uses "equational fixed point" (from antelope), big conjunction of all (s_i <=> F_s_i) formulas
def model_check_fixed2_v3(model: Model) -> Function:
    current_set = model.bdd.add_expr("True")
    for i in range(model.num_props):
        current_set = current_set & model.bdd.apply("<=>", labeled_by(f"s__{i}", model), model.update_fns[f"s__{i}"])
    return current_set


# formula: ↓x (EX (~x & (EX x)))
# cycles of size 2  (those might be part of bigger cycles)
def model_check_fixed3(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ex_x = EX(model, x)
    and_inner = ~x & ex_x
    ex_outer = EX(model, and_inner)
    return bind(model, 'x', ex_outer)


# formula: ↓x (EX (EF x))
# Cycles of any size (SCC)
# TODO - more EFFICIENT
def model_check_fixed4(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef = EF(model, x)
    ex = EX(model, ef)
    return bind(model, 'x', ex)


# formula: ↓x. ((EX (EF x)) & (EG s3))
# cycles with a possible path going through only s3 states
def model_check_fixed5(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef_x = EF(model, x)
    ex = EX(model, ef_x)

    s3 = labeled_by("s__3", model)
    eg_s3 = EG(model, s3)

    and_inner = ex & eg_s3
    return bind(model, 'x', and_inner)


# formula: EF ↓x (EF ((~s0) & EF (s0 & x) ) )
# cycles with oscillating gene s0
def model_check_fixed6(model: Model) -> Function:
    x = create_comparator(model, 'x')
    s0 = labeled_by("s__0", model)
    and_inner = x & s0
    ef_inner_inner = EF_v2(model, and_inner)

    and_outer = ~s0 & ef_inner_inner
    ef_inner = EF_v2(model, and_outer)

    binder = bind(model, 'x', ef_inner)
    return EF_v2(model, binder)


# formula: (EG s2) & (EF ~s0)
# states with some path through only s2 states + some path reaching ~s0
def model_check_fixed7(model: Model) -> Function:
    s2 = labeled_by("s__2", model)
    eg_s2 = EG(model, s2)

    not_s0 = ~labeled_by("s__0", model)
    ef = EF(model, not_s0)
    return eg_s2 & ef


# ↓x. EX ( ~x & (↓y. EX y) )
# states which have transition to a different state with a self-loop
def model_check_fixed8(model: Model) -> Function:
    y = create_comparator(model, 'y')
    ex_y = EX(model, y)
    binder_y = bind(model, 'y', ex_y)

    not_x = ~create_comparator(model, 'x')
    and_inner = not_x & binder_y
    ex_outer = EX(model, and_inner)
    return bind(model, 'x', ex_outer)


# ↓x. AG EF x
# states which are part of a sink SCC
def model_check_fixed9(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef_x = EF_v2(model, x)
    ag = AG_v3(model, ef_x)
    return bind(model, 'x', ag)


# ↓x. EX ( ~x & (↓y. AX y) )
# states which have transition to a different state which is a sink state
def model_check_fixed10(model: Model) -> Function:
    y = create_comparator(model, 'y')
    ax_y = AX(model, y)
    binder_y = bind(model, 'y', ax_y)

    not_x = ~create_comparator(model, 'x')
    and_inner = not_x & binder_y
    ex_outer = EX(model, and_inner)
    return bind(model, 'x', ex_outer)


# ↓x. EX ( ~x & (↓y. AX y) ), with better inner binder
def model_check_fixed10_v2(model: Model) -> Function:
    binder_y = model_check_fixed2_v3(model)
    not_x = ~create_comparator(model, 'x')
    and_inner = not_x & binder_y

    binder_x_current = model.bdd.add_expr("False")
    for i in range(model.num_props):
        binder_x_current = binder_x_current | bind(model, 'x', pre_E_one_var(model, f"s__{i}", and_inner))
    return binder_x_current


# ↓x. EX ( ↓y. AX (y & ~x)) )
# states which have transition to a different state which is a sink state, NESTED BINDER VERSION of prev
def model_check_fixed11(model: Model) -> Function:
    y = create_comparator(model, 'y')
    not_x = ~create_comparator(model, 'x')
    and_inner = not_x & y

    binder_y_current = model.bdd.add_expr("True")
    for i in range(model.num_props):
        binder_y_current = binder_y_current & bind(model, 'y', pre_A_one_var(model, f"s__{i}", and_inner))

    binder_x_current = model.bdd.add_expr("False")
    for i in range(model.num_props):
        binder_x_current = binder_x_current | bind(model, 'x', pre_E_one_var(model, f"s__{i}", binder_y_current))
    return binder_x_current


# ↓x. ( ∃y. ( x & EX y ) )
# states which have some successor
# should give the same results as "pre_E_all_vars(model, model.bdd.add_expr("TRUE"))"
def model_check_fixed12(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'y')
    ex_y = EX(model, y)
    intersection = x & ex_y
    exists_y = existential(model, 'y', intersection)
    return bind(model, 'x', exists_y)


# ↓x. (∃y. (x & AX (y & AX y)))
# states which have all its transitions (includes none) to some SINK state (could be itself)
# should give the same results as "sinks | pre_A(sinks)"
def model_check_fixed13(model: Model) -> Function:
    y = create_comparator(model, 'y')
    ax_y = AX(model, y)
    intersection_inner = y & ax_y
    ax_outer = AX(model, intersection_inner)
    x = create_comparator(model, 'x')
    intersection_outer = x & ax_outer

    exists_y = existential(model, 'y', intersection_outer)
    return bind(model, 'x', exists_y)


# ↓x. (∃y. (x & EX (~x & y & AX y)))
# states which have transition to a different state, which is a SINK state
# should give the same results as "model_check_fixed10"
def model_check_fixed14(model: Model) -> Function:
    y = create_comparator(model, 'y')
    ax_y = AX(model, y)
    not_x = ~create_comparator(model, 'x')
    intersection_inner = y & ax_y & not_x
    ex = EX(model, intersection_inner)
    x = create_comparator(model, 'x')
    intersection_outer = x & ex

    exists_y = existential(model, 'y', intersection_outer)
    return bind(model, 'x', exists_y)

# TODO: Something with binder + jump (or existential+jump)


# ============================================================================================= #
# ======================================= PARSING PART ======================================== #
# ============================================================================================= #


# parses a file with a boolean network, creates model from it
# all lines except first one are in the form: "variable_name, update_fn"
# BUT to handle params, we will add lines in form: "param_name," (no update fn) - those will be params
def bnet_parser(file_name: str):
    # first preprocess the file content
    file = open(file_name, "r")
    content = file.read()
    # todo: maybe clean the content (no need if examples are clean)
    lines = content.split("\n")[1:]  # first line does not contain data
    if not lines[-1]:
        lines.pop()  # last item might be just empty string after last newline
    lines_ordered = sorted(lines, key=lambda x: x.split(",")[0])

    # collect all the variable names and their update functions and reorder them
    # order will be alphabetical, upper case first, lowercase later (like ASCII)
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

    # define a BDD vars will be named s0,s1... and we will store full names elsewhere
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

    """
    my_order2 = dict()
    for i in range(num_props):
        my_order2[f"s__{i}"] = i
        my_order2[f"x__{i}"] = i + num_props
        my_order2[f"y__{i}"] = i + 2 * num_props
    for i in range(num_params):
        my_order2[f"p__{i}"] = i + 3 * num_props
    """

    bdd.reorder(my_order)
    # bdd.configure(reordering=False)  # auto reorder disabled (probably)? - it is slower

    # go through update function strings one by one and create dict of BDDs (functions) from them
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
    model = Model(model_name, bdd, num_props, prop_names, num_params, param_names, real_update_dict, update_dict_renamed, name_dict_reversed)
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


def bdd_dumper(file_name: str):
    model = bnet_parser(file_name)
    result = AX(model, create_comparator(model, 'x'))

    var_order = {}
    for i in range(model.num_props):
        var_order[f"s__{i}"] = i
        var_order[f"x__{i}"] = i + 1

    vars_to_show = [f"s__{i}" for i in range(model.num_props)]+[f"x__{i}" for i in range(model.num_props)]
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


def print_results(result: Function, model: Model, message: str = "", show_all: bool = False) -> None:
    if message:
        print(message)

    vars_to_show = [f"s__{i}" for i in range(model.num_props)]+[f"p__{i}" for i in range(model.num_params)]
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)
    print(f"{len(list(assignments))} RESULTS FOUND IN TOTAL")

    if not show_all:
        return

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

    # -----------------------------------------------------------------------------------
    """
    # printing pairs (var_name, value), params first, then propositions
    for assignment in assignments_sorted:
        # we will print only 0/1 instead True/False
        transformed = [(model.name_dict[item[0]], int(item[1])) for item in assignment]
        print(transformed)
    print()
    """
    # -----------------------------------------------------------------------------------
    # printing all variables in alphabetical order
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)  # assigning a generator again, was depleted
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (model.name_dict[x[0]])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (eval_assignment(x, model.num_props + model.num_params)))

    # printing all pairs alphabetically (var_name, value)
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)
    print(f"{len(list(assignments))} RESULTS FOUND IN TOTAL")
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


# test "↓x (EX set1 | EX set2)"
def simple_main(file_name: str):
    model = bnet_parser(file_name)
    results = model_check_fixed9(model)
    print_results(results, model, "", True)


# we have 4 command line args: name of file + type of test + number of test + version of test
if __name__ == '__main__':
    simple_main("D:\\sysbio\\SYBILA\\5. MC combined with PBN\\bnet example files\\029a.bnet")
    # simple_main("D:\\sysbio\\SYBILA\\5. MC combined with PBN\\bnet example files\\095a.bnet")
