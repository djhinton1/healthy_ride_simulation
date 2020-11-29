"""
Wrapper for model assertions.
"""

def assert_greater_than_zero(var, name):
    """
    Raises Value Error if var is less than zero

    Params
    --------
    var: [int | float] Number that must be greater than zero.

    name: [str] Name of variable, used for error message.
    """
    if var < 0:
        raise ValueError(f"{name} must be greater than or equal to zero.")

def assert_id(id):
    """
    Raises Type Error if id is not an int; and then if it passes, check to make sure that it is greater than zero.

    Params
    --------
    id: [int] Number that must be type int
    """
    if not isinstance(id, int):
        raise TypeError("id must be in int")
    else:
        assert_greater_than_zero(id, "id")
