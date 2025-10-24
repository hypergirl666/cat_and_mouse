import random
from typing import List
from src.model.mouse import Mouse
from constants import (
    SCREEN_WIDTH,
    MOUSE_SPAWN_OFFSET_Y,
    MOUSE_SPAWN_MARGIN,
    MOUSE_SPAWN_INTERVAL,
    MOUSE_REMOVE_OFFSET
)


class MouseManager:
    """Управляет созданием, удалением и обновлением мышей"""

    def __init__(self) -> None:
        self._mice: List[Mouse] = []
        self._collected_count = 0
        self._spawn_timer = 0
        self._spawn_interval = MOUSE_SPAWN_INTERVAL

    def update(self, world_offset: float, platforms: List) -> None:
        """Обновляет состояние всех мышей"""
        # Обновляем существующих мышей
        for mouse in self._mice:
            mouse.update()

        # Удаляем собранные мыши
        self._remove_collected_mice()

        # Удаляем мыши за экраном
        self._remove_offscreen_mice(world_offset)

        # Спавним новые мыши
        self._spawn_timer += 1
        if self._spawn_timer >= self._spawn_interval:
            self._spawn_mouse(world_offset, platforms)
            self._spawn_timer = 0

    def _spawn_mouse(self, world_offset: float, platforms: List) -> None:
        """Создает новую мышь на случайной платформе"""
        if not platforms:
            return

        # Выбираем случайную платформу
        platform = random.choice(platforms)

        # Позиция на платформе (сверху)
        x = platform.x + random.randint(
            MOUSE_SPAWN_MARGIN,
            int(platform.width) - MOUSE_SPAWN_MARGIN
        )
        y = platform.y + MOUSE_SPAWN_OFFSET_Y  # Над платформой

        # Проверяем, чтобы мышь была на экране
        if x > world_offset and x < world_offset + SCREEN_WIDTH:
            new_mouse = Mouse(x, y)
            self._mice.append(new_mouse)

    def _remove_collected_mice(self) -> None:
        """Удаляет собранные мыши"""
        mice_to_remove = [mouse for mouse in self._mice if mouse.collected]
        for mouse in mice_to_remove:
            self._mice.remove(mouse)
            self._collected_count += 1

    def _remove_offscreen_mice(self, world_offset: float) -> None:
        """Удаляет мышей, которые ушли за левую границу экрана"""
        mice_to_remove = []

        for mouse in self._mice:
            mouse_x, mouse_y = mouse.get_position()
            screen_x = mouse_x - world_offset

            if screen_x < -MOUSE_REMOVE_OFFSET:
                mice_to_remove.append(mouse)

        for mouse in mice_to_remove:
            self._mice.remove(mouse)

    def check_collisions(self, player) -> bool:
        """Проверяет коллизии игрока с мышами"""
        had_collision = False

        for mouse in self._mice:
            if not mouse.collected and mouse.check_collision(player):
                mouse.collect()
                player.handle_collision(mouse)
                had_collision = True

        return had_collision

    def get_visible_mice(self, world_offset: float) -> List[Mouse]:
        """Возвращает мышей в зоне видимости"""
        visible_mice = []

        for mouse in self._mice:
            mouse_x, mouse_y = mouse.get_position()
            screen_x = mouse_x - world_offset

            if (-MOUSE_REMOVE_OFFSET <
                screen_x <
                    SCREEN_WIDTH + MOUSE_REMOVE_OFFSET):
                visible_mice.append(mouse)

        return visible_mice

    # Свойства

    @property
    def mice(self) -> List[Mouse]:
        return self._mice.copy()

    @property
    def collected_count(self) -> int:
        return self._collected_count

    @property
    def active_mice_count(self) -> int:
        return len([mouse for mouse in self._mice if not mouse.collected])
