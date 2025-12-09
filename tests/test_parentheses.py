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


# Tests for parentheses
class TestParentheses(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()

	# Test for unmatched left parens
	def test_unmatched_lparen(self):
		with self.assertRaises(expressionparse.TokenizeException):
			self.tree.parse('1+(2+3')

	# Test for unmatched right parens
	def test_unmatched_rparen(self):
		with self.assertRaises(expressionparse.TokenizeException):
			self.tree.parse('1+(2+3))')

	# Make sure parenthetical expressions are evaluated first
	def test_oop_parens(self):
		self.tree.parse('2*(1+3)')
		self.assertEqual(self.tree.evaluate(), 8)

	# The tree should be the same for expressions where the parentheses don't change anything
	def test_irrelevant_parens(self):
		self.tree.parse('2*4+5')
		u = expressionparse.Tree()
		u.parse('(2*4)+5')

		self.assertEqual(self.tree, u)

	# Test for addition on the left
	def test_add_left(self):
		self.tree.parse('1+(2*2)')
		self.assertEqual(self.tree.evaluate(), 5)

	# Test for addition on the right
	def test_add_right(self):
		self.tree.parse('(2*2)+1')
		self.assertEqual(self.tree.evaluate(), 5)

	# Test for subtraction on the left
	def test_sub_left(self):
		self.tree.parse('1-(2*2)')
		self.assertEqual(self.tree.evaluate(), -3)

	# Test for subtraction on the right
	def test_sub_right(self):
		self.tree.parse('(2*2)-1')
		self.assertEqual(self.tree.evaluate(), 3)

	# Test for multiplication on the left
	def test_mul_left(self):
		self.tree.parse('2*(2*2)')
		self.assertEqual(self.tree.evaluate(), 8)

	# Test for multiplication on the right
	def test_mul_right(self):
		self.tree.parse('(2*2)*2')
		self.assertEqual(self.tree.evaluate(), 8)

	# Test for division on the left
	def test_div_left(self):
		self.tree.parse('2/(2*2)')
		self.assertEqual(self.tree.evaluate(), 0.5)

	# Test for division on the right
	def test_div_right(self):
		self.tree.parse('(2*2)/2')
		self.assertEqual(self.tree.evaluate(), 2)

	# Test for implied multiplication of parenthetical expressions
	def test_implied_mul(self):
		self.tree.parse('(1+1)(1+1)')
		self.assertEqual(self.tree.evaluate(), 4)

	# Test for multiple parenthetical expressions
	def test_multi_parens(self):
		self.tree.parse('(1+2)*3-(3+4)*5')
		self.assertEqual(self.tree.evaluate(), -26)

	# Test for deeply-nested parenthetical expressions (5 levels)
	def test_nested_parens(self):
		self.tree.parse('2*(1+(3/(1-(2*(6-5)))))')
		self.assertEqual(self.tree.evaluate(), -4)

	# Test for multiple sets of nested parentheses
	def test_multi_nested_parens(self):
		self.tree.parse('1/(1+(3*(2-3)))+3*(4-(1/(1+2)))')
		self.assertEqual(self.tree.evaluate(), 10.5)

