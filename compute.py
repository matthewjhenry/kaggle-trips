from math import radians, cos, sin, asin, sqrt
from numpy import *
import mycluster

def haversine(v1,v2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lon1=v1[1]
    lat1=v1[0]
    lon2=v2[1]
    lat2=v2[0]
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

north_pole = (90,0)
weight_limit = 1000
sleigh_weight = 10

def weighted_trip_length(stops, weights): 
    tuples = [tuple(x) for x in stops.values]
    # adding the last trip back to north pole, with just the sleigh weight
    tuples.append(north_pole)
    weights.append(sleigh_weight)
    
    dist = 0.0
    prev_stop = north_pole
    prev_weight = sum(weights)
    for i in range(len(tuples)):        
        dist = dist + haversine(tuples[i], prev_stop) * prev_weight
        prev_stop = tuples[i]   
        prev_weight = prev_weight - weights[i]
    return dist

def weighted_reindeer_weariness(all_trips):
    uniq_trips = all_trips.TripId.unique()
    
    if any(all_trips.groupby('TripId').Weight.sum() > weight_limit):
        raise Exception("One of the sleighs over weight limit!")
 
    dist = 0.0
    for t in uniq_trips:
        this_trip = all_trips[all_trips.TripId==t]
        dist = dist + weighted_trip_length(this_trip[['Latitude','Longitude']], this_trip.Weight.tolist())
    
    return dist
