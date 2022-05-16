from src.abstract_syntax_tree import *
from src.evaluator_update_fn import eval_update_fn_tree
from src.exceptions import *
from src.model import *
from src.parse_hctl_formula import parser_wrapper_hctl
from src.parse_update_function.parser_wrapper_update_fn import parse_update_fn_to_tree

from collections import OrderedDict
from pathlib import Path
from typing import Set, Dict, Tuple


"""
File wrapping the functionality for parsing models and formulas.
"""


def get_prop_names_from_hctl(node, props_collected: Set[str]) -> None:
    """
    Collect names of all propositions from HCTL formula tree.
    Result is collected into the parameter props_collected.
    """
    if type(node) == TerminalNode:
        # DO not add any of true/false or variable names, only propositions
        if node.category == NodeType.TRUE or node.category == NodeType.FALSE or \
                node.category == NodeType.VAR:
            return
        props_collected.add(node.value)
    elif type(node) == UnaryNode or type(node) == HybridNode:
        get_prop_names_from_hctl(node.child, props_collected)
    elif type(node) == BinaryNode:
        get_prop_names_from_hctl(node.left, props_collected)
        get_prop_names_from_hctl(node.right, props_collected)


def get_names_from_update_fn(node) -> Set[str]:
    """Collect names of props and params in the update function's tree."""
    props_and_params = set()
    get_names_from_update_fn_rec(node, props_and_params)
    return props_and_params


def get_names_from_update_fn_rec(node, props_and_params: Set[str]) -> None:
    """
    Recursively collect names of all propositions and params from the update
    function's tree. Result is collected into parameter props_and_params.
    """
    if type(node) == TerminalNode:
        # DO not add any of true/false nodes, only proposition or parameter nodes
        if node.category == NodeType.TRUE or node.category == NodeType.FALSE:
            return
        props_and_params.add(node.value)
    elif type(node) == UnaryNode:
        get_names_from_update_fn_rec(node.child, props_and_params)
    elif type(node) == BinaryNode:
        get_names_from_update_fn_rec(node.left, props_and_params)
        get_names_from_update_fn_rec(node.right, props_and_params)


def rename_terminals_update_fn(node, rename_dict: Dict[str, str]) -> None:
    """
    Rename all terminal nodes in the update function's tree (propositions and
    parameters), according to the given mapping.
    """
    if type(node) == TerminalNode:
        # rename proposition (param) nodes
        if node.category == NodeType.TRUE or node.category == NodeType.FALSE:
            return
        node.value = rename_dict[node.value]
        node.subform_string = node.value
    elif type(node) == UnaryNode:
        rename_terminals_update_fn(node.child, rename_dict)
        node.subform_string = "(" + OP_TO_STRING[node.category] + node.child.subform_string + ")"
    elif type(node) == BinaryNode:
        rename_terminals_update_fn(node.left, rename_dict)
        rename_terminals_update_fn(node.right, rename_dict)
        inner_name = node.left.subform_string + OP_TO_STRING[node.category] + node.right.subform_string
        node.subform_string = "(" + inner_name + ")"


def rename_props_in_hctl(node, rename_dict: Dict[str, str]) -> None:
    """
    Rename all propositions in terminal nodes of HCTL formula tree, according
    to the given mapping (but do not touch state-variable terminals).
    """
    if type(node) == TerminalNode:
        # only rename proposition nodes, not state variable or constant nodes
        if node.category == NodeType.VAR or node.category == NodeType.TRUE or \
                node.category == NodeType.FALSE:
            return
        node.value = rename_dict[node.value]
        node.subform_string = node.value
    elif type(node) == UnaryNode:
        rename_props_in_hctl(node.child, rename_dict)
        node.subform_string = "(" + OP_TO_STRING[node.category] + node.child.subform_string + ")"
    elif type(node) == BinaryNode:
        rename_props_in_hctl(node.left, rename_dict)
        rename_props_in_hctl(node.right, rename_dict)
        inner_name = node.left.subform_string + OP_TO_STRING[node.category] + node.right.subform_string
        node.subform_string = "(" + inner_name + ")"
    elif type(node) == HybridNode:
        rename_props_in_hctl(node.child, rename_dict)
        inner_name = OP_TO_STRING[node.category] + node.var + ":" + node.child.subform_string
        node.subform_string = "(" + inner_name + ")"


def reduce_number_of_vars(node, rename_dict: Dict[str, str], last_used_name: str):
    """Rename as many state-variables to identical canonical names, without altering the meaning.

    Recursively reduce the number of unique state variables in the formula by renaming
    them, without changing the meaning of the formula. Count the max number of nested vars.
    This is useful for not having redundant BDD variables, and for canonization step later.

    Args:
        node: Root of the tree representing the processed subformula
        rename_dict: Mapping of names of encountered variables to new canonical names
        last_used_name: Last canonical name used for var that is still being quantified
            Holds the role of the stack.

    Returns:
        Maximal number of the nested variable quantifiers encountered on a path
        from node to a terminal.
    """

    # When encountering bind/exist node, add new name mapping (to x, xx, xxx...)
    # When finding terminal with free var or jump, rename corresponding var using rename_dict
    # After leaving binder/exist, remove corresponding mapping from the rename_dict

    if type(node) == TerminalNode:
        # do NOT change names of any true/false or proposition nodes, only state-variables
        if node.category == NodeType.VAR:
            node.value = '{' + rename_dict[node.value[1:-1]] + '}'
            node.subform_string = node.value
        num_hybrid = 0
    elif type(node) == UnaryNode:
        # just dive deeper and then rename the node string
        num_hybrid = reduce_number_of_vars(node.child, rename_dict, last_used_name)
        node.subform_string = "(" + OP_TO_STRING[node.category] + node.child.subform_string + ")"
    elif type(node) == BinaryNode:
        # just dive deeper and then rename the node string
        num_hybrid1 = reduce_number_of_vars(node.left, rename_dict, last_used_name)
        num_hybrid2 = reduce_number_of_vars(node.right, rename_dict, last_used_name)
        num_hybrid = max(num_hybrid1, num_hybrid2)
        inner_name = node.left.subform_string + OP_TO_STRING[node.category] + node.right.subform_string
        node.subform_string = "(" + inner_name + ")"
    else: #  type(node) == HybridNode:
        # if we hit binder or exist, addin its new var name mapping to dict
        if node.category == NodeType.BIND or node.category == NodeType.EXIST:
            last_used_name = last_used_name + 'x'
            rename_dict[node.var[1:-1]] = last_used_name

        # rename the var of this hybrid node (if it is a "jump" node, name should be in dict already)
        var_before = node.var[1:-1]
        node.var = '{' + rename_dict[node.var[1:-1]] + '}'
        # just dive deeper and then rename the node string
        num_hybrid = reduce_number_of_vars(node.child, rename_dict, last_used_name)
        inner_name = OP_TO_STRING[node.category] + node.var + ":" + node.child.subform_string
        node.subform_string = "(" + inner_name + ")"

        # when leaving binder/exist, delete the added var from dict (and increment counter)
        if node.category == NodeType.BIND or node.category == NodeType.EXIST:
            rename_dict.pop(var_before)
            num_hybrid += 1 # increment the number of seen hybrid quantifiers
    return num_hybrid


def parse_bnet_file(file_name: str):
    """Parse BN from bnet file, return lists of variables and update functions."""
    content = Path(file_name).read_text()
    lines = content.splitlines()

    # the first input line usually does not carry any information
    if "targets" in lines[0] and "factors" in lines[0]:
        lines.pop(0)

    lines = [line for line in lines if line.strip()]  # remove empty/blank lines
    lines_ordered = sorted(lines, key=lambda x: x.split(",")[0])

    var_names = [line.split(",")[0] for line in lines_ordered]
    update_fn_strings = [line.split(",")[1] for line in lines_ordered]
    return var_names, update_fn_strings


def collect_param_names(prop_names, update_fn_trees):
    """Collect names of parameters from update functions' trees."""
    param_names = set()
    for tree in update_fn_trees:
        new_props_params = get_names_from_update_fn(tree)
        new_params = new_props_params.difference(prop_names)
        param_names = param_names.union(new_params)
    return sorted(param_names)


def canonize_props_params(prop_names, param_names, as_tree_hctl, update_fn_trees):
    """
    Canonize propositions and parameters in formula and update fn trees.
    Return the renaming mapping.
    """
    rename_dict = dict()
    # canonize proposition names to s0, s1... and parameter names to p0, p1...
    for i in range(len(prop_names)):
        rename_dict[prop_names[i]] = f"s__{i}"
    for i in range(len(param_names)):
        rename_dict[param_names[i]] = f"p__{i}"

    # canonize proposition names in HCTL formula tree
    rename_props_in_hctl(as_tree_hctl, rename_dict)
    # canonize prop/param names in update fn trees
    for tree in update_fn_trees:
        rename_terminals_update_fn(tree, rename_dict)

    return rename_dict


def create_bdd_manager(num_props, num_params, var_names):
    """Create a BDD manager with all necessary variables in 'good' order."""
    bdd_manager = BDD()
    vrs = [f"s__{i}" for i in range(num_props)]       # propositions describing state
    vrs.extend(f"p__{i}" for i in range(num_params))  # parameters
    for var_name in var_names:
        vrs.extend(f"{var_name}__{i}" for i in range(num_props))  # HCTL variables
    bdd_manager.declare(*vrs)

    # reordering BDD vars to desired order
    # now it is: s0,x0,y0,...,s1,x1,y0,...,s2,...,p0,p1...
    my_order = dict()
    for i in range(num_props):
        my_order[f"s__{i}"] = i * (len(var_names) + 1)
    for idx, var_name in enumerate(var_names):
        for i in range(num_props):
            my_order[f"{var_name}__{i}"] = i * (len(var_names) + 1) + idx + 1
    for i in range(num_params):
        my_order[f"p__{i}"] = i + (len(var_names) + 1) * num_props
    bdd_manager.reorder(my_order)
    return bdd_manager


def parse_all(file_name: str, formula: str) -> Tuple[Model, Node]:
    """Parse network and HCTL formula into a symbolic representation and syntax tree.

    Args:
        file_name: Name of the file with Boolean network in bnet format.
        formula: String representing HCTL formula in our encoding.

    Returns:
        A pair containing model object and formula syntax tree, where model object is
        a symbolic representation of the network (influenced by formula variables).
    """

    # collect all BN variable names and their update functions from the bnet file
    prop_names, update_fn_strings = parse_bnet_file(file_name)

    # collect proposition names from parse tree of the HCTL formula
    as_tree_hctl = parser_wrapper_hctl.parse_to_tree(formula)
    props_in_hctl = set()
    get_prop_names_from_hctl(as_tree_hctl, props_in_hctl)

    # check that props_in_hctl includes only valid propositions
    invalid_props = props_in_hctl.difference(prop_names)
    if invalid_props:
        raise InvalidPropError(invalid_props.pop())

    # minimize number of state-vars in HCTL tree, partially canonize their names and collect them
    num_vars = reduce_number_of_vars(as_tree_hctl, dict(), "")
    var_names = ["x" * i for i in range(1, num_vars + 1)]

    # create syntax trees for update functions and collect their parameters (inputs)
    update_fn_trees = [parse_update_fn_to_tree(update_str) for update_str in update_fn_strings]
    param_names = collect_param_names(prop_names, update_fn_trees)

    # canonize proposition names to s0, s1... and parameter names to p0, p1...
    rename_dict = canonize_props_params(prop_names, param_names, as_tree_hctl, update_fn_trees)

    # create a BDD manager with correctly ordered variables
    bdd_manager = create_bdd_manager(len(prop_names), len(param_names), var_names)

    # create BDD-encoding for each update function by evaluating their syntax trees
    list_update_fns = [eval_update_fn_tree(as_tree, bdd_manager) for as_tree in update_fn_trees]
    update_dict = OrderedDict()
    for i in range(len(prop_names)):
        update_dict[f"s__{i}"] = list_update_fns[i]

    # pack it all into a model object and return it together with a formula syntax tree
    name_dict_reversed = {y: x for x, y in rename_dict.items()}
    model_name = file_name.split("/")[-1]
    model = Model(model_name, bdd_manager, prop_names, param_names,
                  var_names, update_dict, name_dict_reversed)
    return model, as_tree_hctl
