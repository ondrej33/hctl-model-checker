from typing import List

# change this depending on environment
from dd.autoref import BDD, Function
# from dd.cudd import BDD, Function


class Model:
    def __init__(self, name: str, bdd: BDD, num_props: int, names_props: List[str],
                 num_params: int, names_params: List[str], update_fns, update_strings, name_dict):
        self.name = name
        self.bdd = bdd
        self.num_props = num_props
        self.names_props = names_props        # full names for props s0, s1 ... (ASCII alphabetical order)
        self.num_params = num_params
        self.names_params = names_params      # full names for params p0, p1 ... (ASCII alphabetical order)
        self.update_fns = update_fns          # dict with vars + their update funcs, starts with F_s0, F_s1 ...
        self.update_strings = update_strings  # dict with vars + string for their update fns (experimenting)
        self.name_dict = name_dict            # dict with short var names + long var names
