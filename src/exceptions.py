"""
This file includes basic exception classes.
"""

class InvalidPropError(Exception):
    """Raised when the invalid proposition is encountered in a formula."""

    def __init__(self, bad_prop):
        self.bad_prop = bad_prop


class InvalidUpdateFnOperationError(Exception):
    """Raised when the invalid operator is encountered in a BN update function."""

    def __init__(self, invalid_op):
        self.invalid_op = invalid_op


class InvalidHctlOperationError(Exception):
    """Raised when the invalid operator is encountered in a HCTL formula."""

    def __init__(self, invalid_op):
        self.invalid_op = invalid_op
