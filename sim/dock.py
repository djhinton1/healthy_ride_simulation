from .assert_helper import assert_charge, assert_id
from .bike import Bike

class Dock:
    """
    At each station, there is a dock to which a bike can connect. There are a certain number of docks per station. There are a few things that we will need to know:

        * Dock id, only station unique. There may be similar dock numbers at other stations.
        * Whether or not there is a bike connected to the dock.
        * Whether or not the dock has the capibility to charge the bikes. (to be added later)
        * a bike log for knowing which bikes attatch to it. 

    """

    def __init__(self, id, charge, station):
        """
        Params
        --------
        id: [int > 0] The dock id at the station.

        charge: [boolean] The dock has charging capibilities.

        station: [int > 0] The station that this dock belongs to.
        """
        assert_id(id)
        self._id = id

        assert_charge(charge)
        self._can_charge = charge

        assert_id(station)
        self._station = station

        self._bike = None # assigned when bike docks
        self._log = [] # adapts as bikes are checked in

    @property
    def id(self):
        return self._id

    @property
    def can_charge(self):
        return self._can_charge

    @property
    def station(self):
        return self._station

    @property
    def bike(self):
        return self._bike

    @bike.setter
    def bike(self, bike):
        if (bike == None) or (isinstance(bike, Bike)):
            self._bike = bike
        else:
            raise TypeError("bike must be of Bike type")

    @property
    def log(self):
        return self._log

    def check_in(self, bike):
        """
        Check this bike into this bike.

        Params
        ------
        bike [Bike] The bike to check into the dock.
        """
        
        if isinstance(self.bike, Bike):
            raise Exception("attempting to check a bike into a dock that is already occupied")
        
        self.bike = bike

        self._log.append({
            'event': 'check-in',
            'dock_id': self.id,
            'bike_id': self.bike.id,
            'bike_type': self.bike.bike_type,
            'bike_rider': self.bike.rider,
            'from_station': self.bike.from_station
        })

    def check_out(self, user_type):
        """
        Check out the bike that is currently at the dock.

        Params
        -------
        user_type: [str] The type of user checking out this bike.
        """

        if not isinstance(self.bike, Bike):
            raise Exception("attempting to check out a bike that does not exist at the dock")
        
        self.bike.rider = user_type
        self.bike.from_station = self.station

        self._log.append({
            'event': 'check-out',
            'dock_id': self.id,
            'bike_id': self.bike.id,
            'bike_type': self.bike.bike_type,
            'bike_rider': self.bike.rider,
        })

        bike = self.bike
        self.bike = None
        return bike



