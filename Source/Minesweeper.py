import random
from typing import List

import pygame
from pygame import locals

from .Cell import (
    Cell,
    CellType,
)
from .Conts import (
    Const,
    GameMode,
)
from .Exceptions import (
    GameError,
    MinesNumberError,
    HeightError,
    WidthError,
)

__all__ = ['Minesweeper']


class Minesweeper:
    def __init__(self, game_mode: GameMode = GameMode.easy, mines_count: int = None, height: int = None,
                 width: int = None):
        if game_mode is GameMode.custom:
            if any((x is None for x in (mines_count, height, width))):
                raise GameError('Fields must me specified if custom game mode is selected: mines_count, height, width.')
            if mines_count < Const.Game.min_mines_count:
                raise MinesNumberError(f'Wrong mines_count value. '
                                       f'mines_count must be greater than {Const.Game.min_mines_count}.')
            self.__mines_count = mines_count
            if height < Const.Game.min_height:
                raise HeightError('Wrong height value.'
                                  f'height must be greater than {Const.Game.min_height}.')
            self.__height = height
            if width < Const.Game.min_width:
                raise WidthError('Wrong width value.'
                                 f'width must be greater than {Const.Game.min_width}.')
            self.__width = width
            if mines_count > (height * width) // 3:
                raise MinesNumberError(f'Wrong mines_count value.'
                                       f'mines_count must be lower than (height * width) // 2')
        elif game_mode not in list(GameMode):
            raise GameError(f'Wrong game mode specified: {game_mode}. '
                            f'Available game modes: {", ".join([str(x) for x in GameMode])}.')
        else:
            self.__mines_count = Const.Game.modes[game_mode]['mines_count']
            self.__height = Const.Game.modes[game_mode]['size']
            self.__width = Const.Game.modes[game_mode]['size']
        self.__running = True
        self.__flags_counter = 0
        self.__rect_field: List[List[pygame.Rect]] = []
        self.__field: List[List[Cell]] = []

        # PyGame
        pygame.init()
        pygame.display.set_caption(Const.Game.name)
        self.__Screen = pygame.display.set_mode((self.display_width, self.display_height))
        self.__Clock = pygame.time.Clock()

        # Fonts
        self.__CellFont = pygame.font.Font(Const.Font.cell, Const.Font.cell_size)
        self.__MenuFont = pygame.font.Font(Const.Font.menu, Const.Font.menu_size)

    @property
    def display_width(self):
        result = (Const.Size.cell_space + Const.Size.cell) * self.height + Const.Size.space * 2
        result -= Const.Size.cell_space
        return result

    @property
    def display_height(self):
        result = (Const.Size.cell + Const.Size.cell_space) * self.height + Const.Size.space * 3
        result -= Const.Size.cell_space
        result += Const.Size.menu_height
        return result

    @property
    def mines_count(self) -> int:
        return self.__mines_count

    @property
    def height(self) -> int:
        return self.__height

    @property
    def width(self) -> int:
        return self.__width

    def __draw_game(self):
        self.__Screen.fill(Const.Color.background)

        # Menu rect
        menu_width = self.display_width - (Const.Size.space * 2)
        self.__menu_rect = pygame.Rect(Const.Size.space, Const.Size.space, menu_width, Const.Size.menu_height)
        pygame.draw.rect(self.__Screen, Const.Color.menu, self.__menu_rect)

        # Mines rect
        mines_x = self.__menu_rect.x + Const.Size.space * 2
        mines_y = self.__menu_rect.y + ((Const.Size.menu_height - Const.Size.menu_block_height) // 2)
        self.__mines_rect = pygame.Rect(mines_x, mines_y, Const.Size.menu_block_width, Const.Size.menu_block_height)
        pygame.draw.rect(self.__Screen, Const.Color.menu_block, self.__mines_rect)

        # Mines text
        mines_text = self.__MenuFont.render(
            str(self.mines_count),
            True,
            Const.Color.red,
        )
        mines_text_rect = mines_text.get_rect(center=(self.__mines_rect.centerx, self.__mines_rect.centery))
        self.__Screen.blit(mines_text, mines_text_rect)

        # Start button
        start_x = self.__menu_rect.centerx - Const.Size.start_button // 2
        start_y = self.__menu_rect.centery - Const.Size.start_button // 2
        self.__start_rect = pygame.Rect(start_x, start_y, Const.Size.start_button, Const.Size.start_button)
        pygame.draw.rect(self.__Screen, Const.Color.red, self.__start_rect)

        # Timer rect
        timer_x = self.__menu_rect.x + self.__menu_rect.width - Const.Size.space * 2 - Const.Size.menu_block_width
        timer_y = self.__menu_rect.y + ((Const.Size.menu_height - Const.Size.menu_block_height) // 2)
        self.__timer_rect = pygame.Rect(timer_x, timer_y, Const.Size.menu_block_width, Const.Size.menu_block_height)
        pygame.draw.rect(self.__Screen, Const.Color.menu_block, self.__timer_rect)

    def __draw_field(self):
        self.__rect_field = []

        temp_x = Const.Size.space
        temp_y = Const.Size.menu_height + Const.Size.space * 2

        # Generate field
        for i in range(self.height):
            row = []
            for j in range(self.width):
                cell = pygame.Rect(temp_x, temp_y, Const.Size.cell, Const.Size.cell)
                row.append(cell)
                temp_x += Const.Size.cell_space + Const.Size.cell

            temp_x = Const.Size.space
            temp_y += Const.Size.cell_space + Const.Size.cell
            self.__rect_field.append(row)

        # Draw field
        for row_index in range(self.height):
            for cell_index in range(self.width):
                cell = self.__field[row_index][cell_index]
                cell_rect = self.__rect_field[row_index][cell_index]

                # Cell text
                if (cell.type is CellType.number) and cell.is_opened:
                    pygame.draw.rect(self.__Screen, Const.Color.cell_opened, cell_rect)
                    text = self.__CellFont.render(
                        str(self.__field[row_index][cell_index].number),
                        True,
                        Const.Color.black,
                    )
                    text_rect = text.get_rect(center=(cell_rect.centerx, cell_rect.centery))
                    self.__Screen.blit(text, text_rect)
                elif (cell.type is CellType.mine) and cell.is_opened:
                    pygame.draw.rect(self.__Screen, Const.Color.cell_mine, cell_rect)
                elif (cell.type is CellType.empty) and cell.is_opened:
                    pygame.draw.rect(self.__Screen, Const.Color.cell_opened, cell_rect)
                elif cell.is_flagged:
                    pygame.draw.rect(self.__Screen, Const.Color.cell_flagged, cell_rect)
                else:
                    pygame.draw.rect(self.__Screen, Const.Color.cell_hidden, cell_rect)

    def __generate_field(self):
        self.__field = [[Cell(CellType.empty) for _ in range(self.width)] for _ in range(self.height)]

        # Set mines
        mines_planted = []
        while len(mines_planted) < self.mines_count:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in mines_planted:
                self.__field[y][x].set_mine()
                mines_planted.append((x, y))

        # Set cell numbers
        for row_index, row in enumerate(self.__field):
            for cell_index, cell in enumerate(row):
                if cell.type is CellType.mine:
                    continue

                # Count mines around cell
                adjacent_cells = self.get_adjacent_cells(row_index, cell_index)
                mines_count = len([x for x in adjacent_cells if x.type is CellType.mine])

                # Set cell number
                if mines_count > 0:
                    cell.set_number(mines_count)

    def start_game(self) -> None:
        start_ticks = pygame.time.get_ticks()
        self.__draw_game()
        self.__generate_field()
        self.__draw_field()

        while True:
            self.__draw_field()
            pygame.display.update()

            # Check events
            for event in pygame.event.get():
                if event.type == locals.QUIT:
                    return
                elif event.type == locals.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Start game
                        if self.__start_rect.collidepoint(pygame.mouse.get_pos()):
                            self.__running = True
                            return self.start_game()

                    # Cell press
                    if self.__running:
                        for row_index in range(self.height):
                            for cell_index in range(self.width):
                                cell_rect = self.__rect_field[row_index][cell_index]
                                cell = self.__field[row_index][cell_index]
                                if cell_rect.collidepoint(pygame.mouse.get_pos()):
                                    if (event.button == 1) and not cell.is_flagged:
                                        if cell.type is CellType.number:
                                            cell.is_opened = True
                                        if cell.type is CellType.mine:
                                            self.__game_over()
                                        if cell.type is CellType.empty:
                                            cell.is_opened = True
                                            self.__open_cells_around_empty_cells()
                                    elif event.button == 3:
                                        cell.is_flagged = not cell.is_flagged

            # Check win
            if self.__all_cells_are_open():
                self.__game_over()

            # Update timer
            if self.__running:
                self.__update_timer((pygame.time.get_ticks() - start_ticks) // 1000)

            # Update mines counter
            self.__update_mines_count()

            # Frame rate
            self.__Clock.tick(Const.Game.frame_rate)

    def __update_timer(self, time: int):
        pygame.draw.rect(self.__Screen, Const.Color.menu_block, self.__timer_rect)
        text = self.__MenuFont.render(
            str(time),
            True,
            Const.Color.red,
        )
        text_rect = text.get_rect(center=(self.__timer_rect.centerx, self.__timer_rect.centery))
        self.__Screen.blit(text, text_rect)
        pygame.display.update()

    def __update_mines_count(self):
        flags_count = len([row for row in self.__field for x in row if x.is_flagged])
        mines_count = self.mines_count - flags_count
        pygame.draw.rect(self.__Screen, Const.Color.menu_block, self.__mines_rect)
        text = self.__MenuFont.render(
            str(mines_count),
            True,
            Const.Color.red,
        )
        text_rect = text.get_rect(center=(self.__mines_rect.centerx, self.__mines_rect.centery))
        self.__Screen.blit(text, text_rect)
        pygame.display.update()

    def __game_over(self):
        for row in self.__field:
            for cell in row:
                cell.is_opened = True
        self.__draw_field()
        pygame.draw.rect(self.__Screen, Const.Color.green, self.__start_rect)
        pygame.display.update()
        self.__running = False

    def get_adjacent_cells(self, row_index, cell_index) -> List[Cell]:
        adjacent_cells = []
        if row_index > 0:
            if cell_index > 0:
                adjacent_cells.append(self.__field[row_index - 1][cell_index - 1])
            adjacent_cells.append(self.__field[row_index - 1][cell_index])
            if cell_index < self.width - 1:
                adjacent_cells.append(self.__field[row_index - 1][cell_index + 1])
        if cell_index > 0:
            adjacent_cells.append(self.__field[row_index][cell_index - 1])
        if cell_index < self.width - 1:
            adjacent_cells.append(self.__field[row_index][cell_index + 1])
        if row_index < self.height - 1:
            if cell_index > 0:
                adjacent_cells.append(self.__field[row_index + 1][cell_index - 1])
            adjacent_cells.append(self.__field[row_index + 1][cell_index])
            if cell_index < self.width - 1:
                adjacent_cells.append(self.__field[row_index + 1][cell_index + 1])
        return adjacent_cells

    def __open_cells_around_empty_cells(self):
        cell_changed = True
        while cell_changed:
            cell_changed = False
            for row_index, row in enumerate(self.__field):
                for cell_index, cell in enumerate(row):
                    if (cell.type is CellType.empty) and cell.is_opened:
                        adjacent_cells = self.get_adjacent_cells(row_index, cell_index)
                        for adjacent_cell in adjacent_cells:
                            if (adjacent_cell.type is not CellType.mine) and not adjacent_cell.is_opened:
                                adjacent_cell.is_opened = True
                                cell_changed = True

    def __all_cells_are_open(self) -> bool:
        for row in self.__field:
            for cell in row:
                if not cell.is_opened:
                    if not ((cell.type is CellType.mine) and cell.is_flagged):
                        return False
        return True
