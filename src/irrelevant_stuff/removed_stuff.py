from src.implementation import *


# computes the set of states which can make transition ONLY into the initial set and nowhere else
# applying the update function of the given `var`
# SHOULD BE USED ONLY BY FUNCTIONS IN THIS FILE
def pre_A_one_var(model: Model, initial: Function, var: str) -> Function:
    return ~pre_E_one_var(model, ~initial, var)


# computes the set of states which can make transition ONLY into the initial set and nowhere else
# applying ALL of the update functions
def pre_A_all_vars(model: Model, initial: Function) -> Function:
    current_set = model.bdd.add_expr("True")
    for i in range(model.num_props):
        current_set = current_set & pre_A_one_var(model, initial, f"s__{i}")

    # TODO: add same thing as for pre_E_all_vars - create explicit self loops
    return current_set


# AX computed through small update BDDs using pre_A_all_vars
def AX_v2(model: Model, phi: Function) -> Function:
    return pre_A_all_vars(model, phi)


# fixpoint version of AF
def AF_v2(model: Model, phi: Function) -> Function:
    # lfpZ. ( phi OR AX Z )
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = model.bdd.apply("or", new, AX(model, old))
    return old


# fixpoint version of AG
def AG_v2(model: Model, phi: Function) -> Function:
    old = phi
    new = model.bdd.add_expr("False")
    while old != new:
        new = old
        old = old & AX(model, old)
    return old


# binder AX, binder pushed inside:   ↓x. (AX SET1)
def optimized_binder_AX(model: Model, set1: Function) -> Function:
    current_set = model.bdd.add_expr("True")
    comparator = create_comparator(model, 'x')
    vars_to_get_rid = [f"x__{i}" for i in range(model.num_props)]

    for i in range(model.num_props):
        intersection = comparator & pre_A_one_var(model, set1, f"s__{i}")
        current_set = current_set & model.bdd.quantify(intersection, vars_to_get_rid)

    # TODO: add same thing as for pre_E_all_vars - create explicit self loops
    return current_set


# for testing purposes
def bdd_dumper(file_name: str):
    # formula here is just a placeholder to save var names
    model, _ = parse_all(file_name, "AX {x}")

    result = AX(model, create_comparator(model, 'x'))

    var_order = {}
    for i in range(model.num_props):
        var_order[f"s__{i}"] = i
        var_order[f"x__{i}"] = i + 1

    vars_to_show = [f"s__{i}" for i in range(model.num_props)]+[f"x__{i}" for i in range(model.num_props)]
    assignments = model.bdd.pick_iter(result, care_vars=vars_to_show)  # assigning a generator again, was depleted
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (x[0][0], len(x[0]), x[0])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (eval_assignment(x, model.num_props) + eval_color(x, model.num_params)))

    # we will print params first, then proposition values
    for assignment in assignments_sorted:
        # we will print only 0/1 instead True/False
        transformed_params = [int(item[1]) for item in assignment[0:model.num_params]]
        print(transformed_params, end="  ")
        transformed_props = [int(item[1]) for item in assignment[len(assignment) - model.num_props:]]
        print(transformed_props)
