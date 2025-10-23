# src/model/world.py (переработанный)
from typing import List
from src.model.platform import Platform
from src.model.platform_generator import PlatformGenerator
from src.model.platform_manager import PlatformManager
from constants import SCREEN_WIDTH, INITIAL_PLATFORMS, VISIBLE_PLATFORM_RANGE


class World:
    def __init__(self) -> None:
        """Инициализация игрового мира с разделением ответственности"""
        self._world_offset: float = 0

        # Композиция вместо наследования
        self._platform_generator = PlatformGenerator()
        initial_platforms = (
            self._platform_generator.generate_initial_platforms()
            )
        self._platform_manager = PlatformManager(initial_platforms)

    @property
    def world_offset(self) -> float:
        return self._world_offset

    @world_offset.setter
    def world_offset(self, value: float) -> None:
        self._world_offset = float(value)

    @property
    def platform_count(self) -> int:
        return self._platform_manager.count

    @property
    def active_platform_count(self) -> int:
        return len(self.get_visible_platforms())

    def get_platforms(self) -> List[Platform]:
        return self._platform_manager.platforms.copy()

    def get_visible_platforms(self) -> List[Platform]:
        return self._platform_manager.get_visible_platforms(self._world_offset)

    def update(self, player_x_movement: float) -> None:
        """Обновление состояния мира"""
        # Обновляем смещение мира
        self.world_offset += player_x_movement

        # Удаление платформ за левой границей
        self._platform_manager.remove_offscreen_platforms(self._world_offset)

        # Генерация новых платформ впереди
        self._generate_ahead_platforms()

        # Обновление всех платформ
        self._update_all_platforms()

    def _generate_ahead_platforms(self) -> None:
        """Генерирует новые платформы впереди игрока"""
        while self._need_more_platforms():
            last_platform = self._platform_manager.get_last_platform()
            new_platform = (
                self._platform_generator.generate_platform(last_platform)
            )
            self._platform_manager.add_platform(new_platform)

    def _need_more_platforms(self) -> bool:
        """Проверяет, нужно ли генерировать больше платформ"""
        if self._platform_manager.count < INITIAL_PLATFORMS:
            return True

        last_platform = self._platform_manager.get_last_platform()
        if not last_platform:
            return True

        return (last_platform.x + last_platform.width <
                self._world_offset + SCREEN_WIDTH + VISIBLE_PLATFORM_RANGE)

    def _update_all_platforms(self) -> None:
        """Обновляет все платформы"""
        for platform in self._platform_manager.platforms:
            platform.update()

    # Остальные методы (коллизии и т.д.) остаются в World
    def check_player_collisions(self, player) -> bool:
        """Проверяет коллизии игрока с платформами"""
        had_collision = False

        for platform in self.get_visible_platforms():
            if player.check_collision(platform):
                player.handle_collision(platform)
                platform.handle_collision(player)
                had_collision = True

        return had_collision

    def can_move_left(self) -> bool:
        return self._world_offset > 0
