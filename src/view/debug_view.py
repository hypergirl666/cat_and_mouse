import pygame
from src.view.hitbox_renderer import HitboxRenderer
from constants import DEBUG_TEXT_COLOR
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.utils.sound_manager import SoundManager


class DebugView:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        self._hitbox_renderer = HitboxRenderer()

    def draw(self,
             screen,
             player,
             world,
             game_state,
             sound_manager: Optional['SoundManager'] = None):
        """Отрисовка отладочной информации"""
        debug_text = [
            f"Позиция: {player.world_x:.1f}",
            f"Y: {player.y:.1f}",
            f"Платформ: {world.platform_count}",
            f"Хитбоксы: {'ON' if game_state.show_hitboxes else 'OFF'} (H)",
        ]

        # Добавляем информацию о звуке, если передан sound_manager
        if sound_manager is not None:
            music_status = "ON" if pygame.mixer.music.get_busy() else "OFF"
            sound_status = "ON" if sound_manager.sound_volume > 0 else "OFF"

            debug_text.extend([
                f"Музыка: {music_status} (M)",
                f"Звуки: {sound_status} (N)",
            ])

        for i, text in enumerate(debug_text):
            text_surface = self.font.render(text, True, DEBUG_TEXT_COLOR)
            screen.blit(text_surface, (10, 10 + i * 25))
