import googlemaps
import json
from datetime import datetime

def get_travel_duration(location, destination, when, via=None):
    gmaps = googlemaps.Client(key='AIzaSyDNdXDHY511Ykm2fkq3dolQM80LDXtWep0')

    if via is not None:
        via = 'via:' + via

    directions_result = gmaps.directions(
        location,
        destination,
        departure_time=when,
        waypoints=via,
        traffic_model='best_guess'
    )

    normal_duration     = directions_result[0]['legs'][0]['duration']
    duration_in_traffic = directions_result[0]['legs'][0]['duration_in_traffic']

    return {
        "normal": normal_duration["value"],
        "current": duration_in_traffic["value"]
    }

def travel_time_over_threshold(normal, current):
    diff = current - normal
    
    # If current travel time is better than normal, great!
    if diff <= 0:
        return False

    # Otherwise, make sure it's not more than 25% worse than normal
    if diff / normal <= 0.25:
        return False

    # If it is, trigger threshold
    return True