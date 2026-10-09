def calculate_parking_fee(hours: int, is_weekend: bool, has_pass: bool) -> float:
    if hours <= 0:
        raise ValueError("hours must be > 0")

    if hours > 24:
        hours = 24

    if has_pass:
        return 0.0

    if hours <= 2:
        cost = 0.0
    else:
        cost = (hours - 2) * 50.0

    if is_weekend:
        cost *= 0.8

    if cost > 1000.0:
        cost = 1000.0

    return cost
