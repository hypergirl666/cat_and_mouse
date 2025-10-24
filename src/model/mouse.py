import pygame
from typing import Tuple
from src.model.interfaces import IGameObject, ICollidable
from constants import (
    MOUSE_WIDTH, MOUSE_HEIGHT,
    MOUSE_ANIMATION_AMPLITUDE, MOUSE_ANIMATION_FRAME_DIVISOR,
    MOUSE_ANIMATION_SPEED
)


class Mouse(IGameObject, ICollidable):
    def __init__(self, x: float, y: float):
        """
        Инициализация мыши - собираемого предмета
        """
        self._x = float(x)
        self._y = float(y)
        self._width = MOUSE_WIDTH
        self._height = MOUSE_HEIGHT
        self._collected = False
        self._animation_frame = 0
        self._animation_speed = MOUSE_ANIMATION_SPEED

        # Хитбокс для коллизий
        self._hitbox = pygame.Rect(self._x, self._y, self._width, self._height)

    # Свойства

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def collected(self) -> bool:
        return self._collected

    @property
    def hitbox(self) -> pygame.Rect:
        return self._hitbox

    # Реализция интерфейса IGameObject

    def update(self, *args, **kwargs) -> None:
        """Обновление анимации мыши"""
        if not self._collected:
            # Простая анимация - покачивание вверх-вниз
            self._animation_frame += self._animation_speed  # type: ignore
            if int(self._animation_frame) % MOUSE_ANIMATION_FRAME_DIVISOR == 0:
                self._y += MOUSE_ANIMATION_AMPLITUDE
            else:
                self._y -= MOUSE_ANIMATION_AMPLITUDE
            self._update_hitbox()

    def get_position(self) -> Tuple[float, float]:
        return self._x, self._y

    def get_rect(self) -> pygame.Rect:
        return self._hitbox

    # Реализация интерфейса ICollidable

    def check_collision(self, other) -> bool:
        """Проверка коллизии с другим объектом"""
        if self._collected:
            return False

        if hasattr(other, 'get_rect'):
            other_rect = other.get_rect()
            # Используем текущий хитбокс мыши (без смещения мира)
            return self._hitbox.colliderect(other_rect)
        return False

    def handle_collision(self, other) -> None:
        """Обработка столкновения с игроком"""
        if (not self._collected and
            hasattr(other, '__class__') and
                other.__class__.__name__ == 'Player'):
            self._collected = True

    def get_hitbox(self, world_offset: float = 0) -> pygame.Rect:
        return pygame.Rect(
            self._x - world_offset,
            self._y,
            self._width,
            self._height
        )

    # Приватные методы

    def _update_hitbox(self) -> None:
        self._hitbox = pygame.Rect(self._x, self._y, self._width, self._height)

    # Публичные методы

    def collect(self) -> None:
        """Помечает мышь как собранную"""
        self._collected = True

    def respawn(self, new_x: float, new_y: float) -> None:
        """Перемещает мышь в новую позицию"""
        self._x = new_x
        self._y = new_y
        self._collected = False
        self._update_hitbox()
