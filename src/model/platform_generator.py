# src/model/platform_generator.py
import random
from typing import List
from src.model.platform import Platform
from constants import (
    PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX,
    MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH,
    PLATFORM_START_Y, PLATFORM_HEIGHT_VARIATION,
    PLATFORM_Y_RANGE_MIN, PLATFORM_Y_RANGE_MAX,
    START_PLATFORM_WIDTH, INITIAL_PLATFORMS,
    PLATFORM_ALTERNATION_PATTERN, PLATFORM_ALTERNATION_MULTIPLIER
)


class PlatformGenerator:
    """Отвечает за генерацию платформ"""

    def __init__(self):
        pass

    def generate_initial_platforms(self) -> List[Platform]:
        """Генерация стартовых платформ"""
        platforms = []

        # Стартовая платформа
        start_platform = Platform(0, PLATFORM_START_Y, START_PLATFORM_WIDTH)
        platforms.append(start_platform)

        # Последующие платформы
        for i in range(1, INITIAL_PLATFORMS + 1):
            last_platform = platforms[-1]

            x = (
                last_platform.x
                + last_platform.width
                + random.randint(PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX)
            )

            y = (PLATFORM_START_Y -
                 (i % PLATFORM_ALTERNATION_PATTERN) *
                 PLATFORM_HEIGHT_VARIATION *
                 PLATFORM_ALTERNATION_MULTIPLIER)
            width = random.randint(MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH)

            new_platform = Platform(x, y, width)
            platforms.append(new_platform)

        return platforms

    def generate_platform(self, last_platform: Platform) -> Platform:
        """Генерация одной новой платформы после последней"""
        new_x = (
            last_platform.x
            + last_platform.width
            + random.randint(PLATFORM_SPACING_MIN, PLATFORM_SPACING_MAX)
        )

        new_y = random.randint(PLATFORM_Y_RANGE_MIN, PLATFORM_Y_RANGE_MAX)
        new_width = random.randint(MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH)

        return Platform(new_x, new_y, new_width)
