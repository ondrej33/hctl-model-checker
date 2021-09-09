from implementation import *


# ============================================================================================= #
# ================================= FIXED FORMULAE EVALUATION ================================= #
# ============================================================================================= #


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
    ag = AG_v2(model, ef_x)
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


# test "↓x (EX set1 | EX set2)"
def simple_main(file_name: str):
    model = bnet_parser(file_name)
    results = model_check_fixed9(model)
    print_results(results, model, "", True)


# we have 4 command line args: name of file + type of test + number of test + version of test
if __name__ == '__main__':
    # TODO add path
    path_to_bnet = ""
    simple_main(path_to_bnet)
