from dd.cudd import BDD, Function
from typing import List


# the main structure representing the combination of the Boolean network and HCTL formula
# contains update functions, metadata (numbers and names of propositions, variables,...), and more
class Model:
    def __init__(self, name: str, bdd: BDD, names_props: List[str],
                 names_params: List[str], names_vars: List[str], update_fns, name_dict):
        self.name = name
        self.bdd = bdd

        self.update_fns = update_fns          # dict with vars + their update funcs, starts with F_s0, F_s1 ...
        self.name_dict = name_dict            # dict with short var names + long var names

        self.names_props = names_props        # full names for props s0, s1 ... (ASCII alphabetical order)
        self.names_params = names_params      # full names for params p0, p1 ... (ASCII alphabetical order)
        self.names_vars = names_vars          # full names for vars x, xx, xxx ... (ASCII alphabetical order)

        self.num_props = len(names_props)
        self.num_params = len(names_params)
        self.num_vars = len(names_vars)

        # unit set initially includes whole colored state space, but can be later restricted to only some colors
        self.unit_colored_set = self.bdd.add_expr("True")
        self.empty_colored_set = self.bdd.add_expr("False")

        self.stable = self.compute_stable()

    # computes stable states in network using a big conjunction of all (s_i <=> F_s_i) formulas
    # this is later used as a way to artificially introduce self loops on stable states
    def compute_stable(self) -> Function:
        current_set = self.unit_colored_set
        for i in range(self.num_props):
            current_set = current_set & self.bdd.apply("<=>", self.bdd.add_expr(f"s__{i}"), self.update_fns[f"s__{i}"])
        return current_set

    def mk_unit_colored_set(self):
        return self.unit_colored_set

    def mk_empty_colored_set(self):
        return self.empty_colored_set
