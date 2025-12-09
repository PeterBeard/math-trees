math-trees
==========

Use Python to create and evaluate parse trees for simple algebraic expressions.

Prerequisites
=============

This software works in both Python 2.7 and Python 3.

Usage
=====

To use the library, simply import the main Python file with `import expressionparse`

To parse an expression, create a new Tree object and use its parse() method:

    import expressionparse
    
    expression = 'x+y'

    t = expressionparse.Tree(expression)

The software is currently only capable of parsing expressions written using infix notation and containing only the +,-,*,/,^, and ! operations.

Output
------

Once an expression has been parsed, various output options are available (all return strings):

* Polish Notation (`Tree.toPolishNotation`)
* Infix Notation (`Tree.toInfixNotation`)
* Reverse Polish Notation (`Tree.toReversePolishNotation`)

```python
    >>> t = expressionparse.Tree('2*2+1')
    >>> print(t.toPolishNotation())
    
    + * 2 2 1
    
    >>> print(t.toInfixNotation())
    
    2 * 2 + 1
    
    >>> print(t.toReversePolishNotation())
    
    2 2 * 1 +
```

Trees and nodes can also be stringified using the str() operator. This will output using infix notation but with explicit delineation of the various nodes using square brackets.

```python
    >>> t = expressionparse.Tree('2*2+1')
    >>> print(t)
    
    [ [ 2 * 2 ] + 1 ]
```

Evaluating Expressions
----------------------

Expressions containing only numbers can be evaluated using the Tree.evaluate method. If an error is encountered during evaluation, an EvalException will be raised.

```python
    >>> t = expressionparse.Tree('1+2')
    >>> print(t.evaluate())
    
    3.0
```

Variables
---------

The math-trees library can parse expressions containing variables with single-character names, e.g. 'x' or 'y'.

Expressions containing variables cannot be evaluated unless the values of all variables have been set using the Tree.setVariable method.

```python
    >>> t = expressionparse.Tree('x+2')
    >>> t.setVariable('x',1)
    >>> print(t.evaluate())
    
    3.0
```
