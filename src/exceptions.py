class InvalidPropError(Exception):
    def __init__(self, bad_prop):
        self.bad_prop = bad_prop

