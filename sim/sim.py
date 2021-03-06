import xlrd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from sim.station import Station
from sim.bike import Bike
import mpld3
import random
import pprint

class Simulation:
    """
    This class controls the behavior of the simulation.
    """

    def __init__(self, path):
        
        # taking the stations from the excel file and turning them into Station objects for the simulation loaded with the docks and bikes as specificed in the excel file. 
        stations = {}
        station_data = get_data(path)
        for element in station_data:
            stations[int(element.get('station_id'))] = Station(

                id = int(element.get('station_id')),
                longitude = element.get('longitude'),
                latitude = element.get('latitude'),
                dock_count = int(element.get('dock_count')),
                status = element.get('status'),
                bikes = int(element.get('bike_count')),
                description = element.get('description')

            )

        
        # need the station demand and the associated weights so that we can generate a weighted random selection as start location. 
        # Has format [[stations],[weights]]
        demand_weights = get_weights(path)
        
        # we also need transition weights so that we can determine where the rider will go after they have picked up the bike. 
        transition_weights = get_transitions(path)

        # need the user weights so that we know what type of user is moving between the stations.
        user_weights = [['undergraduate', 'graduate', 'faculty'],[50, 30, 20]]

        # we need to know how many events we should have in the current iteration
        activity_weights = [[1,2,3,4,5],[50,40,30,20,10]]

        
        # SIMULATION ////////////

        in_transit = []

        # generate how many trips we are taking in this iteration
        num_trips = random.choices(
            activity_weights[0], 
            weights = activity_weights[1],
            k = 1
        )[0]

        # generate statring locations for those trips
        start_stations = random.choices(
            demand_weights[0],
            weights = demand_weights[1],
            k = num_trips
        )

        for trip in start_stations:

            # for each trip, pick a destination location
            end_station = random.choices(
                transition_weights[trip][0],
                weights = transition_weights[trip][1],
                k = 1
            )[0]
            
            # for each trip, pick a user type
            user_type = random.choices(
                user_weights[0],
                weights = user_weights[1],
                k = 1
            )[0]

            # check out the bikes from the correct stations
            bike = stations[trip].take_bike(user_type)
            bike.to_station = end_station

            # add bikes to in_transit
            in_transit.append(bike)

        for bike in in_transit:
            # return bikes to approperate stations
            stations[bike.to_station].dock_bike(bike)

        # print out the log
        for i in stations:
            if stations[i].activity:
                print("\nLOG FOR " + str(stations[i].id))
                print("---------------------")
                for j in stations[i].log:
                    pprint.pprint(j)
                    print("\n")
                
              
        


# Helper Functions
###################################################
def get_data(path):
    """
    Reads in the excel file required to generate the stations. Also makes a map showing which stations are considered inactive.

    Params
    --------
    path: [str] The file path to the desired excel worksheet. 

    Returns
    --------
    A list of dictionaries that each contain information from one row of the excel file. 
    """

    df = pd.DataFrame(columns=('longitude', 'latitude', 'status'))
    
    worksheet = get_worksheet(path, 0)
    first_row = [] # The row where we stock the name of the column
    for col in range(worksheet.ncols):
        first_row.append( worksheet.cell_value(0,col) )

    # transform the workbook to a list of dictionaries and build map df at the same time
    data =[]
    for row in range(1, worksheet.nrows):
        elm = {}
        for col in range(worksheet.ncols):
            elm[first_row[col]]=worksheet.cell_value(row,col)
        
        # data frame used to create map visualization parsed at same time the station dictionaries are being made
        df2 = pd.DataFrame([[
            elm.get('longitude'), 
            elm.get('latitude'), 
            elm.get('status')

            ]], columns=('longitude', 'latitude', 'status')
        )

        df = df.append(df2, ignore_index=True) # append map df
        data.append(elm) # append station sictionary
    '''
    # Plotting the Stations
    # Read in the shape file for pittsburgh
    street_map = gpd.read_file('/Users/djhinton/Documents/GitHub/healthy_ride_simulation/sim/tl_2017_42003_roads/tl_2017_42003_roads.shp')

    # set the projection type and generate point geometry according to longitude and latitude columns in df
    crs = {'init':'epsg:4326'}
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    geo_df = gpd.GeoDataFrame(
        df,
        crs = crs,
        geometry = geometry
    ) 

    # creating the map over which to plot our stations
    fig, ax = plt.subplots(figsize = (15,15))
    plt.xlim(-80.01,-79.9)
    plt.ylim( 40.40,40.50)
    plt.title('Healthy Ride Active vs. Inactive Stations ', fontsize=15,fontweight='bold')
    street_map.plot(ax = ax, color = 'grey')

    # these variables are used to help mitigate plotting errors when all stations are active or when all stations are inactive
    active_df = geo_df['status'] == 'active'
    inactive_df = geo_df['status'] == 'inactive'

    # plot active stations
    if not geo_df[active_df].empty:
        geo_df[active_df].plot(ax = ax, markersize = 40, color = 'blue', marker = 'o', label = 'active')

    # plot inactive stations
    if not geo_df[inactive_df].empty:
        geo_df[inactive_df].plot(ax = ax, markersize = 40, color = 'red', marker = '^', label = 'inactive')
    
    # save map as html file
    mpld3.save_html(fig, 'active_stations.html')
    '''
    return data

def get_worksheet(path, sheet):
    """
    Returns a specific worksheet from the excel file provided in the path.

    Params
    --------
    path: [str] The file path to the desired excel worksheet. 

    sheet: [int >= 0] The sheet index to obtain.

    Returns
    --------
    A indexed worksheet from a workbook provided by the path.
    """
    workbook = xlrd.open_workbook(path, on_demand = True)
    worksheet = workbook.sheet_by_index(sheet)
    return worksheet

def get_weights(path):
    """
    Gets the station demand from the excel worksheet provided. The worksheet contains the names and id's of stations as well as the number of trips that orginated at that station.

    Params
    --------
    path: [str] The file path to the desired excel worksheet. 

    Returns
    --------
    A nested list containing the station id's and their weights (number of that station's observations observations)
    """
    station_demand_weights = [[],[]]
    demand_worksheet = get_worksheet(path, 1)
    for row in range(1, demand_worksheet.nrows):
        station_demand_weights[0].append(int(demand_worksheet.cell_value(row, 0)))
        station_demand_weights[1].append(int(demand_worksheet.cell_value(row, 2)))
    return station_demand_weights

def get_transitions(path):
    """
    Will load the weights of transitions within the network. The sheet contains one row for every unique occurance of a transition from one station to another, identifying the from_Station and the to_Station. These rows have the number of transitions along this from-to route that we have observed.

    Params
    --------
    path: [str] The file path to the desired excel worksheet. 

    Returns
    --------
    A dictionary where the keys are unique station id's and the value is a nested list containing the to-stations and their weights (number of observations). Has the following format { int : [[],[]] } 
    """
    transition_weights = {}
    transition_worksheet = get_worksheet(path, 2)
    for row in range(1, transition_worksheet.nrows):
        if not int(transition_worksheet.cell_value(row, 0)) in transition_weights:
            transition_weights[int(transition_worksheet.cell_value(row, 0))] = [[int(transition_worksheet.cell_value(row, 1))],[int(transition_worksheet.cell_value(row, 2))]]
        else:
            transition_weights[int(transition_worksheet.cell_value(row, 0))][0].append(int(transition_worksheet.cell_value(row, 1)))

            transition_weights[int(transition_worksheet.cell_value(row, 0))][1].append(int(transition_worksheet.cell_value(row, 2)))
    return transition_weights
