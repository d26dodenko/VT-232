# test_cinema.py

import pytest
from cinema import calculate_ticket_price, MOVIES

# Позитивные тест-кейсы

def test1_adult_full_price():
    # Взрослый, полная цена
    assert calculate_ticket_price("человек-паук: нет пути домой", 30, False, False) == 800.0


def test2_child_half_price():
    # Ребёнок 10 лет, детский тариф
    assert calculate_ticket_price("холодное сердце 3", 10, False, False) == 275.0


def test3_senior_discount():
    # Пенсионер 70 лет, пенсионный тариф
    assert calculate_ticket_price("астрал 6", 70, False, False) == 490.0


def test4_cheapest_movie():
    # Самый дешёвый фильм, взрослый
    assert calculate_ticket_price("последний богатырь. колобок", 30, False, False) == 250.0


def test5_weekend_markup():
    # Выходной день, наценка 15%
    assert calculate_ticket_price("человек-паук: нет пути домой", 30, False, True) == 920.0


# Граничные тест-кейсы

def test6_age_5_free():
    # Возраст 5 лет — бесплатно
    assert calculate_ticket_price("человек-паук: нет пути домой", 5, False, False) == 0.0


def test7_age_6_paid():
    # Возраст 6 лет — уже платно
    assert calculate_ticket_price("человек-паук: нет пути домой", 6, False, False) == 400.0


def test8_age_17_child():
    # Возраст 17 лет — последний детский
    assert calculate_ticket_price("сумерки: сага. новолуние", 17, False, False) == 150.0


def test9_age_18_adult():
    # Возраст 18 лет — первый взрослый
    assert calculate_ticket_price("сумерки: сага. новолуние", 18, False, False) == 300.0


def test10_age_64_adult():
    # Возраст 64 года — последний взрослый
    assert calculate_ticket_price("сумерки: сага. новолуние", 64, False, False) == 300.0


def test11_age_65_senior():
    # Возраст 65 лет — первый пенсионный
    assert calculate_ticket_price("сумерки: сага. новолуние", 65, False, False) == 210.0


def test12_free_and_weekend():
    # Бесплатный билет + выходной — наценка не применяется
    assert calculate_ticket_price("человек-паук: нет пути домой", 5, False, True) == 0.0


# Скидка для студентов

def test13_student_discount():
    # Студент 20 лет — скидка 20%
    assert calculate_ticket_price("сумерки: сага. новолуние", 20, True, False) == 240.0


def test14_student_with_weekend():
    # Студент 20 лет + выходной
    assert calculate_ticket_price("сумерки: сага. новолуние", 20, True, True) == pytest.approx(276.0)


def test15_student_17_no_discount():
    # Студент 17 лет — скидка не применяется (детский тариф)
    assert calculate_ticket_price("сумерки: сага. новолуние", 17, True, False) == 150.0


def test16_student_65_no_discount():
    # Студент 65 лет — скидка не применяется (пенсионный тариф)
    assert calculate_ticket_price("сумерки: сага. новолуние", 65, True, False) == 210.0


# Негативные тест-кейсы

def test17_unknown_movie():
    # Несуществующий фильм
    with pytest.raises(ValueError, match="unknown movie"):
        calculate_ticket_price("гарри поттер и философский камень", 30, False, False)


def test18_empty_movie():
    # Пустое название фильма
    with pytest.raises(ValueError, match="unknown movie"):
        calculate_ticket_price("", 30, False, False)


def test19_negative_age():
    # Отрицательный возраст
    with pytest.raises(ValueError, match="age must be >= 0"):
        calculate_ticket_price("сумерки: сага. новолуние", -1, False, False)


def test20_zero_age():
    # Нулевой возраст — младенец, бесплатно
    assert calculate_ticket_price("сумерки: сага. новолуние", 0, False, False) == 0.0
