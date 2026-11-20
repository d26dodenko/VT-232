# Лабораторная работа №1 <br> Составление тест-кейсов для готового кода. Качество ПО и место тестирования в жизненном цикле
## Цель работы
Сформировать системное представление о качестве ПО и роли тестирования в жизненном цикле; приобрести практические навыки проектирования тест-кейсов и написания автотестов на основе готового кода.

**Задачи:**

1. Проанализировать готовый модуль и выделить бизнес-правила, входные и выходные данные, ограничения.
2. Составить набор тест-кейсов: позитивных, негативных, граничных, покрывающих эквивалентные классы.
3. Оформить тест-кейсы по стандартным атрибутам.
4. Реализовать автотесты на Python + pytest.
5. Запустить тесты и зафиксировать результаты.
6. Сделать вывод о связи тестирования, качества ПО и жизненного цикла.

## Задание:

1. Изучить исходный код и выписать все бизнес-правила.
2. Определить:
   - входные параметры;
   - выходной параметр;
   - допустимые и недопустимые значения;
   - граничные значения.
3. Составить **не менее 10 тест-кейсов**:
   - позитивные;
   - негативные;
   - граничные;
   - проверяющие скидку для premium-пользователей;
   - проверяющие бесплатную доставку.
4. Написать автотесты на `pytest`.
5. Запустить тесты командой `pytest -v`.
6. Сделать вывод: какие ветви кода покрыты, какие риски остались, почему тестирование важно для качества.

## Ход работы:
# Исходный код
```python
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
```
# Анализ
**Бизнес-правила:**
1. Тираж должен быть целым числом не меньше 1. Иначе — ValueError.
2. Цена за штуку определяется по диапазонам тиража:
 - до 100 шт. включительно — 10 руб/шт;
 - от 101 до 500 шт. включительно — 8 руб/шт;
 - от 501 до 1000 шт. включительно — 6 руб/шт;
 - свыше 1000 шт. — 5 руб/шт.
3. Заказ в выходной день (is_weekend=True) увеличивает стоимость на 20%.
4. Срочный заказ (is_urgent=True) увеличивает стоимость на 50%.
5. VIP-клиент (is_vip=True) получает скидку 10% на итоговую стоимость.
Наценки и скидка применяются последовательно: сначала выходные, затем срочность, затем VIP.

**Входные параметры:**

- quantity (int) — тираж (количество экземпляров). Допустимые значения: целые числа >= 1. Недопустимые значения: < 1, 0, отрицательные числа.
- is_urgent (bool) — признак срочного заказа. Допустимые значения: True, False.
- is_weekend (bool) — признак работы в выходной день. Допустимые значения: True, False.
- is_vip (bool) — признак VIP-клиента. Допустимые значения: True, False.

**Выходной параметр:**

- cost (float) — итоговая стоимость печати в рублях. При quantity < 1 функция выбрасывает исключение ValueError, выходного значения нет.

**Граничные значения:**

- 1 — минимальный допустимый тираж;
- 100 / 101 — граница перехода с 10 руб/шт на 8 руб/шт;
- 500 / 501 — граница перехода с 8 руб/шт на 6 руб/шт;
- 1000 / 1001 — граница перехода с 6 руб/шт на 5 руб/шт;
- 0 — недопустимое значение (ниже минимума, ValueError);
- -5 — недопустимое значение (отрицательный тираж, ValueError).

# Тесты
**Реализация автотестов**
```python
# test_print_cost.py

import pytest
from print_cost import calculate_print_cost


def test_min_quantity():
    assert calculate_print_cost(1, False, False, False) == 10.0


def test_quantity_100_boundary():
    assert calculate_print_cost(100, False, False, False) == 1000.0


def test_quantity_101_boundary():
    assert calculate_print_cost(101, False, False, False) == 808.0


def test_quantity_500_boundary():
    assert calculate_print_cost(500, False, False, False) == 4000.0


def test_quantity_501_boundary():
    assert calculate_print_cost(501, False, False, False) == 3006.0


def test_quantity_1000_boundary():
    assert calculate_print_cost(1000, False, False, False) == 6000.0


def test_quantity_1001_boundary():
    assert calculate_print_cost(1001, False, False, False) == 5005.0


def test_zero_quantity_raises():
    with pytest.raises(ValueError):
        calculate_print_cost(0, False, False, False)


def test_negative_quantity_raises():
    with pytest.raises(ValueError):
        calculate_print_cost(-5, False, False, False)


def test_urgent_order():
    assert calculate_print_cost(100, True, False, False) == 1500.0


def test_weekend_order():
    assert calculate_print_cost(100, False, True, False) == 1200.0


def test_vip_discount():
    assert calculate_print_cost(100, False, False, True) == 900.0


def test_combined_conditions():
    assert calculate_print_cost(200, True, True, True) == 2592.0
```

**Позитивные:**
- test_min_quantity — минимальный тираж (1 шт.), цена 10 руб/шт, итог 10.0.
- test_urgent_order — срочный заказ на 100 шт., наценка 50%, итог 1500.0.
- test_weekend_order — заказ в выходной день на 100 шт., наценка 20%, итог 1200.0.
- test_vip_discount — VIP-клиент, 100 шт., скидка 10%, итог 900.0.
- test_combined_conditions — комбинация: срочно + выходной + VIP на 200 шт., итог 2592.0.

**Граничные:**
- test_quantity_100_boundary — верхняя граница первого диапазона, 100 шт. по 10 руб, итог 1000.0.
- test_quantity_101_boundary — нижняя граница второго диапазона, 101 шт. по 8 руб, итог 808.0.
- test_quantity_500_boundary — верхняя граница второго диапазона, 500 шт. по 8 руб, итог 4000.0.
- test_quantity_501_boundary — нижняя граница третьего диапазона, 501 шт. по 6 руб, итог 3006.0.
- test_quantity_1000_boundary — верхняя граница третьего диапазона, 1000 шт. по 6 руб, итог 6000.0.
- test_quantity_1001_boundary — первое значение четвёртого диапазона, 1001 шт. по 5 руб, итог 5005.0.

**Негативные:**
- test_zero_quantity_raises — тираж 0, ожидается ValueError.
- test_negative_quantity_raises — тираж -5, ожидается ValueError.

**Покрытие ветвей кода**
- Ветвь quantity < 1 — ValueError покрыта тестами test_zero_quantity_raises и test_negative_quantity_raises.
- Ветвь quantity <= 100 (10 руб/шт) покрыта test_min_quantity, test_quantity_100_boundary, test_urgent_order, test_weekend_order, test_vip_discount.
- Ветвь 100 < quantity <= 500 (8 руб/шт) покрыта test_quantity_101_boundary, test_quantity_500_boundary, test_combined_conditions.
- Ветвь 500 < quantity <= 1000 (6 руб/шт) покрыта test_quantity_501_boundary, test_quantity_1000_boundary.
- Ветвь quantity > 1000 (5 руб/шт) покрыта test_quantity_1001_boundary.
- Наценка is_weekend=True — ×1.2 покрыта test_weekend_order, test_combined_conditions.
- Наценка is_urgent=True — ×1.5 покрыта test_urgent_order, test_combined_conditions.
- Скидка is_vip=True — ×0.9 покрыта test_vip_discount, test_combined_conditions.
- Случай «все флаги False» покрыт базовыми тестами: test_min_quantity, всеми *_boundary, негативными.
Покрыты все ветви if/elif и все три множителя. Порядок применения наценок зафиксирован тестом test_combined_conditions.

## Вывод
Проведённая работа наглядно демонстрирует, что тестирование — неотъемлемая часть жизненного цикла разработки ПО, а не завершающий этап. Модульные тесты, написанные на раннем этапе, позволяют выявлять дефекты бизнес-логики в момент их появления, когда стоимость исправления минимальна: ошибка, найденная на этапе модульного тестирования, обходится на порядки дешевле, чем обнаруженная на этапе интеграции или, тем более, в эксплуатации. 
Автотесты выполняют три ключевые функции: 
1. они документируют ожидаемое поведение функции и служат исполняемой спецификацией;
2. обеспечивают регрессионную защиту — при рефакторинге или изменении требований позволяют быстро убедиться, что существующее поведение не нарушено; 
3. повышают доверие к коду и снижают риск внесения изменений. 
Таким образом, систематическое тестирование напрямую влияет на качество ПО: оно обеспечивает предсказуемость поведения, снижает количество дефектов, ускоряет разработку за счёт раннего обнаружения ошибок и в конечном итоге повышает надёжность продукта на всех этапах его жизненного цикла.