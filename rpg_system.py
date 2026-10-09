import math

# Достижение персонажа
class Achievement:

    def __init__(self, name: str, xp_bonus: int):
        self.name = name
        self.xp_bonus = xp_bonus

# Статистика персонажа после расчета
class CharacterStats:

    def __init__(
            self,
            level: int,
            base_xp: int,
            class_bonus_xp: float,
            achievement_bonus_xp: int,
            total_effective_xp: float,
            xp_to_next_level,
            is_max_level: bool,
    ):
        self.level = level
        self.base_xp = base_xp
        self.class_bonus_xp = class_bonus_xp
        self.achievement_bonus_xp = achievement_bonus_xp
        self.total_effective_xp = total_effective_xp
        self.xp_to_next_level = xp_to_next_level
        self.is_max_level = is_max_level

# Класс персонажа
class RPGCharacter:

    MAX_LEVEL = 100
    BASE_XP_PER_LEVEL = 100

    CLASS_MULTIPLIERS = {
        "warrior": 1.0,
        "mage": 1.2,
        "rogue": 1.5,
        "healer": 1.3,
    }

    AVAILABLE_ACHIEVEMENTS = {
        "first_blood": Achievement("first_blood", 50),
        "treasure_hunter": Achievement("treasure_hunter", 150),
        "boss_slayer": Achievement("boss_slayer", 300),
        "speedrunner": Achievement("speedrunner", 200),
    }

    def __init__(self, character_class: str):
        if character_class not in self.CLASS_MULTIPLIERS:
            raise ValueError(
                f"Unknown class: {character_class}. "
                f"Available: {list(self.CLASS_MULTIPLIERS.keys())}"
            )

        self.character_class = character_class
        self.multiplier = self.CLASS_MULTIPLIERS[character_class]
        self.achievements = []
    # Добавить достижение персонажу
    def add_achievement(self, achievement_name: str) -> None:
        if achievement_name not in self.AVAILABLE_ACHIEVEMENTS:
            raise ValueError(f"Unknown achievement: {achievement_name}")

        achievement = self.AVAILABLE_ACHIEVEMENTS[achievement_name]

        # Проверка на дублирование
        for existing in self.achievements:
            if existing.name == achievement.name:
                raise ValueError(f"Achievement '{achievement_name}' already added")

        self.achievements.append(achievement)

    # Валидация опыта
    def _validate_xp(self, total_xp: int) -> None:
        if not isinstance(total_xp, int):
            raise TypeError(f"total_xp must be int, got {type(total_xp).__name__}")
        if total_xp < 0:
            raise ValueError("total_xp must be >= 0")

    # Рассчитать суммарный бонус от достижений
    def _calculate_achievement_bonus(self) -> int:
        total = 0
        for achievement in self.achievements:
            total += achievement.xp_bonus
        return total

    # Рассчитать уровень
    def _calculate_level(self, effective_xp: float) -> int:
        calculated = int(math.sqrt(effective_xp / self.BASE_XP_PER_LEVEL))
        if calculated > self.MAX_LEVEL:
            return self.MAX_LEVEL
        return calculated

    # Рассчитать прогресс до следующего уровня
    def _calculate_xp_progress(self, level: int, effective_xp: float):
        if level >= self.MAX_LEVEL:
            return None

        next_level_xp = (level + 1) ** 2 * self.BASE_XP_PER_LEVEL

        return next_level_xp - effective_xp

    def calculate_stats(self, total_xp: int) -> CharacterStats:
        """
        рассчитать статистику персонажа.
        total_xp: базовый опыт персонажа
        CharacterStats с полной информацией о персонаже
        """
        self._validate_xp(total_xp)

        # Множитель класса
        class_bonus_xp = total_xp * self.multiplier - total_xp

        # Сумма бонусов достижений
        achievement_bonus_xp = self._calculate_achievement_bonus()

        # Итоговый опыт
        total_effective_xp = total_xp + class_bonus_xp + achievement_bonus_xp

        # Рассчитать уровень
        level = self._calculate_level(total_effective_xp)

        # Рассчитать прогресс
        xp_to_next = self._calculate_xp_progress(level, total_effective_xp)

        return CharacterStats(
            level=level,
            base_xp=total_xp,
            class_bonus_xp=class_bonus_xp,
            achievement_bonus_xp=achievement_bonus_xp,
            total_effective_xp=total_effective_xp,
            xp_to_next_level=xp_to_next,
            is_max_level=(level == self.MAX_LEVEL),
        )