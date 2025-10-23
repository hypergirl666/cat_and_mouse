import os
import pygame
import random


def load_image(name, scale=None, assets_dir="assets"):
    try:
        img = pygame.image.load(os.path.join(assets_dir, name)).convert_alpha()
        return pygame.transform.scale(img, scale) if scale else img
    except BaseException:
        print(f"Ошибка загрузки: {os.path.join(assets_dir, name)}")
        surf = pygame.Surface((100, 100))
        surf.fill(
            (random.randint(
                0, 255), random.randint(
                0, 255), random.randint(
                0, 255)))
        return surf
