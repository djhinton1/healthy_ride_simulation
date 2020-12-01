
from .assert_helper import *
from .dock import Dock
from .bike import Bike


class Station:
    """
    This class will control the behavior of the stations 
    """

    def __init__(self, id, longitude, latitude, dock_count, status, bikes, description):
        """
        Parameters
        ----------
        id: [int > 0] station number.

        longitude: [double] contains map longitude coordinate for the station.

        latitude: [double] contains map latitude coordinates for the station.

        dock_count: [int > 0] number of docks at the station.

        status: [str] Station condition, used to assess effect of eliminating the station.

        bikes: [int > 0] Number of bikes at the station.

        description: [str] Description of the station.
        """
        
        assert_id(id)
        self._id = id

        self._longitude = longitude
        self._latitude = latitude

        assert_id(dock_count)
        self._dock_count = dock_count
        self._docks = [
            Dock(
                id = i, charge = False, station = self.id
            )
            for i in range(dock_count)
        ]

        assert_status(status)
        self._status = status

        assert_bikes(dock_count, bikes)
        for i in range(bikes):
            self.docks[i].bike = Bike(((self.id * 100) + i), "manual")

        self._checkouts = [] # list of trips away from the station (station is origin)

        self._checkins = [] # list of trips to the station (station is destination)

        self._log = [] # list of all activity at the station

        self._description = description

        self._activity = None
    
    
    @property
    def id(self):
        return self._id

    @property
    def longitude(self):
        return self._longitude

    @property
    def latitude(self):
        return self._latitude

    @property
    def activity(self):
        return self._activity
    
    @property
    def location(self):
        return self._location

    @property
    def dock_count(self):
        return self._dock_count

    @property
    def docks(self):
        return self._docks

    @property
    def checkouts(self):
        for dock in self.docks:
            if not dock.log:
                continue

            for trip in dock.log:
                if trip.get('event') == "check-out":
                    self._checkouts.append(trip)

        return self._checkouts

    @property
    def checkins(self):
        for dock in self.docks:
            if not dock.log:
                continue

            for trip in dock.log:
                if trip.get('event') == "check-in":
                    self._checkins.append(trip)
                    
        return self._checkins

    @property
    def log(self):
        desc = {'station_desc': self.description}
        for dock in self.docks:
            if not dock.log:
                continue

            for trip in dock.log:
                desc.update(trip)
                self._log.append(desc)
        return self._log

    @property
    def status(self):
        return self._status

    @property
    def bikes(self):
        """
        Returns
        --------
        Number of bikes currently at the station.
        """
        bikes = [1 if dock.bike else 0 for dock in self.docks]
        return sum(bikes)

    @property
    def description(self):
        return self._description

    def take_bike(self, user):
        if self.bikes == 0: # there are no bikes to take
            return None
        
        for dock in self.docks:
            if dock.bike:
                self._activity = 1
                return dock.check_out(user)

    def dock_bike(self, bike):
        if self.bikes == self.dock_count: # station is full
            return None
        
        for dock in self.docks:
            if not dock.bike:
                self._activity = 1
                dock.check_in(bike)
                return 1

    

