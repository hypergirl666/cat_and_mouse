import pygame
from src.view.hitbox_renderer import HitboxRenderer
from src.utils.resource_loader import ResourceLoader
from constants import (
    PLAYER_IMAGE,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    HITBOX_COLOR,
)


class PlayerView:
    def __init__(self):
        super().__init__()
        self.image = ResourceLoader.load_image(
            PLAYER_IMAGE,
            scale=(PLAYER_WIDTH, PLAYER_HEIGHT)
        )
        self._hitbox_renderer = HitboxRenderer()

    def draw(self, screen, player) -> None:
        """Отрисовывает игрока на экране"""
        # Отрисовка спрайта с учетом направления
        flipped_image = pygame.transform.flip(
            self.image, not player.facing_right, False
        )
        screen.blit(flipped_image, (player.x, player.y))

    def draw_player_hitbox(self, screen, player) -> None:
        """Отрисовка хитбокса игрока"""
        self._hitbox_renderer.draw_hitbox(screen, player.hitbox, HITBOX_COLOR)
