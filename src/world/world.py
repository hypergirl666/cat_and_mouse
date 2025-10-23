import random
from constants import *
from src.entities.platform import Platform


class World:
    def __init__(self):
        """Инициализация игрового мира"""
        self.platforms = []
        self.world_offset = 0  # Смещение мира по горизонтали
        self._generate_initial_platforms()

    def _generate_initial_platforms(self):
        """Генерация стартовых платформ"""
        # Стартовая платформа (под игроком)
        start_y = SCREEN_HEIGHT - 100
        self.platforms.append(Platform(0, start_y, 400))

        # Последующие платформы
        for i in range(1, INITIAL_PLATFORMS + 1):
            x = self.platforms[-1].x + self.platforms[-1].width + random.randint(
                PLATFORM_SPACING_MIN,
                PLATFORM_SPACING_MAX
            )
            y = start_y - (i % 2) * 50  # Через одну платформу выше/ниже
            width = random.randint(MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH)
            self.platforms.append(Platform(x, y, width))

    def _generate_new_platform(self):
        """Генерация одной новой платформы"""
        last_platform = self.platforms[-1]
        new_x = last_platform.x + last_platform.width + random.randint(
            PLATFORM_SPACING_MIN,
            PLATFORM_SPACING_MAX
        )
        new_y = random.randint(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 80)
        new_width = random.randint(MIN_PLATFORM_WIDTH, MAX_PLATFORM_WIDTH)
        return Platform(new_x, new_y, new_width)

    def update(self, player_x_movement):
        """
        Обновление состояния мира
        :param player_x_movement: смещение игрока по X
        """
        self.world_offset += player_x_movement

        # Удаление платформ за левой границей экрана
        self._remove_offscreen_platforms()

        # Генерация новых платформ впереди
        self._generate_ahead_platforms()

    def _remove_offscreen_platforms(self):
        """Удаляет платформы, которые ушли за границу экрана"""
        while (len(self.platforms) > 0 and
               self.platforms[0].x + self.platforms[0].width < self.world_offset - WORLD_OFFSET_MARGIN):
            self.platforms.pop(0)

    def _generate_ahead_platforms(self):
        """Генерирует новые платформы впереди игрока"""
        while (len(self.platforms) < INITIAL_PLATFORMS or
               self.platforms[-1].x < self.world_offset + SCREEN_WIDTH + VISIBLE_PLATFORM_RANGE):
            self.platforms.append(self._generate_new_platform())

    def get_visible_platforms(self):
        """
        Возвращает платформы, которые находятся в зоне видимости
        :return: список Platform объектов
        """
        visible = []
        for platform in self.platforms:
            if (-VISIBLE_PLATFORM_RANGE < platform.x - self.world_offset <
                    SCREEN_WIDTH + VISIBLE_PLATFORM_RANGE):
                visible.append(platform)
        return visible

    def draw(self, screen):
        """Отрисовывает все видимые платформы"""
        for platform in self.get_visible_platforms():
            platform.draw(screen, self.world_offset)
