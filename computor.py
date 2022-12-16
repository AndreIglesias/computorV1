# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computor.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ciglesia <ciglesia@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/12 15:45:24 by ciglesia          #+#    #+#              #
#    Updated: 2022/12/16 18:24:44 by ciglesia         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import re
import copy
from pprint import pprint

symbol_table = {'x', 'X', '^', '+', '-', '*', '/', '=', '.'}
symbol_op = {'+', '-', '*', '/'}
symbol_friend = {'x', 'X'}
symbol_exp = "⁰¹²³⁴⁵⁶⁷⁸⁹"

class Polynome(object):
    def __init__(self, eq: str):
        self.eq = eq
        self.ast = None
        self.ast_left = None
        self.ast_right = None
        self.equation = {}
        self.__parser()
        self.reduced_left = self.__dictionary(self.ast_left)
        self.reduced_right = self.__dictionary(self.ast_right)
        self.reduced = None
        self.__reduce_d()
        self.degree = 0
        if len(self.reduced) != 0:
            self.degree = max(self.reduced)
        self.print_info()

    def __print_exponent(self, exponent: int):
        xp = "⁾"
        sign = ""
        if exponent < 0:
            sign = "⁻"
            exponent *= -1
        while exponent > 0:
            xp += symbol_exp[int(abs(exponent % 10))]
            exponent //= 10
        xp += sign
        xp += "⁽"
        print(xp[::-1], end="")

    def __quadratic(self, a: int or float, b: int or float, c: int or float) -> tuple:
        print("Steps:")
        print("x = ( -b ± sqrt(b⁽²⁾ - 4(a)(c)) ) / 2(a)".format(-b, b, a, c, a))
        print("x = ( -({:}) ± sqrt({:}⁽²⁾ - 4({:})({:})) ) / 2({:})".format(-b, b, a, c, a))
        b2 = b ** 2
        ac4 = 4 * a * c
        a2 = 2 * a
        print("x = ( -({:}) ± sqrt(({:}) - ({:})) ) / {:}".format(-b, b2, ac4, a2))
        print("x = ( -({:}) ± sqrt({:}) ) / {:}".format(-b, b2 - ac4, a2))
        sq = round((b2 - ac4)**(1/2), 4)
        print("x = ( -({:}) ± {:} ) / {:}".format(-b, sq, a2))
        print("x1 = ( -({:}) - {:} ) / {:}".format(-b, sq, a2))
        print("x2 = ( -({:}) + {:} ) / {:}".format(-b, sq, a2))
        print("x1 = {:} / {:}".format((-b) - sq, a2))
        print("x2 = {:} / {:}".format((-b) + sq, a2))
        print("Solutions:")
        x1 = round(((-b) - sq) / a2, 4)
        xa1, xb1 = x1.as_integer_ratio()
        if xb1 != 1 and (-1000 < xa1 and xa1 < 1000) and \
           (-1000 < xb1 and xb1 < 1000):
            print("x1 = {:} or {:}/{:}".format(x1, xa1, xb1))
        else:
            print("x1 = {:}".format(x1))
        x2 = round(((-b) + sq) / a2, 4)
        xa2, xb2 = x2.as_integer_ratio()
        if xb2 != 1 and (-1000 < xa2 and xa2 < 1000) and \
           (-1000 < xb2 and xb2 < 1000):
            print("x2 = {:} or {:}/{:}".format(x2, xa2, xb2))
        else:
            print("x2 = {:}".format(x2))
        return (x1, x2)


    def __print_reduced(self):
        first = True
        for key in sorted(self.reduced):
            # Print operation
            # print("{",self.reduced[key], ",", key, "}")
            if not first and self.reduced[key] >= 0:
                print(" + ", end="");
            elif not first and self.reduced[key] < 0:
                print(" - ", end="")

            # Print int or float
            if first and self.reduced[key] < 0:
                print("-", end="")
            if isinstance(self.reduced[key], int) or self.reduced[key].is_integer():
                if abs(self.reduced[key]) != 1 or key == 0:
                    print(abs(int(self.reduced[key])), end="")
                    if key != 0:
                        print(" * ", end="")
            else:
                print(abs(self.reduced[key]), end="")
                if key != 0:
                    print(" * ", end="")
            if key != 0:
                print("x", end="")
            if key != 0 and key != 1:
                self.__print_exponent(key)
            first = False
        print(" = 0")

    def print_info(self):
        print("Reduced form:", end=" ")
        if len(self.reduced) != 0:
            self.__print_reduced()
        else:
            print("0 = 0")

        # Degree
        print("Polynomial degree:", self.degree)

        # Solve roots
        if self.degree > 2:
            print("The polynomial degree is strictly greater than 2, I can't solve.")
        elif len(self.reduced) != 0 and min(self.reduced) < 0:
            print("X^exponent is lower than 0, I can't solve.")
        else:
            # a -> a * x^2
            # b -> b * x
            # c -> c
            a, b, c = 0, 0, 0
            if 2 in self.reduced:
                a = self.reduced[2]
            if 1 in self.reduced:
                b = self.reduced[1]
            if 0 in self.reduced:
                c = self.reduced[0]
            if a != 0:
                self.__quadratic(a, b, c)
            elif b != 0:
                print("Steps:")
                print("x = {:} / {:}".format(-c, b))
                x = round(-c / b, 4)
                if abs(x) == 0:
                    print("X = 0")
                else:
                    a, b = x.as_integer_ratio()
                    if b != 1 and (-1000 < a and a < 1000) and \
                       (-1000 < b and b < 1000):
                        print("x = {:} or {:}/{:}".format(x, a, b))
                    else:
                        print("x = {:}".format(x))
            elif len(self.reduced) == 0:
                print("No roots to solve")
            else:
                print("Error: Mathematical inconcistency")

    def print_ast(self):
        print('\nAST (lf): ', end="")
        pprint(self.ast[0], width=42)
        print('\nAST (rg): ', end="")
        pprint(self.ast[1], width=42)

    def print_dictionary(self):
        print('\nDict (lf): ', end="")
        pprint(self.reduced_left, width=42)
        print('\nDict (rg): ', end="")
        pprint(self.reduced_right, width=42)
        print('\nDictionary: ', end="")
        pprint(self.reduced)

    # Syntax Analysis

    def __token_list(self, eq: str, op1: set, sep1: str, op2: set, sep2: str) -> list:
        eq_op = list(filter(lambda x: x in op1, eq))
        x = [re.split(sep1, eq), eq_op]
        for i in range(len(x[0])):
            x_op = list(filter(lambda x: x in op2, x[0][i]))
            tup = re.split(sep2, x[0][i])
            for j in range(len(tup)):
                tup[j] = tup[j].replace('m', '-')
            x[0][i] = (tup, x_op)
        return (x)

    def __valid_coeff(self, n: str) -> bool:
        try:
            float(n)
            return (True)
        except ValueError:
            if len(n) == 0 or n[0] != 'X' or len(n) > 1 and n[1] != '^' or len(n) == 2:
                return (False)
            elif len(n) > 2:
                try:
                    int(n[2:])
                except ValueError:
                    return (False)
                return (True)
            return (True)

    def __syntax_structure(self, eq: str):
        for term in eq[0]:
            for coeff in term[0]:
                if coeff == '':
                    raise ValueError("Synytax Error: Empty token next to symbol")
                elif not self.__valid_coeff(coeff):
                    raise ValueError("Synytax Error: Invalid token: {:}".format(coeff))

    def __parser(self):
        self.eq = self.eq.replace(" ", "").replace("\n", "").replace("\t", "").replace("x", "X")
        if self.eq == '':
            raise ValueError("Error: Empty equation")

        # Not any invalid characters
        equal = 0
        for _ in self.eq:
            if _ not in "0123456789" and _ not in symbol_table:
                raise ValueError("Lexer Error: non identifiable token: {:}".format(_))
            if _ == '=':
                equal += 1

        # Always only one equal symbol
        if equal != 1:
            raise ValueError("Syntax Error: Equation needs ONE equal symbol")

        # Except negative numbers
        self.eq = self.eq.replace("*-", "*m").replace("/-", "/m").replace("=-", "=m")
        if self.eq[0] == '-':
            self.eq = 'm' + self.eq[1:]
        self.eq = self.eq.replace("mX", "m1*X")

        # Token list
        eq1, eq2 = self.eq.split("=")
        eq1 = self.__token_list(eq1, { '+', '-' }, '\+|\-', { '*', '/' }, '\*|\/')
        eq2 = self.__token_list(eq2, { '+', '-' }, '\+|\-', { '*', '/' }, '\*|\/')

        # Verify syntax structure
        self.__syntax_structure(eq1)
        self.__syntax_structure(eq2)

        self.ast_left = eq1
        self.ast_right = eq2
        self.ast = [copy.deepcopy(eq1), copy.deepcopy(eq2)]


    def __reduce_term(self, term: tuple) -> tuple:
        coeff = 1
        degree = 0

        # Initialize coeff or degree
        if 'X' in term[0][0]:
            degree = 1
            if len(term[0][0]) != 1:
                degree = int(term[0][0][2:])
        else:
            coeff = float(term[0][0])

        # Calculate coeff and degree
        i = 1
        for op in term[1]:
            if len(term[0]) <= i:
                break
            if op == '*':
                ## if X without exponent (R01)
                if 'X' in term[0][i]:
                    if len(term[0][i]) == 1:
                        degree += 1
                    else:
                        degree += int(term[0][i][2:])
                else:
                    coeff *= float(term[0][i])
            elif op == '/':
                if 'X' in term[0][i]:
                    if len(term[0][i]) == 1:
                        degree -= 1
                    else:
                        degree -= int(term[0][i][2:])
                else:
                    coeff /= float(term[0][i])
            i += 1
        return (degree, coeff)

    def __dictionary(self, ast: list) -> dict:
        """
        return dictionary with { degree : coefficient }
        {
          X^degree: coeff,
          0: coeff,
          ...,
          n: coeff,
        }
        """
        new = {}

        # Reduce terms
        for t in range(len(ast[0])):
            ast[0][t] = self.__reduce_term(ast[0][t])

        # Reduce equation
        new[ast[0][0][0]] = ast[0][0][1]
        i = 1
        for op in ast[1]:
            if op == '+':
                if ast[0][i][0] in new:
                    new[ast[0][i][0]] += ast[0][i][1]
                else:
                    new[ast[0][i][0]] = ast[0][i][1]
            elif op == '-':
                if ast[0][i][0] in new:
                    new[ast[0][i][0]] -= ast[0][i][1]
                else:
                    new[ast[0][i][0]] = -ast[0][i][1]
            i += 1
        return (new)

    def __reduce_d(self):
        self.reduced = copy.deepcopy(self.reduced_left)
        for key in self.reduced_right:
            if key in self.reduced:
                self.reduced[key] -= self.reduced_right[key]
            else:
                self.reduced[key] = -self.reduced_right[key]
        self.reduced = { key: val for key, val in self.reduced.items() if val != 0}

if '__main__' == __name__:
    if len(sys.argv) > 3 or len(sys.argv) == 1 or (len(sys.argv) > 2 and sys.argv[2] != "-v"):
        print("Usage: python3 computor.py '<polynomial equaion>' [-v]")
        print()
        print("Rules:")
        print("       - Lexic:")
        print("                • Equal          : =")
        print("                • Multiplication : *")
        print("                • Division       : /")
        print("                • Addition       : +")
        print("                • Substraction   : -")
        print("                • Variable Exp.  : ^")
        print("                • Variable       : x / X")
        print("                • Coefficient    : n (float / int)")
        print("       - Syntax:")
        print("                • ONE equal sign")
        print("                • Operations are binary")
        print("                • Spaces are irrelevant")
        print("                • Exponents are only for variables")
        print("       - Semantic:")
        print("                • Polynomial degree in range [0, 2]")
        print("                • Mathematically consistent")
        print("                • No divisions by zero")
        print()
        print("Example:")
        print("       python3 computor.py '8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^2 = 3 * X^0'")
        print()
        exit()
    try:
        eq = sys.argv[1]
        poly = Polynome(eq)
        if len(sys.argv) > 2 and sys.argv[2] == '-v':
            poly.print_ast()
            poly.print_dictionary()
    except ValueError as msg:
        print(msg)
