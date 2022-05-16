"""Preparing the working directory and settings"""
import os
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SRC_DIR))
os.chdir(PROJECT_DIR)

import sys
sys.path.append(PROJECT_DIR)

from src.evaluator_hctl import eval_tree
from src.parse_all import parse_all
from src.printing import get_states_only


def run_benchmark_tests():
    """
    Run set of automatic tests on several large models and formulas, and
    compare the numbers of results found to the precomputed ones. Whole set
    of tests might take around 45 minutes to complete.
    """

    # Strong basin of an oscillating attractor
    formula1 = "AF !{x}: (AX (~{x} && AF {x}))"
    # Strong basin of an oscillating attractor which is not a simple cycle
    formula2 = "AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))"
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
    if len(sys.argv) == 1:
        print("Running the tests for several coloured benchmark models and complex formulae.")
        print("Some tests may take several minutes to compute.")
        run_benchmark_tests()
    else:
        print("Script does not take any arguments.")
        print("Usage: test_benchmarks.py")
