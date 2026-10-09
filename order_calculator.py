PREMIUM_EXTRA_DISCOUNT = 0.05      # дополнительная скидка для premium
FREE_SHIPPING_THRESHOLD = 5000.0   # порог бесплатной доставки
SHIPPING_COST = 350.0              # стоимость доставки


def calculate_order_total(
    subtotal: float,
    is_premium: bool = False,
    promo_discount: float = 0.0,
) -> dict:
    if subtotal < 0:
        raise ValueError("subtotal must be >= 0")
    if not 0.0 <= promo_discount <= 0.5:
        raise ValueError("promo_discount must be in [0, 0.5]")

    # Базовые скидки по сумме заказа
    if subtotal >= 10000:
        base_discount = 0.10
    elif subtotal >= 5000:
        base_discount = 0.05
    else:
        base_discount = 0.0

    # Промокод применяется поверх базовой скидки (суммируется)
    discount = min(base_discount + promo_discount, 0.5)

    # Premium получает дополнительную скидку
    if is_premium:
        discount = min(discount + PREMIUM_EXTRA_DISCOUNT, 0.5)

    discount_amount = round(subtotal * discount, 2)
    total_after_discount = subtotal - discount_amount

    # Бесплатная доставка: по сумме ДО скидки или для premium
    if subtotal >= FREE_SHIPPING_THRESHOLD or is_premium:
        shipping = 0.0
    else:
        shipping = SHIPPING_COST

    total = round(total_after_discount + shipping, 2)

    return {
        "subtotal": subtotal,
        "discount_percent": round(discount * 100, 2),
        "discount_amount": discount_amount,
        "shipping": shipping,
        "total": total,
    }