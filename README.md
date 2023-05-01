# Gelic
A dynamically-typed, C-based syntax programming language. Supports arithmetic operations,
conditional statements, and loops. Written in Python 3.

## Usage
1. Clone or download this repository.
2. Navigate to project's root directory.
3. On the terminal, run the command below to start the Gelic interactive mode:
   - `python3 .\gelic.py`

   To run an external .txt file execute the command below. A test folder is provided for sample programs:
   - `python3 .\gelic.py .\test\fib.txt`


## Data Types
- Booleans: 
  - `true; // not false`
  - `false: // not *not* false`
- Numbers:
  - Gelic has only one kind of number: floating point.
  - `1234; // evaluated as 1234.0`
  - `12.34; // float`
- Strings:
  - Gelic strings are enclosed in double quotes.
  - `"Gelic using double quotes for strings."`
  - `"";`
  - `"123";`
- Nulls:
  - Gelic uses the `nil` keyword to represent "no value".

## Expressions
- Arithmetic:
  - Gelic supports basic arithmetic operations just as C does.
  - The minus operator is both used as in infix and a prefix. '-' can be used to negate a number:
    - `-2;`
- Comparison and Equality:
  - Gelic also supports comparison operators:
    - `3 < 4; // true`
    - `3 <= 3; // true`
    - `6 > 10; // false`
    - `6 >= 7; // false`
    - `1 == 2: // false`
    - `"cat" != "dog"; // true`
- Logical Operators:
  - The not operator, a prefix !, returns false if its operand is true, and vice versa.
    - `!true; // false`
    - `!false; // true`
  - `and` and `or` logical operators, identical with C's `&&` (and) and `||` (or)
    - `true and false; // false`
    - `true and true; // true`
    - `false or false; // false`
    - `true or false; // true`
- Precedence and grouping
  - Gelic's operators have the same precedence and associativity as C.
    - `var average = (min + max) / 2;`

## Statements
- Print
  - `print` evaluates a single expression and displays the result to standard output. Syntax is similar to Python 2.
    - `print "Hello, world"; // Hello, world`

# **NOTE: README in progress**