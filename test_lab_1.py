import pytest
from lab1 import calculate_cd_order_cost


class TestCdOrderCost:
    """Набор автотестов для проверки бизнес-логики расчёта стоимости заказа."""

    # позитивные тест-кейсы
    def test_base_standard_order(self):
        """Базовый позитивный сценарий"""
        assert calculate_cd_order_cost(5, 300.0, False, False) == 2000.0

    def test_premium_discount(self):
        """Проверка скидки для premium-пользователей"""
        assert calculate_cd_order_cost(5, 300.0, False, True) == 1850.0

    def test_express_delivery(self):
        """Проверка экспресс-доставки"""
        assert calculate_cd_order_cost(5, 300.0, True, False) == 2500.0

    def test_free_delivery_boundary(self):
        """Бесплатная доставка (граничное значение 10)"""
        assert calculate_cd_order_cost(10, 300.0, False, False) == 3000.0

    def test_premium_with_free_delivery(self):
        """Комбинация premium-скидки и бесплатной доставки"""
        assert calculate_cd_order_cost(10, 300.0, False, True) == 2700.0

    # граничные значения
    def test_min_cds_boundary(self):
        """Минимальное количество дисков (1)"""
        assert calculate_cd_order_cost(1, 300.0, False, False) == 800.0

    def test_max_cds_boundary(self):
        """Максимальное количество дисков (50)"""
        assert calculate_cd_order_cost(50, 300.0, False, False) == 15000.0

    def test_just_below_free_delivery(self):
        """Количество дисков на 1 меньше границы бесплатной доставки (9)"""
        assert calculate_cd_order_cost(9, 300.0, False, False) == 3200.0

    # негативные тест-кейсы
    def test_zero_cds(self):
        """Нулевое количество дисков"""
        with pytest.raises(ValueError):
            calculate_cd_order_cost(0, 300.0, False, False)

    def test_exceed_max_cds(self):
        """Превышение максимального лимита дисков"""
        with pytest.raises(ValueError):
            calculate_cd_order_cost(51, 300.0, False, False)

    def test_negative_price(self):
        """Отрицательная цена диска"""
        with pytest.raises(ValueError):
            calculate_cd_order_cost(5, -10.0, False, False)