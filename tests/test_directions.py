from datetime import datetime
from unittest.mock import patch

from school_run.directions import get_travel_duration, travel_time_over_threshold

mock_result = [
    {
        "summary": "test",
        "legs": [ {
            "start_location": {
                "lat": 41.8507300,
                "lng": -87.6512600
            },
            "end_location": {
                "lat": 41.8525800,
                "lng": -87.6514100
            },
            "polyline": {
                "points": "a~l~Fjk~uOwHJy@P"
            },
            "duration": {
                "value": 19,
                "text": "1 min"
            },
            "duration_in_traffic": {
                "value": 300,
                "text": "5 min"
            },
        }]
    }
]

@patch('school_run.directions.googlemaps.Client')
def test_google_maps_called(gmaps):
    now = datetime.now()
    get_travel_duration("Chicago", "New York", now)
    gmaps.return_value.directions.assert_called_with(
        "Chicago", "New York", departure_time=now, traffic_model="best_guess", waypoints=None
    )

@patch('school_run.directions.googlemaps.Client')
def test_parses_direction_result_correctly(gmaps):
    gmaps.return_value.directions.return_value = mock_result
    duration = get_travel_duration("Chicago", "New York", datetime.now())
    assert duration == { "normal": 19, "current": 300 }

def test_time_over_threshold():
    assert travel_time_over_threshold(60, 120)

def test_time_under_threshold_when_better_than_normal():
    assert travel_time_over_threshold(60, 50) == False

def test_time_under_threshold():
    assert travel_time_over_threshold(60, 70) == False

def test_time_under_threshold():
    assert travel_time_over_threshold(100, 125) == False