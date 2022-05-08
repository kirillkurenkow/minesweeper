from enum import Enum
from typing import (
    Literal,
    Optional,
)
from .Exceptions import CellNumberNotProvided, WrongCellTypeError

__all__ = ['Cell', 'CellType']

T_CELL_NUMBER = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]


class CellType(Enum):
    """
    Cell types
    """
    mine = 'Mine'
    number = 'Number'
    empty = 'Empty'


class Cell:
    def __init__(self, cell_type: CellType, number: Optional[T_CELL_NUMBER] = None):
        if cell_type == CellType.number and number is None:
            raise CellNumberNotProvided('number must be provided if cell_type is CellType.number.')

        self.__cell_type = cell_type
        self.__number = number
        self.is_flagged = False
        self.is_opened = False

    @property
    def type(self) -> CellType:
        """
        Cell type

        :return: self.__cell_type
        """
        return self.__cell_type

    @property
    def number(self) -> T_CELL_NUMBER:
        """
        Cell number

        :return: self.__number
        """
        return self.__number

    def set_number(self, number: T_CELL_NUMBER) -> None:
        """
        Sets number to self

        :param number: New number

        :return: None
        """
        if self.__cell_type != CellType.mine:
            self.__cell_type = CellType.number
            self.__number = number
        else:
            raise WrongCellTypeError('Can not assign number to cell with type CellType.mine.')

    def set_mine(self) -> None:
        """
        Sets self.type to CellType.mine

        :return: None
        """
        self.__cell_type = CellType.mine
        self.__number = None

    def __str__(self) -> str:
        return f'Cell[{self.type}]' if self.type is not CellType.number else f'Cell[{self.number}]'

    def __repr__(self) -> str:
        return str(self)
