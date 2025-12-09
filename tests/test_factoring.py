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


# Test factoring of nodes
class TestFactoring(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()
		self.factored_tree = expressionparse.Tree()

	# Addition of multiplication (common factor on left)
	def test_add_mul_left(self):
		self.tree.parse('x*y+x*z')
		self.factored_tree.parse('x*(y+z)')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of multiplication (common factor on left then right)
	def test_add_mul_left_right(self):
		self.tree.parse('x*y+z*x')
		self.factored_tree.parse('x*(y+z)')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of multiplication (common factor on right then left)
	def test_add_mul_right_left(self):
		self.tree.parse('y*x+x*z')
		self.factored_tree.parse('(y+z)*x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of multiplication (common factor on right)
	def test_add_mul_right(self):
		self.tree.parse('y*x+z*x')
		self.factored_tree.parse('(y+z)*x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of multiplication (common factor on left)
	def test_sub_mul_left(self):
		self.tree.parse('x*y-x*z')
		self.factored_tree.parse('x*(y-z)')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of multiplication (common factor on left then right)
	def test_sub_mul_left_right(self):
		self.tree.parse('x*y-z*x')
		self.factored_tree.parse('x*(y-z)')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of multiplication (common factor on left then right)
	def test_sub_mul_right_left(self):
		self.tree.parse('y*x-x*z')
		self.factored_tree.parse('(y-z)*x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of multiplication (common factor on right)
	def test_sub_mul_right(self):
		self.tree.parse('y*x-z*x')
		self.factored_tree.parse('(y-z)*x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of division (common factor on left)
	def test_add_div_left(self):
		self.tree.parse('x/y+x/z')
		self.factored_tree.parse('x/(y+z)')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of division (common factor on left then right)
	def test_add_div_left_right(self):
		self.tree.parse('x/y+z/x')
		self.factored_tree.parse('x/y+z/x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of division (common factor on right then left)
	def test_add_div_right_left(self):
		self.tree.parse('y/x+x/z')
		self.factored_tree.parse('y/x+x/z')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of division (common factor on right)
	def test_add_div_right(self):
		self.tree.parse('y/x+z/x')
		self.factored_tree.parse('(y+z)/x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of division (common factor on left)
	def test_sub_div_left(self):
		self.tree.parse('x/y-x/z')
		self.factored_tree.parse('x/(y-z)')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of division (common factor on left then right)
	def test_sub_div_left_right(self):
		self.tree.parse('x/y-z/x')
		self.factored_tree.parse('x/y-z/x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of division (common factor on left then right)
	def test_sub_div_right_left(self):
		self.tree.parse('y/x-x/z')
		self.factored_tree.parse('y/x-x/z')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of division (common factor on right)
	def test_sub_div_right(self):
		self.tree.parse('y/x-z/x')
		self.factored_tree.parse('(y-z)/x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of exponentiation (common factor on left)
	def test_add_exp_left(self):
		self.tree.parse('x^y+x^z')
		self.factored_tree.parse('x^y+x^z')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of exponentiation (common factor on left then right)
	def test_add_exp_left_right(self):
		self.tree.parse('x^y+z^x')
		self.factored_tree.parse('x^y+z^x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of exponentiation (common factor on right then left)
	def test_add_exp_right_left(self):
		self.tree.parse('y^x+x^z')
		self.factored_tree.parse('y^x+x^z')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Addition of exponentiation (common factor on right)
	def test_add_exp_right(self):
		self.tree.parse('y^x+z^x')
		self.factored_tree.parse('y^x+z^x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of exponentiation (common factor on left)
	def test_sub_exp_left(self):
		self.tree.parse('x^y-x^z')
		self.factored_tree.parse('x^y-x^z')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of exponentiation (common factor on left then right)
	def test_sub_exp_left_right(self):
		self.tree.parse('x^y-z^x')
		self.factored_tree.parse('x^y-z^x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of exponentiation (common factor on right then left)
	def test_sub_exp_right_left(self):
		self.tree.parse('y^x-x^z')
		self.factored_tree.parse('y^x-x^z')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Subtraction of exponentiation (common factor on right)
	def test_sub_exp_right(self):
		self.tree.parse('y^x-z^x')
		self.factored_tree.parse('y^x-z^x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Multiplication of exponentiation (common factor on left)
	def test_mul_exp_left(self):
		self.tree.parse('x^y*x^z')
		self.factored_tree.parse('x^(y+z)')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Multiplication of exponentiation (common factor on left then right)
	def test_mul_exp_left_right(self):
		self.tree.parse('x^y*z^x')
		self.factored_tree.parse('x^y*z^x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Multiplication of exponentiation (common factor on right then left)
	def test_mul_exp_right_left(self):
		self.tree.parse('y^x*x^z')
		self.factored_tree.parse('y^x*x^z')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Multiplication of exponentiation (common factor on right)
	def test_mul_exp_right(self):
		self.tree.parse('y^x*z^x')
		self.factored_tree.parse('(y*z)^x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Division of exponentiation (common factor on left)
	def test_div_exp_left(self):
		self.tree.parse('x^y/x^z')
		self.factored_tree.parse('x^(y-z)')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Division of exponentiation (common factor on left then right)
	def test_div_exp_left_right(self):
		self.tree.parse('x^y/z^x')
		self.factored_tree.parse('x^y/z^x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Division of exponentiation (common factor on right then left)
	def test_div_exp_right_left(self):
		self.tree.parse('y^x/x^z')
		self.factored_tree.parse('y^x/x^z')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)

	# Division of exponentiation (common factor on right)
	def test_div_exp_right(self):
		self.tree.parse('y^x/z^x')
		self.factored_tree.parse('(y/z)^x')
		self.assertEqual(self.tree.root.factor(), self.factored_tree.root)


