import os
# Change the current working directory
os.chdir('/mnt/c/Users/Ondra/PycharmProjects/HCTL_stuff/')

from src.parse_all import parse_all
from src.Parsing_HCTL_formula.evaluator_hctl import parse_and_eval
from src.implementation import print_results
import time


def run_tests():
    times = []
    for formula in ["!{x}: (AF {x})", "!{x}: (AX {x})", "!{x}: (AG EF {x})", "!{x}: (EG EF {x})"]:
        start = time.time()
        res = parse_and_eval(formula, m)
        end = time.time()
        times.append(end - start)
        print_results(res, m, f"model: {m.name}, formula: {f}", True)
        print()
    print("times: ", times, '\n')


if __name__ == '__main__':
    # TODO: change path
    bnet_path = "bnet_examples/064_free.bnet"
    # placeholder formula to check the vars
    f = "!{x}: (AG EF {x})"
    m = parse_all(bnet_path, f)
    run_tests()
