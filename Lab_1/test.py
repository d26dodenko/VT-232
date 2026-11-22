import pytest
from main import calculate_interest

def test_zero_balance():
    # Нулевой баланс должен вернуть 0.0
    assert calculate_interest(0, 5, 1, False) == 0.0

def test_basic_calculation():
    # Обычный расчет без бонусов
    assert calculate_interest(1000, 10, 1, False) == 1100.0

def test_large_deposit_boundary_below():
    # Баланс чуть ниже 1 млн (бонус не применяется)
    assert calculate_interest(999999.99, 10, 1, False) == 1099999.99

def test_large_deposit_boundary_exact():
    # Ровно 1 млн (применяется бонус +0.5%)
    assert calculate_interest(1000000, 10, 1, False) == 1105000.0

def test_vip_client():
    # VIP клиент (бонус +0.25%)
    assert calculate_interest(1000, 10, 1, True) == 1102.5

def test_vip_and_large_deposit():
    # VIP + Крупный вклад (бонус +0.75%)
    assert calculate_interest(1000000, 10, 1, True) == 1107500.0

def test_min_months():
    # Минимальный срок (1 месяц)
    assert calculate_interest(1000, 10, 1, False) == 1100.0

def test_max_months():
    # Максимальный срок (120 месяцев)
    result = calculate_interest(1000, 10, 120, False)
    assert result > 1000
    assert isinstance(result, float)

def test_negative_balance():
    # Отрицательный баланс
    with pytest.raises(ValueError, match="Balance cannot be negative"):
        calculate_interest(-100, 10, 1, False)

def test_negative_rate():
    # Отрицательная процентная ставка
    with pytest.raises(ValueError, match="Rate cannot be negative"):
        calculate_interest(1000, -5, 1, False)

def test_invalid_months_zero():
    # Срок равен 0
    with pytest.raises(ValueError, match="Months must be an integer between 1 and 120"):
        calculate_interest(1000, 10, 0, False)

def test_invalid_months_too_high():
    # Срок больше 120
    with pytest.raises(ValueError, match="Months must be an integer between 1 and 120"):
        calculate_interest(1000, 10, 121, False)

def test_invalid_months_float():
    # Срок передан как float
    with pytest.raises(ValueError, match="Months must be an integer between 1 and 120"):
        calculate_interest(1000, 10, 1.5, False)