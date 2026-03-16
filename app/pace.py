def pace_from_time(distance_km: float, time_minutes: float) -> float:
    """
    Returns pace (minutes per km)
    """
    if distance_km <= 0:
        raise ValueError("Distance must be greater than zero")

    return time_minutes / distance_km


def time_from_pace(distance_km: float, pace_min_per_km: float) -> float:
    """
    Returns total time in minutes
    """
    if distance_km <= 0:
        raise ValueError("Distance must be greater than zero")

    return distance_km * pace_min_per_km


def required_pace(distance_km: float, target_time_minutes: float) -> float:
    """
    Returns required pace to achieve target time
    """
    if distance_km <= 0:
        raise ValueError("Distance must be greater than zero")

    return target_time_minutes / distance_km