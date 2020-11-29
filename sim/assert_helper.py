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
        raise TypeError("id must be in int.")
    else:
        assert_greater_than_zero(id, "id")

def assert_bike_type(type):
    """
    Raises Type Error if the bike type is not manual or electric.

    Params
    --------
    type: [str] Type of bike.
    """
    if type not in ("electric", "namual"):
        raise ValueError(f"{type} is not a valid bike type.")

def assert_rider(rider):
    """
    Raises value error if rider is not an undergraduate, graduate, or faculty

    Params
    --------
    rider: [str] The type of bike rider.
    """
    if rider not in ("undergraduate", "graduate", "faculty"):
        raise ValueError(f"{rider} is not a valid bike rider.")

def assert_charge(x):
    """
    Raises type error if x is not a boolean

    Params
    --------
    x: [boolean] The dock has charging capibilities. t/f
    """
    if not isinstance(x, bool):
        raise TypeError(f"{x} is not true/false.")
