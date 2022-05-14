"""Preparing the working directory and settings"""
import os
# Change the current working directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SRC_DIR))
os.chdir(PROJECT_DIR)

import sys
sys.path.append(PROJECT_DIR)

from pathlib import Path

from src.testing.fixed_formulas_eval import *
from src.evaluator_hctl import eval_tree, parse_and_eval
from src.parse_all import parse_all
from src.printing import get_states_only


def run_general_tests(model: Model) -> None:
    """
    Run set of tests comparing results of automatically evaluated formulas to
    results of prepared manually evaluated formulas on given model.
    Model should not be too large (20+ vars models take several min).
    """

    # check that "(EX phi1) || (EX phi2)" == "EX (phi1 || phi2)"
    assert parse_and_eval("(EX s__1) || (EX EX {x})", model) == parse_and_eval("EX (s__1 || EX {x}) ", model)
    assert model_check_fixed19(model) == parse_and_eval("(EX {x}) || (EX EX {x})", model)
    # check that "(AX phi1) && (AX phi2)" == "AX (phi1 && phi2)"
    assert parse_and_eval("(AX s__1) && (AX EX {x})", model) == parse_and_eval("AX (s__1 && EX {x}) ", model)
    assert model_check_fixed20(model) == parse_and_eval("(AX {x}) && (AX EX {x})", model)

    # check all the other formulas that are built in fixed_formulas_eval.py
    assert model_check_fixed1(model) == parse_and_eval("!{x}: EX {x}", model)
    assert model_check_fixed1_v2(model) == parse_and_eval("!{x}: EX {x}", model)
    assert model_check_fixed2(model) == parse_and_eval("!{x}: AX {x}", model)
    assert model_check_fixed2_v2(model) == parse_and_eval("!{x}: AX {x}", model)
    assert model_check_fixed3(model) == parse_and_eval("!{x}: (EX (~{x} && EX {x}))", model)
    assert model_check_fixed4(model) == parse_and_eval("!{x}: EX EF {x}", model)
    assert model_check_fixed5(model) == parse_and_eval("!{x}: (EX EF {x}) && (EG s__3)", model)
    assert model_check_fixed6(model) == parse_and_eval("!{x}: 3{xx}: (@{x}: ~{xx} && AX {x}) && (@{xx}: AX {xx})", model)
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

    # these should be evaluated with optimizations for larger models
    assert model_check_fixed21(model) == parse_and_eval("!{x}: (EX {x} || ({x} && s__1))", model)
    assert model_check_fixed22(model) == parse_and_eval("!{x}: (AX {x} || ({x} && s__1))", model)
    assert model_check_fixed23(model) == parse_and_eval("!{x}: ((AX {x} || s__1) || (s__2 || EX {x}))", model)

    assert model_check_fixed24(model) == parse_and_eval("AF !{x}: (AX (~{x} && AF {x}))", model)
    assert model_check_fixed25(model) == parse_and_eval("AF !{x}: ((AX (~{x} && AF {x})) && (EF !{xx}: EX EG ~{xx}))", model)
    print("All tests passed.")


def run_benchmark_tests():
    """
    Run set of automatic tests on several large models and formulas, and
    compare the numbers of results found to the precomputed ones. Whole set of
    tests might take around 45 minutes (strongly depends on Python's caching).
    """

    # Strong basin of an oscillating attractor
    formula1 = "AF !{x}: (AX (~{x} && AF {x}))"
    # Strong basin of an oscillating attractor which is not a simple cycle
    formula2 = "AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX EG ~{y}))"
    # Multiple steady states
    formula3 = "!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})"
    # Fork states existence
    formula4 = "3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y}) && EF ({x} && !{z}: AX {z}) && EF ({y} && !{z}: AX {z}) && AX (EF ({x} && !{z}: AX {z}) ^ EF ({y} && !{z}: AX {z}))"
    formulas = [formula1, formula2, formula3, formula4]

    model1 = "benchmark_models/coloured_benchmarks/1.bnet"  # Interactions in gut microbiome model
    model2 = "benchmark_models/coloured_benchmarks/2.bnet"  # Iron acquisition model
    model3 = "benchmark_models/coloured_benchmarks/3.bnet"  # WG Signaling Pathway model
    model4 = "benchmark_models/coloured_benchmarks/4.bnet"  # Apoptosis network model
    model5 = "benchmark_models/coloured_benchmarks/5.bnet"  # Reduced MAPK network model
    model6 = "benchmark_models/coloured_benchmarks/6.bnet"  # E Protein model
    models = [model1, model2, model3, model4, model5, model6]

    numbers_states1 = [2048, 2048, 640, 2048]
    numbers_states2 = [128, 128, 16, 64]
    numbers_states3 = [65408, 0, 65536, 0]
    numbers_states4 = [0, 0, 0, 0]
    numbers_states5 = [48, 32, 46, 16]
    numbers_states6 = [81920, 0, 81920, 81920]
    numbers_states = [numbers_states1, numbers_states2, numbers_states3,
                      numbers_states4, numbers_states5, numbers_states6]

    for model_num in range(6):
        for form_num in range(4):
            model, as_tree_hctl = parse_all(models[model_num], formulas[form_num])
            res = eval_tree(as_tree_hctl, model)
            states_num = model.bdd.count(get_states_only(res, model), nvars=model.num_props())
            assert states_num == numbers_states[model_num][form_num]
            print(f"Test for model {model_num + 1}, formula {form_num + 1} successful")


if __name__ == '__main__':
    """Run the chosen set of tests on the given model."""
    if len(sys.argv) == 2:
        if Path(sys.argv[1]).exists() and Path(sys.argv[1]).is_file():
            print(f"Running the tests for \"{sys.argv[1]}\".")
            # use some placeholder formula (with the maximal number of HCTL vars that any formula uses (2 atm))
            m, _ = parse_all(sys.argv[1], "3{x}: 3{xx}: (@{x}: ~{xx} && AX{x}) && (@{xx}: AX{xx}) && EF{x} && EF{xx}")
            run_general_tests(m)
        else:
            print(f"File {sys.argv[1]} does not exist")
            print("Usage: testing_automatic.py [model_file]")
    else:
        print("Running the tests for several large models and complex formulae.")
        print("Some tests may take several minutes to compute.")
        run_benchmark_tests()
