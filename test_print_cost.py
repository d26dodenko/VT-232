# test_print_cost.py
import pytest
from print_cost import calculate_print_cost


def test_min_quantity():
    assert calculate_print_cost(1, False, False, False) == 10.0


def test_quantity_100_boundary():
    assert calculate_print_cost(100, False, False, False) == 1000.0


def test_quantity_101_boundary():
    assert calculate_print_cost(101, False, False, False) == 808.0


def test_quantity_500_boundary():
    assert calculate_print_cost(500, False, False, False) == 4000.0


def test_quantity_501_boundary():
    assert calculate_print_cost(501, False, False, False) == 3006.0


def test_quantity_1000_boundary():
    assert calculate_print_cost(1000, False, False, False) == 6000.0


def test_quantity_1001_boundary():
    assert calculate_print_cost(1001, False, False, False) == 5005.0


def test_zero_quantity_raises():
    with pytest.raises(ValueError):
        calculate_print_cost(0, False, False, False)


def test_negative_quantity_raises():
    with pytest.raises(ValueError):
        calculate_print_cost(-5, False, False, False)


def test_urgent_order():
    assert calculate_print_cost(100, True, False, False) == 1500.0


def test_weekend_order():
    assert calculate_print_cost(100, False, True, False) == 1200.0


def test_vip_discount():
    assert calculate_print_cost(100, False, False, True) == 900.0


def test_combined_conditions():
    assert calculate_print_cost(200, True, True, True) == 2592.0