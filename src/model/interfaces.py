import pygame
from abc import ABC, abstractmethod
from typing import Tuple


class IGameObject(ABC):
    """Интерфейс для всех игровых объектов"""

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Обновление состояния объекта"""
        pass

    @abstractmethod
    def get_position(self) -> Tuple[float, float]:
        """Возвращает позицию объекта"""
        pass

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        """Возвращает хитбокс объекта"""
        pass


class ICollidable(ABC):
    """Интерфейс для объектов с коллизиями"""

    @abstractmethod
    def check_collision(self, other) -> bool:
        """Проверка коллизии с другим объектом"""
        pass

    @abstractmethod
    def handle_collision(self, other) -> None:
        """Обработка коллизии"""
        pass

    @abstractmethod
    def get_hitbox(self, world_offset: float = 0) -> pygame.Rect:
        """Возвращает хитбокс для коллизий с учетом смещения мира"""
        pass
