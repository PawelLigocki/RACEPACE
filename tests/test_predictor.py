import pytest
from app.predictor import riegel_predict


def test_predict_longer_distance():
    result = riegel_predict(5, 25, 10)

    assert result > 50


def test_same_distance():
    result = riegel_predict(10, 50, 10)

    assert round(result, 2) == 50

def test_half_marathon_prediction_realistic():
    result = riegel_predict(10, 50, 21.1)

    assert result > 100
    assert result < 130

@pytest.mark.parametrize(
    "d1,t1,d2",
    [
        (5, 25, 10),
        (10, 50, 21.1),
        (21.1, 105, 42.2),
    ],
)
def test_prediction_positive(d1, t1, d2):
    result = riegel_predict(d1, t1, d2)

    assert result > 0
