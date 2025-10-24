from src.model.interfaces import IGameObject, ICollidable
from constants import (
    PLATFORM_HEIGHT, PLATFORM_HITBOX_HEIGHT, PLATFORM_HITBOX_OFFSET
)
import pygame
from typing import Tuple


class Platform(IGameObject, ICollidable):
    def __init__(self, x: float, y: float, width: float):
        """
        Инициализация платформы с полной инкапсуляцией
        """
        # Приватные атрибуты
        self._x = float(x)
        self._y = float(y)
        self._width = float(width)
        self._height = PLATFORM_HEIGHT

        # Хитбокс (только верхняя часть платформы)
        self._hitbox_height = PLATFORM_HITBOX_HEIGHT
        self._hitbox_y_offset = PLATFORM_HITBOX_OFFSET

    # Свойства контролируемого доступа

    @property
    def x(self) -> float:
        """Координата X платформы (только чтение)"""
        return self._x

    @property
    def y(self) -> float:
        """Координата Y платформы (только чтение)"""
        return self._y

    @property
    def width(self) -> float:
        """Ширина платформы (только чтение)"""
        return self._width

    @property
    def height(self) -> float:
        """Высота платформы (только чтение)"""
        return self._height

    # Реализация интерфейса IGameObject

    def update(self, *args, **kwargs) -> None:
        """
        Платформы статичны, поэтому метод пустой
        но должен быть реализован по интерфейсу
        """
        pass

    def get_position(self) -> Tuple[float, float]:
        """IGameObject - возвращает позицию"""
        return self._x, self._y

    def get_rect(self) -> pygame.Rect:
        """IGameObject: возвращает полный прямоугольник"""
        return pygame.Rect(self._x, self._y, self._width, self._height)

    def get_size(self) -> Tuple[float, float]:
        """IGameObject - возвращает размеры"""
        return self._width, self._height

    # Реализация интерфейса ICollidable

    def check_collision(self, other) -> bool:
        """ICollidable - проверка коллизии"""
        if hasattr(other, 'get_rect'):
            other_rect = other.get_rect()
            platform_hitbox = self.get_hitbox(0)  # Без смещения для проверки
            return platform_hitbox.colliderect(other_rect)
        return False

    def handle_collision(self, other) -> None:
        """
        ICollidable - обработка коллизии
        Платформы пассивны, поэтому ничего не делают
        """
        pass

    # Публичные методы

    def get_hitbox(self, world_offset: float = 0) -> pygame.Rect:
        """
        Возвращает текущий хитбокс с учетом смещения камеры
        :param world_offset: Смещение мира по X
        :return: pygame.Rect с актуальными координатами
        """
        return pygame.Rect(
            self._x - world_offset,
            self._y + self._hitbox_y_offset,
            self._width,
            self._hitbox_height,
        )

    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Возвращает границы платформы (x, y, width, height)
        :return: Кортеж с границами
        """
        return self._x, self._y, self._width, self._height

    def contains_point(self, point_x: float, point_y: float) -> bool:
        """
        Проверяет, содержит ли платформа точку
        :param point_x: X координата точки
        :param point_y: Y координата точки
        :return: True если точка внутри платформы
        """
        return (self._x <= point_x <= self._x + self._width and
                self._y <= point_y <= self._y + self._height)

    def distance_to(self, other_platform: 'Platform') -> float:
        """
        Вычисляет расстояние до другой платформы
        :param other_platform: Другая платформа
        :return: Расстояние между центрами платформ
        """
        this_center_x = self._x + self._width / 2
        this_center_y = self._y + self._height / 2
        other_center_x = other_platform.x + other_platform.width / 2
        other_center_y = other_platform.y + other_platform.height / 2

        return ((this_center_x - other_center_x) ** 2 +
                (this_center_y - other_center_y) ** 2) ** 0.5
