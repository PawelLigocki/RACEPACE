import pytest
from app.pace import pace_from_time, time_from_pace, pace_km_to_mile, negative_split
from hypothesis import given, strategies as st
from app.pace import time_to_minutes, minutes_to_time_str


@given(
    distance=st.floats(min_value=0.1, max_value=100),
    time=st.floats(min_value=0.1, max_value=1000),
)
def test_pace_is_always_positive(distance, time):
    from app.pace import pace_from_time

    pace = pace_from_time(distance, time)

    assert pace > 0

def test_pace_calculation():
    pace = pace_from_time(10, 50)
    assert pace == 5


def test_time_from_pace():
    time = time_from_pace(10, 5)
    assert time == 50


@pytest.mark.parametrize(
    "distance,time,expected",
    [
        (5, 25, 5),
        (10, 40, 4),
        (21.1, 105.5, 5),
    ],
)
def test_multiple_pace_cases(distance, time, expected):
    assert pace_from_time(distance, time) == expected


def test_zero_distance():
    with pytest.raises(ValueError):
        pace_from_time(0, 50)

def test_negative_distance():
    with pytest.raises(ValueError):
        pace_from_time(-10, 50)

def test_zero_time():
    with pytest.raises(ValueError):
        pace_from_time(10, 0)

def test_km_to_mile():
    assert round(pace_km_to_mile(5), 2) == 8.05


def test_negative_split():
    first, second = negative_split(100)

    assert first > second
    assert round(first + second) == 100


def test_time_conversion():
    minutes = time_to_minutes(1, 0, 0)
    assert minutes == 60


def test_time_format():
    result = minutes_to_time_str(125)
    assert result == "02:05:00"