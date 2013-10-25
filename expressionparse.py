import inspect
import re

# A general node-related exception
class NodeException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Exception that raised when parsing an expression
class ParseException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Exception that's raised when evaluating an expression
class EvalException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Node(object):
	# Initialize the node
	def __init__(self):
		pass
	# Set a variable
	def setVariable(self, name, value):
		return None
	# Evaluate the node
	def evaluate(self):
		return None
	# Return a nice-looking string representing the node
	def toInfixNotation(self):
		return self.__str__()
	# Return a Polish notation string of the node
	def toPolishNotation(self):
		return self.__str__()
	# Return a Reverse Polish notation string of the node
	def toReversePolishNotation(self):
		return self.__str__()
	# Make a string representation of the node
	def __str__(self):
		return 'Empty Node (' + type(self).__name__ + ')'

# A class representing an expression tree. Contains logic for parsing strings.
# TODO: This class is probably not that different from the Node class, so they should probably be merged or this class should at least be simplified.
class Tree(Node):
	# Initialize the tree
	def __init__(self):
		self.root = None

	# Parse a string expression
	def parse(self, expression):
		self.parseInfixNotation(expression)

	# Parse a string expression written using Infix Notation
	def parseInfixNotation(self, expression):
		operations = ['+','-','*','/','^']
		digits = ['0','1','2','3','4','5','6','7','8','9','.']
		curr_value = Value()
		curr_op = Operation()
		next_op = Operation()
		subexpressions = []
		# Find and parse top-level subexpressions (grouped by parentheses)
		level = 0
		start_index = 0
		end_index = 0
		# First, strip out whitespace from the expression
		expression = expression.replace(' ','')
		# Next replace adjacent parentheses with explicit multiplications so we can parse more easily
		expression = expression.replace(')(',')*(')
		# Make variable multiplications written as adjacent characters (e.g. 3x, xy) explicit
		p = re.compile('(\d+)(\w)')
		expression = p.sub(r'\1*\2',expression)
		p = re.compile('(\w)(\d+)')
		expression = p.sub(r'\1*\2',expression)
		p = re.compile('(\w)(?=\w)')
		expression = p.sub(r'\1*',expression)
		# Multiplication of parenthetical expression can also be written implicitly as 'x(...)' or '(...)x'
		# Make these explicit here
		p = re.compile('([\w\d]+)\(')
		expression = p.sub(r'\1*(',expression)
		p = re.compile('\)([\w\d]+)')
		expression = p.sub(r')*\1',expression)
		# Break the expression up into its subexpressions, recursively parsing them as we go
		for i in range(0,len(expression)):
			char = expression[i]
			if char == '(':
				if level == 0:
					start_index = i+1
				level = level + 1
			elif char == ')':
				level = level - 1
				if level == 0:
					end_index = i
			elif level == 0:
				if char in digits or char in operations:
					subexpressions.append(char)
				else:
					subexpressions.append(Variable(char))
			# Parse the subexpression and add it to the list
			if level == 0 and start_index != end_index:
				subtree = Tree()
				subtree.parse(expression[start_index:end_index])
				subexpressions.append(subtree.root)
				start_index = end_index
		# Were there any unmatched parentheses?
		if level != 0:
			raise ParseException('Unmatched parentheses.')
		# Parse the top-level expression
		for subexp in subexpressions:
			# Invalid character
			if subexp not in operations and subexp not in digits and Node not in inspect.getmro(type(subexp)):
				raise ParseException('Invalid subexpression: ' + str(subexp))
			# Add the digit to the current value
			if subexp in digits or (subexp in operations and len(curr_value) == 0):
				curr_value.append(subexp)
			# Add the operation to the parse tree
			elif subexp in operations:
				# Get an object to represent the operation
				next_op = getOperation(subexp)
				# Add the current value to the current node
				if curr_op.weight > 0:
					curr_op.addChild(curr_value)
					curr_value = Value()
				# If the current value has been set, add it to the next operation and re-root the tree
				if len(curr_value) > 0:
					curr_op = next_op
					curr_op.addChild(curr_value)
					self.root = curr_op
					curr_value = Value()
				# The value was already assigned to the current node, so figure out where to put the next node in the tree
				else:
					# If the next node is heavier than the current one (e.g. * v. +), add it as a child of the current node and make the current node the root of the tree
					if next_op.weight > curr_op.weight:
						c = curr_op.removeChild()
						curr_op.addChild(next_op)
						next_op.addChild(c)
						self.root = curr_op
					# If the current and next nodes have the same weight, add the next node as a child of the current one -- note that this is the same as what we do when the next node is heavier BUT we do NOT re-root the tree
					elif next_op.weight == curr_op.weight:
						c = curr_op.removeChild()
						curr_op.addChild(next_op)
						next_op.addChild(c)
					else:
						next_op.addChild(self.root)
						self.root = next_op
					curr_op = next_op
			# The current subexpression is a node; add it to the tree as-is
			else:
				curr_value = subexp
		# Add the last value to the tree
		curr_op.addChild(curr_value)
		if self.root == None:
			self.root = curr_op

	# Set the value of a variable in the tree
	def setVariable(self, name, value):
		self.root.setVariable(name, value)

	# Try to simplify the tree
	def simplify(self):
		try:
			self.root.simplify()
		except EvalException:
			return False
		# Try to evaluate the simplified root node
		try:
			self.root = self.root.evaluate()
			return True
		except EvalException:
			return False

	# Evaluate the entire tree
	def evaluate(self):
		return self.root.evaluate()

	# Print the tree using Infix Notation
	def toInfixNotation(self):
		return self.root.toInfixNotation()

	# Print the tree using Polish Notation
	def toPolishNotation(self):
		return self.root.toPolishNotation()

	# Print the tree using Reverse Polish Notation
	def toReversePolishNotation(self):
		return self.root.toReversePolishNotation()

	# Make a string representation of the tree
	def __str__(self):
		return self.root.__str__()
	
	# Get the length of the tree
	def __len__(self):
		return len(self.root)

	# Check if two trees are equal
	def __eq__(self, other):
		if isinstance(other, Tree):
			return self.root == other.root
		return False

# A class representing a numeric value, e.g. 5, -7, 2.1, etc.
class Value(Node):
	# Initialize the node
	def __init__(self, val=''):
		self.value = str(val)
	# Append a digit to the value
	def append(self, digit):
		self.value = self.value + str(digit)
	# Simplify the node
	def simplify(self):
		return self
	# Evaluate the node
	def evaluate(self):
		return float(self.value)
	# The length of the value
	def __len__(self):
		return len(self.value)
	# See if two values are equal
	def __eq__(self, other):
		if isinstance(other, Value):
			return self.value == other.value
		return False
	# Return a string representation of the value
	def __str__(self):
		return self.value

# Class representing a variable, e.g. x
class Variable(Node):
	# Initialize the node
	def __init__(self, name=''):
		self.name = str(name)
		self.value = Value()
	# Simplify the node
	def simplify(self):
		return self
	# Evaluate the node
	def evaluate(self):
		try:
			return self.value.evaluate()
		except:
			raise EvalException('Cannot evaluate expressions that contain uninitialized variables.')
	# Set the value of the variable
	def set(self, value):
		if type(value).__name__ == 'Value':
			self.value = value
		else:
			self.value = Value(value)
	# Unset the value of the variable
	def unset(self):
		self.value = Value()
	# Compare two variables
	def __eq__(self, other):
		if type(other) == type(self):
			if self.name == other.name:
				if self.value == other.value:
					return True
				else:
					return False
			else:
				return False
		else:
			return False
	# The length of the value
	def __len__(self):
		return len(self.name)
	# Return a string representation of the value
	def __str__(self):
		try:
			self.value.evaluate()
			return '{' + self.name + '=' + str(self.value) + '}'
		except:
			return self.name

# A class representing a mathematical operation, e.g. plus, minus, etc.
class Operation(Node):
	# Initialize the operation
	def __init__(self):
		self.left = None
		self.right = None
		self.parent = None
		self.weight = 0
		self.symbol = '?'
	# Add a child to the node
	def addChild(self, child):
		if self.left == None:
			self.left = child
			child.parent = self
		elif self.right == None:
			self.right = child
			child.parent = self
		else:
			raise NodeException('Node already has two children.')
	# Remove a child from the node
	def removeChild(self):
		if self.right != None:
			node = self.right
			self.right = None
			node.parent = None
		elif self.left != None:
			node = self.left
			self.left = None
			node.parent = None
		else:
			raise NodeException('Node has no children to remove.')
		return node

	# Try to factor the node
	def factor(self):
		# Factor the children first (if possibe)
		# Left child
		try:
			self.left = self.left.factor()
		except:
			pass
		# Right child
		try:
			self.right = self.right.factor()
		except:
			pass
		# Currently we only know how to factor sums of multiplications since both are commutative
		parent_type = type(self).__name__
		parent_weight = self.weight
		child_type = type(self.left).__name__
		# Make sure the children are both operations, both the same type, and have a greater weight
		if Operation in type(self.left).__bases__ and type(self.left) == type(self.right) and self.left.weight - self.weight == 1:
			# Get grandchildren
			llgc = self.left.left
			lrgc = self.left.right
			rlgc = self.right.left
			rrgc = self.right.right
			common_factor_on_left = False
			# Find the common factor (if any)
			if llgc == rlgc:
				common_factor = llgc
				common_factor_on_left = True
				different_left = lrgc
				different_right = rrgc
			elif llgc == rrgc:
				common_factor = llgc
				common_factor_on_left = True
				different_left = lrgc
				different_right = rlgc
			elif lrgc == rlgc:
				common_factor = lrgc
				different_left = llgc
				different_right = rrgc
			elif lrgc == rrgc:
				common_factor = lrgc
				different_left = llgc
				different_right = rlgc
			else:
				return self
			# Create a new parent node with the type of the original child
			if child_type == 'Times':
				new_parent = Times()
			elif child_type == 'Divide':
				# This operation requires the common factor to be on the same side in both children
				if llgc == rlgc or lrgc == rrgc:
					new_parent = Divide()
				else:
					return self
			elif child_type == 'Exponent':
				# This operation requires the common factor to be on the same side in both children
				if llgc == rlgc or lrgc == rrgc:
					new_parent = Exponent()
				else:
					return self
			else:
				return self
			# Create a new child node with the type of the original parent
			if parent_type == 'Plus':
				new_child = Plus()
			elif parent_type == 'Minus':
				new_child = Minus()
			elif parent_type == 'Times':
				new_child = Times()
			elif parent_type == 'Divide':
				new_child = Divide()
			else:
				return self
			# Add the differing factors as children
			new_child.addChild(different_left)
			new_child.addChild(different_right)
			# Add the common factor as a child of the times node
			if common_factor_on_left:
				new_parent.addChild(common_factor)
				new_parent.addChild(new_child)
			else:
				new_parent.addChild(new_child)
				new_parent.addChild(common_factor)
			# Return the re-factored node
			return new_parent
		else:
			return self

	# Simplify the node
	def simplify(self):
		simplified = True
		try:
			lvalue = self.left.simplify()
			self.left = lvalue
		except EvalException:
			simplified = False	

		try:
			rvalue = self.right.simplify()
			self.right = rvalue
		except EvalException:
			simplified = False

		if simplified:
			return Value(self.evaluate())
		else:
			return self

	# Check whether the node contains a certain variable
	def containsVariable(self, varname):
		# Is the variable in the left child?
		if type(self.left).__name__ == 'Variable' and self.left.name == varname:
			return True
		elif type(self.left).__name__ != 'Value':
			return self.left.containsVariable(varname)
		# Is the variable in the right child?
		if type(self.right).__name__ == 'Variable' and self.right.name == varname:
			return True
		elif type(self.right).__name__ != 'Value':
			return self.right.containsVariable(varname)
		# Didn't find the variable
		return False

	# Set the value of a variable in this node
	def setVariable(self, name, value):
		# See if the variable exists in the left and/or right subtrees
		# Left side
		if type(self.left).__name__ == 'Variable' and self.left.name == name:
			self.left.set(value)
		else:
			self.left.setVariable(name, value)
		# Right side
		if type(self.right).__name__ == 'Variable' and self.right.name == name:
			self.right.set(value)
		else:
			self.right.setVariable(name, value)
		

	# Return the value of this node
	def evaluate(self):
		return None
			
	# See if two operation nodes are equal
	def __eq__(self, other):
		if type(other) == type(self):
			return (self.left == other.left) and (self.right == other.right)
		return False

	# Return a Infix Notation string representing the operation
	def toInfixNotation(self):
		lstring = self.left.toInfixNotation()
		rstring = self.right.toInfixNotation()
		string = ''
		if Operation in type(self.left).__bases__ and self.weight > self.left.weight:
			string += '(' + lstring + ')'
		else:
			string += lstring

		string += ' ' + self.symbol + ' '
		if Operation in type(self.right).__bases__ and self.weight > self.right.weight:
			string += '(' + rstring + ')'
		else:
			string += rstring

		return string

	# Return a Polish Notation string of the operation
	def toPolishNotation(self):
		lstring = self.left.toPolishNotation()
		rstring = self.right.toPolishNotation()
		string = self.symbol + ' '
		if Operation in type(self.left).__bases__ and self.weight > self.left.weight:
			string += '(' + lstring + ')'
		else:
			# Pull off the operator if the left child has the same type
			if type(self) == type(self.left):
				string += lstring[2:]
			else:
				string += lstring
		string += ' '
		if Operation in type(self.right).__bases__ and self.weight > self.right.weight:
			string += '(' + rstring + ')'
		else:
			# Pull off the operator if the right child has the same type
			if type(self) == type(self.right):
				string += rstring[2:]
			else:
				string += rstring
		
		return string

	# Return a Reverse Polish Notation string of the operation
	def toReversePolishNotation(self):
		lstring = self.left.toReversePolishNotation()
		rstring = self.right.toReversePolishNotation()
		string = ''
		if Operation in type(self.left).__bases__ and self.weight > self.left.weight:
			string += '(' + lstring + ')'
		else:
			# Pull off the operator if the left child has the same type
			if type(self) == type(self.left):
				string += lstring[:-2]
			else:
				string += lstring
		string += ' '
		if Operation in type(self.right).__bases__ and self.weight > self.right.weight:
			string += '(' + rstring + ')'
		else:
			# Pull off the operator if the right child has the same type
			if type(self) == type(self.right):
				string += rstring[:-2]
			else:
				string += rstring
		
		string += ' ' + self.symbol

		return string
		#return '(' + self.left.toReversePolishNotation() + ' ' + self.right.toReversePolishNotation() + ' ' + self.symbol + ' )'

	# Return the length of the node
	def __len__(self):
		return len(self.left) + len(self.right)

	# Return a string representation of the node
	def __str__(self):
		return '[ ' + self.left.__str__() + ' ' + self.symbol + ' ' + self.right.__str__() + ' ]'

# Add two nodes together
class Plus(Operation):
	# Initialize the node
	def __init__(self):
		super(Plus,self).__init__()
		self.weight = 1
		self.symbol = '+'
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() + self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')

# Subtract two nodes
class Minus(Operation):
	# Initialize the node
	def __init__(self):
		super(Minus,self).__init__()
		self.weight = 1
		self.symbol = '-'
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() - self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')

# Multiply two nodes
class Times(Operation):
	# Initialize the node
	def __init__(self):
		super(Times,self).__init__()
		self.weight = 2
		self.symbol = '*'
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() * self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')
	# Try to factor the node
	def factor(self):
		# Factor the children first (if possibe)
		# Left child
		try:
			self.left = self.left.factor()
		except:
			pass
		# Right child
		try:
			self.right = self.right.factor()
		except:
			pass
		# Currently we only know how to factor sums of multiplications since both are commutative
		parent_type = type(self).__name__
		parent_weight = self.weight
		child_type = type(self.left).__name__
		# Make sure the children are both operations, both the same type, and have a greater weight
		if Operation in type(self.left).__bases__ and type(self.left) == type(self.right) and self.left.weight - self.weight == 1:
			if child_type != 'Exponent':
				return super(Times,self).factor()
			else:
				# Get grandchildren
				llgc = self.left.left
				lrgc = self.left.right
				rlgc = self.right.left
				rrgc = self.right.right
				common_factor_on_left = False
				# Find the common factor (if any)
				if llgc == rlgc:
					common_factor = llgc
					common_factor_on_left = True
					different_left = lrgc
					different_right = rrgc
				elif llgc == rrgc:
					common_factor = llgc
					common_factor_on_left = True
					different_left = lrgc
					different_right = rlgc
				elif lrgc == rlgc:
					common_factor = lrgc
					different_left = llgc
					different_right = rrgc
				elif lrgc == rrgc:
					common_factor = lrgc
					different_left = llgc
					different_right = rlgc
				else:
					return self
				# If the common factor is on the right, normal factoring rules apply
				if not common_factor_on_left:
					return super(Times,self).factor()
				# Create a new parent node with the type of the original child
				if child_type == 'Exponent':
					# This operation requires the common factor to be on the same side in both children
					if llgc == rlgc or lrgc == rrgc:
						new_parent = Exponent()
					else:
						return self
				else:
					return self
				# Since this is a multiplication, we need to convert to addition of the exponents
				new_child = Plus()
				# Add the differing factors as children
				new_child.addChild(different_left)
				new_child.addChild(different_right)
				# Add the common factor as a child of the times node
				new_parent.addChild(common_factor)
				new_parent.addChild(new_child)
				# Return the re-factored node
				return new_parent
		else:
			return self
	# Return an Infix Notation string representing the operation
	def toInfixNotation(self):
		lstring = self.left.toInfixNotation()
		rstring = self.right.toInfixNotation()
		
		if Operation in type(self.left).__bases__ and self.weight > self.left.weight:
			lstring = '(' + lstring + ')'

		if Operation in type(self.right).__bases__ and self.weight > self.right.weight:
			rstring = '(' + rstring + ')'

		# Multiplication of variables is usually written with the variables adjacent to each other
		if not (type(self.left).__name__ == 'Value' and type(self.right).__name__ == 'Value'):
			return lstring + rstring
		else:
			return lstring + ' * ' + rstring

	# Return a string representation of the operation
	def __str__(self):
		# Multiplication of variables is usually written with the variables adjacent to each other
		if type(self.left).__name__ == 'Variable' and type(self.right).__name__ == 'Variable':
			return '[ ' + self.left.name + self.right.name + ' ]'
		else:
			return '[ ' + self.left.__str__() + ' * ' + self.right.__str__() + ' ]'

# Divide two nodes
class Divide(Operation):
	# Initialize the node
	def __init__(self):
		super(Divide,self).__init__()
		self.weight = 2
		self.symbol = '/'
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() / self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')
	# Try to factor the node
	def factor(self):
		# Factor the children first (if possibe)
		# Left child
		try:
			self.left = self.left.factor()
		except:
			pass
		# Right child
		try:
			self.right = self.right.factor()
		except:
			pass
		# Currently we only know how to factor sums of multiplications since both are commutative
		parent_type = type(self).__name__
		parent_weight = self.weight
		child_type = type(self.left).__name__
		# Make sure the children are both operations, both the same type, and have a greater weight
		if Operation in type(self.left).__bases__ and type(self.left) == type(self.right) and self.left.weight - self.weight == 1:
			if child_type != 'Exponent':
				return super(Divide,self).factor()
			else:
				# Get grandchildren
				llgc = self.left.left
				lrgc = self.left.right
				rlgc = self.right.left
				rrgc = self.right.right
				common_factor_on_left = False
				# Find the common factor (if any)
				if llgc == rlgc:
					common_factor = llgc
					common_factor_on_left = True
					different_left = lrgc
					different_right = rrgc
				elif llgc == rrgc:
					common_factor = llgc
					common_factor_on_left = True
					different_left = lrgc
					different_right = rlgc
				elif lrgc == rlgc:
					common_factor = lrgc
					different_left = llgc
					different_right = rrgc
				elif lrgc == rrgc:
					common_factor = lrgc
					different_left = llgc
					different_right = rlgc
				else:
					return self
				# If the common factor is on the right, normal factoring rules apply
				if not common_factor_on_left:
					return super(Divide,self).factor()
				# Create a new parent node with the type of the original child
				if child_type == 'Exponent':
					# This operation requires the common factor to be on the same side in both children
					if llgc == rlgc or lrgc == rrgc:
						new_parent = Exponent()
					else:
						return self
				else:
					return self
				# Since this is a multiplication, we need to convert to addition of the exponents
				new_child = Minus()
				# Add the differing factors as children
				new_child.addChild(different_left)
				new_child.addChild(different_right)
				# Add the common factor as a child of the times node
				new_parent.addChild(common_factor)
				new_parent.addChild(new_child)
				# Return the re-factored node
				return new_parent
		else:
			return self

# Exponentiate two nodes
class Exponent(Operation):
	# Initialize the node
	def __init__(self):
		super(Exponent,self).__init__()
		self.weight = 3
		self.symbol = '^'
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			lvalue = self.left.evaluate()
			rvalue = self.right.evaluate()
			# Exponents are dumb and mean when negative numbers are involved
			if lvalue < 0:
				if rvalue == int(rvalue):
					return lvalue ** rvalue
				else:
					# The answer will be complex
					return (lvalue + 0j) ** rvalue
			else:
				return lvalue ** rvalue
		else:
			raise NodeException('Node does not have enough children.')

# Return an object of the correct type given the symbol representing an operation
def getOperation(operation_symbol):
	if operation_symbol == '+':
		return Plus()
	elif operation_symbol == '-':
		return Minus()
	elif operation_symbol == '*':
		return Times()
	elif operation_symbol == '/':
		return Divide()
	elif operation_symbol == '^':
		return Exponent()
	else:
		raise ParseError('Unknown operation "' + operation_symbol + '"')

