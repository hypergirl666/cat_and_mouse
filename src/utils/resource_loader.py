from src.utils.helpers import load_image
from constants import ASSETS_DIR


class ResourceLoader:
    @staticmethod
    def load_image(name, scale=None):
        return load_image(name, scale, assets_dir=ASSETS_DIR)
