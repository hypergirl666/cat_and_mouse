import pygame
from typing import Dict, Optional
from constants import SOUNDS_DIR, MUSIC_VOLUME, SOUND_VOLUME


class SoundManager:
    """Менеджер для управления музыкой и звуковыми эффектами"""

    def __init__(self) -> None:
        self._sounds: Dict[str, pygame.mixer.Sound] = {}
        self._current_music: Optional[str] = None
        self._music_volume = MUSIC_VOLUME
        self._sound_volume = SOUND_VOLUME

        # Инициализация микшера
        pygame.mixer.init()

    def load_sound(self, name: str, filename: str) -> None:
        """Загружает звуковой эффект"""
        try:
            sound = pygame.mixer.Sound(f"{SOUNDS_DIR}/{filename}")
            sound.set_volume(self._sound_volume)
            self._sounds[name] = sound
        except pygame.error as e:
            print(f"Ошибка загрузки звука {filename}: {e}")

    def load_music(self, filename: str) -> None:
        """Загружает музыкальный файл (для фоновой музыки)"""
        try:
            pygame.mixer.music.load(f"{SOUNDS_DIR}/{filename}")
            pygame.mixer.music.set_volume(self._music_volume)
        except pygame.error as e:
            print(f"Ошибка загрузки музыки {filename}: {e}")

    def play_sound(self, name: str) -> None:
        """Воспроизводит звуковой эффект"""
        if name in self._sounds:
            self._sounds[name].play()

    def play_music(self, loop: bool = True) -> None:
        """Воспроизводит фоновую музыку"""
        if loop:
            pygame.mixer.music.play(-1)  # -1 означает бесконечный цикл
        else:
            pygame.mixer.music.play()

    def stop_music(self) -> None:
        """Останавливает фоновую музыку"""
        pygame.mixer.music.stop()

    def pause_music(self) -> None:
        """Ставит музыку на паузу"""
        pygame.mixer.music.pause()

    def unpause_music(self) -> None:
        """Продолжает воспроизведение музыки"""
        pygame.mixer.music.unpause()

    def set_music_volume(self, volume: float) -> None:
        """Устанавливает громкость музыки (0.0 - 1.0)"""
        self._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._music_volume)

    def set_sound_volume(self, volume: float) -> None:
        """Устанавливает громкость звуковых эффектов (0.0 - 1.0)"""
        self._sound_volume = max(0.0, min(1.0, volume))
        for sound in self._sounds.values():
            sound.set_volume(self._sound_volume)

    @property
    def music_volume(self) -> float:
        return self._music_volume

    @property
    def sound_volume(self) -> float:
        return self._sound_volume
