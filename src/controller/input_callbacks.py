from abc import ABC, abstractmethod


class IInputCallbacks(ABC):
    """Единый интерфейс для всех callback'ов ввода"""

    @abstractmethod
    def on_jump(self) -> None:
        """Callback для прыжка"""
        pass

    @abstractmethod
    def on_toggle_hitbox(self) -> None:
        """Callback для переключения хитбоксов"""
        pass

    @abstractmethod
    def get_movement(self, can_move_left: bool) -> float:
        """Callback для получения движения"""
        pass
