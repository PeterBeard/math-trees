# Parse numeric expressions using trees
class NodeException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ParseException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class EvalException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Tree(object):
	# Initialize the tree
	def __init__(self):
		self.root = None
	# Get the length of the tree
	def __len__(self):
		return len(self.root)
	# Check if two trees are equal
	def __eq__(self, other):
		if isinstance(other, Tree):
			return self.root == other.root
		return False
	# Parse a string expression
	def parse(self, expression):
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
		for char in subexpressions:
			# Invalid character
			if char not in operations and char not in digits and type(char).__name__ not in ['Node', 'Variable', 'Plus', 'Minus', 'Times', 'Divide', 'Exponent', 'Value']:
				raise ParseException('Invalid character: ' + str(char))
			# Add the digit to the current value
			if char in digits or (char in operations and len(curr_value) == 0):
				curr_value.append(char)
			# Add the operation to the parse tree
			elif char in operations:
				if char == '+':
					next_op = Plus()
				elif char == '-':
					next_op = Minus()
				elif char == '*':
					next_op = Times()
				elif char == '/':
					next_op = Divide()
				else:
					next_op = Exponent()
				if curr_op.weight > 0:
					curr_op.addChild(curr_value)
					curr_value = Value()
				if len(curr_value) > 0:
					curr_op = next_op
					curr_op.addChild(curr_value)
					self.root = curr_op
					curr_value = Value()
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
			else:
				curr_value = char
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
	# Make a string representation of the tree
	def __str__(self):
		return self.root.__str__()

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
	# Make a string representation of the node
	def __str__(self):
		return 'Empty Node (' + type(self).__name__ + ')'

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

class Operation(Node):
	# Initialize the operation
	def __init__(self):
		self.left = None
		self.right = None
		self.parent = None
		self.weight = 0
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
	# Return the length of the node
	def __len__(self):
		return len(self.left) + len(self.right)

# Add two nodes together
class Plus(Operation):
	# Initialize the node
	def __init__(self):
		super(Plus,self).__init__()
		self.weight = 1
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() + self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')
	# Return a string representation of the operation
	def __str__(self):
		return '[ ' + self.left.__str__() + ' + ' + self.right.__str__() + ' ]'

# Subtract two nodes
class Minus(Operation):
	# Initialize the node
	def __init__(self):
		super(Minus,self).__init__()
		self.weight = 1
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() - self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')
	# Return a string representation of the operation
	def __str__(self):
		return '[ ' + self.left.__str__() + ' - ' + self.right.__str__() + ' ]'

# Multiply two nodes
class Times(Operation):
	# Initialize the node
	def __init__(self):
		super(Times,self).__init__()
		self.weight = 2
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() * self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')
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
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() / self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')
	# Return a string representation of the operation
	def __str__(self):
		return '[ ' + self.left.__str__() + ' / ' + self.right.__str__() + ' ]'
# Exponentiate two nodes
class Exponent(Operation):
	# Initialize the node
	def __init__(self):
		super(Exponent,self).__init__()
		self.weight = 3
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
	# Return a string representation of the operation
	def __str__(self):
		return '[ ' + self.left.__str__() + ' ^ ' + self.right.__str__() + ' ]'


