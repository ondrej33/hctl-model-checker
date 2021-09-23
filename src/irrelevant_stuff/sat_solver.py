from src.Parsing_update_fns.parser_update_fn import parse_to_tree
from src.Parsing_update_fns.evaluator_update_fn import eval_tree
from dd.autoref import BDD
from termcolor import colored


def eval_assignment(assignment, num_vars) -> int:
    result_val = 0
    for i in range(num_vars):
        result_val += assignment[len(assignment) - 1 - i][1] * 2 ** i
    return result_val


if __name__ == '__main__':
    formula = "(x1 || ~x2) && (~x1 || x2 || x3) && ~x1"
    num_props = 3
    tree = parse_to_tree(formula)

    bdd = BDD()
    # TODO: declare bdd from formula
    vrs = [f"x{i}" for i in range(1, 4)]
    bdd.declare(*vrs)

    my_order = dict()
    for i in range(1, 4):
        my_order[f"x{i}"] = i
    bdd.reorder(my_order)

    result = eval_tree(tree, bdd)

    assignments = bdd.pick_iter(result, care_vars=vrs)
    # sorting vars in individual outputs (dict has random order, even though bdd has the right one)
    sorted_inside = [sorted(assignment.items(), key=lambda x: (x[0])) for assignment in assignments]
    # now sorting the outputs by its binary values (using s0,s1...) as main part + by its color as second part
    assignments_sorted = sorted(sorted_inside, key=lambda x: (eval_assignment(x, num_props)))

    for assignment in assignments_sorted:
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

