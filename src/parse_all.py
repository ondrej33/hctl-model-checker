from src.model import *
from src.Parsing_HCTL_formula import parser_hctl
from src.Parsing_update_fns import parser_update_fn
from src.Parsing_update_fns import evaluator_update_fn
from src.abstract_syntax_tree import *
from src.exceptions import *

from collections import OrderedDict
from typing import Set, Dict, Tuple


# this collects names of all variables from HCTL formula's AST into param variables
# and all propositions into param props
def get_prop_names_from_hctl_ast(node, props_collected: Set[str]) -> None:
    if type(node) == TerminalNode:
        # DO not add any of true/false or vars, only proposition nodes
        if node.value == "True" or node.value == "False" or "{" in node.value:
            return
        props_collected.add(node.value)
    elif type(node) == UnaryNode or type(node) == HybridNode:
        get_prop_names_from_hctl_ast(node.child, props_collected)
    elif type(node) == BinaryNode:
        get_prop_names_from_hctl_ast(node.left, props_collected)
        get_prop_names_from_hctl_ast(node.right, props_collected)


# this collects names of all propositions and params in update function's AST into param props
def get_names_from_update_fn_ast(node, props_and_params: Set[str]) -> None:
    if type(node) == TerminalNode:
        # DO not add any of true/false nodes, only proposition (param) nodes
        if node.value == "True" or node.value == "False":
            return
        props_and_params.add(node.value)
    elif type(node) == UnaryNode:
        get_names_from_update_fn_ast(node.child, props_and_params)
    elif type(node) == BinaryNode:
        get_names_from_update_fn_ast(node.left, props_and_params)
        get_names_from_update_fn_ast(node.right, props_and_params)


# this renames all terminal nodes in update function AST
def rename_terminals_update_fn_ast(node, rename_dict: Dict[str, str]) -> None:
    if type(node) == TerminalNode:
        # rename proposition (param) nodes
        if node.value == "True" or node.value == "False":
            return
        node.value = rename_dict[node.value]
        node.subform_string = node.value
    elif type(node) == UnaryNode:
        rename_terminals_update_fn_ast(node.child, rename_dict)
        node.subform_string = "(" + node.value + node.child.subform_string + ")"
    elif type(node) == BinaryNode:
        rename_terminals_update_fn_ast(node.left, rename_dict)
        rename_terminals_update_fn_ast(node.right, rename_dict)
        node.subform_string = "(" + node.left.subform_string + node.value + node.right.subform_string + ")"


# this renames all propositions in terminal nodes in HCTL formula (does not touch vars)
def rename_propositions_in_hctl_ast(node, rename_dict: Dict[str, str]) -> None:
    if type(node) == TerminalNode:
        # DO NOT rename state-variable nodes, ONLY proposition nodes (and unify true/false)
        if '{' in node.value or node.value == "True" or node.value == "False":
            return
        node.value = rename_dict[node.value]
        node.subform_string = node.value
    elif type(node) == UnaryNode:
        rename_propositions_in_hctl_ast(node.child, rename_dict)
        node.subform_string = "(" + node.value + node.child.subform_string + ")"
    elif type(node) == BinaryNode:
        rename_propositions_in_hctl_ast(node.left, rename_dict)
        rename_propositions_in_hctl_ast(node.right, rename_dict)
        node.subform_string = "(" + node.left.subform_string + node.value + node.right.subform_string + ")"
    elif type(node) == HybridNode:
        # first rename the "var" field of the node, then move to child
        rename_propositions_in_hctl_ast(node.child, rename_dict)
        node.subform_string = "(" + node.value + node.var + ":" + node.child.subform_string + ")"


# renames as many state-variables as possible to the identical names, without changing the formula
# its like canonicalization, we will end up with less vars in total
def make_state_vars_canonical_ast(node, rename_dict: Dict[str, str], last_used_name: str, num_vars=0):
    """
    # if we find hybrid node with bind or exist, we add new var-name to rename_dict and stack (x, xx, xxx...)
    # we derive the name using the last thing on stack
    # after we leave this binder/exist, we remove its var from rename_dict and stack
    # dont forget to rename var field in hybrid node

    # when we find terminal with free variable, we rename it using rename-dict, we do the same when we encounter jump

    # possible problem: we want to rename var to "x", but "x" is already somewhere in subformula -> is it ok?
    """

    if type(node) == TerminalNode:
        # DO NOT change names of any true/false or proposition nodes, only state-variables
        if '{' not in node.value:
            return
        node.value = '{' + rename_dict[node.value[1:-1]] + '}'
        node.subform_string = node.value
    elif type(node) == UnaryNode:
        # just dive deeper and then rename string
        num_vars = make_state_vars_canonical_ast(node.child, rename_dict, last_used_name, num_vars)
        node.subform_string = "(" + node.value + node.child.subform_string + ")"
    elif type(node) == BinaryNode:
        # just dive deeper and then rename string
        num_vars1 = make_state_vars_canonical_ast(node.left, rename_dict, last_used_name, num_vars)
        num_vars2 = make_state_vars_canonical_ast(node.right, rename_dict, last_used_name, num_vars)
        num_vars = max(num_vars1, num_vars2)
        node.subform_string = "(" + node.left.subform_string + node.value + node.right.subform_string + ")"
    elif type(node) == HybridNode:
        # if we hit binder or exist, we are adding its new var name to dict & stack
        if node.value == "!" or node.value == "3":
            last_used_name = last_used_name + 'x'
            rename_dict[node.var[1:-1]] = last_used_name
            num_vars = max(num_vars, len(last_used_name))

        # we rename the var in node (if we hit jump the name should be in dict already)
        var_before = node.var[1:-1]
        node.var = '{' + rename_dict[node.var[1:-1]] + '}'
        # and we dive deeper in the tree
        num_vars = make_state_vars_canonical_ast(node.child, rename_dict, last_used_name, num_vars)
        node.subform_string = "(" + node.value + node.var + ":" + node.child.subform_string + ")"

        # and at last, when we leave binder/exist, we delete the added var from dict and stack
        if node.value == "!" or node.value == "3":
            # last_used_name = last_used_name[0:-1]
            rename_dict.pop(var_before)
    return num_vars


def parse_all(file_name: str, formula: str) -> Tuple[Model, Node]:
    # TODO: GO THROUGH THE TREES ONLY ONCE (collect terminal names while building the trees, later just rename them)
    
    # first preprocess the file content
    file = open(file_name, "r")
    content = file.read()
    # TODO: maybe clean the content (no need atm, because test examples are clean)

    lines = content.split("\n")[1:]           # first line does not contain data
    lines = [line for line in lines if line]  # remove empty lines
    lines_ordered = sorted(lines, key=lambda x: x.split(",")[0])

    # collect all the variable names and their update functions from bnet file
    prop_names = [line.split(",")[0] for line in lines_ordered]
    update_fn_strings = [line.split(",")[1] for line in lines_ordered]

    # collect prop names from parse tree of a HCTL formula
    as_tree_hctl = parser_hctl.parse_to_tree(formula)
    props_in_hctl = set()
    get_prop_names_from_hctl_ast(as_tree_hctl, props_in_hctl)

    # check that props_in_hctl includes only props from prop_names
    invalid_props = props_in_hctl.difference(prop_names)
    if invalid_props:
        raise InvalidPropError(invalid_props.pop())

    # rename state-vars to canonical form in hctl tree, add new names to list
    num_vars = make_state_vars_canonical_ast(as_tree_hctl, dict(), "", 0)
    var_names = ["x" * i for i in range(1, num_vars + 1)]
    # TODO: check that binders and free variables correspond to each other, no free vars

    # create as_trees for update functions and collect their terminals (props or params)
    update_fn_trees = [parser_update_fn.parse_to_tree(update_str) for update_str in update_fn_strings]
    props_and_params_set = set()
    for as_tree in update_fn_trees:
        get_names_from_update_fn_ast(as_tree, props_and_params_set)

    # from set collected above choose those terminals that are not props -> they are PARAMS
    param_names = sorted(props_and_params_set.difference(prop_names))

    # now we have all building elements, lets create rename dictionary
    # we will rename props to s0, s1... and params to p0, p1...
    name_dict = dict()
    for i in range(len(prop_names)):
        name_dict[prop_names[i]] = f"s__{i}"
    for i in range(len(param_names)):
        name_dict[param_names[i]] = f"p__{i}"

    # rename props in hctl formula tree, rename props/params in update trees
    rename_propositions_in_hctl_ast(as_tree_hctl, name_dict)
    for as_tree in update_fn_trees:
        rename_terminals_update_fn_ast(as_tree, name_dict)

    # create a BDD
    bdd = BDD()
    vrs = [f"s__{i}" for i in range(len(prop_names))]                   # state describing vars
    vrs.extend(f"p__{i}" for i in range(len(param_names)))              # params
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
    return model, as_tree_hctl
