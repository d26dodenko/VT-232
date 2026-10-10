
def calculate_cd_order_cost(num_cds: int, price_per_cd: float, is_express: bool, is_premium: bool) -> float:
    """
    Расчёт итоговой стоимости заказа CD-дисков.

    Бизнес-правила:
    1. num_cds должен быть от 1 до 50, price_per_cd >= 0. Иначе ValueError.
    2. Базовая стоимость = num_cds * price_per_cd.
    3. Для premium-пользователей (is_premium=True) скидка 10% на товары.
    4. Доставка:
       - бесплатно, если num_cds >= 10;
       - 1000, если выбрана экспресс-доставка (is_express=True);
       - 500 в остальных случаях.
    """
    if num_cds < 1 or num_cds > 50:
        raise ValueError("num_cds не более 50")
    if price_per_cd < 0:
        raise ValueError("price_per_cd должно быть >= 0")


    base_cost = num_cds * price_per_cd
    if is_premium:
        base_cost *= 0.9  #скидка 10%

    # стоимость доставки
    if num_cds >= 10:
        shipping_cost = 0.0
    elif is_express:
        shipping_cost = 1000.0
    else:
        shipping_cost = 500.0

    return base_cost + shipping_cost