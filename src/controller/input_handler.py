import pygame
from constants import (
    JUMP_KEY,
    TOGGLE_HITBOX_KEY,
    MOVE_RIGHT_KEY,
    MOVE_LEFT_KEY,
    PLAYER_SPEED,
)
from src.controller.input_callbacks import IInputCallbacks


class InputHandler:
    def __init__(
        self,
        callbacks: IInputCallbacks,
    ):
        """
        Инициализация обработчика ввода
        :param callbacks: Объект с callback методами
        """
        self.callbacks = callbacks

    def process_event(self, event) -> None:
        """Обработка отдельных событий"""
        if event.type == pygame.KEYDOWN:
            if event.key == JUMP_KEY:
                self.callbacks.on_jump()
            elif event.key == TOGGLE_HITBOX_KEY:
                self.callbacks.on_toggle_hitbox()

    def get_movement(self, can_move_left: bool) -> float:
        """Получение вектора движения от пользователя"""
        keys = pygame.key.get_pressed()
        movement = 0.0

        if keys[MOVE_RIGHT_KEY]:
            movement = PLAYER_SPEED
        elif keys[MOVE_LEFT_KEY] and can_move_left:
            movement = -PLAYER_SPEED

        return movement
