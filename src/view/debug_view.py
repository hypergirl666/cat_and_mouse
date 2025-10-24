import pygame
from src.view.hitbox_renderer import HitboxRenderer
from constants import (
    DEBUG_TEXT_COLOR, DEBUG_FONT_NAME,
    DEBUG_FONT_SIZE, DEBUG_LINE_SPACING,
    DEBUG_MARGIN
)
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.utils.sound_manager import SoundManager


class DebugView:
    def __init__(self):
        self.font = pygame.font.SysFont(DEBUG_FONT_NAME, DEBUG_FONT_SIZE)
        self._hitbox_renderer = HitboxRenderer()
        self._line_spacing = DEBUG_LINE_SPACING
        self._margin = DEBUG_MARGIN

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
            f"Активных мышей: {world.active_mice_count}",
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
            screen.blit(text_surface, (self._margin,
                                       self._margin + i * self._line_spacing))
