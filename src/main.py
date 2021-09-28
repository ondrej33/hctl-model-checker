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

from parse_all import parse_all
from Parsing_HCTL_formula.evaluator_hctl import eval_tree
from implementation import print_results
from exceptions import *


def main(file_name: str, formula: str):
    # TODO: create some main body around the implementation
    # TODO: make this something different than just copy of testing_full_eval
    try:
        model, as_tree_hctl = parse_all(file_name, formula)
    except InvalidPropError as e:
        print("Formula includes non existing proposition:", e.bad_prop)
        return
    except Exception:
        print("Error during parsing happened")
        return

    try:
        res = eval_tree(as_tree_hctl, model)
        print_results(res, model, f"model: {model.name}, formula: {formula}", show_all=False)
    except Exception:
        print("Error during evaluation happened")


# usage: testing_full_eval.py path_to_bnet formula
if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Wrong number of arguments")

