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
		self.root = Node()
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
		operation_weights = {
			'+':1,
			'-':1,
			'*':2,
			'/':2,
			'^':3
		}
		digits = ['0','1','2','3','4','5','6','7','8','9','.']
		curr_value = Value()
		curr_weight = 0
		next_weight = 0
		curr_op = None
		next_op = None
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
			if char not in operations and char not in digits and type(char).__name__ not in ['Node', 'Variable', 'Plus', 'Minus', 'Times', 'Divided', 'Exponent', 'Value']:
				raise ParseException('Invalid character')
			# Add the digit to the current value
			if char in digits or (char in operations and len(curr_value) == 0):
				curr_value.append(char)
			# Add the operation to the parse tree
			elif char in operations:
				next_weight = operation_weights[char]
				if curr_op != None:
					curr_op.addChild(curr_value)
					curr_value = Value()
				else:
					curr_weight = next_weight
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
				if len(curr_value) > 0:
					curr_op = next_op
					curr_op.addChild(curr_value)
					self.root = curr_op
					curr_value = Value()
				else:
					if next_weight > curr_weight:
						c = curr_op.removeChild()
						curr_op.addChild(next_op)
						next_op.addChild(c)
						self.root = curr_op
					else:
						next_op.addChild(self.root)
						self.root = next_op
					curr_op = next_op
					curr_weight = next_weight
			else:
				curr_value = char
		# Add the last value to the tree
		curr_op.addChild(curr_value)
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
	# Evaluate the node
	def evaluate(self):
		return 0
	# Make a string representation of the node
	def __str__(self):
		return 'Empty Node'

class Value(Node):
	# Initialize the node
	def __init__(self, val=''):
		self.value = str(val)
	# Append a digit to the value
	def append(self, digit):
		self.value = self.value + str(digit)
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
	# Evaluate the node
	def evaluate(self):
		raise EvalException('Cannot evaluate expressions that contain variables.')
		return self.name
	# The length of the value
	def __len__(self):
		return len(self.name)
	# Return a string representation of the value
	def __str__(self):
		return self.name

class Operation(Node):
	# Initialize the operation
	def __init__(self):
		self.left = None
		self.right = None
	# Add a child to the node
	def addChild(self, child):
		if not self.left:
			self.left = child
		elif not self.right:
			self.right = child
		else:
			raise NodeException('Node already has two children.')
	# Remove a child from the node
	def removeChild(self):
		if self.right:
			node = self.right
			self.right = None
		elif self.left:
			node = self.left
			self.left = None
		else:
			raise NodeException('Node has no children to remove.')
		return node
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
	# Evaluate the node
	def evaluate(self):
		if self.left and self.right:
			return self.left.evaluate() * self.right.evaluate()
		else:
			raise NodeException('Node does not have enough children.')
	# Return a string representation of the operation
	def __str__(self):
		return '[ ' + self.left.__str__() + ' * ' + self.right.__str__() + ' ]'

# Divide two nodes
class Divide(Operation):
	# Initialize the node
	def __init__(self):
		super(Divide,self).__init__()
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


