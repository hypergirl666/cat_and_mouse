from setuptools import setup, find_packages

setup(
    name="cat_and_mouse",
    version="0.1",
    packages=find_packages(),
    package_data={
        "": ["*.png", "*.json"]  # Включаем все ресурсы
    },
    install_requires=[
        "pygame>=2.0.0"  # Указываем зависимости
    ],
)
