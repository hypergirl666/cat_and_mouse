import pygame
import sys
from src.view.game_view import GameView
from src.view.player_view import PlayerView
from src.view.world_view import WorldView
from src.view.debug_view import DebugView
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, FPS


class GameLoop:
    def __init__(self, game_controller):
        self._game_controller = game_controller
        self._screen = None
        self._clock = None
        self._view = None

    def _initialize_views(self) -> GameView:
        """Инициализация всех view с внедрением зависимостей"""
        player_view = PlayerView()
        world_view = WorldView()
        debug_view = DebugView()

        return GameView(
            screen=self._screen,
            player_view=player_view,
            world_view=world_view,
            debug_view=debug_view
        )

    def _initialize(self) -> None:
        """Инициализация дисплея и view"""
        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self._clock = pygame.time.Clock()
        self._view = self._initialize_views()  # ✅ Внедрение зависимостей

    def _process_events(self) -> None:
        """Обработка всех событий ввода"""
        self._game_controller.handle_events()

    def _update_game(self) -> None:
        """Обновление игровой логики"""
        self._game_controller.update()

    def _render_frame(self) -> None:
        """Отрисовка кадра"""
        self._view.render(
            self._game_controller.game_state,
            self._game_controller.player,
            self._game_controller.world
        )

    def run(self) -> None:
        """Запуск главного игрового цикла"""
        if not self._screen:
            self._initialize()

        while self._game_controller.game_state.running:
            self._process_events()
            self._update_game()
            self._render_frame()
            self._clock.tick(FPS)

        pygame.quit()
        sys.exit()
