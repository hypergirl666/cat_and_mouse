import pygame
from src.model.game_state import GameState
from src.model.player import Player
from src.model.world import World
from src.controller.input_handler import InputHandler
from src.controller.game_loop import GameLoop
from src.controller.input_callbacks import IInputCallbacks
from src.utils.sound_manager import SoundManager
from constants import (
    BACKGROUND_MUSIC, SOUND_VOLUME,
    TOGGLE_MUSIC_KEY, TOGGLE_SOUND_KEY,
    MOUSE_SCORE
)


class GameController(IInputCallbacks):
    def __init__(self):
        """Инициализация контроллера игры с разделением ответственности"""
        # Модель
        self._game_state = GameState()
        self._player = Player()
        self._world = World()

        # Ввод - теперь передаем self как callback
        self._input_handler = InputHandler(self)

        # Звук
        self._sound_manager = SoundManager()
        self._load_sounds()

        # Временное состояние
        self._current_movement = 0.0
        self._was_on_ground = False
        self._last_mouse_count = 0

    # Свойства для контролируемого доступа

    @property
    def game_state(self) -> GameState:
        """Состояние игры (только чтение)"""
        return self._game_state

    @property
    def player(self) -> Player:
        """Игрок (только чтение)"""
        return self._player

    @property
    def world(self) -> World:
        """Мир (только чтение)"""
        return self._world

    @property
    def input_handler(self) -> InputHandler:
        """Обработчик ввода (только чтение)"""
        return self._input_handler

    @property
    def sound_manager(self) -> SoundManager:
        """Звуки (только чтение)"""
        return self._sound_manager

    # Реализация интерфейса IInputCallbacks

    def _load_sounds(self) -> None:
        """Загружает все звуки и музыку"""

        # Загружаем фоновую музыку
        self._sound_manager.load_music(BACKGROUND_MUSIC)

        # Запускаем музыку
        self._sound_manager.play_music()

    def on_jump(self) -> None:
        """Обработка прыжка"""
        self._player.jump()

    def on_toggle_hitbox(self) -> None:
        """Переключение хитбоксов"""
        self._game_state.toggle_hitboxes()

    def get_movement(self, can_move_left: bool) -> float:
        """Получение вектора движения"""
        return self._input_handler.get_movement(can_move_left)

    # Приватные методы обновления

    def _process_input(self) -> None:
        """Обработка ввода пользователя"""
        # Получаем движение через callback
        self._current_movement = self.get_movement(self._world.can_move_left())

    def _update_world(self) -> None:
        """Обновление состояния мира"""
        self._world.update(self._current_movement)

    def _update_player(self) -> None:
        """Обновление состояния игрока"""
        # Сохраняем предыдущее состояние для определения приземления

        self._player.update(
            self._world.get_visible_platforms(),
            self._current_movement
        )

    def _handle_collisions(self) -> None:
        """Обработка коллизий"""
        had_collision = self._world.check_player_collisions(self._player)

        if had_collision:
            self._sound_manager.play_sound("collision")

        # Проверяем сбор мышей и начисляем очки
        if self._world.collected_mice_count > self._last_mouse_count:
            self._game_state.add_score(MOUSE_SCORE)
            self._sound_manager.play_sound("mouse_collect")
            self._last_mouse_count = self._world.collected_mice_count

    # Публичные методы

    def handle_events(self) -> None:
        """Обработка событий ввода"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_state.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == TOGGLE_MUSIC_KEY:
                    self._toggle_music()
                elif event.key == TOGGLE_SOUND_KEY:
                    self._toggle_sounds()
                else:
                    self._input_handler.process_event(event)

    def _toggle_music(self) -> None:
        """Переключает музыку"""
        if pygame.mixer.music.get_busy():
            self._sound_manager.stop_music()
        else:
            self._sound_manager.play_music()

    def _toggle_sounds(self) -> None:
        """Переключает звуковые эффекты"""
        current_volume = self._sound_manager.sound_volume
        if current_volume > 0:
            self._sound_manager.set_sound_volume(0.0)
        else:
            self._sound_manager.set_sound_volume(SOUND_VOLUME)

    def update(self) -> None:
        """Обновление игровой логики"""
        self._process_input()
        self._update_world()
        self._update_player()
        self._handle_collisions()

    def run(self) -> None:
        """Запуск игры через GameLoop"""
        game_loop = GameLoop(self)
        game_loop.run()

    def reset_game(self) -> None:
        """Сброс игры к начальному состоянию"""
        self._game_state.reset()
        self._player = Player()
        self._world = World()
        self._current_movement = 0.0

    def get_game_info(self) -> dict:
        """
        Возвращает информацию о текущем состоянии игры
        :return: словарь с информацией о игре
        """
        return {
            'player_position': self._player.get_position(),
            'player_velocity_y': self._player.vel_y,
            'player_jumping': self._player.is_jumping,
            'world_offset': self._world.world_offset,
            'platform_count': self._world.platform_count,
            'active_platforms': self._world.active_platform_count,
            'score': self._game_state.score,
            'show_hitboxes': self._game_state.show_hitboxes,
            'running': self._game_state.running
        }
