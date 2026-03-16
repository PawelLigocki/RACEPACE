import pytest
from app.pace import pace_from_time, time_from_pace


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