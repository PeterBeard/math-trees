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


# Tests for the multiplication operator
class TestMultiplication(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()

	# Test multiplication of two positive integers
	def test_pos_pos_int(self):
		self.tree.parse('1*1')
		self.assertEqual(self.tree.evaluate(), 1)

	# Test multiplication of two positive floats
	def test_pos_pos_float(self):
		self.tree.parse('1.5*0.5')
		self.assertEqual(self.tree.evaluate(), 0.75)

	# Test multiplication of one positive and one negative integer
	def test_pos_neg_int(self):
		self.tree.parse('1*-1')
		self.assertEqual(self.tree.evaluate(), -1)

	# Test multiplication of one negative and one positive integer
	def test_neg_pos_int(self):
		self.tree.parse('-1*1')
		self.assertEqual(self.tree.evaluate(), -1)

	# Test multiplication of one positive and one negative float 
	def test_pos_neg_float(self):
		self.tree.parse('1.5*-0.5')
		self.assertEqual(self.tree.evaluate(), -0.75)

	# Test multiplication of one negative and one positive float
	def test_neg_pos_float(self):
		self.tree.parse('-0.5*1.5')
		self.assertEqual(self.tree.evaluate(), -0.75)

	# Test multiplication of two negative integers
	def test_neg_neg_int(self):
		self.tree.parse('-1*-1')
		self.assertEqual(self.tree.evaluate(), 1)

	# Test multiplication of two negative floats
	def test_neg_neg_float(self):
		self.tree.parse('-1.5*-0.5')
		self.assertEqual(self.tree.evaluate(), 0.75)

