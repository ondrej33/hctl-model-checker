from __future__ import annotations
from heapq import heappop, heappush
from typing import Set, Dict, Optional, Tuple, List


class BddNode:
    def __init__(self, number: int, var: Optional[str], high: Optional[BddNode] = None, low: Optional[BddNode] = None):
        self.number = number  # number 2+, (0 and 1 for FALSE and TRUE nodes)
        self.var = var
        self.parents = set()
        self.high = high
        self.low = low

    def add_child(self, child: BddNode, is_high: bool):
        child.parents.add(self)
        if is_high:
            self.high = child
        else:
            self.low = child

    def add_both(self, low: BddNode, high: BddNode):
        low.parents.add(self)
        high.parents.add(self)
        self.high = high
        self.low = low

    # just define something so that heapq can be used on nodes
    def __lt__(self, other: BddNode):
        return self.number < other.number


class Bdd:
    def __init__(self, root: BddNode, vars_order: Dict[str, int]):
        self.vars_order = vars_order
        self.vars_list = sorted([var for var in vars_order], key=lambda x: vars_order[x], reverse=True)
        self.root = root
        self.zero = BddNode(0, None)
        self.one = BddNode(1, None)
        self.nodes = {0: self.zero, 1: self.one, 2: self.root}  # others have to be added manually
        self.unique_num = root.number + 1  # something to hold unique number for next node, we'll use least bigger num

    def add_node(self, node: BddNode):
        # node.number must be unique
        if self.nodes.get(node.number) is not None:
            print("not unique node")
            return
        self.nodes[node.number] = node
        if node.number >= self.unique_num:
            self.unique_num = node.number + 1

    def swap_terminals(self):
        self.one, self.zero = self.zero, self.one
        self.one.number = 1
        self.zero.number = 0

    def dump_rec(self, node: BddNode, seen: Set[int]) -> None:
        if node.number in seen:
            return
        seen.add(node.number)

        if node.low:
            print(f"{node.number} -> {node.low.number} [style=dashed]")
            self.dump_rec(node.low, seen)
        if node.high:
            print(f"{node.number} -> {node.high.number}")
            self.dump_rec(node.high, seen)

    def dump(self):
        print("digraph G {")
        for n in self.nodes:
            if self.root.number == n:
                print(n, "[color=deepskyblue]")
            else:
                print(n)
            if n == 0 or n == 1:
                print("[shape = polygon]")
        self.dump_rec(self.root, set())
        print("}\n")

    # returns decimal value of binary vector v1,v2,v3... and it is used for sorting assignments
    def eval_assignment(self, assignment) -> int:
        result_val = 0
        for i in range(len(assignment)):
            result_val += assignment[len(assignment) - 1 - i][1] * (2 ** i)
        return result_val

    def add_missing_vars(self, assignment: List[Tuple[str, int]]):
        counter = 0
        results = [assignment]
        for idx, var in enumerate(self.vars_list):
            if counter < len(assignment) and assignment[counter][0] == var:
                counter += 1
            else:
                # var is missing, add it to all results in both form (one form to original, one to copy)
                copies = []
                for r in results:
                    r_copy = r.copy()
                    r.append((var, 0))
                    r_copy.append((var, 1))
                    copies.append(r_copy)
                results.extend(copies)
        return results

    def get_assignments_rec(self, node: BddNode, current_assignment: List[Tuple[str, int]], assignments: List[List[Tuple[str, int]]]):
        if node == self.one:
            filled = self.add_missing_vars(current_assignment)
            assignments.extend(filled)
        elif node != self.zero:
            self.get_assignments_rec(node.low, current_assignment + [(node.var, 0)], assignments)
            self.get_assignments_rec(node.high, current_assignment + [(node.var, 1)], assignments)

    def get_assignments(self):
        assignments = []
        self.get_assignments_rec(self.root, [], assignments)
        for assignment in assignments:
            assignment.sort(key=lambda x: self.vars_order[x[0]])
        assignments.sort(key=lambda x: self.eval_assignment(x))
        print(assignments)
        print()
        for assignment in assignments:
            print([x[1] for x in assignment])

    def build_from_assignments(self):
        pass

    def reduce(self):
        """
        non-unique nodes:
            get all pairs of node and if node1.low == node2.low and node1.high == node2.high:
                delete node2 and use node1 instead of it
        redundant tests:
            if node.low == node.high:
                delete node and use its low instead of it
        """
        changed = True
        while changed:
            changed = False

            # redundant tests:
            to_delete = set()
            for _, node in self.nodes.items():
                if node == self.one or node == self.zero:
                    continue
                if node.low == node.high:
                    changed = True

                    # change parents of the child
                    node.low.parents.remove(node)
                    node.low.parents = node.low.parents.union(node.parents)

                    # change children of parents
                    if node == self.root:
                        self.root = node.low
                    else:
                        for parent in node.parents:
                            if parent.low == node:
                                parent.low = node.low
                            else:
                                parent.high = node.low
                    # delete node from bdd
                    to_delete.add(node.number)
            for n in to_delete:
                self.nodes.pop(n)

            # non-unique nodes:
            to_delete = set()
            # first find the pairs
            for _, node1 in self.nodes.items():
                for _, node2 in self.nodes.items():
                    if node1 == self.one or node1 == self.zero or node2 == self.one or node2 == self.zero or node1 == node2:
                        continue
                    if (node2, node1) in to_delete:
                        continue
                    if node1.low == node2.low and node1.high == node2.high and node1.var == node2.var:
                        to_delete.add((node1, node2))
                        changed = True
            # now delete node2 of the each pair and replace it with node1
            for node1, node2 in to_delete:
                # it is enough to solve the parents (children are the same)
                for parent in node2.parents:
                    node1.parents.add(parent)
                    if parent.low == node2:
                        parent.low = node1
                    else:
                        parent.high = node1
                # delete node from bdd
                self.nodes.pop(node2.number)


def quantify_existential(bdd: Bdd, to_delete: Set[str]):
    seen = set()
    queue = []  # weird heap, will contain tuples in form (priority, node, came_from)
    heappush(queue, (0, bdd.one, None))

    while queue:
        _, node, came_from = heappop(queue)

        if node.var in to_delete:
            # the case where deleted node is root, we just make root the came_from node
            if node == bdd.root:
                bdd.root = came_from
                # TODO - something more needed probably - somehow merge root's 2 children? if its not terminal
                # TODO - or just dont care about the second branch??

            # now go through parents, swap the edges and add parents to queue
            for parent in node.parents:
                if parent.low == node:
                    parent.low = came_from
                else:
                    parent.high = came_from

                came_from.parents.add(parent)

                # we will add parent to the queue if it is not there
                if parent not in seen:
                    seen.add(parent)
                    heappush(queue, (bdd.vars_order[parent.var], parent, came_from))

            # now delete node from its children parent lists and also from BDD
            if came_from == node.low:
                node.high.parents.remove(node)
            else:
                node.low.parents.remove(node)
            came_from.parents.remove(node)
            bdd.nodes.pop(node.number)
        else:
            for parent in node.parents:
                if parent not in seen:
                    seen.add(parent)
                    heappush(queue, (bdd.vars_order[parent.var], parent, node))

    # remove the vars from BDD
    for var in to_delete:
        bdd.vars_list.remove(var)
        bdd.vars_order.pop(var)


def exists_last_var(bdd: Bdd):
    last_var = bdd.vars_list[-1]  # this should be the last variable
    parents_of_1_to_remove = [parent for parent in bdd.one.parents if parent.var == last_var]

    # now lets go through the selected parent nodes and remove them
    for node in parents_of_1_to_remove:
        # if the BDD has only 1 layer and we are removing root, lets change root to true_node
        if node == bdd.root:
            bdd.root = bdd.one

        # now go through node's parents, and make true_node their child instead of the current node
        for parent in node.parents:
            if parent.low == node:
                parent.low = bdd.one
            else:
                parent.high = bdd.one
            bdd.one.parents.add(parent)

        # now delete node from its children parent lists (from true_node + also from false_node)
        bdd.one.parents.remove(node)
        if bdd.one == node.low:
            node.high.parents.remove(node)
        else:
            node.low.parents.remove(node)

        # remove deleted node from bdd
        bdd.nodes.pop(node.number)

    # remove the vars from BDD
    bdd.vars_list.pop()
    bdd.vars_order.pop(last_var)


def swap_var_node(bdd: Bdd, f: BddNode, var_to_swap_with: str):
    assert f != bdd.one and f != bdd.zero
    f1 = f.high
    f0 = f.low

    # change var in the node
    old_var = f.var
    f.var = var_to_swap_with

    # create 2 new nodes and use them as children
    g0 = BddNode(bdd.unique_num, old_var)
    bdd.add_node(g0)
    g1 = BddNode(bdd.unique_num, old_var)
    bdd.add_node(g1)
    f.add_both(g0, g1)

    # now handle swapping of children depending on the node children having the right var or not
    if f0.var == var_to_swap_with and f1.var == var_to_swap_with:
        g0.add_both(f0.low, f1.low)
        g1.add_both(f0.high, f1.high)
        g0.low.parents.remove(f0)
        g0.high.parents.remove(f1)
        g1.low.parents.remove(f0)
        g1.high.parents.remove(f1)

        f0.parents.remove(f)
        f1.parents.remove(f)
        if not f0.parents:
            bdd.nodes.pop(f0.number)
        if not f1.parents:
            bdd.nodes.pop(f1.number)

    elif f0.var == var_to_swap_with and f1.var != var_to_swap_with:
        g0.add_both(f0.low, f1)
        g1.add_both(f0.high, f1)
        g0.low.parents.remove(f0)
        g0.high.parents.remove(f)
        g1.low.parents.remove(f0)
        g1.high.parents.remove(f)

        f0.parents.remove(f)
        if not f0.parents:
            bdd.nodes.pop(f0.number)

    elif f0.var != var_to_swap_with and f1.var == var_to_swap_with:
        g0.add_both(f0, f1.low)
        g1.add_both(f0, f1.high)
        g0.low.parents.remove(f)
        g0.high.parents.remove(f1)
        g1.low.parents.remove(f)
        g1.high.parents.remove(f1)

        f1.parents.remove(f)
        if not f1.parents:
            bdd.nodes.pop(f1.number)

    elif f0.var != var_to_swap_with and f1.var != var_to_swap_with:
        g0.add_both(f0, f1)
        g1.add_both(f0, f1)
        g0.low.parents.remove(f)
        g0.high.parents.remove(f)
        g1.low.parents.remove(f)
        g1.high.parents.remove(f)

    # we dont have to do anything in case both f0 and f1 have different variable, the swapping is free


def swap_var_level(bdd: Bdd, v1: str, v2: str):
    nodes_v1 = [node for (num, node) in bdd.nodes.items() if node.var == v1]
    for node in nodes_v1:
        swap_var_node(bdd, node, v2)

    # change variable order to the new one
    bdd.vars_order[v1] += 1
    bdd.vars_order[v2] -= 1
    v1_idx = bdd.vars_list.index(v1)
    bdd.vars_list[v1_idx] = v2
    bdd.vars_list[v1_idx + 1] = v1

    bdd.reduce()


def build(root_initials: Tuple[int, str],
          other_node_initials: Set[Tuple[int, str]],
          edge_pairs: Set[Tuple[int, int, int]],  # parent, low, high
          var_order: Dict[str, int]) -> Bdd:
    bdd = Bdd(BddNode(root_initials[0], root_initials[1]), var_order)
    for num, var in other_node_initials:
        bdd.add_node(BddNode(num, var))
    for parent, low, high in edge_pairs:
        bdd.nodes[parent].add_both(bdd.nodes[low], bdd.nodes[high])
    return bdd


def main():
    """
    root_node = (2, 's0')
    other_nodes = {(3, 'x0'), (4, 'x0'), (5, 's1'), (6, 's1'), (7, 's1'), (8, 's1'), (9, 'x1'), (10, 'x1')}
    edge_pairs = {(2, 3, 4), (3, 5, 7), (4, 6, 8), (5, 9, 0), (6, 0, 9), (7, 10, 0), (8, 0, 10), (9, 1, 0), (10, 0, 1)}
    var_order = {'s0': 4, 'x0': 3, 's1': 2, 'x1': 1}  # it is reversed for the needs of algorithm, 0 for True/False
    bdd = build(root_node, other_nodes, edge_pairs, var_order)
    """

    """
    root_node = (2, 'x1')
    other_nodes = {(3, 'x2'), (4, 'x3')}
    edge_pairs = {(2, 0, 3), (3, 4, 1), (4, 1, 0)}
    var_order = {'x1': 3, 'x2': 2, 'x3': 1}  # it is reversed for the needs of algorithm, 0 for True/False
    bdd = build(root_node, other_nodes, edge_pairs, var_order)
    """

    root_node = (2, 'x1')
    other_nodes = {(3, 'x2'), (4, 'x2'), (5, 'x3'), (6, 'x3')}
    edge_pairs = {(2, 3, 4), (3, 6, 5), (4, 5, 1), (5, 0, 1), (6, 1, 0)}
    var_order = {'x1': 3, 'x2': 2, 'x3': 1}  # it is reversed for the needs of algorithm, 0 for True/False
    bdd = build(root_node, other_nodes, edge_pairs, var_order)

    bdd.dump()


if __name__ == '__main__':
    main()


"""
digraph G {
TRUE [shape = polygon]
FALSE [shape = polygon]

1 -> 2 [style=dashed]
1 -> 3
2 -> 4 [style=dashed]
4 -> 6 [style=dashed]
6 -> TRUE [style=dashed]
3 -> 7 [style=dashed]
7 -> 8 [style=dashed]
8 -> TRUE
3 -> 9
9 -> 10
10 -> TRUE [style=dashed]
2 -> 11
11 -> 12
12 -> TRUE
9 -> FALSE [style=dashed]
11 -> FALSE [style=dashed]
12 -> FALSE [style=dashed]
8 -> FALSE [style=dashed]
4 -> FALSE
7 -> FALSE
6 -> FALSE
10 -> FALSE
}
"""