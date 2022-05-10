"""Preparing the working directory and settings"""
import os
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_DIR)
os.chdir(PROJECT_DIR)

import sys
sys.path.append(PROJECT_DIR)

from pathlib import Path
from time import time

from src.evaluator_hctl import eval_tree
from src.exceptions import *
from src.printing import print_results
from src.parse_all import parse_all


def main(file_name: str, formula: str):
    """Manage the whole model checking process (parsing, evaluating, printing)"""
    try:
        start = time()
        model, as_tree_hctl = parse_all(file_name, formula)
    except InvalidPropError as e:
        print("Formula includes non existing proposition:", e.bad_prop)
        return
    except InvalidUpdateFnOperationError as e:
        print("Invalid operation found in update function:", e.invalid_op)
        return
    except Exception as e:
        print("Error during parsing happened:\n", str(e))
        return

    try:
        res = eval_tree(as_tree_hctl, model)
        end = time()
        res_time = end - start
    except Exception as e:
        print("Error during evaluation happened:\n", str(e))
        return

    try:
        print_results(res, model, f"model: {model.name}, formula: {formula}", show_all=False)
        print(res_time)
        print()
    except Exception as e:
        print("Error during summarizing happened:", str(e))
        return


if __name__ == '__main__':
    if len(sys.argv) == 3:
        if Path(sys.argv[1]).exists() and Path(sys.argv[1]).is_file():
            main(sys.argv[1], sys.argv[2])
        else:
            print(f"File {sys.argv[1]} does not exist")
            print("Usage: model_check.py path_to_bnet formula")
    else:
        print("Wrong number of arguments")
        print("Usage: model_check.py path_to_bnet formula")
