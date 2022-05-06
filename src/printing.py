from src.model import *
from termcolor import colored


"""
This contains all the functions for result printing and necessary functionality
"""


#returns decimal value of binary vector s0,s1,s2...
# is used for sorting assignments
def encode_assignment(assignment, num_props) -> int:
    result_val = 0
    for i in range(num_props):
        result_val += assignment[len(assignment) - 1 - i][1] * 2 ** i
    return result_val


# returns decimal value of binary vector p0,p1,p2... - BUT uses inverted values
# is used for sorting as a addition to previous function
def encode_color(assignment, num_cols) -> float:
    result_val = 0
    for i in range(num_cols):
        result_val += assignment[len(assignment) - 1 - i][1] * (1 / 2 ** i)
    return result_val


# gets rid of all parameters from BDD using projection
# bdd must support only props and params, no state-variables
def get_states_only(phi: Function, model: Model):
    vars_to_get_rid = [f"p__{i}" for i in range(model.num_params)]
    return model.bdd.quantify(phi, vars_to_get_rid)


# using projection gets rid of all propositions from BDD
# bdd must support only props and params, no state-variables
def get_colors_only(phi: Function, model: Model):
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props)]
    return model.bdd.quantify(phi, vars_to_get_rid)


# Print number of computed results in the final BDD (number of state-color pairs),
# and then numbers of colors & states alone
def print_results_fast(result: Function, model: Model, message: str = ""):
    if message:
        print(message)

    assignments = model.bdd.count(result, nvars=model.num_props + model.num_params)
    print(f"{assignments} RESULTS FOUND IN TOTAL")

    result_colors = get_colors_only(result, model)
    assignments = model.bdd.count(result_colors, nvars=model.num_params)
    print(f"{assignments} COLORS FOUND IN TOTAL")

    result_states = get_states_only(result, model)
    assignments = model.bdd.count(result_states, nvars=model.num_props)
    print(f"{assignments} STATES FOUND IN TOTAL")

    print(f"props: {model.num_props}, params: {model.num_params}")


def print_results(result: Function, model: Model, message: str = "", show_all: bool = False) -> None:
    print_results_fast(result, model, message)

    if not show_all:
        return

    """
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)  # assigning a generator again, was depleted
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (x[0][0], len(x[0]), x[0])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (encode_assignment(x, model.num_props) + encode_color(x, model.num_params)))

    # we will print params first, then proposition values
    for assignment in assignments_sorted:
        # we will print only 0/1 instead True/False
        transformed_params = [int(item[1]) for item in assignment[0:model.num_params]]
        print(transformed_params, end="  ")
        transformed_props = [int(item[1]) for item in assignment[len(assignment) - model.num_props:]]
        print(transformed_props)
    print()
    """

    # -----------------------------------------------------------------------------------

    # printing all variables in alphabetical order, colored, like in AEON
    """
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)  # assigning a generator again, was depleted
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (model.name_dict[x[0]])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (encode_assignment(x, model.num_props + model.num_params)))

    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)
    for assignment in assignments_sorted:
        # we will print only 0/1 instead True/False
        transformed = [(model.name_dict[item[0]], int(item[1])) for item in assignment]
        for var, val in transformed:
            text = ""
            if val == 0:
                text = colored('!' + var, 'red')
            else:
                text = colored(var, "green")
            print(text, end=" ")
        print()
    print()
    """

    assignments = model.bdd.pick_iter(result)
    print(f"{len(list(assignments))} RESULTS FOUND IN TOTAL")

    assignments = model.bdd.pick_iter(result)
    sorted_inside = [sorted(assignment.items(), key=lambda x: x[0]) for assignment in assignments]

    for assignment in sorted_inside:
        # we will print only 0/1 instead True/False
        transformed = [(item[0], int(item[1])) for item in assignment]
        for var, val in transformed:
            text = ""
            if val == 0:
                text = colored('!' + var, 'red')
            else:
                text = colored(var, "green")
            print(text, end=" ")
        print()
    print()


