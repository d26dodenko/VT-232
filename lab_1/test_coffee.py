import pytest
from coffee import calculate_bonus

# Граница нижнего порога
def test_tc01_zero_purchase():
    assert calculate_bonus(0, False) == 0


def test_tc02_just_below_threshold():
    assert calculate_bonus(299, False) == 0


def test_tc03_exactly_threshold():
    assert calculate_bonus(300, False) == 3


# Диапазон 300–999
def test_tc04_regular_purchase():
    assert calculate_bonus(550, False) == 5


def test_tc05_just_below_1000():
    assert calculate_bonus(999, False) == 9


# Диапазон от 1000
def test_tc06_exactly_1000():
    assert calculate_bonus(1000, False) == 50


def test_tc07_large_purchase():
    assert calculate_bonus(2500, False) == 125


# Владелец карты: удвоение
def test_tc08_card_holder_small():
    assert calculate_bonus(300, True) == 6


def test_tc09_card_holder_large():
    assert calculate_bonus(1000, True) == 100


def test_tc10_card_holder_zero():
    assert calculate_bonus(0, True) == 0


# Негативные сценарии
def test_tc11_negative_amount():
    with pytest.raises(ValueError):
        calculate_bonus(-1, False)


def test_tc12_negative_amount_card_holder():
    with pytest.raises(ValueError):
        calculate_bonus(-100, True)