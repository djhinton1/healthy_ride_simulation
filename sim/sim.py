import xlrd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import numpy
import pandas as pd
import matplotlib.pyplot as plt
from sim.station import Station
import mpld3

class Simulation:
    """
    This class controls the behavior of the simulation.
    """

    def __init__(self, path):
        
        # taking the stations from the excel file and turning them into Station objects for the simulation loaded with the docks and bikes as specificed in the excel file. 

        stations = {}
        station_data = get_data(path,0)
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
        









# Helper Functions
###################################################
def get_data(path, sheet):
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
    workbook = xlrd.open_workbook(path, on_demand = True)
    worksheet = workbook.sheet_by_index(sheet)
    first_row = [] # The row where we stock the name of the column
    for col in range(worksheet.ncols):
        first_row.append( worksheet.cell_value(0,col) )

    # transform the workbook to a list of dictionaries
    data =[]
    for row in range(1, worksheet.nrows):
        elm = {}
        for col in range(worksheet.ncols):
            elm[first_row[col]]=worksheet.cell_value(row,col)
        
        # data frame used to create visualization
        df2 = pd.DataFrame([[
            elm.get('longitude'), 
            elm.get('latitude'), 
            elm.get('status')

            ]], columns=('longitude', 'latitude', 'status')
        )

        df = df.append(df2, ignore_index=True)
        data.append(elm)

    # Plotting the Stations
    street_map = gpd.read_file('/Users/djhinton/Documents/GitHub/healthy_ride_simulation/sim/tl_2017_42003_roads/tl_2017_42003_roads.shp')

    crs = {'init':'epsg:4326'}
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    geo_df = gpd.GeoDataFrame(
        df,
        crs = crs,
        geometry = geometry
    ) 

    fig, ax = plt.subplots(figsize = (15,15))
    plt.xlim(-80.01,-79.9)
    plt.ylim( 40.40,40.50)
    plt.title('Healthy Ride Active vs. Inactive Stations ', fontsize=15,fontweight='bold')
    street_map.plot(ax = ax, color = 'grey')

    active_df = geo_df['status'] == 'active'
    inactive_df = geo_df['status'] == 'inactive'

    if not geo_df[active_df].empty:
        geo_df[active_df].plot(ax = ax, markersize = 40, color = 'blue', marker = 'o', label = 'active')

    if not geo_df[inactive_df].empty:
        geo_df[inactive_df].plot(ax = ax, markersize = 40, color = 'red', marker = '^', label = 'inactive')
    
    mpld3.save_html(fig, 'active_stations.html')

    return data
        

'''
var = average number of customers per day
var = average probability of starting at a 
var = average probability of ending up at a station (to station)

need for loop where each iteration is one day
average probability of from-station * average customer number (number of bikes from station / day)
average probability of to-station * average number of customers

^ from this, we know the number of bikes coming to and leaving from the station, we can subtract these numbers and learn the difference and compare that to the number of bikes starting at the station. 

Station A:
* start # of bikes = 5
* # of bikes leaving the station  = 18
* # of bikes going to the station = 12

start (if negative)
18 - 12 = 6 bikes // lost demand

demand  = bikes leaving station + bikes coming to the station // which are important
'''
