# computorV1
A program that solves a polynomial equation of up to second degree.

## Usage
```bash
Usage: python3 computor.py '<polynomial equaion>' [-v]

-v    : verbose (displays AST and Dictionaries)

Rules :
       - Lexic:
                • Equal          : =
                • Multiplication : *
                • Division       : /
                • Addition       : +
                • Substraction   : -
                • Variable Exp.  : ^
                • Variable       : x / X
                • Coefficient    : n (float / int)
       - Syntax:
                • ONE equal sign
                • Operations are binary
                • Spaces are irrelevant
                • Exponents are only for variables
       - Semantic:
                • Polynomial degree in range [0, 2]
                • Mathematically consistent
                • No divisions by zero

Example:
       python3 computor.py '8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^2 = 3 * X^0'
```
## Examples
```bash
$ python3 computor.py '125 * X + 10 * X^2 = 0'
Reduced form: 125 * x + 10 * x⁽²⁾ = 0
Polynomial degree: 2
Steps:

x = ( -b ± sqrt(b⁽²⁾ - 4(a)(c)) ) / 2(a)

a = 10.0
b = 125.0
c = 0

x = ( -(125.0) ± sqrt(125.0⁽²⁾ - 4(10.0)(0)) ) / 2(10.0)
x = ( -(125.0) ± sqrt((15625.0) - (0.0)) ) / 20.0
x = ( -(125.0) ± sqrt(15625.0) ) / 20.0

The discriminant is positive and has 2 real and distinct roots

x = ( -(125.0) ± 125.0 ) / 20.0
x1 = ( -(125.0) - 125.0 ) / 20.0
x2 = ( -(125.0) + 125.0 ) / 20.0
x1 = -250.0 / 20.0
x2 = 0.0 / 20.0

Solutions:
x1 = -12.5 or -23/2
x2 = 0
```
