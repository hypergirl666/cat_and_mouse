import os
import pygame
import random
from constants import (
    ASSETS_DIR,
    FALLBACK_SURFACE_WIDTH,
    FALLBACK_SURFACE_HEIGHT
)


def load_image(name, scale=None, assets_dir=ASSETS_DIR):
    try:
        img = pygame.image.load(os.path.join(assets_dir, name)).convert_alpha()
        return pygame.transform.scale(img, scale) if scale else img
    except BaseException:
        print(f"Ошибка загрузки: {os.path.join(assets_dir, name)}")
        surf = pygame.Surface((FALLBACK_SURFACE_WIDTH,
                               FALLBACK_SURFACE_HEIGHT))
        surf.fill((
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ))
        return surf
