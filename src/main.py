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
os.chdir('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff')

import sys
sys.path.append('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff/')
sys.path.append('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff/src')
sys.path.append('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff/src/Parsing_HCTL_formula')
sys.path.append('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff/src/Parsing_update_fns')

from parse_all import parse_all
from Parsing_HCTL_formula.evaluator_hctl import eval_tree
from implementation import print_results
from exceptions import *


def main(file_name: str, formula: str):

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
    except:
        print("Error during evaluation happened")


# usage: testing_full_eval.py path_to_bnet formula
if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Wrong number of arguments")

