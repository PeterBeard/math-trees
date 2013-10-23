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

unittest.main()

