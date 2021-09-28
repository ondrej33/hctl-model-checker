"""
import os
# Change the current working directory
os.chdir('/home/xhuvar/HCTL_stuff')

import sys
sys.path.append('/home/xhuvar/HCTL_stuff/')
sys.path.append('/home/xhuvar/HCTL_stuff/src')
sys.path.append('/home/xhuvar/HCTL_stuff/src/Parsing_HCTL_formula')
sys.path.append('/home/xhuvar/HCTL_stuff/src/Parsing_update_fns')
sys.path.append('/home/xhuvar/HCTL_stuff/venv/lib/python3.8/site-packages')
"""

import os
# Change the current working directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
os.chdir(PROJECT_DIR)

import sys
sys.path.append(PROJECT_DIR)
sys.path.append('{SRC_DIR}')
sys.path.append('{SRC_DIR}/Parsing_HCTL_formula')
sys.path.append('{SRC_DIR}/Parsing_update_fns')

from src.parse_all import parse_all
from Parsing_HCTL_formula.evaluator_hctl import eval_tree
from src.implementation import print_results
import time


def run_test(file_name, formula):
    model, as_tree_hctl = parse_all(file_name, formula)
    start = time.time()
    res = eval_tree(as_tree_hctl, model)
    end = time.time()
    res_time = end - start

    print_results(res, model, f"model: {model.name}, formula: {formula}", show_all=False)
    print(formula, ": ", res_time, "\n")


# usage: testing_full_eval.py path_to_bnet formula
if __name__ == '__main__':
    if len(sys.argv) == 3:
        run_test(sys.argv[1], sys.argv[2])
    else:
        path_to_bnet = "bnet_examples/007.bnet"
        """
        run_test(path_to_bnet, "!{x}: AX {x}")
        run_test(path_to_bnet, "!{x}: AX AF {x}")
        run_test(path_to_bnet, "!{x}: AG EF {x}")
        run_test(path_to_bnet, "!{x}: EG EF {x}")

        run_test(path_to_bnet, "3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})")
        run_test(path_to_bnet, "3{x}: 3{y}: (@{x}: AG~{y} && AG EF {x}) && (@{y}: AG EF {y})")
        """

        run_test(path_to_bnet, "3{x}: 3{y}: (@{x}: AG~{y} && AG EF {x}) && (@{y}: AG EF {y})")
