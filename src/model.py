from dd.cudd import BDD, Function
from typing import List


class Model:
    """Main structure containing the symbolic representation of parsed model.

    Represents information about the Boolean network (update functions, ...)
    and also some needed info about the HCTL formula (state-variables).

    Attributes:
        name: Name of the model.
        bdd: A BDD manager.
        update_fns: Dictionary mapping BN variables to their update functions, starts with F_s0, F_s1
        name_dict: Dictionary mapping short canonical variable names to original names
        names_props: Sequence with original names for props s0, s1 ... (in ASCII alphabetical order)
        names_params: Sequence with original names for params p0, p1 ... (in ASCII alphabetical order)
        names_vars: Sequence with original names for vars x, xx ... (in ASCII alphabetical order)
        unit_colored_set: BDD encoding for the unit colored-state set, initially whole space
        empty_colored_set: BDD encoding for the empty colored-state set, initially empty set
        stable: BDD encoding the set of colored stable states (fixed points)
    """

    def __init__(self, name: str, bdd: BDD, names_props: List[str],
                 names_params: List[str], names_vars: List[str], update_fns, name_dict):
        self.name = name
        self.bdd = bdd
        self.update_fns = update_fns

        self.name_dict = name_dict
        self.names_props = names_props
        self.names_params = names_params
        self.names_vars = names_vars

        # unit set initially includes whole colored state space, but can be later restricted to only some colors
        self.unit_colored_set = self.bdd.add_expr("True")
        self.empty_colored_set = self.bdd.add_expr("False")
        self.stable = self.compute_stable()

    def compute_stable(self) -> Function:
        """
        Compute stable states using a big conjunction of all (s_i <=> F_s_i) formulas.
        This is later used as a way to artificially introduce self-loops on terminal states.
        """
        current_set = self.unit_colored_set
        for i in range(self.num_props()):
            current_set = current_set & self.bdd.apply("<=>", self.bdd.add_expr(f"s__{i}"), self.update_fns[f"s__{i}"])
        return current_set

    def mk_unit_colored_set(self):
        return self.unit_colored_set

    def mk_empty_colored_set(self):
        return self.empty_colored_set

    def num_props(self):
        return len(self.names_props)

    def num_params(self):
        return len(self.names_params)

    def num_vars(self):
        return len(self.names_vars)
