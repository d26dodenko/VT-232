# bank_account.py

def calculate_interest(balance: float, rate_percent: float, months: int, is_vip: bool) -> float:
    """
    Расчёт итоговой суммы на счету после начисления процентов.

    Бизнес-правила:
    1. Баланс (balance) не может быть отрицательным. При нарушении — ValueError.
    2. Процентная ставка (rate_percent) не может быть отрицательной. При нарушении — ValueError.
    3. Срок (months) должен быть целым числом от 1 до 120 включительно. При нарушении — ValueError.
    4. Базовая формула: Итог = balance * (1 + rate_percent / 100) ** months
    5. Если баланс >= 1_000_000, клиент получает бонус +0.5% к ставке (rate_percent += 0.5).
    6. Для VIP-клиентов (is_vip=True) применяется дополнительная скидка на комиссию за обслуживание,
       но в данной задаче это выражается в том, что их эффективная ставка увеличивается еще на 0.25%.
    7. Итоговая сумма округляется до 2 знаков после запятой.
    """
    if balance < 0:
        raise ValueError("Balance cannot be negative")
    if rate_percent < 0:
        raise ValueError("Rate cannot be negative")
    if not isinstance(months, int) or months < 1 or months > 120:
        raise ValueError("Months must be an integer between 1 and 120")

    effective_rate = rate_percent

    # Бонус для крупных вкладов
    if balance >= 1_000_000:
        effective_rate += 0.5

    # Бонус для VIP
    if is_vip:
        effective_rate += 0.25

    final_amount = balance * (1 + effective_rate / 100) ** months

    return round(final_amount, 2)