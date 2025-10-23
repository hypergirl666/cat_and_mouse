from src.utils.helpers import load_image
from constants import *


class Platform:
    def __init__(self, x, y, width):
        """
        Инициализация платформы
        :param x: Позиция X в мировых координатах
        :param y: Позиция Y в мировых координатах
        :param width: Ширина платформы в пикселях
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT

        # Хитбокс (только верхняя часть платформы)
        self.hitbox_height = PLATFORM_HITBOX_HEIGHT
        self.hitbox_y_offset = PLATFORM_HITBOX_OFFSET

        # Загрузка и подготовка изображения
        self.image = self._create_platform_surface()

    def _create_platform_surface(self):
        """Создает поверхность платформы с тайлами"""
        platform_img = load_image(
            PLATFORM_IMAGE,
            (PLATFORM_WIDTH,
             PLATFORM_HEIGHT),
            assets_dir=ASSETS_DIR)
        tile_width = platform_img.get_width()

        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(0, self.width, tile_width):
            surface.blit(platform_img, (i, 0))
        return surface

    def get_hitbox(self, world_offset):
        """
        Возвращает текущий хитбокс с учетом смещения камеры
        :param world_offset: Смещение мира по X
        :return: pygame.Rect с актуальными координатами
        """
        return pygame.Rect(
            self.x - world_offset,
            self.y + self.hitbox_y_offset,
            self.width,
            self.hitbox_height
        )

    def draw(self, screen, offset_x):
        """
        Отрисовка платформы на экране
        :param screen: Поверхность для отрисовки
        :param offset_x: Смещение мира по X
        """
        screen_x = self.x - offset_x
        screen.blit(self.image, (screen_x, self.y))

        # Отрисовка хитбокса (если включено)
        if SHOW_HITBOXES:
            hitbox = self.get_hitbox(offset_x)
            hitbox_surface = pygame.Surface(
                (hitbox.width, hitbox.height),
                pygame.SRCALPHA
            )
            hitbox_surface.fill(HITBOX_COLOR)
            screen.blit(hitbox_surface, (hitbox.x, hitbox.y))
