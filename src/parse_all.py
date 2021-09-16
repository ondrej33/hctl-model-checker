from src.model import *
from src.Parsing_HCTL_formula import parser_hctl
from src.Parsing_update_fns import parser_update_fn
from src.Parsing_update_fns import evaluator_update_fn
from src.abstract_syntax_tree import *
from collections import OrderedDict


# this collects names of all variables from HCTL formula's AST into param variables
# and all propositions into param props
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


# this collects names of all propositions and params in update function's AST into param props
def get_names_from_update_fn_ast(node, props_and_params):
    if type(node) == TerminalNode:
        # DO not add any of true/false nodes, only proposition (param) nodes
        if node.value in {"True", "true", "False", "false", "ff", "tt"}:
            return
        else:
            props_and_params.add(node.value)
    elif type(node) == UnaryNode:
        get_names_from_update_fn_ast(node.child, props_and_params)
    elif type(node) == BinaryNode:
        get_names_from_update_fn_ast(node.left, props_and_params)
        get_names_from_update_fn_ast(node.right, props_and_params)


# this renames all terminal nodes in update function AST
def rename_terminals_update_fn_ast(node, rename_dict):
    if type(node) == TerminalNode:
        # DO not rename any of true/false nodes, only proposition (param) nodes
        if node.value in {"True", "true", "False", "false", "ff", "tt"}:
            return
        else:
            node.value = rename_dict[node.value]
            node.subform_string = node.value
    elif type(node) == UnaryNode:
        rename_terminals_update_fn_ast(node.child, rename_dict)
        node.subform_string = "(" + node.value + node.child.subform_string + ")"
    elif type(node) == BinaryNode:
        rename_terminals_update_fn_ast(node.left, rename_dict)
        rename_terminals_update_fn_ast(node.right, rename_dict)
        node.subform_string = "(" + node.left.subform_string + node.value + node.right.subform_string + ")"


# this renames all terminal nodes in HCTL formula
def rename_terminals_hctl_ast(node, rename_dict):
    if type(node) == TerminalNode:
        # DO not add any of true/false nodes, only proposition nodes
        if node.value in {"True", "true", "False", "false", "ff", "tt"}:
            return
        elif '{' in node.value:
            node.value = '{' + rename_dict[node.value[1:-1]] + '}'
            node.subform_string = node.value
        else:
            node.value = rename_dict[node.value]
            node.subform_string = node.value
    elif type(node) == UnaryNode:
        rename_terminals_hctl_ast(node.child, rename_dict)
        node.subform_string = "(" + node.value + node.child.subform_string + ")"
    elif type(node) == BinaryNode:
        rename_terminals_hctl_ast(node.left, rename_dict)
        rename_terminals_hctl_ast(node.right, rename_dict)
        node.subform_string = "(" + node.left.subform_string + node.value + node.right.subform_string + ")"
    elif type(node) == HybridNode:
        rename_terminals_hctl_ast(node.child, rename_dict)
        node.subform_string = "(" + node.value + node.var + ":" + node.child.subform_string + ")"


def parse_all(file_name: str, formula: str):
    # TODO: GO THROUGH THE TREES ONLY ONCE (collect terminal names while building the trees, later just rename them)
    
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

    # collect VARIABLE names (from free vars) + prop names from parse tree of a HCTL formula
    # TODO: check that binders and free variables correspond to each other
    as_tree_hctl = parser_hctl.parse_to_tree(formula)
    var_names_set = set()
    props_in_hctl = set()
    get_names_from_hctl_ast(as_tree_hctl, var_names_set, props_in_hctl)
    var_names = sorted(var_names_set)
    # TODO: check that props_in_hctl correspond with prop_names (that theres nothing wrong in formula)

    # create as_trees for update functions and collect their terminals (props or params)
    update_fn_trees = [parser_update_fn.parse_to_tree(update_str) for update_str in update_fn_strings]
    props_and_params_set = set()
    for as_tree in update_fn_trees:
        get_names_from_update_fn_ast(as_tree, props_and_params_set)

    # from set collected above choose those terminals that are not props -> they are PARAMS
    param_names = sorted(props_and_params_set.difference(prop_names))

    # now we have all building elements, lets create rename dictionary
    name_dict = dict()
    for i in range(len(prop_names)):
        name_dict[prop_names[i]] = f"s__{i}"
    for i in range(len(param_names)):
        name_dict[param_names[i]] = f"p__{i}"
    for i in range(len(var_names)):
        name_dict[var_names[i]] = "x" * (i + 1)

    # rename props/params in update trees, rename props/vars in formula tree
    rename_terminals_hctl_ast(as_tree_hctl, name_dict)
    for as_tree in update_fn_trees:
        rename_terminals_update_fn_ast(as_tree, name_dict)

    # create a BDD
    bdd = BDD()
    vrs = [f"s__{i}" for i in range(len(prop_names))]           # state describing vars
    vrs.extend(f"p__{i}" for i in range(len(param_names)))      # params
    for var_name in var_names:
        vrs.extend(f"{var_name}__{i}" for i in range(len(prop_names)))  # HCTL variables
    bdd.declare(*vrs)

    # reordering to some desired order (now it is s0,x0,y0,s1...,p0,p1...)
    my_order = dict()
    for i in range((len(prop_names))):
        my_order[f"s__{i}"] = i * (len(var_names) + 1)
    for idx, var_name in enumerate(var_names):
        for i in range((len(prop_names))):
            my_order[f"{var_name}__{i}"] = i * (len(var_names) + 1) + idx + 1
    for i in range((len(param_names))):
        my_order[f"p__{i}"] = i + (len(var_names) + 1) * len(prop_names)
    bdd.reorder(my_order)
    # bdd.configure(reordering=False)  # auto reorder disabled (probably)? - it is slower when disabled

    # create bdd functions from update trees via evaluator_update_fn.eval_tree
    list_update_fns = [evaluator_update_fn.eval_tree(as_tree, bdd) for as_tree in update_fn_trees]
    update_dict = OrderedDict()
    for i in range(len(prop_names)):
        update_dict[f"s__{i}"] = list_update_fns[i]

    # pack it all into a whole model and return it
    name_dict_reversed = {y: x for x, y in name_dict.items()}
    model_name = file_name.split("/")[-1]
    model = Model(model_name, bdd, prop_names, param_names, var_names, update_dict, name_dict_reversed)
    return model
