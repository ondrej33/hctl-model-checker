from src.model import *
from termcolor import colored


"""
This contains all the functions for result printing and necessary functionality
"""


# Return decimal value of binary vector s0,s1,s2...
# this is used for sorting resulting assignments
def encode_assignment(assignment, num_props) -> int:
    result_val = 0
    for i in range(num_props):
        result_val += assignment[len(assignment) - 1 - i][1] * 2 ** i
    return result_val


# Return decimal value of binary vector p0,p1,p2... - BUT uses inverted values
# this is used for result sorting as a addition to previous function
def encode_color(assignment, num_cols) -> float:
    result_val = 0
    for i in range(num_cols):
        result_val += assignment[len(assignment) - 1 - i][1] * (1 / 2 ** i)
    return result_val


# Get rid of all parameters from the BDD instance using projection
# bdd must support only props and params, no state-variables
def get_states_only(phi: Function, model: Model):
    vars_to_get_rid = [f"p__{i}" for i in range(model.num_params())]
    return model.bdd.quantify(phi, vars_to_get_rid)


# Get rid of all propositions from the BDD instance using projection
# BDD must support only props and params, no state-variables
def get_colors_only(phi: Function, model: Model):
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props())]
    return model.bdd.quantify(phi, vars_to_get_rid)


# Print number of computed results in the final BDD (number of state-color pairs),
# and then numbers of colors & states alone
def print_results_fast(result: Function, model: Model, message: str = ""):
    if message:
        print(message)

    assignments = model.bdd.count(result, nvars=model.num_props() + model.num_params())
    print(f"{assignments} RESULTS FOUND IN TOTAL")

    result_colors = get_colors_only(result, model)
    assignments = model.bdd.count(result_colors, nvars=model.num_params())
    print(f"{assignments} COLORS FOUND IN TOTAL")

    result_states = get_states_only(result, model)
    assignments = model.bdd.count(result_states, nvars=model.num_props())
    print(f"{assignments} STATES FOUND IN TOTAL")

    print(f"props: {model.num_props()}, params: {model.num_params()}")


# Print results, either in short or long form
# Short form includes just the basic statistics (number of results etc.)
# Long form includes detailed listing of all results (might be infeasible)
def print_results(result: Function, model: Model, message: str = "", show_all: bool = False) -> None:
    print_results_fast(result, model, message)

    if not show_all:
        return

    # now print ordered resulting assignments
    # for each resulting assignment, prints its propositions+parameters, in alphabetical order, colored
    # propositions assigned 0 are colored red, props assigned 1 assigned green

    vars_to_show = [f"s__{i}" for i in range(model.num_props())] + [f"p__{i}" for i in range(model.num_params())]
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)
    # sorting vars in individual items
    sorted_inside = [sorted(assignment.items(), key=lambda x: (model.name_dict[x[0]])) for assignment in assignments]
    # now sorting the whole items by the binary encoding of given states, parameters
    assignments_sorted = sorted(sorted_inside, key=lambda x: (encode_assignment(x, model.num_props() + model.num_params())))

    print("Satisfying colored states:")
    for assignment in assignments_sorted:
        # assign correct names to the propositions and parameters
        transformed = [(model.name_dict[item[0]], int(item[1])) for item in assignment]
        for var, val in transformed:
            if val == 0:
                text = colored('!' + var, 'red')
            else:
                text = colored(var, "green")
            print(text, end=" ")
        print()
    print()
