# cinema.py

# Доступные фильмы и их цены
MOVIES = {
    "человек-паук: нет пути домой": 800.0,
    "сумерки: сага. новолуние": 300.0,
    "холодное сердце 3": 550.0,
    "последний богатырь. колобок": 250.0,
    "астрал 6": 700.0,
}

# Константы
CHILD_AGE = 6          
ADULT_AGE = 18        
SENIOR_AGE = 65      

CHILD_DISCOUNT = 0.5   
SENIOR_DISCOUNT = 0.3 
STUDENT_DISCOUNT = 0.2 
WEEKEND_MARKUP = 1.15  

def calculate_ticket_price(movie: str, age: int, is_student: bool, is_weekend: bool) -> float:
    """
    Расчёт стоимости билета в кино.

    Доступные фильмы:
    - человек-паук: нет пути домой — 800
    - сумерки: сага. новолуние — 300
    - холодное сердце 3 — 550
    - последний богатырь. колобок — 250
    - астрал 6 — 700

    Бизнес-правила:
    1. Если movie нет в списке — ValueError("unknown movie").
    2. Если age < 0 — ValueError("age must be >= 0").
    3. Если age < 6 — бесплатно.
    4. Если age < 18 — детский тариф: 50% от базовой цены фильма.
    5. Если age >= 65 — пенсионный тариф: 30% от базовой цены.
    6. Иначе — полная цена.
    7. Если is_student=True и 18 <= age < 65 — скидка 20%.
    8. Если is_weekend=True — наценка 15% (кроме бесплатных).
    """
    if movie not in MOVIES:
        raise ValueError("unknown movie")
    if age < 0:
        raise ValueError("age must be >= 0")

    if age < CHILD_AGE:
        return 0.0

    base_price = MOVIES[movie]
    price = base_price

    if age < ADULT_AGE:
        price *= 1 - CHILD_DISCOUNT
    elif age >= SENIOR_AGE:
        price *= 1 - SENIOR_DISCOUNT
    elif is_student:
        price *= 1 - STUDENT_DISCOUNT

    if is_weekend:
        price *= WEEKEND_MARKUP

    return round(price, 2)
