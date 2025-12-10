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

import expressionparse
import unittest


# Make sure the parser can handle various edge case expressions
class TestParser(unittest.TestCase):
    def setUp(self):
        self.tree = expressionparse.Tree()

    # Entire expression is a single int
    def testIsInt(self):
        self.tree.parse('1')
        self.assertEqual(self.tree.evaluate(), 1)

    # Entire expression is a single float
    def testIsFloat(self):
        self.tree.parse('1.5')
        self.assertEqual(self.tree.evaluate(), 1.5)

    # Entire expression is a single variable
    def testIsVariable(self):
        self.tree.parse('x')
        self.tree.setVariable('x',1)
        self.assertEqual(self.tree.evaluate(), 1)

    # Implicit multiplication (e.g. 3x = 3 * x) is tricky
    def testImplicitMultiplication(self):
        self.tree.parse('3x')
        node = expressionparse.Times()
        node.left = expressionparse.Value('3')
        node.right = expressionparse.Variable('x')
        self.assertEqual(self.tree.root, node)

    # Does implicit multiplication with multiple variables work
    def testImplicitMultiplicationMultipleVariables(self):
        self.tree.parse('3x + 9y - 2')

        x_node = expressionparse.Times()
        x_node.left = expressionparse.Value('3')
        x_node.right = expressionparse.Variable('x')

        y_node = expressionparse.Times()
        y_node.left = expressionparse.Value('9')
        y_node.right = expressionparse.Variable('y')

        variable_node = expressionparse.Plus()
        variable_node.left = x_node
        variable_node.right = y_node

        root_node = expressionparse.Minus()
        root_node.left = variable_node
        root_node.right = expressionparse.Value('2')

        self.assertEqual(self.tree.root, root_node)

    # Implicit multiplication with the same variable repeated
    def testImplicitMultiplicationRepeatedVariable(self):
        self.tree.parse('3x + 9x - 2')

        x1_node = expressionparse.Times()
        x1_node.left = expressionparse.Value('3')
        x1_node.right = expressionparse.Variable('x')

        x2_node = expressionparse.Times()
        x2_node.left = expressionparse.Value('9')
        x2_node.right = expressionparse.Variable('x')

        variable_node = expressionparse.Plus()
        variable_node.left = x1_node
        variable_node.right = x2_node

        root_node = expressionparse.Minus()
        root_node.left = variable_node
        root_node.right = expressionparse.Value('2')

        self.assertEqual(self.tree.root, root_node)

    # What if the whole expression is in parentheses
    def testParens(self):
        self.tree.parse('(1+1)')
        self.assertEqual(self.tree.evaluate(), 2)

    # Test multiple sets of nested parentheses
    def testParenNesting(self):
        self.tree.parse('(1+(2*(1+1))-(5*(4-2/(1-2))))+3')
        self.assertEqual(self.tree.evaluate(), -22)

    # Test big numbers (i.e. greater than a single digit)
    def testBigNumbers(self):
        self.tree.parse('100')
        self.assertEqual(self.tree.root.value, '100')

        self.tree.parse('2^10')
        self.assertEqual(self.tree.evaluate(), 1024)

        self.tree.parse('1989/221')
        self.assertEqual(self.tree.evaluate(), 9)


