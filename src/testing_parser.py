import os
# Change the current working directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
os.chdir(PROJECT_DIR)

import sys
sys.path.append(PROJECT_DIR)
sys.path.append(f'{SRC_DIR}')
sys.path.append(f'{SRC_DIR}/Parsing_HCTL_formula')
sys.path.append(f'{SRC_DIR}/Parsing_update_fns')

from pathlib import Path

from src.fixed_formulas_eval import *
from src.Parsing_HCTL_formula.evaluator_hctl import parse_and_eval
from src.parse_all import parse_all


def run_tests(model: Model) -> None:
    # check that "(EX phi1) || (EX phi2)" == "EX (phi1 || phi2)"
    assert parse_and_eval("(EX s__1) || (EX EX {x})", model) == parse_and_eval("EX (s__1 || EX {x}) ", model)
    assert model_check_fixed19(model) == parse_and_eval("(EX {x}) || (EX EX {x})", model)
    # check that "(AX phi1) && (AX phi2)" == "AX (phi1 && phi2)"
    assert parse_and_eval("(AX s__1) && (AX EX {x})", model) == parse_and_eval("AX (s__1 && EX {x}) ", model)
    assert model_check_fixed20(model) == parse_and_eval("(AX {x}) && (AX EX {x})", model)

    # check all the other formulas that are built in fixed_formulas_eval.py
    assert model_check_fixed1_v2(model) == parse_and_eval("!{x}: EX {x}", model)
    assert model_check_fixed2_v2(model) == parse_and_eval("!{x}: AX {x}", model)
    assert model_check_fixed3(model) == parse_and_eval("!{x}: (EX (~{x} && EX {x}))", model)
    assert model_check_fixed4(model) == parse_and_eval("!{x}: EX EF {x}", model)
    assert model_check_fixed5(model) == parse_and_eval("!{x}: (EX EF {x}) && (EG s__3)", model)
    assert model_check_fixed6(model) == parse_and_eval("EF !{x}: EF (~s__0 && EF (s__0 && {x}))", model)
    assert model_check_fixed7(model) == parse_and_eval("(EG s__2) && (EF ~s__0)", model)
    assert model_check_fixed8(model) == parse_and_eval("!{x}: AX AF {x}", model)
    assert model_check_fixed9(model) == parse_and_eval("!{x}: AG EF {x}", model)
    assert model_check_fixed10(model) == parse_and_eval("!{x}: EX (~{x} && (!{xx}: AX {xx}))", model)
    assert model_check_fixed10_v2(model) == parse_and_eval("!{x}: EX (~{x} && (!{xx}: AX {xx}))", model)
    assert model_check_fixed11(model) == parse_and_eval("!{x}: EX (!{xx}: AX ({xx} && ~{x}))", model)
    assert model_check_fixed12(model) == parse_and_eval("!{x}: (3{xx}: {x} && EX {xx})", model)
    assert model_check_fixed13(model) == parse_and_eval("!{x}: 3{xx}: ({x} && AX ({xx} && AX {xx}))", model)
    assert model_check_fixed14(model) == parse_and_eval("!{x}: 3{xx}: ({x} && EX (~{x} && {xx} && AX {xx}))", model)
    assert model_check_fixed15(model) == parse_and_eval("3{x}: 3{xx}: (@{x}: ~{xx} && AX {x}) && (@{xx}: AX {xx})", model)
    assert model_check_fixed16(model) == parse_and_eval("!{x}: EG EF {x}", model)
    assert model_check_fixed17(model) == parse_and_eval("3{x}: 3{xx}: (@{x}: AG~{xx} && AG EF {x}) && (@{xx}: AG EF {xx})", model)
    assert model_check_fixed18(model) == parse_and_eval("3{x}: 3{xx}: (@{x}: ~{xx} && AX{x}) && (@{xx}: AX{xx}) && EF{x} && EF{xx}", model)

    # those should be evaluated with optimizations
    assert model_check_fixed21(model) == parse_and_eval("!{x}: (EX {x} || ({x} && s__1))", model)
    assert model_check_fixed22(model) == parse_and_eval("!{x}: (AX {x} || ({x} && s__1))", model)
    assert model_check_fixed23(model) == parse_and_eval("!{x}: ((AX {x} || s__1) || (s__2 || EX {x}))", model)

    assert model_check_fixed24(model) == parse_and_eval("AF !{x}: (AX (~{x} && AF {x}))", model)
    assert model_check_fixed25(model) == parse_and_eval("AF !{x}: ((AX (~{x} && AF {x})) && (EF !{xx}: EX EG ~{xx}))", model)


if __name__ == '__main__':
    # runs the whole set of tests on the given model
    if len(sys.argv) == 2:
        if Path(sys.argv[1]).exists() and Path(sys.argv[1]).is_file():
            # first use some placeholder formula (with the maximal number of HCTL vars that any formula uses (2 atm))
            m, _ = parse_all(sys.argv[1], "3{x}: 3{xx}: (@{x}: ~{xx} && AX{x}) && (@{xx}: AX{xx}) && EF{x} && EF{xx}")
            run_tests(m)
        else:
            print(f"File {sys.argv[1]} does not exist")
            print("Usage: testing_parser.py path_to_bnet")
    else:
        print("Wrong number of arguments")
        print("Usage: testing_parser.py path_to_bnet")
