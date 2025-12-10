# Expressionparse v0.2 -- Create syntax trees for mathematical expressions
#
# Copyright (C) 2025, Peter Beard <github@peterbeard.co>
# 
# This file is part of Expressionparse.
# 
# Expressionparse is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# 
# Expressionparse is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Expressionparse. If not, see <http://www.gnu.org/licenses/>.

from expressionparse import Tree
import unittest


# Tests for generating expressions in Reverse Polish Notation (RPN)
class TestReversePolishNotation(unittest.TestCase):
    def test_addition(self):
        tree = Tree("1+1")
        self.assertEqual(tree.toReversePolishNotation(), "1 1 +")
        tree = Tree("1+1+1")
        # TODO: This should probably be "1 1 1 +" but it isn't because the
        #       syntax trees we generate are binary
        self.assertEqual(tree.toReversePolishNotation(), "1 1 1 + +")

    def test_subtraction(self):
        tree = Tree("2-1")
        self.assertEqual(tree.toReversePolishNotation(), "2 1 -")

    def test_multiplication(self):
        tree = Tree("2*3")
        self.assertEqual(tree.toReversePolishNotation(), "2 3 *")

    def test_division(self):
        tree = Tree("2/3")
        self.assertEqual(tree.toReversePolishNotation(), "2 3 /")

    def test_exponents(self):
        tree = Tree("3^5")
        self.assertEqual(tree.toReversePolishNotation(), "3 5 ^")

    def test_factorial(self):
        tree = Tree("5!")
        self.assertEqual(tree.toReversePolishNotation(), "5 !")
        tree = Tree("(4+1)!")
        self.assertEqual(tree.toReversePolishNotation(), "4 1 + !")

    def test_order_of_operations(self):
        tree = Tree("3 + 4 * 5")
        # Note that argument order is preserved and there are no parentheses
        # because each operation takes at most two arguments
        self.assertEqual(tree.toReversePolishNotation(), "3 4 5 * +")

        tree = Tree("4 * 5 + 3")
        self.assertEqual(tree.toReversePolishNotation(), "4 5 * 3 +")

    def test_parentheses(self):
        tree = Tree("(3 + 4) * (5 + 6)")
        self.assertEqual(tree.toReversePolishNotation(), "3 4 + 5 6 + *")
