def riegel_predict(
    known_distance_km: float,
    known_time_minutes: float,
    target_distance_km: float,
) -> float:
    """
    Predict race time using Riegel formula
    """

    if known_distance_km <= 0 or target_distance_km <= 0:
        raise ValueError("Distance must be positive")

    exponent = 1.06

    predicted_time = known_time_minutes * (
        target_distance_km / known_distance_km
    ) ** exponent

    return predicted_time