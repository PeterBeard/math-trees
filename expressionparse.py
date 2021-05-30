# Expressionparse v0.2 -- Create syntax trees for mathematical expressions
#
# Copyright (C) 2021, Peter Beard <peter.b.beard@gmail.com>
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

import math
import re
import copy


# A general node-related exception
class NodeException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Exception raised when tokenizing an expression
class TokenizeException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


# Exception that's raised when parsing an expression
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


# The base node class. Implements evaluation and stringification functions.
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


# A class to tokenize input strings and feed the tokens to the parser
class Tokenizer(object):
    # Some static constants
    OPENPAREN = '('
    CLOSEPAREN = ')'

    # Initialize the tokenizer and tokenize the string
    def __init__(self, string):
        self.tokens = []
        # First, strip out whitespace from the string
        string = string.replace(' ','')
        # Next replace adjacent parentheses with explicit multiplications so we can parse more easily
        string = string.replace(')(',')*(')
        # Check for unmatches parentheses
        level = 0
        for char in string:
            if char == '(':
                level += 1
            elif char == ')':
                level -= 1
        if level != 0:
            raise TokenizeException('Unmatched parenthesis.')
        # Make variable multiplications written as adjacent characters (e.g. 3x, xy) explicit
        p = re.compile('(\d+)(\w)')
        string = p.sub(r'\1*\2',string)
        p = re.compile('(\w)(\d+)')
        string = p.sub(r'\1*\2',string)
        p = re.compile('(\w)(?=\w)')
        string = p.sub(r'\1*',string)
        # Multiplication of parenthetical expression can also be written implicitly as 'x(...)' or '(...)x'
        # Make these explicit here
        p = re.compile('([\w\d]+)\(')
        string = p.sub(r'\1*(',string)
        p = re.compile('\)([\w\d]+)')
        string = p.sub(r')*\1',string)
        # The characters that we recognize
        numbers = '01234567890.'
        operators = '+-*/^!'
        # Iterate over the string and create tokens of the appropriate type
        curr_value = Value()
        for i in range(0,len(string)):
            char = string[i]
            if char == Tokenizer.OPENPAREN:
                self.pushToken(char)
            elif char == Tokenizer.CLOSEPAREN:
                if len(curr_value) > 0:
                    self.pushToken(curr_value)
                    curr_value = Value()
                self.pushToken(char)
            elif char in numbers or (char == '-' and string[i+1] in numbers and len(curr_value) == 0 and string[i-1] != Tokenizer.CLOSEPAREN):
                curr_value.append(char)
                # Last value in the string
                if i == len(string)-1:
                    self.pushToken(curr_value)
            elif char in operators:
                if len(curr_value) > 0:
                    self.pushToken(curr_value)
                    curr_value = Value()
                self.pushToken(getOperation(char))
            else:
                if len(curr_value) > 0:
                    self.pushToken(curr_value)
                    curr_value = Value()
                self.pushToken(Variable(char))

    # Return the next token in the list (at the beginning)
    def getToken(self):
        if len(self.tokens) > 0:
            return self.tokens.pop(0)
        else:
            return None

    # Return the next token in the list without removing it
    def peekToken(self):
        if len(self.tokens) > 0:
            return self.tokens[0]
        else:
            return None

    # Add a token to the end of the list
    def pushToken(self, token):
        self.tokens.append(token)


# A class representing an expression tree. Contains logic for parsing strings.
# TODO: This class is probably not that different from the Node class, so they
# 	    should probably be merged or this class should at least be simplified.
class Tree(Node):
    # Initialize the tree
    def __init__(self):
        super(Tree, self).__init__()
        self.root = None

    # Parse a string expression
    def parse(self, expression):
        # TODO: This function should be able to detect the type of notation and choose the correct parser
        self.parseInfixNotation(expression)

    # Parse a string expression written using Infix Notation
    def parseInfixNotation(self, expression):
        # Tokenize the expression
        tokenizer = Tokenizer(expression)
        # Iterate over the tokens
        tokenIndex = 0
        token = 0
        curr_value = None
        subtree_root = Operation()
        prev_op = None
        curr_op = None
        self.root = Operation()
        paren_stack = []
        while token is not None:
            tokenIndex += 1
            token = tokenizer.getToken()
            # No tokens left
            if token is None:
                # If there are no operations, the current value must be the entire tree
                if len(subtree_root) == 0:
                    subtree_root = curr_value
                elif curr_value is not None and len(subtree_root) < 2:
                    subtree_root.addChild(curr_value)
                break
            # Parse the token
            if token == Tokenizer.OPENPAREN:
                paren_stack.append(copy.deepcopy(subtree_root))
                subtree_root = Operation()
                prev_op = Operation()
                curr_op = Operation()
            elif token == Tokenizer.CLOSEPAREN:
                paren_op = paren_stack.pop()
                # Insert the parenthetical expression in the tree
                if len(paren_op) < 2:
                    paren_op.addChild(subtree_root)
                else:
                    paren_op.addWhereOpen(subtree_root)
                # Re-root the tree and continue parsing
                subtree_root = paren_op
                prev_op = subtree_root
            elif isinstance(token, Variable) or isinstance(token, Value):
                if curr_value is None:
                    curr_value = token
                    if (tokenizer.peekToken() is None or tokenizer.peekToken() == Tokenizer.CLOSEPAREN) and prev_op is not None:
                        prev_op.addChild(curr_value)
                        curr_value = None
                #else:
                #	raise ParseException("Too many values at token " + str(tokenIndex))
            elif isinstance(token, Operation):
                if curr_value == None and subtree_root.symbol == '?':
                    token.addChild(subtree_root.left)
                    subtree_root = token
                    prev_op = token
                elif prev_op is not None and len(prev_op) > 0:
                    if curr_value != None:
                        prev_op.addChild(curr_value)
                        curr_value = None
                    curr_op = token
                    # Determine parent-child relationship based on operation weights
                    # If the next node is heavier than the current one (e.g. * v. +), add it as a child of the current node and make the current node the root of the tree
                    if curr_op.weight > prev_op.weight:
                        c = prev_op.removeChild()
                        prev_op.addChild(curr_op)
                        curr_op.addChild(c)
                        subtree_root = prev_op
                    # If the current and next nodes have the same weight, add the next node as a child of the current one -- note that this is the same as what we do when the next node is heavier BUT we do NOT re-root the tree
                    elif curr_op.weight == prev_op.weight:
                        c = prev_op.removeChild()
                        prev_op.addChild(curr_op)
                        curr_op.addChild(c)
                    # If the next node is lighter than the current one, add the current node as a child of the next one and make the next one the root of the tree
                    else:
                        curr_op.addChild(subtree_root)
                        subtree_root = curr_op
                    prev_op = curr_op
                else:
                    prev_op = token
                    prev_op.addChild(curr_value)
                    subtree_root = prev_op
                    curr_value = None
        # An undefined operation with only one child can be simplified. Let's.
        if isinstance(subtree_root, Operation) and subtree_root.symbol == '?' and subtree_root.right == None:
            self.root = subtree_root.left
        else:
            self.root = subtree_root

    # Set the value of a variable in the tree
    def setVariable(self, name, value):
        if isinstance(self.root, Operation):
            self.root.setVariable(name, value)
        elif isinstance(self.root, Variable) and self.root.name == name:
            self.root.set(value)

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
        super(Value, self).__init__()
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
        super(Variable, self).__init__()
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
        if isinstance(value, Value):
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
        super(Operation, self).__init__()
        self.left = None		# Initialize left child to none
        self.right = None		# Initialize right child to none
        self.parent = None		# Initialize parent to none
        self.weight = 0			# Default weight is 0
        self.symbol = '?'		# Default operator symbol is ?
        self.arity = 2			# Default to binary operator

    # Add a child to the node
    def addChild(self, child):
        if self.left is None:
            self.left = child
            child.parent = self
        elif self.right is None:
            self.right = child
            child.parent = self
        else:
            raise NodeException('Node already has two children.')

    # Remove a child from the node
    def removeChild(self):
        if self.right is not None:
            node = self.right
            self.right = None
            node.parent = None
        elif self.left is not None:
            node = self.left
            self.left = None
            node.parent = None
        else:
            raise NodeException('Node has no children to remove.')
        return node

    # Find somewhere in this tree to add a child node. Return false if there are no open spots
    def addWhereOpen(self, child):
        # Can we have another child?
        if self.right is None:
            self.addChild(child)
            return True
        else:
            # Try to add the new child to one of our child nodes
            if isinstance(self.left, Operation) and isinstance(self.right, Operation):
                # Try the left node first
                success = self.left.addWhereOpen(child)
                # Only try the right node if the left node failed
                if not success:
                    success = self.right.addWhereOpen(child)
                return success
            # Can we insert into the left node?
            elif isinstance(self.left, Operation):
                return self.left.addWhereOpen(child)
            # What about the right node?
            elif isinstance(self.right, Operation):
                return self.right.addWhereOpen(child)
            # There was nowhere to insert another node
            else:
                return False

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
        if isinstance(self.left, Operation) and type(self.left) == type(self.right) and self.left.weight - self.weight == 1:
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
        if isinstance(self.left, Variable) and self.left.name == varname:
            return True
        elif not isinstance(self.left, Value):
            return self.left.containsVariable(varname)
        # Is the variable in the right child?
        if isinstance(self.right, Variable) and self.right.name == varname:
            return True
        elif not isinstance(self.right, Value):
            return self.right.containsVariable(varname)
        # Didn't find the variable
        return False

    # Set the value of a variable in this node
    def setVariable(self, name, value):
        # See if the variable exists in the left and/or right subtrees
        # Left side
        if isinstance(self.left, Variable) and self.left.name == name:
            self.left.set(value)
        else:
            self.left.setVariable(name, value)
        # Right side
        if isinstance(self.right, Variable) and self.right.name == name:
            self.right.set(value)
        else:
            self.right.setVariable(name, value)

    # Return the value of this node
    def evaluate(self):
        return None

    # Return an Infix Notation string representing the operation
    def toInfixNotation(self):
        # Unary operators
        if self.arity == 1:
            lstring = self.left.toInfixNotation()
            if isinstance(self.left, Operation) and self.weight > self.left.weight:
                string = '(' + lstring + ')'
            else:
                string = lstring
            string += self.symbol
        # Binary operators
        elif self.arity == 2:
            lstring = self.left.toInfixNotation()
            rstring = self.right.toInfixNotation()
            string = ''
            if isinstance(self.left, Operation) and self.weight > self.left.weight:
                string += '(' + lstring + ')'
            else:
                string += lstring

            string += ' ' + self.symbol + ' '
            if isinstance(self.right, Operation) and self.weight > self.right.weight:
                string += '(' + rstring + ')'
            else:
                string += rstring
        else:
            raise ValueError('Operators with arity other than 1 or 2 cannot be converted to infix notation')

        return string

    # Return a Polish Notation string of the operation
    def toPolishNotation(self):
        if self.arity == 1:
            lstring = self.left.toPolishNotation()
            string = self.symbol + ' '
            if isinstance(self.left, Operation) and self.weight > self.left.weight:
                string += '(' + lstring + ')'
            else:
                # Pull off the operator if the left child has the same type
                if isinstance(self, type(self.left)):
                    string += lstring[2:]
                else:
                    string += lstring
        else:
            lstring = self.left.toPolishNotation()
            rstring = self.right.toPolishNotation()
            string = self.symbol + ' '
            if isinstance(self.left, Operation) and self.weight > self.left.weight:
                string += '(' + lstring + ')'
            else:
                # Pull off the operator if the left child has the same type
                if isinstance(self, type(self.left)):
                    string += lstring[2:]
                else:
                    string += lstring
            string += ' '
            if isinstance(self.right, Operation) and self.weight > self.right.weight:
                string += '(' + rstring + ')'
            else:
                # Pull off the operator if the right child has the same type
                if isinstance(self, type(self.right)):
                    string += rstring[2:]
                else:
                    string += rstring

        return string

    # Return a Reverse Polish Notation string of the operation
    def toReversePolishNotation(self):
        if self.arity == 1:
            lstring = self.left.toReversePolishNotation()
            if isinstance(self.left, Operation) and self.weight > self.left.weight:
                string = '(' + lstring + ')'
            else:
                # Pull off the operator if the left child has the same type
                if type(self) == type(self.left):
                    string = lstring[:-2]
                else:
                    string = lstring
            string += ' ' + self.symbol
        else:
            lstring = self.left.toReversePolishNotation()
            rstring = self.right.toReversePolishNotation()
            string = ''
            if isinstance(self.left, Operation) and self.weight > self.left.weight:
                string += '(' + lstring + ')'
            else:
                # Pull off the operator if the left child has the same type
                if type(self) == type(self.left):
                    string += lstring[:-2]
                else:
                    string += lstring
            string += ' '
            if isinstance(self.right, Operation) and self.weight > self.right.weight:
                string += '(' + rstring + ')'
            else:
                # Pull off the operator if the right child has the same type
                if type(self) == type(self.right):
                    string += rstring[:-2]
                else:
                    string += rstring

            string += ' ' + self.symbol

        return string

    # See if two operation nodes are equal
    def __eq__(self, other):
        if type(other) == type(self):
            return (self.left == other.left) and (self.right == other.right)
        return False

    # Return the length of the node
    def __len__(self):
        left_len = 0
        right_len = 0
        # Get the lengths of the non-None children
        if self.left is not None:
            left_len = len(self.left)
        if self.right is not None:
            right_len = len(self.right)
        # Return the sum of the lengths
        return left_len + right_len

    # Return a string representation of the node
    def __str__(self):
        # Unary operators
        if self.arity == 1:
            return '[ ' + self.left.__str__() + ' ' + self.symbol + ' ]'
        # Binary operatorys
        else:
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
        if isinstance(self.left, Operation) and type(self.left) == type(self.right) and self.left.weight - self.weight == 1:
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

        if isinstance(self.left, Operation) and self.weight > self.left.weight:
            lstring = '(' + lstring + ')'

        if isinstance(self.right, Operation) and self.weight > self.right.weight:
            rstring = '(' + rstring + ')'

        # Multiplication of variables is usually written with the variables adjacent to each other
        if isinstance(self.left, Variable) or isinstance(self.right, Variable):
            return lstring + rstring
        else:
            return lstring + ' * ' + rstring


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
        if isinstance(self.left, Operation) and type(self.left) == type(self.right) and self.left.weight - self.weight == 1:
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


# Calculate the factorial of a node
# ** This is an unary operator **
class Factorial(Operation):
    # Initialize the node
    def __init__(self):
        super(Factorial, self).__init__()
        self.weight = 4
        self.symbol = '!'
        self.arity = 1

    # Add a child to the node
    def addChild(self, child):
        if self.left is None:
            self.left = child
            child.parent = self
        else:
            raise NodeException('Node already has one child.')

    # Remove a child from the node
    def removeChild(self):
        if self.left is not None:
            c = self.left
            self.left = None
            c.parent = None
            return c
        else:
            raise NodeException('Node has no children to remove.')

    # Evaluate the node
    def evaluate(self):
        if self.left is not None and self.right is None:
            cvalue = self.left.evaluate()
            # Right now factorial is only defined for the natural numbers
            if cvalue >= 0 and cvalue == int(cvalue):
                return math.factorial(cvalue)
            else:
                raise EvalException('Cannot compute the factorial of negative numbers or non-integers.')
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
    elif operation_symbol == '!':
        return Factorial()
    else:
        raise ParseException('Unknown operation "' + operation_symbol + '"')
