
class station:
    """
    This class will control the behavior of the stations 
    """

    def __init__(self, id, location, dock_count):
        """
        Parameters
        ----------
        id: [int > 0] station number.

        location: [tuple, ]

        dock_count: [int > 0] number of docks at the station.
        """
        
        self._id = id
        self._location = location
        self._dock_count = dock_count
        self._available_docks = dock_count # to start, they all will be open until we assign bikes to the station.

        # if the station possesses electric bike charging capibility, then the station type will be Electric, if the station possesses no charging capibility then the type will be manual. Right now, we will only be considering the station types that are manual. 
        self._station_type = "Manual"
        
        # number of 
        self._parked_bikes = [None]
    
    @property
    def id(self):
        return self._id
    
    @property
    def location(self):
        return self._location

    @property
    def dock_count(self):
        return self._dock_count

    @property
    def available_docks(self):
        return self._available_docks

    # adding bikes to the station
    def add_bike(self, bike):
        if self._available_docks == 0:
            print("there are not enough spaces at this station")
        else:
            self._parked_bikes.append(bike)
            self._available_docks += -1


    

