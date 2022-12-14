# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computor.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ciglesia <ciglesia@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/12 15:45:24 by ciglesia          #+#    #+#              #
#    Updated: 2022/12/14 18:09:06 by ciglesia         ###   ########.fr        #
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
        if exponent < 0:
            xp += "⁻"
            exponent *= -1
        while exponent > 0:
            xp += symbol_exp[int(abs(exponent % 10))]
            exponent //= 10
        xp += "⁽"
        print(xp[::-1], end="")

    def __quadratic(self, a: int or float, b: int or float, c: int or float) -> tuple:
        print("Steps:")
        print("x = (  -b ± sqrt(b⁽²⁾ - 4(a)(c))  ) / 2(a)".format(-b, b, a, c, a))
        print("x = (  -({:}) ± sqrt({:}⁽²⁾ - 4({:})({:}))  ) / 2({:})".format(-b, b, a, c, a))
        b2 = b ** 2
        ac4 = 4 * a * c
        a2 = 2 * a
        print("x = (  -({:}) ± sqrt(({:}) - ({:}))  ) / {:}".format(-b, b2, ac4, a2))
        print("x = (  -({:}) ± sqrt({:})  ) / {:}".format(-b, b2 - ac4, a2))
        sq = (b2 - ac4)**(1/2)
        print("x = (  -({:}) ± {:}  ) / {:}".format(-b, sq, a2))
        print("x1 = (  -({:}) - {:}  ) / {:}".format(-b, sq, a2))
        print("x2 = (  -({:}) + {:}  ) / {:}".format(-b, sq, a2))
        print("x1 = {:} / {:}".format((-b) - sq, a2))
        print("x2 = {:} / {:}".format((-b) + sq, a2))
        print("Solutions:")
        print("x1 = {:}".format(((-b) - sq) / a2))
        print("x2 = {:}".format(((-b) + sq) / a2))
        return (((-b) - sq) / a2, ((-b) + sq) / a2)


    def __print_reduced(self):
        first = True
        for key in sorted(self.reduced):
            # Print operation
            # print(self.reduced[key], key)
            if not first and self.reduced[key] >= 0:
                print(" + ", end="");
            elif not first and self.reduced[key] < 0:
                print(" - ", end="")

            # Print int or float
            if first and self.reduced[key] < 0:
                print("-", end="")
            if self.reduced[key].is_integer():
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
        else:
            # a -> n * x^2
            # b -> n * x
            # c -> n
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
                print("x = - {:} / {:}".format(c, b))
                if b == 0:
                    print("Error: Division by zero")
                else:
                    print("x = {:}".format(-c / b))
            elif len(self.reduced) == 0:
                print("No roots to solve")
            else:
                print("Error: Mathematical inconcistency")

    def print_ast(self):
        print('\nAST: ', end="")
        pprint(self.ast[0], width=42)
        print('\nAST: ', end="")
        pprint(self.ast[1], width=42)

    def print_dictionary(self):
        print('\nDictionary: ', end="")
        pprint(self.reduced)

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
        self.eq = self.eq.replace(" ", "").replace("x", "X")
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
        self.eq = self.eq.replace("mX", "m1*X")
        if self.eq[0] == '-':
            self.eq = 'm' + self.eq[1:]

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
                self.reduced[key] = self.reduced_right[key]
        self.reduced = { key: val for key, val in self.reduced.items() if val != 0}

if '__main__' == __name__:
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        print("Usage: python3 computor.py '<polynomial equaion>'")
        exit()
    eq = sys.argv[1]
    poly = Polynome(eq)
    poly.print_ast()
    poly.print_dictionary()
