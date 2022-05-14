from src.implementation_components import *

"""
This file contains several 'manually' evaluated HCTL formulae.
This can be later used to test the parser or evaluator.
"""


# ============================================================================================= #
# ================================= FIXED FORMULAE EVALUATION ================================= #
# ============================================================================================= #

"""
List of formulas included in current version:
    1: "!{x}: EX {x}"
    2: "!{x}: AX {x}"
    3: "!{x}: (EX (~{x} && EX {x}))"
    4:  "!{x}: EX EF {x}"
    5: "!{x}: (EX EF {x}) && (EG s__3)"
    6: "!{x}: 3{xx}: (@{x}: ~{xx} && AX {x}) && (@{xx}: AX {xx})"
    7: "(EG s__2) && (EF ~s__0)"
    8: "!{x}: AX AF {x}"
    9: "!{x}: AG EF {x}"
    10: "!{x}: EX (~{x} && (!{xx}: AX {xx}))"
    11: "!{x}: EX (!{xx}: AX ({xx} && ~{x}))"
    12: "!{x}: (3{xx}: {x} && EX {xx})"
    13: "!{x}: 3{xx}: ({x} && AX ({xx} && AX {xx}))"
    14: "!{x}: 3{xx}: ({x} && EX (~{x} && {xx} && AX {xx}))"
    15: "3{x}: 3{xx}: (@{x}: ~{xx} && AX {x}) && (@{xx}: AX {xx})"
    16: "!{x}: EG EF {x}"
    17: "3{x}: 3{xx}: (@{x}: AG~{xx} && AG EF {x}) && (@{xx}: AG EF {xx})"
    18: "3{x}: 3{xx}: (@{x}: ~{xx} && AX{x}) && (@{xx}: AX{xx}) && EF{x} && EF{xx}"
    19: "EX ({x} || EX {x})"
    20: "AX ({x} && EX {x})"
    21: "!{x}: (EX {x} || ({x} && s__1))"
    22: "!{x}: (AX {x} || ({x} && s__1))"
    23: "!{x}: ((AX {x} || s__1) || (s__2 || EX {x}))"
    24: "AF !{x}: (AX (~{x} && AF {x}))"
    25: "AF !{x}: ((AX (~{x} && AF {x})) && (EF !{xx}: EX EG ~{xx}))"
"""


# formula: ↓x (EX x)
# unstable steady states (self loop)
def model_check_fixed1(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ex = EX(model, x)
    return bind(model, ex, 'x')


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
    return bind(model, ax, 'x')


# formula: ↓x (AX x), stable steady states (self loop only, sink)
# FASTEST probably, uses "equational fixed point", big conjunction of all (s_i <=> F_s_i) formulas
def model_check_fixed2_v2(model: Model) -> Function:
    return model.stable


# formula: ↓x (EX (~x & (EX x)))
# states that are part of (unstable) cycles of size 2  (those might be part of bigger cycles)
def model_check_fixed3(model: Model) -> Function:
    x = create_comparator(model, 'x')
    not_x = negate(model, x)
    ex_x = EX(model, x)
    and_inner = not_x & ex_x
    ex_outer = EX(model, and_inner)
    return bind(model, ex_outer, 'x')


# formula: ↓x (EX (EF x))
# states that are part of (unstable) cycles of any size
def model_check_fixed4(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef = EF_saturated(model, x)
    ex = EX(model, ef)
    return bind(model, ex, 'x')


# formula: ↓x (EX (EF x))
# states that are part of (unstable) cycles of any size with SATURATION
def model_check_fixed4_v2(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef = EF_saturated(model, x)
    ex = EX(model, ef)
    return bind(model, ex, 'x')


# formula: ↓x. ((EX (EF x)) & (EG s3))
# cycles with a possible path going through only s3 states
def model_check_fixed5(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef_x = EF_saturated(model, x)
    s3 = labeled_by(model, "s__3")

    and_inner = EX(model, ef_x) & EG(model, s3)
    return bind(model, and_inner, 'x')


# formula: "↓x. ∃y: (@x: ~y & AX x) & (@y: AX y)"
# steady states in multi stable systems
def model_check_fixed6(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'xx')
    not_y = negate(model, y)

    jump_y = jump(model, AX(model, y), 'xx')
    jump_x = jump(model, not_y & AX(model, x), 'x')

    and_inner = jump_x & jump_y
    exist_y = existential(model, and_inner, 'xx')
    return bind(model, exist_y, 'x')


# formula: (EG s2) & (EF ~s0)
# states with some possible path through only s2 states + some path reaching ~s0
def model_check_fixed7(model: Model) -> Function:
    s2 = labeled_by(model, "s__2")
    eg_s2 = EG(model, s2)

    not_s0 = negate(model, labeled_by(model, "s__0"))
    ef = EF_saturated(model, not_s0)
    return eg_s2 & ef


# formula: (EG s2) & (EF ~s0)
# states with some possible path through only s2 states + some path reaching ~s0 with SATURATION
def model_check_fixed7_v2(model: Model) -> Function:
    s2 = labeled_by(model, "s__2")
    eg_s2 = EG(model, s2)

    not_s0 = negate(model, labeled_by(model, "s__0"))
    ef = EF_saturated(model, not_s0)
    return eg_s2 & ef


# ↓x. AX AF x
# states that are part of periodic attractors - states that will always reach itself again
def model_check_fixed8(model: Model) -> Function:
    x = create_comparator(model, 'x')
    af = AF(model, x)
    ax = AX(model, af)
    return bind(model, ax, 'x')


# ↓x. AG EF x
# states which are part of a sink SCC
def model_check_fixed9(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef_x = EF_saturated(model, x)
    ag = AG(model, ef_x)
    return bind(model, ag, 'x')


# ↓x. AG EF x
# states which are part of a sink SCC, using SATURATION
def model_check_fixed9_v2(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef_x = EF_saturated(model, x)
    ag = AG(model, ef_x)
    return bind(model, ag, 'x')


# ↓x. EX ( ~x & (↓y. AX y) )
# states which have transition to a different state which is a sink state
def model_check_fixed10(model: Model) -> Function:
    binder_y = model_check_fixed2_v2(model)
    not_x = negate(model, create_comparator(model, 'x'))
    and_inner = not_x & binder_y

    ex_outer = EX(model, and_inner)
    return bind(model, ex_outer, 'x')


# ↓x. EX ( ~x & (↓y. AX y) ), with optimized version of "bind EX"
def model_check_fixed10_v2(model: Model) -> Function:
    binder_y = model_check_fixed2_v2(model)
    not_x = negate(model, create_comparator(model, 'x'))
    and_inner = not_x & binder_y
    return optimized_bind_EX(model, and_inner, 'x')


# ↓x. EX ( ↓y. AX (y & ~x)) )
# states which have transition to a different state which is a sink state, NESTED BINDER VERSION of prev
def model_check_fixed11(model: Model) -> Function:
    y = create_comparator(model, 'xx')
    not_x = negate(model, create_comparator(model, 'x'))
    and_inner = not_x & y

    # TODO: maybe update and use better version for "bind AX"
    binder_y = bind(model, AX(model, and_inner), 'xx')
    return optimized_bind_EX(model, binder_y, 'x')


# ↓x. ( ∃y. ( x & EX y ) )
# states which have some successor, nested operators version
# should give the same results as "pre_E_all_vars(model, model.mk_unit_colored_set()) & ~model.stable"
def model_check_fixed12(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'xx')
    ex_y = EX(model, y)
    intersection = x & ex_y
    exists_y = existential(model, intersection, 'xx')
    return bind(model, exists_y, 'x')


# ↓x. (∃y. (x & AX (y & AX y)))
# states which have all their transitions (includes none) to some SINK state (could be itself)
# should give the same results as "sinks | pre_A(sinks)"
def model_check_fixed13(model: Model) -> Function:
    y = create_comparator(model, 'xx')
    ax_y = AX(model, y)
    intersection_inner = y & ax_y
    ax_outer = AX(model, intersection_inner)
    x = create_comparator(model, 'x')
    intersection_outer = x & ax_outer

    exists_y = existential(model, intersection_outer, 'xx')
    return bind(model, exists_y, 'x')


# ↓x. (∃y. (x & EX (~x & y & AX y)))
# states which have transition to a different state, which is a SINK state
# should give the same results as "model_check_fixed10"
def model_check_fixed14(model: Model) -> Function:
    y = create_comparator(model, 'xx')
    ax_y = AX(model, y)
    not_x = negate(model, create_comparator(model, 'x'))
    intersection_inner = y & ax_y & not_x
    ex = EX(model, intersection_inner)
    x = create_comparator(model, 'x')
    intersection_outer = x & ex

    exists_y = existential(model, intersection_outer, 'xx')
    return bind(model, exists_y, 'x')


# ∃x. ∃y. ((@x. ~y & AX x) & (@y. AX y))
# all colored states in colors where "there exist at least 2 sinks"
def model_check_fixed15(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'xx')
    not_y = negate(model, y)

    jump_y = jump(model, AX(model, y), 'xx')
    jump_x = jump(model, not_y & AX(model, x), 'x')

    and_inner = jump_x & jump_y
    exist_y = existential(model, and_inner, 'xx')
    return existential(model, exist_y, 'x')


# ↓x. EG EF x
# states which are part of any SCC
def model_check_fixed16(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ef_x = EF_saturated(model, x)
    eg = EG(model, ef_x)
    return bind(model, eg, 'x')


# ∃x.∃y.(@x. AG¬y & AG EF x) & (@y. AG EF y)
# at least two final SCCs in the whole system
def model_check_fixed17(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'xx')
    not_y = negate(model, y)

    ag_ef_y = AG(model, EF_saturated(model, y))
    jump_y = jump(model, ag_ef_y, 'xx')

    ag_ef_x = AG(model, EF_saturated(model, x))
    ag_not_y = AG(model, not_y)
    jump_x = jump(model, ag_not_y & ag_ef_x, 'x')

    and_inner = jump_x & jump_y
    exist_y = existential(model, and_inner, 'xx')
    return existential(model, exist_y, 'x')


# ∃x. ∃y. (@x. ~y & AXx) & (@y. AXy) & EFx & EFy
# states  that  have  two  outgoing  paths  to  two  different sinks
# (intersection of basins of attraction of two different sinks)
def model_check_fixed18(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'xx')
    not_y = negate(model, y)

    jump_x = jump(model, not_y & AX(model, x), 'x')
    jump_y = jump(model, AX(model, y), 'xx')

    and_inner = jump_x & jump_y & EF_saturated(model, x) & EF_saturated(model, y)
    exist_y = existential(model, and_inner, 'xx')
    return existential(model, exist_y, 'x')


# EX (x || EX x)
def model_check_fixed19(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ex_x = EX(model, x)
    return EX(model, x | ex_x)


# AX (x && EX x)
def model_check_fixed20(model: Model) -> Function:
    x = create_comparator(model, 'x')
    ex_x = EX(model, x)
    return AX(model, x & ex_x)


# ↓x. (EX x | (x & s1))
def model_check_fixed21(model: Model) -> Function:
    x = create_comparator(model, 'x')
    s1 = labeled_by(model, "s__1")
    return bind(model, EX(model, x) | (x & s1), 'x')


# ↓x. (AX x | (x & s1))
def model_check_fixed22(model: Model) -> Function:
    x = create_comparator(model, 'x')
    s1 = labeled_by(model, "s__1")
    return bind(model, AX(model, x) | (x & s1), 'x')


# ↓x. ((AX x | s1) | (s2 | EX x))
def model_check_fixed23(model: Model) -> Function:
    x = create_comparator(model, 'x')
    s1 = labeled_by(model, "s__1")
    s2 = labeled_by(model, "s__2")
    return bind(model, (AX(model, x) | s1) | (s2 | EX(model, x)), 'x')


# AF !{x}: (AX (~{x} && AF {x}))
# Strong basin of an oscillating attractor
def model_check_fixed24(model: Model) -> Function:
    x = create_comparator(model, 'x')
    not_x = negate(model, x)

    ax = AX(model, not_x & AF(model, x))
    binder = bind(model, ax, 'x')
    return AF(model, binder)


# AF !{x}: ((AX (~{x} && AF {x})) && (EF !{xx}: EX EG ~{xx}))
# Strong basin of an oscillating attractor which is not a cycle
def model_check_fixed25(model: Model) -> Function:
    x = create_comparator(model, 'x')
    y = create_comparator(model, 'xx')
    not_x = negate(model, x)
    not_y = negate(model, y)

    ax = AX(model, not_x & AF(model, x))

    inner_binder = bind(model, EX(model, EG(model, not_y)), 'xx')
    ef = EF_saturated(model, inner_binder)

    outer_binder = bind(model, ax & ef, 'x')
    return AF(model, outer_binder)
