<div align="center">

МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ<br>
РОССИЙСКОЙ ФЕДЕРАЦИИ

<br>

ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ

<br>

«БЕЛГОРОДСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНОЛОГИЧЕСКИЙ УНИВЕРСИТЕТ им. В. Г. Шухова»<br>
(БГТУ им. В. Г. Шухова)

<br><br>

ИНСТИТУТ ИНФОРМАЦИОННЫХ ТЕХНОЛОГИЙ И УПРАВЛЯЮЩИХ СИСТЕМ

<br>

Кафедра программного обеспечения вычислительной<br>
техники и автоматизированных систем

<br><br><br><br>

**Лабораторная работа № 1**<br>
по дисциплине: «Тестирование программных систем»<br>
по теме: «Составление тест-кейсов для готового кода. Качество ПО и место тестирования в жизненном цикле»

<br><br><br><br>

</div>

<div align="right">

Выполнилa: ст. группы ВТ-232<br>
Мирошник Елена Владимировна

<br>

Проверил:<br>
Доденко Олег Павлович

</div>

<br><br><br>

<div align="center">

Белгород, 2026 г.

</div>

---

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

#### Задание 1: Изучить исходный код и выписать все бизнес-правила

1. Если `subtotal < 0` — ошибка `ValueError`.
2. Если `promo_discount` вне диапазона `[0.0; 0.5]` — ошибка `ValueError`.
3. Базовая скидка по сумме заказа до скидок:
   - `subtotal < 5000` — 0%;
   - `5000 <= subtotal < 10000` — 5%;
   - `subtotal >= 10000` — 10%.
4. Промокод суммируется с базовой скидкой.
5. Пользователь с `is_premium == True` получает дополнительную скидку 5%.
6. Итоговая скидка не может превышать 50% (`min(discount, 0.5)`).
7. Доставка бесплатна, если `subtotal >= 5000` **или** пользователь premium.
8. В остальных случаях стоимость доставки — 350 рублей.
9. Итоговая сумма считается как `subtotal - discount_amount + shipping`.

#### Задание 2: Определить входные параметры, выходной параметр, допустимые и недопустимые значения, граничные значения

##### Входные параметры

1. `subtotal` — сумма заказа до скидок.
2. `is_premium` — является ли пользователь premium.
3. `promo_discount` — скидка по промокоду.

##### Выходной параметр

- Словарь с полями `subtotal`, `discount_percent`, `discount_amount`, `shipping`, `total`.

##### Допустимые и недопустимые значения

Допустимые значения:

1. `subtotal >= 0`
2. `is_premium == True | is_premium == False`
3. `0.0 <= promo_discount <= 0.5`

Недопустимые значения:

1. `subtotal < 0`
2. `promo_discount < 0.0`
3. `promo_discount > 0.5`

##### Граничные значения

1. `subtotal: 0` — минимальная сумма.
2. `subtotal: 4999.99` — граница бесплатной доставки снизу.
3. `subtotal: 5000` — порог 5% скидки и бесплатной доставки.
4. `subtotal: 9999.99` — верхняя граница 5%-й скидки.
5. `subtotal: 10000` — порог 10%-й скидки.
6. `promo_discount: 0.0` и `0.5` — границы промокода.
7. Итоговая скидка 50% — верхний предел.

#### Задание 3: Составить не менее 10 тест-кейсов

### Таблица тест-кейсов для модуля расчёта стоимости заказа

| ID    | Название тест-кейса                            | Тип        | Входные данные `(subtotal, is_premium, promo_discount)` | Ожидаемый результат |
|:------|:-----------------------------------------------|:-----------|:--------------------------------------------------------|:--------------------|
| TC-01 | Обычный заказ без скидок                       | Позитивный | `(1000, False, 0)`                                      | `discount=0%, shipping=350, total=1350` |
| TC-02 | Базовая скидка 5% на границе                   | Граничный  | `(5000, False, 0)`                                      | `discount=5%, shipping=0, total=4750` |
| TC-03 | Базовая скидка 10% на границе                  | Граничный  | `(10000, False, 0)`                                     | `discount=10%, shipping=0, total=9000` |
| TC-04 | Промокод 20%                                   | Позитивный | `(2000, False, 0.2)`                                    | `discount=20%, total=1950` |
| TC-05 | Premium на маленьком заказе                    | Позитивный | `(100, True, 0)`                                        | `discount=5%, shipping=0, total=95` |
| TC-06 | Premium + промокод + базовая скидка            | Позитивный | `(10000, True, 0.1)`                                    | `discount=25%, total=7500` |
| TC-07 | Ограничение суммарной скидки 50%               | Граничный  | `(10000, True, 0.5)`                                    | `discount=50%, total=5000` |
| TC-08 | Порог бесплатной доставки снизу                | Граничный  | `(4999.99, False, 0)`                                   | `shipping=350` |
| TC-09 | Порог бесплатной доставки сверху               | Граничный  | `(5000, False, 0)`                                      | `shipping=0` |
| TC-10 | Отрицательная сумма заказа                     | Негативный | `(-100, False, 0)`                                      | `ValueError` |
| TC-11 | Промокод больше 0.5                            | Негативный | `(1000, False, 0.6)`                                    | `ValueError` |
| TC-12 | Промокод меньше 0                              | Негативный | `(1000, False, -0.1)`                                   | `ValueError` |

#### Задание 4: Написать автотесты на `pytest`

Исходный код находится в файле `order_calculator.py`.

```python
PREMIUM_EXTRA_DISCOUNT = 0.05
FREE_SHIPPING_THRESHOLD = 5000.0
SHIPPING_COST = 350.0


def calculate_order_total(
    subtotal: float,
    is_premium: bool = False,
    promo_discount: float = 0.0,
) -> dict:
    if subtotal < 0:
        raise ValueError("subtotal must be >= 0")
    if not 0.0 <= promo_discount <= 0.5:
        raise ValueError("promo_discount must be in [0, 0.5]")

    if subtotal >= 10000:
        base_discount = 0.10
    elif subtotal >= 5000:
        base_discount = 0.05
    else:
        base_discount = 0.0

    discount = min(base_discount + promo_discount, 0.5)

    if is_premium:
        discount = min(discount + PREMIUM_EXTRA_DISCOUNT, 0.5)

    discount_amount = round(subtotal * discount, 2)
    total_after_discount = subtotal - discount_amount

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
```

Тесты находятся в файле `test_order_calculator.py`.

```python
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
        assert r["total"] == 1950


class TestPremiumCases:
    def test_premium_free_shipping_small_order(self):
        r = calculate_order_total(100, True, 0)
        assert r["shipping"] == 0
        assert r["discount_percent"] == 5
        assert r["total"] == 95

    def test_premium_with_promo_and_base(self):
        r = calculate_order_total(10000, True, 0.1)
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
```

#### Задание 5: Запустить тесты командой `pytest -v`

```text
py -m pytest -v
test_order_calculator.py::TestPositiveCases::test_no_discount_regular_user PASSED   [  8%]
test_order_calculator.py::TestPositiveCases::test_base_discount_5_percent PASSED    [ 16%]
test_order_calculator.py::TestPositiveCases::test_base_discount_10_percent PASSED   [ 25%]
test_order_calculator.py::TestPositiveCases::test_promo_discount_20 PASSED          [ 33%]
test_order_calculator.py::TestPremiumCases::test_premium_free_shipping_small_order PASSED [ 41%]
test_order_calculator.py::TestPremiumCases::test_premium_with_promo_and_base PASSED [ 50%]
test_order_calculator.py::TestBoundaryCases::test_below_free_shipping_threshold PASSED [ 58%]
test_order_calculator.py::TestBoundaryCases::test_free_shipping_threshold_exact PASSED [ 66%]
test_order_calculator.py::TestBoundaryCases::test_max_discount_capped_50 PASSED     [ 75%]
test_order_calculator.py::TestNegativeCases::test_negative_subtotal_raises PASSED   [ 83%]
test_order_calculator.py::TestNegativeCases::test_promo_greater_than_half_raises PASSED [ 91%]
test_order_calculator.py::TestNegativeCases::test_promo_negative_raises PASSED      [100%]

======================================= 12 passed in 0.07s =======================================
```

#### Задание 6: Сделать вывод: какие ветви кода покрыты, какие риски остались, почему тестирование важно для качества

##### Какие ветви кода покрыты

Покрыты обе ветви валидации входных данных (`ValueError` при некорректном `subtotal` и при некорректном `promo_discount`), все три ветви расчёта базовой скидки (0%, 5%, 10%), ветви применения промокода и надбавки за premium, ограничение итоговой скидки 50%, а также обе ветви определения доставки — бесплатная (по сумме и по статусу premium) и платная.

##### Какие риски остались

- Округление денежных сумм через `round` может приводить к накоплению копеечных расхождений; в промышленной эксплуатации надёжнее использовать `decimal.Decimal`.
- Не проверяется тип входных данных: строка `"1000"` вместо числа вызовет `TypeError` на этапе сравнения `subtotal < 0`, а не понятное `ValueError`.
- Не обрабатываются значения `NaN` и `inf` для `subtotal` и `promo_discount`.
- Не проверяется случай, когда `promo_discount` равен `0.5`, а базовая скидка уже 10%: сумма обрезается до 50%, но это правило не выделено в отдельный тест (покрыто косвенно через TC-07).
- Отсутствуют интеграционные и нагрузочные тесты.

##### Почему тестирование важно для качества

Чем раньше обнаруживается проблема, тем дешевле обходится её исправление. Если баг найден до релиза в прод, его исправление будет значительно дешевле, чем выпуск hotfix или устранение блокеров после развёртывания.

Тесты служат живой документацией: прочитав их, новый разработчик может понять бизнес-логику, не разбираясь в исходниках. Именно поэтому тест-кейсы составляются по бизнес-правилам, а не по коду: это позволяет выявить расхождения между требованиями и реализацией.

Кроме того, написание тестов приводит к уточнению требований. Например, правило «итоговая скидка не может превышать 50%» было явно выделено только после того, как в тест-кейсе TC-07 возникла необходимость зафиксировать поведение на границе. Так тестирование напрямую влияет на качество ПО и на все этапы жизненного цикла — от анализа требований до сопровождения.