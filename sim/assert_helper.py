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
    if type not in ("electric", "manual"):
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

def assert_location(loc):
    """
    Raises type error if loc is not an integer tuple

    Params
    --------
    loc: [tuple] coordinates of the location
    """
    if not isinstance(loc, tuple):
        raise TypeError(f"{loc} is not a tuple")

def assert_status(stat):
    """
    Raises Type Error if the status is not "active" or "inactive"

    Params
    --------
    stat: [str] Status of the station.
    """
    if stat not in ("active", "inactive"):
        raise ValueError(f'{stat} is not a valid station status.')

def assert_bikes(docks, bikes):
    """
    Raises value error if the number of bikes is greater than the number of docks at the station.

    Params
    --------
    docks: [int > 0] Number of docks at the station.

    bikes: [int > 0] Number of bikes at the station.
    """
    if bikes > docks:
        raise ValueError("cannot have more bikes than docks")
