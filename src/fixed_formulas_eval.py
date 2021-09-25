from src.implementation import *
from src.parse_all import parse_all


# ============================================================================================= #
# ================================= FIXED FORMULAE EVALUATION ================================= #
# ============================================================================================= #


# formula: ↓x (EX x)
# unstable steady states (self loop)
def model_check_fixed1(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ex = EX(model, x)
    return bind(model, 'x', ex)


# formula: ↓x (EX x)
# faster version, uses binder already during computing the EX, with smaller BDDs
def model_check_fixed1_v2(model: Model) -> Function:
    x = create_comparator(model, 'x')
    return optimized_bind_EX(model, x, 'x')


# formula: ↓x (AX x)
# stable steady states - sink states
def model_check_fixed2(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ax = AX(model, x)
    return bind(model, 'x', ax)


# TODO: update "bind AX" and use it next fn
"""
# formula: ↓x (AX x), stable steady states (self loop only, sink)
# faster version, uses binder already during computing the AX, with smaller BDDs
def model_check_fixed2_v2(model: Model) -> Function:
    # TODO: change, do not use pre_A_one_var
    x = create_comparator(model, 'x')

    current_set = model.bdd.add_expr("True")
    for i in range(model.num_props):
        current_set = current_set & bind(model, 'x', pre_A_one_var(model, f"s__{i}", x))
    return current_set
"""


# formula: ↓x (AX x), stable steady states (self loop only, sink)
# FASTEST probably, uses "equational fixed point", big conjunction of all (s_i <=> F_s_i) formulas
def model_check_fixed2_v3(model: Model) -> Function:
    current_set = model.bdd.add_expr("True")
    for i in range(model.num_props):
        current_set = current_set & model.bdd.apply("<=>", labeled_by(f"s__{i}", model), model.update_fns[f"s__{i}"])
    return current_set


# formula: ↓x (EX (~x & (EX x)))
# states that are part of (unstable) cycles of size 2  (those might be part of bigger cycles)
def model_check_fixed3(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ex_x = EX(model, x)
    and_inner = ~x & ex_x
    ex_outer = EX(model, and_inner)
    return bind(model, 'x', ex_outer)


# formula: ↓x (EX (EF x))
# states that are part of (unstable) cycles of any size
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
    s3 = labeled_by("s__3", model)

    and_inner = EX(model, ef_x) & EG(model, s3)
    return bind(model, 'x', and_inner)


# formula: EF ↓x (EF ((~s0) & EF (s0 & x)))
# states that are part of (unstable) cycles with oscillating gene s0
def model_check_fixed6(model: Model) -> Function:
    x = create_comparator(model, 'x')
    s0 = labeled_by("s__0", model)
    ef_inner_inner = EF_v2(model, x & s0)

    and_outer = ~s0 & ef_inner_inner
    ef_inner = EF_v2(model, and_outer)
    binder = bind(model, 'x', ef_inner)
    return EF_v2(model, binder)


# formula: (EG s2) & (EF ~s0)
# states with some possible path through only s2 states + some path reaching ~s0
def model_check_fixed7(model: Model) -> Function:
    s2 = labeled_by("s__2", model)
    eg_s2 = EG(model, s2)

    not_s0 = ~labeled_by("s__0", model)
    ef = EF(model, not_s0)
    return eg_s2 & ef


# ↓x. AX AF x
# states that are part of periodic attractors - states that will always reach itself again
def model_check_fixed8(model: Model) -> Function:
    x = create_comparator(model, 'x')
    af = AF(model, x)
    ax = AX(model, af)
    return bind(model, 'x', ax)


# ↓x. AG EF x
# states which are part of a sink SCC
def model_check_fixed9(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef_x = EF_v2(model, x)
    ag = AG(model, ef_x)
    return bind(model, 'x', ag)


# ↓x. EX ( ~x & (↓y. AX y) )
# states which have transition to a different state which is a sink state
def model_check_fixed10(model: Model) -> Function:
    binder_y = model_check_fixed2_v3(model)
    not_x = ~create_comparator(model, 'x')
    and_inner = not_x & binder_y

    ex_outer = EX(model, and_inner)
    return bind(model, 'x', ex_outer)


# ↓x. EX ( ~x & (↓y. AX y) ), with optimized version of "bind EX"
def model_check_fixed10_v2(model: Model) -> Function:
    binder_y = model_check_fixed2_v3(model)
    not_x = ~create_comparator(model, 'x')
    and_inner = not_x & binder_y
    return optimized_bind_EX(model, and_inner, 'x')


# ↓x. EX ( ↓y. AX (y & ~x)) )
# states which have transition to a different state which is a sink state, NESTED BINDER VERSION of prev
def model_check_fixed11(model: Model) -> Function:
    y = create_comparator(model, 'y')
    not_x = ~create_comparator(model, 'x')
    and_inner = not_x & y

    # TODO: update and use better version for "bind AX"
    binder_y = bind(model, 'y', AX(model, and_inner))
    return optimized_bind_EX(model, binder_y, 'x')


# ↓x. ( ∃y. ( x & EX y ) )
# states which have some successor, nested operators version
# should give the same results as "pre_E_all_vars(model, model.bdd.add_expr("TRUE")) & ~model.stable"
def model_check_fixed12(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'y')
    ex_y = EX(model, y)
    intersection = x & ex_y
    exists_y = existential(model, 'y', intersection)
    return bind(model, 'x', exists_y)


# ↓x. (∃y. (x & AX (y & AX y)))
# states which have all their transitions (includes none) to some SINK state (could be itself)
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


# ∃x. ∃y. ((@x. ~y & AX x) & (@y. AX y))
# all colored states where "there exist at least 2 sinks"
def model_check_fixed15(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'y')

    jump_y = jump(model, 'y', AX(model, y))
    jump_x = jump(model, 'x', ~y & AX(model, x))

    and_inner = jump_x & jump_y
    exist_y = existential(model, 'y', and_inner)
    return existential(model, 'x', exist_y)


# ↓x. EG EF x
# states which are part of any SCC
def model_check_fixed16(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef_x = EF_v2(model, x)
    eg = EG(model, ef_x)
    return bind(model, 'x', eg)


# ∃x.∃y.(@x. AG¬y & AG EFx) & (@y. AG EFy)
# at least two final SCCs in the whole system
def model_check_fixed17(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'y')

    ag_ef_y = AG(model, EF_v2(model, y))
    jump_y = jump(model, 'y', ag_ef_y)

    ag_ef_x = AG(model, EF_v2(model, x))
    ag_not_y = AG(model, ~y)
    jump_x = jump(model, 'x', ag_not_y & ag_ef_x)

    and_inner = jump_x & jump_y
    exist_y = existential(model, 'y', and_inner)
    return existential(model, 'x', exist_y)


# ∃x. ∃y. (@x. ~y & AXx) & (@y. AXy) & EFx & EFy
# states  that  have  two  outgoing  paths  to  two  different sinks
# (intersection of basins of attraction of two different sinks)
def model_check_fixed18(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'y')

    jump_x = jump(model, 'x', ~x & AX(model, x))
    jump_y = jump(model, 'y', AX(model, y))

    and_inner = jump_x & jump_y & EF(model, x) & EF(model, y)
    exist_y = existential(model, 'y', and_inner)
    return existential(model, 'x', exist_y)


# ============================================================================================= #
# =================================== OTHER TESTS AND STUFF =================================== #
# ============================================================================================= #


# test "↓x (EX set1 | EX set2)"
def simple_main(file_name: str):
    # formula here is just a placeholder to save var names
    model, _ = parse_all(file_name, "!{x}: (AX {x})")
    results = model_check_fixed9(model)
    print_results(results, model, "", True)


def simple_main2(file_name: str):
    model = bnet_parser(file_name)
    x = create_comparator(model, 'x')
    intersection = x & labeled_by("s__4", model)
    ax = AX(model, intersection)
    print_results(ax, model)

    comparator = create_comparator(model, "x")
    intersection = comparator & ax
    print_results(intersection, model)

    # now lets use existential quantification to get rid of the bdd vars coding VAR
    vars_to_get_rid = [f"x__{i}" for i in range(model.num_props)]
    result = model.bdd.quantify(intersection, vars_to_get_rid)
    print_results(result, model)


# we have 4 command line args: name of file + type of test + number of test + version of test
if __name__ == '__main__':
    # TODO change path
    path_to_bnet = "bnet_examples/007.bnet"
    simple_main2(path_to_bnet)
