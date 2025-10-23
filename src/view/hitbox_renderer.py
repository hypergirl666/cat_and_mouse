import pygame


class HitboxRenderer:
    """Отвечает за отрисовку хитбоксов (композиция)"""

    @staticmethod
    def draw_hitbox(screen: pygame.Surface,
                    rect: pygame.Rect, color: tuple) -> None:
        """
        Отрисовывает хитбокс на экране
        :param screen: Поверхность для отрисовки
        :param rect: Прямоугольник хитбокса
        :param color: Цвет хитбокса
        """
        hitbox_surface = pygame.Surface(
            (rect.width, rect.height),
            pygame.SRCALPHA
        )
        hitbox_surface.fill(color)
        screen.blit(hitbox_surface, rect.topleft)
