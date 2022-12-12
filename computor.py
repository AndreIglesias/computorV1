# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computor.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ciglesia <ciglesia@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/12/12 15:45:24 by ciglesia          #+#    #+#              #
#    Updated: 2022/12/12 17:29:59 by ciglesia         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys

symbol_table = {'x', 'X', '^', '+', '-', '*', '/', '=', '.'}
symbol_op = {'+', '-', '*', '/'}
symbol_friend = {'x', 'X'}

class Polynome(object):
    def __init__(self, eq: str):
        self.eq = eq
        self.__parser()

    def __valid_coeff(self, eq: str, i: int) -> int:
        decimal = 0
        # Sign validation
        while i < len(eq) and  (eq[i] == '-' or eq[i] == '+'):
            i += 1

        # Symbol positioning
        if i < len(eq) and eq[i] in symbol_table and eq[i] not in symbol_friend:
            raise ValueError("Syntax Error: unexpected symbol: {:}".format(eq[i]))

        # Coefficient validation
        while 0 <= i and i < len(eq) and eq[i] not in symbol_table:
            if eq[i] == '.':
                decimal += 1
            if decimal > 1:
                raise ValueError("Syntax Error: multiple dots in coefficient")
            i += 1
        return (i)

    def __valid_x(self, eq: str, i: int) -> int:
        pass

    def __valid_eq(self, eq: str) -> bool:
        i = 0
        while i < len(eq):
            i = self.valid_coeff(eq, i)
            if i == len(eq):
                break
            elif eq[i] == '*':
                if i + 1 == len(eq):
                    raise ValueError("Syntax Error: the equation cannot end with: {:}".format(eq[i]))
                i += 1
                if eq[i] == 'X' and i + 1 < len(eq) and eq[i + 1] == '^':
                    if i + 2 == len(eq):
                        raise ValueError("Syntax Error: the equation cannot end with: {:}".format(eq[i + 1]))
                    if eq[i + 2] not in "0123456789":
                        raise ValueError("Syntax Error: the equation X^ cannot end with: {:}".format(eq[i + 2]))
                    i += 2
                    while i < len(eq) and eq[i] not in "0123456789":
                        i += 1
                if i < len(eq) and eq[i] in symbol_op:
                    if i + 1 == len(eq):
                        raise ValueError("Syntax Error: the equation cannot end with: {:}".format(eq[i]))
                    if eq[i + 1] in symbol_table and eq[i + 1] not in symbol_friend:
                        raise ValueError("Syntax Error: the operation cannot continue with: {:}".format(eq[i + 1]))
                    i += 1
                continue
            i += 1
            if i < len(eq) and eq[i] in symbol_op:
                if i + 1 == len(eq):
                    raise ValueError("Syntax Error: the equation cannot end with: {:}".format(eq[i]))
                if eq[i + 1] in symbol_table and eq[i + 1] not in symbol_friend:
                    raise ValueError("Syntax Error: the operation cannot continue with: {:}".format(eq[i + 1]))
                i += 1

    def __parser(self):
        self.eq = self.eq.replace(" ", "").replace("x", "X")

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

        eq1, eq2 = self.eq.split("=")




        print(eq1)
        print(eq2)

if '__main__' == __name__:
    if len(sys.argv) > 2 or len(sys.argv) == 1:
        print("Usage: python3 computor.py '<polynomial equaion>'")
        exit()
    eq = sys.argv[1]
    poly = Polynome(eq)
    print(poly.eq)
