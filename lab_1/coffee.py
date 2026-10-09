# Начисление бонусных баллов в кофейне
def calculate_bonus(purchase_amount: float, is_card_holder: bool) -> int:

    if purchase_amount < 0:
        raise ValueError("purchase_amount must be >= 0")

    if purchase_amount < 300:
        bonus = 0
    elif purchase_amount < 1000:
        bonus = int(purchase_amount // 100)
    else:
        bonus = int(purchase_amount * 0.05)

    if is_card_holder:
        bonus *= 2

    return bonus