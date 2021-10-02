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

from src.parse_all import parse_all
from Parsing_HCTL_formula.evaluator_hctl import eval_tree
from src.implementation import print_results_fast, print_results
import time


def run_test(file_name, formula):
    model, as_tree_hctl = parse_all(file_name, formula)
    start = time.time()
    res = eval_tree(as_tree_hctl, model)
    end = time.time()
    res_time = end - start

    # print_results_fast(res, model, f"model: {model.name}, formula: {formula}")
    print_results(res, model, show_all=True)
    print(formula, ": ", res_time, "\n")


def get_result(file_name, formula, real_model):
    _, as_tree_hctl = parse_all(file_name, formula)
    return eval_tree(as_tree_hctl, real_model)


# usage: testing_full_eval.py path_to_bnet formula
if __name__ == '__main__':
    if len(sys.argv) == 3:
        run_test(sys.argv[1], sys.argv[2])
    else:
        path_to_bnet = "bnet_examples/029_free.bnet"
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
        run_test(path_to_bnet, "3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})")


        # MAYBE: fork existence / fork states exactly
        fork_exist1 = "3{z}: 3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (@{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        fork_exist2 = "3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (3{z}: @{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"

        fork_exactly1 = "!{z}: 3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (@{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        fork_exactly2 = "3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (!{z}: @{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        fork_exactly3 = "3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (!{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        fork_exactly4 = "3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (3{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        """

        # TESTING formula for fork state existence
        fork_exist1 = "3{z}: 3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (@{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        fork_exist2 = "3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (3{z}: @{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"

        fork_exactly1 = "!{z}: 3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (@{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        fork_exactly2 = "3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (!{z}: @{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        fork_exactly3 = "3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (!{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"
        fork_exactly4 = "3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (3{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))"

        # we want to use same model and bdd for all parts (formulas use same number of vars, etc)
        m, _ = parse_all(path_to_bnet, fork_exist1)  # just to get model, we'll use it for all formulas

        existence = get_result(path_to_bnet, fork_exist1, m)
        print_results(existence, m, "existence", show_all=True)

        forks = get_result(path_to_bnet, fork_exactly1, m)
        print_results(forks, m, "forks", show_all=True)

        assert existence == get_result(path_to_bnet, fork_exist2, m)

        assert forks == get_result(path_to_bnet, fork_exactly2, m)
        assert forks == get_result(path_to_bnet, fork_exactly3, m)
        assert forks == get_result(path_to_bnet, fork_exactly4, m)
