# src/model/platform_manager.py
from typing import List, Optional
from src.model.platform import Platform
from constants import SCREEN_WIDTH, VISIBLE_PLATFORM_RANGE, WORLD_OFFSET_MARGIN


class PlatformManager:
    """Управляет видимостью и жизненным циклом платформ"""

    def __init__(self, platforms: List[Platform]):
        self._platforms = platforms

    def get_visible_platforms(self, world_offset: float) -> List[Platform]:
        """Возвращает платформы в зоне видимости"""
        visible_platforms = []

        for platform in self._platforms:
            platform_screen_x = platform.x - world_offset

            if (-VISIBLE_PLATFORM_RANGE < platform_screen_x <
                    SCREEN_WIDTH + VISIBLE_PLATFORM_RANGE):
                visible_platforms.append(platform)

        return visible_platforms

    def remove_offscreen_platforms(self,
                                   world_offset: float) -> List[Platform]:
        """Удаляет платформы за левой границей и возвращает удаленные"""
        platforms_to_remove = []

        for platform in self._platforms:
            if (platform.x + platform.width <
                    world_offset - WORLD_OFFSET_MARGIN):
                platforms_to_remove.append(platform)

        for platform in platforms_to_remove:
            self._platforms.remove(platform)

        return platforms_to_remove

    def add_platform(self, platform: Platform) -> None:
        """Добавляет платформу"""
        self._platforms.append(platform)

    def get_last_platform(self) -> Optional[Platform]:
        """Возвращает последнюю платформу"""
        return self._platforms[-1] if self._platforms else None

    @property
    def platforms(self) -> List[Platform]:
        return self._platforms

    @property
    def count(self) -> int:
        return len(self._platforms)
