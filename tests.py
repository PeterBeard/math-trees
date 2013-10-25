# Expressionparse v0.1 -- Create syntax trees for mathematical expressions
#
# Copyright (C) 2013, Peter Beard <peter.b.beard@gmail.com>
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
import cmath

# Tests for the addition operator
class TestAddition(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()
	# Test addition of two positive integers
	def test_pos_pos_int(self):
		self.tree.parse('1+1')
		self.assertEqual(self.tree.evaluate(), 2)
	# Test addition of two positive floats
	def test_pos_pos_float(self):
		self.tree.parse('1.5+1.5')
		self.assertEqual(self.tree.evaluate(), 3.0)
	# Test addition of one positive and one negative integer
	def test_pos_neg_int(self):
		self.tree.parse('1+-1')
		self.assertEqual(self.tree.evaluate(), 0)
	# Test addition of one negative and one positive integer
	def test_neg_pos_int(self):
		self.tree.parse('-1+1')
		self.assertEqual(self.tree.evaluate(), 0)
	# Test addition of one positive and one negative float 
	def test_pos_neg_float(self):
		self.tree.parse('1.5+-0.5')
		self.assertEqual(self.tree.evaluate(), 1.0)
	# Test addition of one negative and one positive float
	def test_neg_pos_float(self):
		self.tree.parse('-0.5+1.5')
		self.assertEqual(self.tree.evaluate(), 1.0)
	# Test addition of two negative integers
	def test_neg_neg_int(self):
		self.tree.parse('-1+-1')
		self.assertEqual(self.tree.evaluate(), -2)
	# Test addition of two negative floats
	def test_neg_neg_float(self):
		self.tree.parse('-1.5+-1.5')
		self.assertEqual(self.tree.evaluate(), -3.0)

# Tests for the subtraction operator
class TestSubtraction(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()
	# Test subtraction of two positive integers
	def test_pos_pos_int(self):
		self.tree.parse('1-1')
		self.assertEqual(self.tree.evaluate(), 0)
	# Test subtraction of two positive floats
	def test_pos_pos_float(self):
		self.tree.parse('1.5-0.5')
		self.assertEqual(self.tree.evaluate(), 1.0)
	# Test subtraction of one positive and one negative integer
	def test_pos_neg_int(self):
		self.tree.parse('1--1')
		self.assertEqual(self.tree.evaluate(), 2)
	# Test subtraction of one negative and one positive integer
	def test_neg_pos_int(self):
		self.tree.parse('-1-1')
		self.assertEqual(self.tree.evaluate(), -2)
	# Test subtraction of one positive and one negative float 
	def test_pos_neg_float(self):
		self.tree.parse('1.5--0.5')
		self.assertEqual(self.tree.evaluate(), 2.0)
	# Test subtraction of one negative and one positive float
	def test_neg_pos_float(self):
		self.tree.parse('-0.5-1.5')
		self.assertEqual(self.tree.evaluate(), -2.0)
	# Test subtraction of two negative integers
	def test_neg_neg_int(self):
		self.tree.parse('-1--1')
		self.assertEqual(self.tree.evaluate(), 0)
	# Test subtraction of two negative floats
	def test_neg_neg_float(self):
		self.tree.parse('-1.5--1.5')
		self.assertEqual(self.tree.evaluate(), 0)

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

# Tests for the division operator
class TestDivision(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()
	# Test division of two positive integers
	def test_pos_pos_int(self):
		self.tree.parse('1/2')
		self.assertEqual(self.tree.evaluate(), 0.5)
	# Test division of two positive floats
	def test_pos_pos_float(self):
		self.tree.parse('1.5/0.5')
		self.assertEqual(self.tree.evaluate(), 3.0)
	# Test division of one positive and one negative integer
	def test_pos_neg_int(self):
		self.tree.parse('1/-2')
		self.assertEqual(self.tree.evaluate(), -0.5)
	# Test division of one negative and one positive integer
	def test_neg_pos_int(self):
		self.tree.parse('-1/2')
		self.assertEqual(self.tree.evaluate(), -0.5)
	# Test division of one positive and one negative float 
	def test_pos_neg_float(self):
		self.tree.parse('1.5/-0.5')
		self.assertEqual(self.tree.evaluate(), -3.0)
	# Test division of one negative and one positive float
	def test_neg_pos_float(self):
		self.tree.parse('-1.5/0.5')
		self.assertEqual(self.tree.evaluate(), -3.0)
	# Test division of two negative integers
	def test_neg_neg_int(self):
		self.tree.parse('-1/-2')
		self.assertEqual(self.tree.evaluate(), 0.5)
	# Test division of two negative floats
	def test_neg_neg_float(self):
		self.tree.parse('-1.5/-1.5')
		self.assertEqual(self.tree.evaluate(), 1.0)

# Tests for the exponentiation operator
class TestExponentiation(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()
	# Test exponentiation of two positive integers
	def test_pos_pos_int(self):
		self.tree.parse('2^2')
		self.assertEqual(self.tree.evaluate(), 4)
	# Test exponentiation of two positive floats
	def test_pos_pos_float(self):
		self.tree.parse('9.0^0.5')
		self.assertEqual(self.tree.evaluate(), 3.0)
	# Test exponentiation of one positive and one negative integer
	def test_pos_neg_int(self):
		self.tree.parse('2^-1')
		self.assertEqual(self.tree.evaluate(), 0.5)
	# Test exponentiation of one negative and one positive integer
	def test_neg_pos_int(self):
		self.tree.parse('-2^1')
		self.assertEqual(self.tree.evaluate(), -2)
	# Test exponentiation of one positive and one negative float 
	def test_pos_neg_float(self):
		self.tree.parse('9.0^-0.5')
		self.assertEqual(self.tree.evaluate(), 1.0/3.0)
	# Test exponentiation of one negative and one positive float
	def test_neg_pos_float(self):
		self.tree.parse('-9.0^2.0')
		self.assertEqual(self.tree.evaluate(), 81.0)
	# Test exponentiation of two negative integers
	def test_neg_neg_int(self):
		self.tree.parse('-2^-2')
		self.assertEqual(self.tree.evaluate(), 0.25)
	# Test exponentiation of two negative floats
	def test_neg_neg_float(self):
		self.tree.parse('-1.5^-1.0')
		self.assertEqual(self.tree.evaluate(), -1.0/1.5)
	# Test square root of a negative number
	def test_complex(self):
		self.tree.parse('-4^0.5')
		self.assertAlmostEqual(self.tree.evaluate(), cmath.sqrt(-4))

# Tests for parentheses
class TestParentheses(unittest.TestCase):
	def setUp(self):
		self.tree = expressionparse.Tree()
	# Test for unmatched left parens
	def test_unmatched_lparen(self):
		with self.assertRaises(expressionparse.ParseException):
			self.tree.parse('1+(2+3')
	# Test for unmatched right parens
	def test_unmatched_rparen(self):
		with self.assertRaises(expressionparse.ParseException):
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

# Run the tests
unittest.main()

