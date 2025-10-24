import pygame
from typing import Tuple, List
from src.model.interfaces import IGameObject, ICollidable
from constants import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_POWER,
    PLAYER_GRAVITY, PLAYER_HITBOX_WIDTH, PLAYER_HITBOX_HEIGHT,
    PLAYER_HITBOX_OFFSET_X, PLAYER_HITBOX_OFFSET_Y,
    SCREEN_HEIGHT, PLAYER_INITIAL_Y,
    PLAYER_INITIAL_X
)


class Player(IGameObject, ICollidable):
    def __init__(self):
        """Инициализация игрока (кота) с инкапсуляцией"""
        # Приватные атрибуты
        self._width = PLAYER_WIDTH
        self._height = PLAYER_HEIGHT
        self._x = PLAYER_INITIAL_X
        self._y = PLAYER_INITIAL_Y
        self._speed = PLAYER_SPEED
        self._jump_power = PLAYER_JUMP_POWER
        self._gravity = PLAYER_GRAVITY
        self._vel_y = 0
        self._is_jumping = False
        self._facing_right = True
        self._world_x = 0

        # Хитбокс игрока
        self._hitbox_width = PLAYER_HITBOX_WIDTH
        self._hitbox_height = PLAYER_HITBOX_HEIGHT
        self._hitbox_offset_x = PLAYER_HITBOX_OFFSET_X
        self._hitbox_offset_y = PLAYER_HITBOX_OFFSET_Y
        self._hitbox = None
        self._update_hitbox()

    # Свойства контролируемого доступа

    @property
    def width(self) -> int:
        """Ширина игрока (только чтение)"""
        return self._width

    @property
    def height(self) -> int:
        """Высота игрока (только чтение)"""
        return self._height

    @property
    def x(self) -> float:
        """Экранная координата X (чтение и запись)"""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Установка X с валидацией и обновлением хитбокса"""
        if not isinstance(value, (int, float)):
            raise ValueError("X coordinate must be a number")
        self._x = float(value)
        self._update_hitbox()

    @property
    def y(self) -> float:
        """Экранная координата Y (чтение и запись)"""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Установка Y с валидацией и обновлением хитбокса"""
        if not isinstance(value, (int, float)):
            raise ValueError("Y coordinate must be a number")
        self._y = float(value)
        self._update_hitbox()

    @property
    def world_x(self) -> float:
        """Мировая координата X (чтение и запись)"""
        return self._world_x

    @world_x.setter
    def world_x(self, value: float) -> None:
        """Установка мировой координаты X с валидацией"""
        if not isinstance(value, (int, float)):
            raise ValueError("World X must be a number")
        self._world_x = float(value)

    @property
    def vel_y(self) -> float:
        """Вертикальная скорость (чтение и запись)"""
        return self._vel_y

    @vel_y.setter
    def vel_y(self, value: float) -> None:
        """Установка вертикальной скорости с валидацией"""
        if not isinstance(value, (int, float)):
            raise ValueError("Velocity must be a number")
        self._vel_y = float(value)

    @property
    def is_jumping(self) -> bool:
        """Состояние прыжка (чтение и запись)"""
        return self._is_jumping

    @is_jumping.setter
    def is_jumping(self, value: bool) -> None:
        """Установка состояния прыжка с валидацией"""
        if not isinstance(value, bool):
            raise ValueError("is_jumping must be boolean")
        self._is_jumping = value

    @property
    def facing_right(self) -> bool:
        """Направление взгляда (чтение и запись)"""
        return self._facing_right

    @facing_right.setter
    def facing_right(self, value: bool) -> None:
        """Установка направления взгляда с валидацией"""
        if not isinstance(value, bool):
            raise ValueError("facing_right must be boolean")
        self._facing_right = value

    @property
    def hitbox(self) -> pygame.Rect:
        """Хитбокс игрока (только чтение)"""
        return self._hitbox

    # Приватные методы

    def _update_hitbox(self) -> None:
        """Обновляет позицию хитбокса игрока"""
        self._hitbox = pygame.Rect(
            self._x + self._hitbox_offset_x,
            self._y + self._hitbox_offset_y,
            self._hitbox_width,
            self._hitbox_height,
        )

    def _resolve_platform_collision(self,
                                    platform_hitbox: pygame.Rect) -> bool:
        """
        Обрабатывает коллизию с одной платформой
        :param platform_hitbox: Хитбокс платформы
        :return: True если игрок приземлился на платформу
        """
        on_ground = False

        if self._hitbox.colliderect(platform_hitbox):
            # Приземление на платформу
            if self._vel_y > 0 and self._hitbox.bottom > platform_hitbox.top:
                self.y = (platform_hitbox.top -
                          (self._hitbox_offset_y + self._hitbox_height))
                self.vel_y = 0
                self.is_jumping = False
                on_ground = True
            # Удар головой о платформу снизу
            elif self._vel_y < 0 and self._hitbox.top < platform_hitbox.bottom:
                self.y = platform_hitbox.bottom - self._hitbox_offset_y
                self.vel_y = 0

        return on_ground

    def _apply_gravity(self) -> None:
        """Применяет гравитацию к игроку"""
        self.vel_y += self._gravity
        self.y += self._vel_y

    def _check_screen_bounds(self, on_ground: bool) -> None:
        """Проверяет выход за границы экрана"""
        if self.y > SCREEN_HEIGHT - self._height and not on_ground:
            self.y = SCREEN_HEIGHT - self._height
            self.vel_y = 0
            self.is_jumping = False

    # Реализация интерфейса IGameObject

    def update(self, platforms: List, x_movement: float = 0) -> None:
        """
        Обновляет состояние игрока - ТОЛЬКО ЛОГИКА
        :param platforms: Список активных платформ
        :param x_movement: Движение по X
        """
        # Обновляем мировую позицию
        self.world_x += x_movement

        # Применяем гравитацию
        self._apply_gravity()

        # Проверка коллизий с платформами
        on_ground = False
        for platform in platforms:
            platform_hitbox = platform.get_hitbox(self.world_x)
            on_ground = (self._resolve_platform_collision(platform_hitbox) or
                         on_ground)

        # Проверка выхода за границы экрана
        self._check_screen_bounds(on_ground)

    def get_position(self) -> Tuple[float, float]:
        """IGameObject - возвращает позицию (экранные координаты)"""
        return self._x, self._y

    def get_rect(self) -> pygame.Rect:
        """IGameObject - возвращает хитбокс"""
        return self._hitbox

    # Реализация интерфейса ICollidable

    def check_collision(self, other) -> bool:
        """ICollidable - проверка коллизии"""
        if hasattr(other, 'get_hitbox'):
            # Для платформ используем их метод get_hitbox
            other_hitbox = other.get_hitbox(self.world_x)
            return self._hitbox.colliderect(other_hitbox)
        elif hasattr(other, 'get_rect'):
            # Для других объектов используем get_rect
            return self._hitbox.colliderect(other.get_rect())
        return False

    def handle_collision(self, other) -> None:
        """ICollidable - обработка коллизии"""
        # Базовая реализация - можно расширить для разных типов объектов
        if hasattr(other, 'get_hitbox'):
            other_hitbox = other.get_hitbox(self.world_x)
            self._resolve_platform_collision(other_hitbox)

    def get_hitbox(self, world_offset: float = 0) -> pygame.Rect:
        """
        ICollidable - возвращает хитбокс для коллизий
        :param world_offset: Смещение мира (игнорируется)
        :return: pygame.Rect с хитбоксом игрока
        """
        return self._hitbox

    # Публичные методы

    def jump(self) -> None:
        """Выполняет прыжок, если игрок на земле"""
        if not self.is_jumping:
            self.vel_y = -self._jump_power
            self.is_jumping = True

    def move(self, direction: int) -> float:
        """
        Устанавливает направление движения
        :param direction: 1 (вправо) или -1 (влево)
        :return: величина движения
        """
        self.facing_right = direction > 0
        return direction * self._speed
