import pytest
from parking import calculate_parking_fee

def test_case_negative_hours():
    with pytest.raises(ValueError, match="hours must be > 0"):
        calculate_parking_fee(-1, False, False)

def test_case_zero_hours():
    with pytest.raises(ValueError):
        calculate_parking_fee(0, False, False)

def test_case_monthly_pass():
    assert calculate_parking_fee(10, False, True) == 0.0

def test_case_standard_rate():
    assert calculate_parking_fee(10, False, False) == 400.0

def test_case_weekend_discount():
    assert calculate_parking_fee(10, True, False) == 320.0

def test_case_free_zone_boundary():
    assert calculate_parking_fee(2, False, False) == 0.0

def test_case_paid_zone_start():
    assert calculate_parking_fee(3, False, False) == 50.0

def test_case_max_cap_weekday():
    assert calculate_parking_fee(24, False, False) == 1000.0

def test_case_max_cap_weekend():
    assert calculate_parking_fee(24, True, False) == 880.0

def test_case_over_24_hours():
    assert calculate_parking_fee(30, False, False) == 1000.0
