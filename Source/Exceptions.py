__all__ = ['GameError', 'MinesNumberError', 'HeightError', 'WidthError']


class GameError(Exception):
    ...


class MinesNumberError(GameError):
    ...


class HeightError(GameError):
    ...


class WidthError(GameError):
    ...
