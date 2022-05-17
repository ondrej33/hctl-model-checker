"""Preparing the working directory and settings"""
import os
# Change the current working directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(SRC_DIR))
os.chdir(PROJECT_DIR)

import sys
sys.path.append(PROJECT_DIR)

from src.evaluator_hctl import eval_tree
from src.parse_all import parse_all

def run_attractor_tests():
    """
    Evaluate formula for attractors on several models, and compare the numbers
    of results found against the pre-computed ones.
    """
    model1 = "benchmark_models/model_collection_large/[var-10]__[id-084]__[BOOLEAN-CELL-CYCLE]/model_inputs_free.bnet"
    model2 = "benchmark_models/model_collection_large/[var-11]__[id-029]__[TOLL-PATHWAY-OF-DROSOPHILA]/model_inputs_free.bnet"
    model3 = "benchmark_models/model_collection_large/[var-15]__[id-010]__[CARDIAC-DEVELOPMENT]/model_inputs_free.bnet"
    model4 = "benchmark_models/model_collection_large/[var-17]__[id-089]__[MAPK-REDUCED-1]/model_inputs_free.bnet"
    model5 = "benchmark_models/model_collection_large/[var-20]__[id-024]__[BUDDING-YEAST-CELL-CYCLE]/model_inputs_free.bnet"
    model6 = "benchmark_models/model_collection_large/[var-20]__[id-003]__[MAMMALIAN-CELL-CYCLE]/model_inputs_free.bnet"
    models = [model1, model2, model3, model4, model5, model6]

    numbers_states1 = 113
    numbers_states2 = 4
    numbers_states3 = 6
    numbers_states4 = 3607
    numbers_states5 = 27668
    numbers_states6 = 3
    numbers_states = [numbers_states1, numbers_states2, numbers_states3,
                      numbers_states4, numbers_states5, numbers_states6]

    for model_num in range(len(models)):
        model, as_tree_hctl = parse_all(models[model_num], "!{x}: AG EF {x}")
        res = eval_tree(as_tree_hctl, model)
        states_num = model.bdd.count(res, nvars=model.num_props() + model.num_params())
        assert states_num == numbers_states[model_num]
        print(f"Test for model {model_num + 1} successful")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Running the attractor tests.")
        run_attractor_tests()
    else:
        print("Script does not take any arguments.")
        print("Usage: test_attractors.py")
