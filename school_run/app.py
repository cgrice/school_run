import os
import humanize
from datetime import datetime, timedelta

from school_run.directions import get_travel_duration, travel_time_over_threshold
from school_run.notifications import send_sms

def lambda_handler(event, context):
    start_location = os.environ.get("SCHOOL_RUN_FROM", "Manchester")
    end_location   = os.environ.get("SCHOOL_RUN_TO", "Liverpool")
    via_waypoint   = os.environ.get("SCHOOL_RUN_ALTERNATIVE_VIA", "Bolton")
    alt_route_name = os.environ.get("SCHOOL_RUN_ALTERNATIVE_NAME", "Bolton")

    # Request directions via public transit
    # tomorrow = datetime.today() + timedelta(days=1)
    departure_time = datetime.now().replace(hour=8, minute=10, second=0, microsecond=0)
    # departure_time = tomorrow.replace(day=15, hour=8, minute=10, second=0, microsecond=0)
    
    route_one = get_travel_duration(start_location, end_location, departure_time)
    route_two = get_travel_duration(start_location, end_location, departure_time, via=via_waypoint)
    
    print(route_one, route_two)

    if travel_time_over_threshold(route_one["normal"], route_one["current"]):
        travel_time = humanize.naturaldelta(
            timedelta(seconds=route_one["current"])
        )

        message = "School run will take longer than normal - estimated %s." % travel_time

        if route_two["current"] < route_one["current"]:
            alt_travel_time = humanize.naturaldelta(
                timedelta(seconds=route_two["current"])
            )
            message = message + " Traval via %s could be faster - estimated %s." % (alt_route_name, alt_travel_time)

        send_sms(message)






