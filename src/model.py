from typing import List

# change this depending on environment
from dd.autoref import BDD, Function
# from dd.cudd import BDD, Function


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
