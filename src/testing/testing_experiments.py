import os
# Change the current working directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SRC_DIR))
os.chdir(PROJECT_DIR)

import sys
sys.path.append(PROJECT_DIR)
sys.path.append(f'{SRC_DIR}')

from src.parse_all import parse_all
from src.parse_hctl_formula.evaluator_hctl import eval_tree
from src.printing import print_results_fast, print_results
from src.fixed_formulas_eval import *

import time
import timeout_decorator

@timeout_decorator.timeout(1 * 3600)
def run_test(file_name, formula):
    start = time.time()
    model, as_tree_hctl = parse_all(file_name, formula)

    res = eval_tree(as_tree_hctl, model)
    end = time.time()

    # print_results(res, model, show_all=True)
    print_results_fast(res, model, f"model: {model.name}, formula: {formula}")
    print(end - start)
    print()


def get_result(file_name, formula, real_model):
    _, as_tree_hctl = parse_all(file_name, formula)
    return eval_tree(as_tree_hctl, real_model)


def compute_stable(file_name):
    start = time.time()
    formula = "!{x}: AX {x}"
    model, as_tree_hctl = parse_all(file_name, formula)

    #res = eval_tree(as_tree_hctl, model)
    #stable = model_check_fixed2_v3(model)

    stable = model.stable

    end = time.time()
    print(formula, ": ", end - start)
    print_results_fast(stable, model)


# usage: testing_full_eval.py path_to_bnet formula
if __name__ == '__main__':
    # we will have general 'if' branch and test-specific 'else' branch
    if len(sys.argv) == 3:
        run_test(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        compute_stable(sys.argv[1])

    else:

        """
        # pre-defined formulas to choose from:
        
        run_test(path_to_bnet, "!{x}: AX {x}")
        run_test(path_to_bnet, "!{x}: AX AF {x}")
        run_test(path_to_bnet, "!{x}: AG EF {x}")
        run_test(path_to_bnet, "!{x}: EG EF {x}")

        # Existence of two SCCs
        run_test(path_to_bnet, "3{x}: 3{y}: (@{x}: AG~{y} && AG EF {x}) && (@{y}: AG EF {y})")

        # Strong basin of an oscillating attractor
        run_test(path_to_bnet, "AF !{x}: (AX (~{x} && AF {x}))")

        # Strong basin of an oscillating attractor which is not a cycle
        run_test(path_to_bnet, "AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX EG ~{y}))")

        # Existence of two sinks
        run_test(path_to_bnet, "!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})")

        # Fork states existence
        run_test(path_to_bnet, "3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y}) && EF ({x} && !{z}: AX {z}) && EF ({y} && !{z}: AX {z}) && AX (EF ({x} && !{z}: AX {z}) ^ EF ({y} && !{z}: AX {z}))")
        """
        names = "029 095 064 097 063 067 010 053 104 035 036 037 021 028 062 049 003 119 131 022 047 042 045 033 034 038 042 045 033 034 038 027 098".split(' ')

        for name in names:
            print(name)
            path_to_bnet = f"bnet_examples/{name}_free.bnet"
            run_test(path_to_bnet, "!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})")
