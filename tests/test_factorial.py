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


# Tests for the factorial operator
class TestFactorial(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()

	# Test factorial of a positive int
	def test_pos_int(self):
		self.tree.parse('3!')
		self.assertEqual(self.tree.evaluate(), 6)

	# Test factorial of 0
	def test_zero(self):
		self.tree.parse('0!')
		self.assertEqual(self.tree.evaluate(), 1)

	# Test factorial of a negative int
	def test_neg_int(self):
		self.tree.parse('-1!')
		with self.assertRaises(expressionparse.EvalException):
			self.tree.evaluate()

	# Test factorial of a non-int
	def test_non_int(self):
		self.tree.parse('1.5!')
		with self.assertRaises(expressionparse.EvalException):
			self.tree.evaluate()


