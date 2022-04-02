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


# computes the set of successors for the given set
# by applying the update function of the given `var`
# SHOULD BE USED ONLY BY FUNCTIONS IN THIS FILE
# TODO: test if right
def post_E_one_var(model: Model, given_set: Function, var: str) -> Function:
    """
    GO_DOWN = !X & Exists((SET & X & !B_X), 'X')
    GO_UP = X & Exists((SET & !X & B_X), 'X')
    """

    var_bdd = labeled_by(model, var)
    go_down = ~var_bdd & model.bdd.quantify(given_set & var_bdd & ~model.update_fns[var], [var])
    go_up = var_bdd & model.bdd.quantify(given_set & ~var_bdd & model.update_fns[var], [var])
    return go_down | go_up


# computes the set of successors for the given set
# by applying ALL of the update functions
def post_E_all_vars(model: Model, given_set: Function) -> Function:
    current_set = model.bdd.add_expr("False")
    for i in range(model.num_props):
        current_set = current_set | post_E_one_var(model, given_set, f"s__{i}")

    # TODO: add same thing as for pre_E_all_vars - create self loops - this helps for "bind x: EY x"
    # TODO: problem with self-loops might arrise again, but this time in sources - we have reversed graph
    return current_set


def EY(model: Model, phi: Function) -> Function:
    return post_E_all_vars(model, phi)


# computed through pure EY
# TODO: check if this is right
def AY(model: Model, phi: Function) -> Function:
    return ~EY(model, ~phi)


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
    assignments_sorted = sorted(
        sorted_inside,
        key=lambda x: (encode_assignment(x, model.num_props) + encode_color(x, model.num_params))
    )

    # we will print params first, then proposition values
    for assignment in assignments_sorted:
        # we will print only 0/1 instead True/False
        transformed_params = [int(item[1]) for item in assignment[0:model.num_params]]
        print(transformed_params, end="  ")
        transformed_props = [int(item[1]) for item in assignment[len(assignment) - model.num_props:]]
        print(transformed_props)


"""
this is an OBSOLETE function, use parse_all() instead
parses a file with a boolean network, creates model from it - BUT STATE VARIABLES ARE ADDED MANUALLY atm
only testing version, can break quickly...
USES SPECIAL TYPE OF BNET FORMAT:
    all lines except first one are in the form: "variable_name, update_fn"
    BUT to handle params, we MUST add lines in form: "param_name," (there is no update fn) - those will be params
"""
def bnet_parser(file_name: str) -> Model:
    # first preprocess the file content
    file = open(file_name, "r")
    content = file.read()

    lines = content.split("\n")[1:]           # first line does not contain data
    lines = [line for line in lines if line]  # remove empty lines
    lines_ordered = sorted(lines, key=lambda x: x.split(",")[0])

    # collect all the variable names and their update functions and reorder them
    # order will be alphabetical, uppercase first, lowercase later (like ASCII)
    update_dict = OrderedDict()
    prop_names = []
    param_names = []
    for line in lines_ordered:
        var_func_pair = line.split(",")
        if var_func_pair[1]:  # if this is not empty, we have var and its update fn
            prop_names.append(var_func_pair[0])
            update_dict[var_func_pair[0]] = var_func_pair[1]
        else:  # otherwise we have parameter with no update fn
            param_names.append(var_func_pair[0])
    num_props = len(prop_names)
    num_params = len(param_names)

    # rename props/params in update functions, as we will be using only the short versions (s0,s1... or p0...)
    # we will start renaming the longest ones, so that we dont overwrite them with some substring
    name_dict = dict()
    for i in range(num_props):
        name_dict[prop_names[i]] = f"s__{i}"
    for i in range(num_params):
        name_dict[param_names[i]] = f"p__{i}"
    for prop in prop_names:
        for p in sorted((prop_names+param_names), key=lambda x: len(x), reverse=True):
            update_dict[prop] = update_dict[prop].replace(p, name_dict[p])

    # define a BDD vars will be named s0,s1... and we will store full names elsewhere, also add 2 HCTL vars
    bdd = BDD()
    vrs = [f"s__{i}" for i in range(num_props)]       # state describing vars
    vrs.extend(f"p__{i}" for i in range(num_params))  # params
    vrs.extend(f"x__{i}" for i in range(num_props))   # state-variable x (for HCTL MC)
    vrs.extend(f"y__{i}" for i in range(num_props))   # state-variable y (for HCTL MC)
    vrs.extend(f"z__{i}" for i in range(num_props))   # state-variable z (for HCTL MC)
    bdd.declare(*vrs)

    # reordering to some desired order (now it is s0,x0,y0,z0,s1,x1...,p0,p1...)
    my_order = dict()
    for i in range(num_props):
        my_order[f"s__{i}"] = i * 4
        my_order[f"x__{i}"] = i * 4 + 1
        my_order[f"y__{i}"] = i * 4 + 2
        my_order[f"z__{i}"] = i * 4 + 3
    for i in range(num_params):
        my_order[f"p__{i}"] = i + 4 * num_props
    bdd.reorder(my_order)
    # bdd.configure(reordering=False)  # auto reorder disabled (probably)? - it is slower when disabled

    # go through update function strings one by one and create dict of BDDs (update functions) from them
    list_update_fns = [bdd.add_expr(update_dict[prop]) for prop in update_dict]
    real_update_dict = OrderedDict()
    for i in range(num_props):
        real_update_dict[f"s__{i}"] = list_update_fns[i]

    update_dict_renamed = OrderedDict()
    for i in range(num_props):
        update_dict_renamed[f"s__{i}"] = update_dict[prop_names[i]]

    # pack it all into a whole model and return it
    name_dict_reversed = {y: x for x, y in name_dict.items()}
    model_name = file_name.split("\\")[-1]
    model = Model(model_name, bdd, prop_names, param_names, ['x', 'y', 'z'], real_update_dict, name_dict_reversed)
    return model
