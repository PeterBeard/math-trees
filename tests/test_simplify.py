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

from expressionparse import Tree, simplify
import unittest


# Tests for simplifying nodes
class TestSimplify(unittest.TestCase):
    def test_lone_digit(self):
        tree = Tree("4")
        self.assertEqual(simplify(tree.root), 4.0)

    def test_expression(self):
        tree = Tree("4 + 1")
        self.assertEqual(simplify(tree.root), 5.0)

    def test_undefined_variable(self):
        tree = Tree("x")
        self.assertEqual(simplify(tree.root), tree.root)

    def test_multiple_variables(self):
        tree = Tree("x + y")
        self.assertEqual(simplify(tree.root), tree.root)

    def test_undefined_variable_in_expression(self):
        tree = Tree("(6/3) * x + 2")
        simplified_tree = Tree("2*x+2")
        self.assertEqual(simplify(tree.root), simplified_tree.root)

    def test_defined_variable(self):
        tree = Tree("x")
        tree.setVariable("x", 5)
        self.assertEqual(simplify(tree.root), 5.0)
