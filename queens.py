# queens.py
#
# ICS 33 Spring 2024
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self


Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'


class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position

    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'


class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position

    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'


class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""

    def __init__(self, rows: int, columns: int):
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""
        self.row = rows
        self.column = columns
        self.queen_loc = []

    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        num_queens = len(self.queen_loc)
        return num_queens

    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""
        return self.queen_loc

    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""
        if position in self.queen_loc:
            return True
        elif position not in self.queen_loc:
            return False

    def any_queens_unsafe(self) -> bool:
        """Returns True if any queens on the chessboard are unsafe (i.e., they can
        be captured by at least one other queen on the chessboard), or False otherwise."""
        num_queens = len(self.queen_loc)
        for i in range(num_queens):
            first_queen = self.queen_loc[i]
            for j in range(num_queens):
                if i != j:
                    second_queen = self.queen_loc[j]
                    if first_queen.row == second_queen.row and abs(first_queen.column - second_queen.column) <= 1:
                        return True
                    if first_queen.column == second_queen.column and abs(first_queen.row - second_queen.row) <= 1:
                        return True
                    if abs(first_queen.column - second_queen.column) == abs(first_queen.row - second_queen.row):
                        return True
        return False

    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions,
        without modifying 'self' in any way.  Raises a DuplicateQueenError when
        there is already a queen in at least one of the given positions."""
        new_loc = self.queen_loc.copy()
        new_state = QueensState(self.row, self.column)
        for position in positions:
            if position not in self.queen_loc:
                new_loc.append(position)
            else:
                raise DuplicateQueenError(position)
        new_state.queen_loc = new_loc
        return new_state

    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions,
        without modifying 'self' in any way.  Raises a MissingQueenError when there
        is no queen in at least one of the given positions."""
        new_loc = self.queen_loc.copy()
        new_state = QueensState(self.row, self.column)
        for position in positions:
            if position in self.queen_loc:
                new_loc.remove(position)
            else:
                raise MissingQueenError(position)
        new_state.queen_loc = new_loc
        return new_state
