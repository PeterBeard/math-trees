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

	# What if the whole expression is in parentheses
	def testParens(self):
		self.tree.parse('(1+1)')
		self.assertEqual(self.tree.evaluate(), 2)

	# Test multiple sets of nested parentheses
	def testParenNesting(self):
		self.tree.parse('(1+(2*(1+1))-(5*(4-2/(1-2))))+3')
		self.assertEqual(self.tree.evaluate(), -22)


