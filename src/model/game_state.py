class GameState:
    def __init__(self):
        self._running = True
        self._show_hitboxes = False
        self._score = 0
        self._world_offset = 0.0

    # Свойства для доступа к данным

    @property
    def running(self) -> bool:
        """Состояние работы игры (чтение и запись)"""
        return self._running

    @running.setter
    def running(self, value: bool) -> None:
        """Установка состояния работы игры с валидацией"""
        if not isinstance(value, bool):
            raise ValueError("Running must be a boolean")
        self._running = value

    @property
    def show_hitboxes(self) -> bool:
        """Отображение хитбоксов (чтение и запись)"""
        return self._show_hitboxes

    @show_hitboxes.setter
    def show_hitboxes(self, value: bool) -> None:
        """Установка отображения хитбоксов с валидацией"""
        if not isinstance(value, bool):
            raise ValueError("Show hitboxes must be a boolean")
        self._show_hitboxes = value

    @property
    def score(self) -> int:
        """Счет игры (чтение)"""
        return self._score

    @property
    def world_offset(self) -> float:
        """Смещение мира (чтение)"""
        return self._world_offset

    # Публичные методы для управления состоянием

    def toggle_hitboxes(self) -> None:
        """Переключение отображения хитбоксов"""
        self._show_hitboxes = not self._show_hitboxes

    def add_score(self, points: int) -> None:
        """
        Добавление очков к счету
        :param points: количество очков для добавления
        """
        if not isinstance(points, int):
            raise ValueError("Points must be an integer")
        if points < 0:
            raise ValueError("Points cannot be negative")
        self._score += points

    def reset_score(self) -> None:
        """Сброс счета к нулю"""
        self._score = 0

    def set_world_offset(self, offset: float) -> None:
        """
        Установка смещения мира
        :param offset: новое значение смещения
        """
        if not isinstance(offset, (int, float)):
            raise ValueError("World offset must be a number")
        self._world_offset = float(offset)

    def update_world_offset(self, delta: float) -> None:
        """
        Обновление смещения мира на заданное значение
        :param delta: изменение смещения
        """
        if not isinstance(delta, (int, float)):
            raise ValueError("Delta must be a number")
        self._world_offset += float(delta)

    def reset(self) -> None:
        """Сброс состояния игры к начальным значениям"""
        self._running = True
        self._show_hitboxes = False
        self._score = 0
        self._world_offset = 0.0

    def get_state_info(self) -> dict:
        """
        Возвращает информацию о состоянии игры
        :return: словарь с информацией о состоянии
        """
        return {
            'running': self._running,
            'show_hitboxes': self._show_hitboxes,
            'score': self._score,
            'world_offset': self._world_offset
        }
