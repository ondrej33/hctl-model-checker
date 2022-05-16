"""Preparing the working directory and settings."""
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


def print_error_usage(error_message: str) -> None:
    print(error_message)
    print("Usage: model_check.py model_file formula [-p]")


def valid_file(file_name: str) -> bool:
    return Path(file_name).exists() and Path(file_name).is_file()


def main(file_name: str, formula: str, print_all: bool) -> None:
    """Manage the whole model checking process (parsing, evaluating, printing).

    A body wrapping the whole parsing and model checking process wih simple
    error handling.

    Args:
        file_name: A path to a file with BN model
        formula: A string with valid HCTL formula
        print_all: If True, all satisfying assignments are attempted to print
    """
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
        print_results(res, model, f"model: {model.name}, formula: {formula}", show_all=print_all)
        print(res_time)
        print()
    except Exception as e:
        print("Error during summarizing happened:", str(e))
        return


if __name__ == '__main__':
    if 3 <= len(sys.argv) < 5:
        if valid_file(sys.argv[1]):
            if len(sys.argv) == 3:
                main(sys.argv[1], sys.argv[2], print_all=False)
            elif sys.argv[3] == "-p":
                main(sys.argv[1], sys.argv[2], print_all=True)
            else:
                print_error_usage(f"Invalid argument {sys.argv[3]}.")
        else:
            print_error_usage(f"File {sys.argv[1]} does not exist.")
    else:
        print_error_usage("Wrong number of arguments.")