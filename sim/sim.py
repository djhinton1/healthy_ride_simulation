"""
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
"""
