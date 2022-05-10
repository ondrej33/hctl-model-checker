from src.model import *
from termcolor import colored


"""
File containing functionality for result printing and aggregation.
"""


def encode_assignment_props(assignment, num_props) -> int:
    """
    Return decimal value representing the binary assignment to propositions.
    This is used for sorting resulting assignments
    """
    result_val = 0
    for i in range(num_props):
        result_val += assignment[len(assignment) - 1 - i][1] * 2 ** i
    return result_val


def encode_color(assignment, num_cols) -> float:
    """
    Return inverted decimal value representing the color (assignment to parameters)
    This is used (as secondary criteria) for sorting resulting assignments
    """
    result_val = 0
    for i in range(num_cols):
        result_val += assignment[len(assignment) - 1 - i][1] * (1 / 2 ** i)
    return result_val


def get_states_only(phi: Function, model: Model):
    """Get rid of all parameters from the BDD instance using projection.

    Args:
        phi: bdd-encoded set of colored-states - bdd instance must not depend on state-vars
        model: model object
    """
    vars_to_get_rid = [f"p__{i}" for i in range(model.num_params())]
    return model.bdd.quantify(phi, vars_to_get_rid)


def get_colors_only(phi: Function, model: Model):
    """Get rid of all propositions from the BDD instance using projection.

    Args:
        phi: bdd-encoded set of colored-states - bdd instance must not depend on state-vars
        model: model object
    """
    vars_to_get_rid = [f"s__{i}" for i in range(model.num_props())]
    return model.bdd.quantify(phi, vars_to_get_rid)


def print_results_fast(result: Function, model: Model, message: str = ""):
    """
    Print number of computed BDD-encoded results (number of state-color pairs),
    and also information about colors / states alone
    """
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


def print_colored_assignments(model, assignments):
    """Print all given assignments, color propositions based on values."""
    print("Satisfying colored states:")
    for assignment in assignments:
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


def print_results(result: Function, model: Model, message: str = "", show_all=False) -> None:
    """
    Print results, either in short (aggregated) form or long full form.
    Short form includes just the basic statistics (number of results etc.).
    Long form includes detailed listing of all results (might be infeasible).
    """
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
    assignments_sorted = sorted(sorted_inside, key=lambda x: (
        encode_assignment_props(x, model.num_props() + model.num_params())
    ))

    print_colored_assignments(model, assignments_sorted)