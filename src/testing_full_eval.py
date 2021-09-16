"""
import os
# Change the current working directory
os.chdir('~/HCTL_stuff')

import sys
sys.path.append('~/HCTL_stuff/src')
sys.path.append('~/HCTL_stuff/src/Parsing_HCTL_formula')
sys.path.append('~/HCTL_stuff/src/Parsing_update_fns')
"""

import os
# Change the current working directory
os.chdir('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff')

import sys
sys.path.append('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff/src')
sys.path.append('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff/src/Parsing_HCTL_formula')
sys.path.append('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff/src/Parsing_update_fns')


from parse_all import parse_all
from Parsing_HCTL_formula.evaluator_hctl import eval_tree
from implementation import print_results
import time


def run_tests(file_name):
    times = []
    for formula in ["!{x}: (AF {x})", "!{x}: (AX {x})", "!{x}: (AG EF {x})", "!{x}: (EG EF {x})"]:
        model, as_tree_hctl = parse_all(file_name, formula)
        start = time.time()
        res = eval_tree(as_tree_hctl, model)
        end = time.time()
        times.append(end - start)
        print_results(res, model, f"model: {model.name}, formula: {formula}", False)
        print()
    print("times: ", times, '\n')


if __name__ == '__main__':
    # TODO: change path
    bnet_path = "bnet_examples/064_free.bnet"
    run_tests(bnet_path)
