"""Модуль настроек игры"""
import configparser
from os.path import join


class Settings:
    def __init__(self, filename='settings.ini'):
        """Чтение настроек"""
        self._config = configparser.ConfigParser(default_section='')
        self._config.optionxform = str
        self._config.read(filename, encoding='utf8')

    def _global(self):
        return self._config['GLOBAL']

    def _level(self):
        return self._config['LEVEL']

    @property
    def levels(self):
        return list(self._config['LEVELS'].values())

    @property
    def picture_size(self):
        """Размер картинок"""
        return int(self._global()['size_picture'])

    @property
    def height_toolbar(self):
        """Высота панельки с жизнями в блоках"""
        return int(self._global()['height_toolbar'])

    def picture(self, name: str):
        """Имя файла с изображением `name`"""
        name_image_file = self._config['PICTURES'].get(name, None)
        if not name_image_file:
            raise FileNotFoundError()
        else:
            return join(self._global()['images_dir'], name_image_file)

    # region level
    @property
    def levels_dir(self):
        """Директория с уровнями"""
        return self._level()['levels_dir']

    def map_file(self, level):
        """Файл с описанием карты уровня"""
        return join(self.levels_dir, level, self._level()['map'])

    def background_image(self, level):
        """Файл с задним фоном уровня"""
        return join(self.levels_dir, level, self._level()['background'])

    @property
    def wall_symbol(self):
        """Символ, обозначающий стену на карте"""
        return self._level()['wall_symbol']

    @property
    def empty_symbol(self):
        """Символ, обозначающий пустое место"""
        return self._level()['empty_symbol']

    # endregion
