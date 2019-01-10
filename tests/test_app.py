import os

from datetime import datetime
from unittest.mock import patch, call

from school_run.app import lambda_handler

os.environ = {
    "SCHOOL_RUN_FROM": "Wigan",
    "SCHOOL_RUN_TO": "Chorley",
    "SCHOOL_RUN_ALTERNATIVE_VIA": "Atherton, Lancashire",
    "SCHOOL_RUN_ALTERNATIVE_NAME": "Atherton",
}

@patch("school_run.app.get_travel_duration")
def test_handler_gets_directions(get_travel_duration):
    get_travel_duration.side_effect = [
        { "normal": 60, "current": 60 },
        { "normal": 60, "current": 60 }
    ]
    departure_time = datetime.now().replace(hour=8, minute=10, second=0, microsecond=0)
    lambda_handler(None, None)
    get_travel_duration.assert_has_calls([
        call("Wigan", "Chorley", departure_time), 
        call("Wigan", "Chorley", departure_time, via="Atherton, Lancashire")
    ], any_order=False)

@patch("school_run.app.send_sms")
@patch("school_run.app.get_travel_duration")
def test_sends_message_if_first_route_slow(get_travel_duration, send_sms):
    get_travel_duration.side_effect = [
        { "normal": 60, "current": 300 },
        { "normal": 60, "current": 400 }
    ]
    lambda_handler(None, None)
    send_sms.assert_called_with("School run will take longer than normal - estimated 5 minutes.")

@patch("school_run.app.send_sms")
@patch("school_run.app.get_travel_duration")
def test_sends_extra_message_if_alt_route_faster(get_travel_duration, send_sms):
    get_travel_duration.side_effect = [
        { "normal": 60, "current": 500 },
        { "normal": 60, "current": 300 }
    ]

    lambda_handler(None, None)

    expected_message = """School run will take longer than normal - estimated 8 minutes. 
Traval via Atherton could be faster - estimated 5 minutes.""".replace("\n", "").strip()

    send_sms.assert_called_with(expected_message)