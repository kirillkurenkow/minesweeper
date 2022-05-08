from enum import Enum
from typing import Literal, Optional


T_CELL_NUMBER = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9]


class CellType(Enum):
    mine = 'Mine'
    number = 'Number'
    empty = 'Empty'


class Cell:
    def __init__(self, cell_type: CellType, number: Optional[T_CELL_NUMBER] = None):
        if cell_type == CellType.number and number is None:
            raise Exception('No number provided')
        self.__cell_type = cell_type
        self.__number = number
        self.is_flagged = False
        self.is_opened = False

    @property
    def type(self) -> CellType:
        return self.__cell_type

    @property
    def number(self) -> T_CELL_NUMBER:
        return self.__number

    def set_number(self, number: T_CELL_NUMBER):
        if self.__cell_type != CellType.mine:
            self.__cell_type = CellType.number
            self.__number = number

    def set_mine(self):
        self.__cell_type = CellType.mine
        self.__number = None

    def __str__(self):
        return f'Cell[{self.type}]' if self.type is not CellType.number else f'Cell[{self.number}]'

    def __repr__(self):
        return str(self)
