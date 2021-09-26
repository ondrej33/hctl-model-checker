from src.fixed_formulas_eval import *
from src.Parsing_HCTL_formula.evaluator_hctl import parse_and_eval


def run_tests(model: Model) -> None:

    # check that "(EX phi1) || (EX phi2)" == "EX (phi1 || phi2)"
    assert parse_and_eval("(EX s__1) || (EX EX {x})", model) == parse_and_eval("EX (s__1 || EX {x}) ", model)
    assert model_check_fixed19(model) == parse_and_eval("(EX {x}) || (EX EX {x})", model)
    # check that "(AX phi1) && (AX phi2)" == "AX (phi1 && phi2)"
    assert parse_and_eval("(AX s__1) && (AX EX {x})", model) == parse_and_eval("AX (s__1 && EX {x}) ", model)
    assert model_check_fixed20(model) == parse_and_eval("(AX {x}) && (AX EX {x})", model)

    # check all the other formulas that are built in fixed_formulas_eval.py
    assert model_check_fixed1_v2(model) == parse_and_eval("!{x}: EX {x}", model)
    assert model_check_fixed2_v3(model) == parse_and_eval("!{x}: AX {x}", model)
    assert model_check_fixed3(model) == parse_and_eval("!{x}: (EX (~{x} && EX {x}))", model)
    assert model_check_fixed4(model) == parse_and_eval("!{x}: EX EF {x}", model)
    assert model_check_fixed5(model) == parse_and_eval("!{x}: (EX EF {x}) && (EG s__3)", model)
    assert model_check_fixed6(model) == parse_and_eval("EF !{x}: EF (~s__0 && EF (s__0 && {x}))", model)
    assert model_check_fixed7(model) == parse_and_eval("(EG s__2) && (EF ~s__0)", model)
    assert model_check_fixed8(model) == parse_and_eval("!{x}: AX AF {x}", model)
    assert model_check_fixed9(model) == parse_and_eval("!{x}: AG EF {x}", model)
    assert model_check_fixed10(model) == parse_and_eval("!{x}: EX (~{x} && (!{y}: AX {y}))", model)
    assert model_check_fixed10_v2(model) == parse_and_eval("!{x}: EX (~{x} && (!{y}: AX {y}))", model)
    assert model_check_fixed11(model) == parse_and_eval("!{x}: EX (!{y}: AX ({y} && ~{x}))", model)
    assert model_check_fixed12(model) == parse_and_eval("!{x}: (3{y}: {x} && EX {y})", model)
    assert model_check_fixed13(model) == parse_and_eval("!{x}: 3{y}: ({x} && AX ({y} && AX {y}))", model)
    assert model_check_fixed14(model) == parse_and_eval("!{x}: 3{y}: ({x} && EX (~{x} && {y} && AX {y}))", model)
    assert model_check_fixed15(model) == parse_and_eval("3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})", model)
    assert model_check_fixed16(model) == parse_and_eval("!{x}: EG EF {x}", model)
    assert model_check_fixed17(model) == parse_and_eval("3{x}: 3{y}: (@{x}: AG~{y} && AG EF {x}) && (@{y}: AG EF {y})", model)
    assert model_check_fixed18(model) == parse_and_eval("3{x}: 3{y}: (@{x}: ~{y} && AX{x}) && (@{y}: AX{y}) && EF{x} && EF{y}", model)

    # those should be evaluated with optimizations
    assert model_check_fixed21(model) == parse_and_eval("!{x}: (EX {x} || ({x} && s__1))", model)
    assert model_check_fixed22(model) == parse_and_eval("!{x}: (AX {x} || ({x} && s__1))", model)
    assert model_check_fixed23(model) == parse_and_eval("!{x}: ((AX {x} || s__1) || (s__2 || EX {x}))", model)


if __name__ == '__main__':
    # TODO change path
    path_to_bnet = "bnet_examples/095a.bnet"
    m = bnet_parser(path_to_bnet)
    run_tests(m)
