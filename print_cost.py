# print_cost.py

def calculate_print_cost(quantity: int, is_urgent: bool, is_weekend: bool, is_vip: bool) -> float:
    """
    Расчёт стоимости печати в типографии.

    Бизнес-правила:
    1. Если quantity < 1 — ValueError.
    2. Базовая цена за штуку зависит от тиража:
       - quantity <= 100: 10.0 руб/шт
       - 100 < quantity <= 500: 8.0 руб/шт
       - 500 < quantity <= 1000: 6.0 руб/шт
       - quantity > 1000: 5.0 руб/шт
    3. Если is_weekend=True, наценка 20% (работа в выходной день).
    4. Если is_urgent=True, наценка 50% (срочный заказ).
    5. Если is_vip=True, скидка 10% на итоговую стоимость.
    """
    if quantity < 1:
        raise ValueError("quantity must be >= 1")

    if quantity <= 100:
        price_per_item = 10.0
    elif quantity <= 500:
        price_per_item = 8.0
    elif quantity <= 1000:
        price_per_item = 6.0
    else:
        price_per_item = 5.0

    cost = quantity * price_per_item

    if is_weekend:
        cost *= 1.2
    if is_urgent:
        cost *= 1.5
    if is_vip:
        cost *= 0.9

    return cost