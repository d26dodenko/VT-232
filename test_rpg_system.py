import pytest
from rpg_system import RPGCharacter, CharacterStats


class TestCharacterCreation:

    def test_create_warrior(self):
        char = RPGCharacter("warrior")
        assert char.character_class == "warrior"
        assert char.multiplier == 1.0

    def test_create_mage(self):
        char = RPGCharacter("mage")
        assert char.multiplier == 1.2

    def test_create_rogue(self):
        char = RPGCharacter("rogue")
        assert char.multiplier == 1.5
        assert len(char.achievements) == 0

    def test_invalid_class_raises(self):
        """Неизвестный класс вызывает ошибку"""
        with pytest.raises(ValueError, match="Unknown class"):
            RPGCharacter("necromancer")

# Добавление достижений
class TestAchievements:

    def test_add_single_achievement(self):
        char = RPGCharacter("warrior")
        char.add_achievement("first_blood")
        assert len(char.achievements) == 1
        assert char.achievements[0].name == "first_blood"

    def test_add_multiple_achievements(self):
        char = RPGCharacter("warrior")
        char.add_achievement("first_blood")
        char.add_achievement("treasure_hunter")
        assert len(char.achievements) == 2

    def test_duplicate_achievement_raises(self):
        char = RPGCharacter("warrior")
        char.add_achievement("first_blood")

        with pytest.raises(ValueError, match="already added"):
            char.add_achievement("first_blood")
    # неизвестное достижение
    def test_invalid_achievement_raises(self):
        char = RPGCharacter("warrior")

        with pytest.raises(ValueError, match="Unknown achievement"):
            char.add_achievement("fake_achievement")


class TestStatsCalculation:
    def test_basic_warrior_stats(self):
        char = RPGCharacter("warrior")
        stats = char.calculate_stats(100)

        assert stats.level == 1
        assert stats.base_xp == 100
        assert stats.class_bonus_xp == 0
        assert stats.achievement_bonus_xp == 0
        assert stats.total_effective_xp == 100

    def test_mage_with_class_bonus(self):
        char = RPGCharacter("mage")
        stats = char.calculate_stats(100)

        assert stats.class_bonus_xp == 20  # 100 * 1.2 - 100
        assert stats.total_effective_xp == 120

    def test_rogue_with_achievement(self):
        char = RPGCharacter("rogue")
        char.add_achievement("first_blood")
        stats = char.calculate_stats(200)

        assert stats.achievement_bonus_xp == 50
        assert stats.total_effective_xp == 350  # 200 * 1.5 + 50

# тест границы уровней
class TestLevelBoundaries:

    def test_level_1_boundary(self):
        char = RPGCharacter("warrior")

        stats_below = char.calculate_stats(99)
        assert stats_below.level == 0

        stats_exact = char.calculate_stats(100)
        assert stats_exact.level == 1

    def test_level_2_boundary(self):
        char = RPGCharacter("warrior")

        stats_below = char.calculate_stats(399)
        assert stats_below.level == 1

        stats_exact = char.calculate_stats(400)
        assert stats_exact.level == 2

    def test_level_10(self):
        char = RPGCharacter("warrior")
        stats = char.calculate_stats(10000)
        assert stats.level == 10


class TestMaxLevel:
    # Ровно максимальный уровень
    def test_exactly_max_level(self):
        char = RPGCharacter("warrior")
        stats = char.calculate_stats(1000000)

        assert stats.level == 100
        assert stats.is_max_level is True
        assert stats.xp_to_next_level is None

    # Превышение максимального уровня
    def test_exceeds_max_level(self):
        char = RPGCharacter("warrior")
        stats = char.calculate_stats(2000000)

        assert stats.level == 100
        assert stats.is_max_level is True


class TestNegativeCases:
    # Отрицательный опыт
    def test_negative_xp_raises(self):
        char = RPGCharacter("warrior")

        with pytest.raises(ValueError, match="total_xp must be >= 0"):
            char.calculate_stats(-100)

    # Дробный опыт
    def test_float_xp_raises(self):
        char = RPGCharacter("warrior")

        with pytest.raises(TypeError, match="must be int"):
            char.calculate_stats(100.5)
    # Нулевой опыт
    def test_zero_xp(self):
        char = RPGCharacter("warrior")
        stats = char.calculate_stats(0)

        assert stats.level == 0
        assert stats.total_effective_xp == 0


class TestAllClasses:
    # Все классы проходят валидацию
    def test_all_classes_valid(self):
        classes = ["warrior", "mage", "rogue", "healer"]

        for char_class in classes:
            char = RPGCharacter(char_class)
            stats = char.calculate_stats(1000)
            assert stats.level >= 1