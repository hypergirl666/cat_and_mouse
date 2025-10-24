import pygame
from typing import List, TYPE_CHECKING
from src.utils.resource_loader import ResourceLoader
from src.view.hitbox_renderer import HitboxRenderer
from constants import MOUSE_IMAGE, MOUSE_SCALE, HITBOX_COLOR

if TYPE_CHECKING:
    from src.model.mouse import Mouse


class MouseView:
    def __init__(self):
        self.image = ResourceLoader.load_image(MOUSE_IMAGE, scale=MOUSE_SCALE)
        self._hitbox_renderer = HitboxRenderer()

    def draw(self,
             screen: pygame.Surface, mice: List['Mouse'],
             world_offset: float) -> None:
        """Отрисовывает всех видимых мышей"""
        for mouse in mice:
            if not mouse.collected:
                self._draw_mouse(screen, mouse, world_offset)

    def _draw_mouse(self,
                    screen: pygame.Surface,
                    mouse: 'Mouse',
                    world_offset: float) -> None:
        """Отрисовка одной мыши"""
        screen_x = int(mouse.x - world_offset)
        screen_y = int(mouse.y)
        screen.blit(self.image, (screen_x, screen_y))

    def draw_hitboxes(self,
                      screen: pygame.Surface, mice: List['Mouse'],
                      world_offset: float) -> None:
        """Отрисовка хитбоксов мышей"""
        for mouse in mice:
            if not mouse.collected:
                hitbox = mouse.get_hitbox(world_offset)
                self._hitbox_renderer.draw_hitbox(screen, hitbox, HITBOX_COLOR)
