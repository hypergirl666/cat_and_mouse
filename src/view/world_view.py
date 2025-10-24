import pygame
from src.utils.resource_loader import ResourceLoader
from src.view.hitbox_renderer import HitboxRenderer
from constants import (
    PLATFORM_IMAGE, PLATFORM_WIDTH, PLATFORM_HEIGHT, HITBOX_COLOR
)


class WorldView:
    def __init__(self):
        super().__init__()
        self.platform_img = ResourceLoader.load_image(
            PLATFORM_IMAGE,
            (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        )
        self._hitbox_renderer = HitboxRenderer()

    def draw(self, screen, world) -> None:
        """Отрисовывает все видимые платформы"""
        for platform in world.get_visible_platforms():
            self._draw_platform(screen, platform, world.world_offset)

    def _draw_platform(self, screen, platform, world_offset):
        """Отрисовка одной платформы"""
        # Создаем поверхность платформы с тайлами
        tile_width = self.platform_img.get_width()

        # Приводим ширину платформы к int для range()
        platform_width_int = int(platform.width)
        platform_height_int = int(platform.height)

        surface = pygame.Surface(
            (platform_width_int, platform_height_int),
            pygame.SRCALPHA
        )

        for i in range(0, platform_width_int, tile_width):
            surface.blit(self.platform_img, (i, 0))

        screen_x = int(platform.x - world_offset)
        screen_y = int(platform.y)
        screen.blit(surface, (screen_x, screen_y))

    def draw_hitboxes(self, screen, world) -> None:
        """Отрисовка хитбоксов платформ"""
        for platform in world.get_visible_platforms():
            hitbox = platform.get_hitbox(world.world_offset)
            self._hitbox_renderer.draw_hitbox(screen, hitbox, HITBOX_COLOR)
