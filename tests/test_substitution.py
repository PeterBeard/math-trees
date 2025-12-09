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


# Test value substitution for variables
class TestSubstitution(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()

	# Single variable
	def test_single_variable(self):
		var = expressionparse.Variable('x')
		var.set(1)
		self.assertEqual(var.evaluate(), 1)

	# Expression with one variable
	def test_exp_one_variable(self):
		self.tree.parse('x+1')
		self.tree.setVariable('x',1)
		self.assertEqual(self.tree.evaluate(), 2)

	# Expression with two instances of one variable
	def test_exp_one_variable_twice(self):
		self.tree.parse('x+1+x')
		self.tree.setVariable('x',1)
		self.assertEqual(self.tree.evaluate(), 3)

	# Expression with two variables
	def test_exp_two_variables(self):
		self.tree.parse('x+y+1')
		self.tree.setVariable('x',1)
		self.tree.setVariable('y',2)
		self.assertEqual(self.tree.evaluate(), 4)

