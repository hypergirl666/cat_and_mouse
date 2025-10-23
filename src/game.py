import sys
from src.entities.player import Player
from src.world.world import World
from src.utils.helpers import load_image
from constants import *


class Game:
    def __init__(self):
        """Инициализация игры"""
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Загрузка ресурсов
        self.background = load_image(
            BACKGROUND_IMAGE,
            (SCREEN_WIDTH,
             SCREEN_HEIGHT),
            assets_dir=ASSETS_DIR)
        self.platform_img = load_image(PLATFORM_IMAGE, assets_dir=ASSETS_DIR)

        # Игровые объекты
        self.player = Player()
        self.world = World()

        # Состояние игры
        self.show_hitboxes = SHOW_HITBOXES

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == JUMP_KEY:
                    self.player.jump()
                if event.key == TOGGLE_HITBOX_KEY:
                    self.show_hitboxes = not self.show_hitboxes

    def update(self):
        """Обновление состояния игры"""
        # Управление движением
        keys = pygame.key.get_pressed()
        player_x_movement = 0

        if keys[MOVE_RIGHT_KEY]:
            player_x_movement = self.player.move(1)
        if keys[MOVE_LEFT_KEY] and self.world.world_offset > 0:
            player_x_movement = self.player.move(-1)

        # Обновление мира и игрока
        self.world.update(player_x_movement)
        self.player.world_x += player_x_movement
        self.player.update(self.world.get_visible_platforms())

    def render(self):
        """Отрисовка игры"""
        # Фон
        self.screen.blit(self.background, (0, 0))

        # Отрисовка мира
        self.world.draw(self.screen)

        # Отрисовка игрока
        self.player.draw(self.screen)

        # Отладочная информация
        self.draw_debug_info()

        pygame.display.flip()

    def draw_debug_info(self):
        """Отрисовка отладочной информации"""
        font = pygame.font.SysFont(None, 24)
        debug_text = [
            f"Позиция: {self.player.world_x:.1f}",
            f"Y: {self.player.y:.1f}",
            f"Платформ: {len(self.world.platforms)}",
            f"Хитбоксы: {'ON' if self.show_hitboxes else 'OFF'} (H)"
        ]

        for i, text in enumerate(debug_text):
            text_surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, 10 + i * 25))

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()
