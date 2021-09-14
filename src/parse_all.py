from model import *
from src.Parsing_HCTL_formula import parser_hctl
from src.Parsing_update_fns import parser_update_fn
from abstract_syntax_tree import *


def get_names_from_hctl_ast(node, variables, props):
    if type(node) == TerminalNode:
        # DO not add any of true/false nodes, only proposition nodes
        if node.value in {"True", "true", "False", "false", "ff", "tt"}:
            return
        elif '{' in node.value:
            variables.add(node.value[1:-1])
        else:
            props.add(node.value)
    elif type(node) == UnaryNode or type(node) == HybridNode:
        get_names_from_hctl_ast(node.child, variables, props)
    elif type(node) == BinaryNode:
        get_names_from_hctl_ast(node.left, variables, props)
        get_names_from_hctl_ast(node.right, variables, props)


def parse_all(file_name: str, formula: str):
    # first preprocess the file content
    file = open(file_name, "r")
    content = file.read()
    # TODO: maybe clean the content (no need atm, because test examples are clean)

    lines = content.split("\n")[1:]  # first line does not contain data
    if not lines[-1]:
        lines.pop()  # last item might be just empty string after last newline
    lines_ordered = sorted(lines, key=lambda x: x.split(",")[0])

    # collect all the variable names and their update functions from bnet file
    prop_names = [line.split(",")[0] for line in lines_ordered]
    update_fn_strings = [line.split(",")[1] for line in lines_ordered]
    num_props = len(prop_names)

    # collect VARIABLE names (from free vars) + prop names from parse tree of a HCTL formula
    # TODO: check that binders and free variables correspond to each other
    as_tree_hctl = parser_hctl.parse_to_tree(formula)
    var_names_set = set()
    props_in_hctl = set()
    get_names_from_hctl_ast(as_tree_hctl, var_names_set, props_in_hctl)
    var_names = sorted(var_names_set)
    # TODO: check that props_in_hctl correspond with prop_names (nothing wrong in formula)

    # create as_trees for update functions and collect their terminals (props or params)
    update_fn_trees = [parser_update_fn.parse_to_tree(update_str) for update_str in update_fn_strings]
    for as_tree in update_fn_trees:
        # TODO: collect all terminals
        pass
    # TODO: choose those terminals that are not props -> params

    # TODO: create rename dictionaries

    # TODO: rename props/params in update trees, rename props/vars in formula tree

    # TODO: create a BDD

    # TODO: create bdd functions from update trees via evaluator_update_fn.eval_tree

    # TODO: create a model and return it

    # TODO: use evaluator_hctl.eval_tree in some OTHER FILE





    """
    # rename props/params in update functions, as we will be using only the short versions (s0,s1... or p0...)
    # we will start renaming the longest ones, so that we dont overwrite them with some substring
    name_dict = dict()
    for i in range(num_props):
        name_dict[prop_names[i]] = f"s__{i}"
    for i in range(num_params):
        name_dict[param_names[i]] = f"p__{i}"
    for prop in prop_names:
        for p in sorted((prop_names + param_names), key=lambda x: len(x), reverse=True):
            update_dict[prop] = update_dict[prop].replace(p, name_dict[p])

    # define a BDD vars will be named s0,s1... and we will store full names elsewhere, also add 2 HCTL vars
    bdd = BDD()
    vrs = [f"s__{i}" for i in range(num_props)]  # state describing vars
    vrs.extend(f"p__{i}" for i in range(num_params))  # params
    vrs.extend(f"x__{i}" for i in range(num_props))  # state-variable x (for HCTL MC)
    vrs.extend(f"y__{i}" for i in range(num_props))  # state-variable y (for HCTL MC)
    bdd.declare(*vrs)

    # reordering to some desired order (now it is s0,x0,y0,s1...,p0,p1...)
    # TODO: try different orders
    my_order = dict()
    for i in range(num_props):
        my_order[f"s__{i}"] = i * 3
        my_order[f"x__{i}"] = i * 3 + 1
        my_order[f"y__{i}"] = i * 3 + 2
    for i in range(num_params):
        my_order[f"p__{i}"] = i + 3 * num_props
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
    model = Model(model_name, bdd, num_props, prop_names, num_params, param_names, real_update_dict,
                  update_dict_renamed, name_dict_reversed)
    return model
    """
