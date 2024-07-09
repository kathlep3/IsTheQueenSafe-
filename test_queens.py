# test_queens.py
#
# ICS 33 Spring 2024
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_queen_count_is_zero_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import QueensState
from collections import namedtuple
import unittest


Position = namedtuple('Position', ['row', 'column'])


class TestQueensState(unittest.TestCase):
    def test_queen_count_is_zero_initially(self):
        state = QueensState(8, 8)
        self.assertEqual(state.queen_count(), 0)

    def test_queens_is_list(self):
        state = QueensState(8, 8)
        self.assertIsInstance(state.queens(), list)

    def test_added_queen_return_instance(self):
        state = QueensState(8, 8)
        position = [Position(row=4, column=6)]
        self.assertIsInstance(state.with_queens_added(position), QueensState)

    def test_queen_added_to_list(self):
        state = QueensState(8, 8)
        count = state.queen_count()
        position = Position(row=4, column=6)
        result = state.with_queens_added([position])
        self.assertEqual(result.queen_count(), count + len([position]))
        self.assertIn(position, result.queens())

    def test_queen_removed_from_list(self):
        state = QueensState(8, 8)
        count = state.queen_count()
        position = Position(row=4, column=6)
        adding = state.with_queens_added([position])
        result = adding.with_queens_removed([position])
        self.assertEqual(result.queen_count(), count)
        self.assertNotIn(position, result.queens())

    def test_has_queen_True(self):
        state = QueensState(8, 8)
        position = Position(row=4, column=6)
        added_to_list = state.with_queens_added([position])
        self.assertTrue(added_to_list)

    def test_has_queen_False(self):
        state = QueensState(8, 8)
        position = Position(row=4, column=6)
        self.assertFalse(state.has_queen(position))

    def test_unsafe_row(self):
        state = QueensState(8, 8)
        adding = state.with_queens_added([Position(0, 1), Position(0, 2)])
        safety = adding.any_queens_unsafe()
        self.assertTrue(safety)

    def test_unsafe_column(self):
        state = QueensState(8, 8)
        adding = state.with_queens_added([Position(4, 4), Position(5, 4)])
        safety = adding.any_queens_unsafe()
        self.assertTrue(safety)

    def test_unsafe_diagonal(self):
        state = QueensState(8, 8)
        adding = state.with_queens_added([Position(4, 4), Position(5, 5)])
        safety = adding.any_queens_unsafe()
        self.assertTrue(safety)

    def test_unsafe_safe(self):
        state = QueensState(8, 8)
        adding = state.with_queens_added([Position(3, 3), Position(5, 4)])
        safety = adding.any_queens_unsafe()
        self.assertFalse(safety)


if __name__ == '__main__':
    unittest.main()
