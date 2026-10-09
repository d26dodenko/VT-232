import pytest
from order_calculator import calculate_order_total


class TestPositiveCases:
    def test_no_discount_regular_user(self):
        r = calculate_order_total(1000, False, 0)
        assert r["discount_percent"] == 0
        assert r["shipping"] == 350
        assert r["total"] == 1350

    def test_base_discount_5_percent(self):
        r = calculate_order_total(5000, False, 0)
        assert r["discount_percent"] == 5
        assert r["shipping"] == 0
        assert r["total"] == 4750

    def test_base_discount_10_percent(self):
        r = calculate_order_total(10000, False, 0)
        assert r["discount_percent"] == 10
        assert r["total"] == 9000

    def test_promo_discount_20(self):
        r = calculate_order_total(2000, False, 0.2)
        assert r["discount_percent"] == 20
        assert r["total"] == 1950  # 1600 + 350 доставка


class TestPremiumCases:
    def test_premium_free_shipping_small_order(self):
        r = calculate_order_total(100, True, 0)
        assert r["shipping"] == 0
        assert r["discount_percent"] == 5
        assert r["total"] == 95

    def test_premium_with_promo_and_base(self):
        r = calculate_order_total(10000, True, 0.1)
        # 10% база + 10% промо + 5% premium = 25%
        assert r["discount_percent"] == 25
        assert r["total"] == 7500


class TestBoundaryCases:
    def test_below_free_shipping_threshold(self):
        r = calculate_order_total(4999.99, False, 0)
        assert r["shipping"] == 350

    def test_free_shipping_threshold_exact(self):
        r = calculate_order_total(5000, False, 0)
        assert r["shipping"] == 0

    def test_max_discount_capped_50(self):
        r = calculate_order_total(10000, True, 0.5)
        # 10 + 50 + 5 => должно быть обрезано до 50%
        assert r["discount_percent"] == 50
        assert r["total"] == 5000


class TestNegativeCases:
    def test_negative_subtotal_raises(self):
        with pytest.raises(ValueError):
            calculate_order_total(-100, False, 0)

    def test_promo_greater_than_half_raises(self):
        with pytest.raises(ValueError):
            calculate_order_total(1000, False, 0.6)

    def test_promo_negative_raises(self):
        with pytest.raises(ValueError):
            calculate_order_total(1000, False, -0.1)