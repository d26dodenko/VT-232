import pytest


def calculate_order_total(items, discount_percent=0, delivery_fee=0):
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid discount")
    subtotal = sum(item["price"] * item["qty"] for item in items)
    discounted = subtotal * (1 - discount_percent / 100.0)
    return round(discounted + delivery_fee, 2)


def test_order_total_basic():
    items = [{"price": 100.0, "qty": 2}, {"price": 50.0, "qty": 1}]
    assert calculate_order_total(items) == 250.0


def test_order_total_with_discount_and_delivery():
    items = [{"price": 200.0, "qty": 1}]
    assert calculate_order_total(items, discount_percent=10, delivery_fee=15.0) == 195.0


def test_order_total_empty_cart():
    assert calculate_order_total([], delivery_fee=10.0) == 10.0


@pytest.mark.parametrize("bad_discount", [-5, 105])
def test_order_total_invalid_discount(bad_discount):
    with pytest.raises(ValueError):
        calculate_order_total([{"price": 10.0, "qty": 1}], discount_percent=bad_discount)
