
class bike:
    """
    Bike Class. For the purposes of the simulation, these are the things we need to know:

        The bike id (not really consequential to the simulation).
        Who it riding the bike. 
        What type of bike it is (mannual or electric).
        
    The rider type will need to be assigned at checkout as many different users can, over time, ride the same bike. 
    """

    def __init__(self, id, bike_type):
        """
        Parameters
        --------------
        id: [int > 0] the bike number.

        bike_type: [manual | electric] the bike type. 
        """

        self._id = id
        self._bike_type = bike_type
        self._rider_type = None #assigned at checkout

    @property
    def id(self):
        return self._id

    @property
    def bike_type(self):
        return self._bike_type

    @property
    def get_rider(self):
        return self._rider_type

    # setting the rider type
    def set_rider(self, rider_type):
        self._rider_type = rider_type


