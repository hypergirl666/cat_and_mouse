from constants import *
from src.utils.helpers import load_image


class Player:
    def __init__(self):
        """Инициализация игрока (кота)"""
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2  # Центрирование по X
        self.y = SCREEN_HEIGHT - 300  # Стартовая позиция Y
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.gravity = PLAYER_GRAVITY
        self.vel_y = 0
        self.is_jumping = False
        self.facing_right = True
        self.world_x = 0  # Позиция в игровом мире

        # Хитбокс игрока
        self.hitbox_width = PLAYER_HITBOX_WIDTH
        self.hitbox_height = PLAYER_HITBOX_HEIGHT
        self.hitbox_offset_x = PLAYER_HITBOX_OFFSET_X
        self.hitbox_offset_y = PLAYER_HITBOX_OFFSET_Y
        self.update_hitbox()

        # Загрузка изображения
        self.image = load_image(PLAYER_IMAGE,
                                scale=(PLAYER_WIDTH, PLAYER_HEIGHT),
                                assets_dir=ASSETS_DIR)

    def update_hitbox(self):
        """Обновляет позицию хитбокса игрока"""
        self.hitbox = pygame.Rect(
            self.x + self.hitbox_offset_x,
            self.y + self.hitbox_offset_y,
            self.hitbox_width,
            self.hitbox_height
        )

    def update(self, platforms):
        """
        Обновляет состояние игрока
        :param platforms: Список активных платформ
        """
        # Применяем гравитацию
        self.vel_y += self.gravity
        self.y += self.vel_y
        self.update_hitbox()

        # Проверка коллизий с платформами
        on_ground = False
        for platform in platforms:
            platform_hitbox = platform.get_hitbox(self.world_x)

            if self.hitbox.colliderect(platform_hitbox):
                # Приземление на платформу
                if self.vel_y > 0 and self.hitbox.bottom > platform_hitbox.top:
                    self.y = platform_hitbox.top - \
                        (self.hitbox_offset_y + self.hitbox_height)
                    self.vel_y = 0
                    self.is_jumping = False
                    on_ground = True
                # Удар головой о платформу снизу
                elif self.vel_y < 0 and self.hitbox.top < platform_hitbox.bottom:
                    self.y = platform_hitbox.bottom - self.hitbox_offset_y
                    self.vel_y = 0

        # Проверка выхода за границы экрана
        if self.y > SCREEN_HEIGHT - self.height and not on_ground:
            self.y = SCREEN_HEIGHT - self.height
            self.vel_y = 0
            self.is_jumping = False

    def draw(self, screen):
        """Отрисовывает игрока на экране"""
        # Отрисовка спрайта с учетом направления
        flipped_image = pygame.transform.flip(self.image,
                                              not self.facing_right,
                                              False)
        screen.blit(flipped_image, (self.x, self.y))

        # Отрисовка хитбокса (если включено)
        if SHOW_HITBOXES:
            hitbox_surface = pygame.Surface(
                (self.hitbox.width, self.hitbox.height),
                pygame.SRCALPHA
            )
            hitbox_surface.fill(HITBOX_COLOR)
            screen.blit(hitbox_surface, (self.hitbox.topleft))

    def jump(self):
        """Выполняет прыжок, если игрок на земле"""
        if not self.is_jumping:
            self.vel_y = -self.jump_power
            self.is_jumping = True

    def move(self, direction):
        """
        Устанавливает направление движения
        :param direction: 1 (вправо) или -1 (влево)
        """
        self.facing_right = direction > 0
        return direction * self.speed
