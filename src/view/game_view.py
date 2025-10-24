import pygame
from src.utils.resource_loader import ResourceLoader
from src.view.mouse_view import MouseView
from constants import BACKGROUND_IMAGE, SCREEN_WIDTH, SCREEN_HEIGHT
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.view.player_view import PlayerView
    from src.view.world_view import WorldView
    from src.view.debug_view import DebugView
    from src.model.game_state import GameState
    from src.model.player import Player
    from src.model.world import World


class GameView:
    def __init__(
        self,
        screen: pygame.Surface,
        player_view: 'PlayerView',
        world_view: 'WorldView',
        debug_view: 'DebugView'
    ):
        """
        Инициализация GameView с внедренными зависимостями
        :param screen: Поверхность для отрисовки
        :param player_view: Внедренная зависимость отрисовки игрока
        :param world_view: Внедренная зависимость отрисовки мира
        :param debug_view: Внедренная зависимость отрисовки отладки
        """
        super().__init__()
        self.screen = screen
        self.background = ResourceLoader.load_image(
            BACKGROUND_IMAGE,
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # Внедренные зависимости
        self._player_view = player_view
        self._world_view = world_view
        self._debug_view = debug_view
        self._mouse_view = MouseView()

    def render(
        self,
        game_state: 'GameState',
        player: 'Player',
        world: 'World'
    ) -> None:
        """
        Отрисовка всей игры
        :param game_state: Состояние игры
        :param player: Игрок
        :param world: Мир
        """
        # Фон
        self.screen.blit(self.background, (0, 0))

        # Мир
        self._world_view.draw(self.screen, world)

        # Игрок
        self._player_view.draw(self.screen, player)

        # Хитбоксы и отладка
        if game_state.show_hitboxes:
            self._player_view.draw_player_hitbox(self.screen, player)
            self._world_view.draw_hitboxes(self.screen, world)

        # Мыши
        self._mouse_view.draw(self.screen,
                              world.get_visible_mice(),
                              world.world_offset)

        # Хитбоксы мышей
        if game_state.show_hitboxes:
            self._mouse_view.draw_hitboxes(self.screen,
                                           world.get_visible_mice(),
                                           world.world_offset)

        self._debug_view.draw(self.screen, player, world, game_state)

        pygame.display.flip()

    # === СВОЙСТВА ДЛЯ ДОСТУПА К ЗАВИСИМОСТЯМ ===

    @property
    def player_view(self) -> 'PlayerView':
        """Вью игрока (только чтение)"""
        return self._player_view

    @property
    def world_view(self) -> 'WorldView':
        """Вью мира (только чтение)"""
        return self._world_view

    @property
    def debug_view(self) -> 'DebugView':
        """Вью отладки (только чтение)"""
        return self._debug_view
