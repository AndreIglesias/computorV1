
symbol_table = {'x', 'X', '^', '+', '-', '*', '/', '=', '.'}
symbol_op = {'+', '-', '*', '/'}
symbol_friend = {'x', 'X'}
symbol_exp = "⁰¹²³⁴⁵⁶⁷⁸⁹"

class CPMath(object):

    # Displaying functions

    def print_exponent(self, exponent: int):
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

    def valid_coeff(self, n: str) -> bool:
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


    # Computing Functions

    def gcd(self, x, y):
        while(y):
            x, y = y, x % y
        return abs(x)

    def float_fraction(self, s):
        be_deci, af_deci = "", ""
        x, y = True, False
        for i in range(len(s)):
            if (s[i] == '.'):
                x, y = False, True
                continue
            if (x):
                be_deci += s[i]
            if (y):
                af_deci += s[i]
        num_be_deci = int(be_deci)
        num_af_deci = 0
        if len(af_deci) != 0:
            num_af_deci = int(af_deci)
        numerator = (num_be_deci * pow(10, len(af_deci)) + num_af_deci)
        denominator = pow(10, len(af_deci))
        gd = self.gcd(numerator, denominator)
        return (numerator // gd, denominator // gd)

    def format_roots(self, x: float or complex) -> str:
        if isinstance(x, complex):
            a, b = self.float_fraction(str(x.real))
            ai, bi = self.float_fraction(str(x.imag))
            if b != 1 and -1000 < a and a < 1000 and -1000 < b and b < 1000:
                sab = "{:}/{:}".format(a, b)
            else:
                sab = "{:}".format(x.real)

            if bi != 1 and -1000 < ai and ai < 1000 and -1000 < bi and bi < 1000:
                sabi = "{:}/{:}j".format(ai, bi)
            else:
                sabi = "{:}j".format(x.imag)
            if x.imag < 0:
                return (sab + sabi)
            return (sab + "+" + sabi)

        a, b = self.float_fraction(str(x))
        if b != 1 and -1000 < a and a < 1000 and -1000 < b and b < 1000:
            sab = "{:}/{:}".format(a, b)
        else:
            sab = None
        if sab != None:
            return (str(x) + " or " + sab)
        return (str(x))

    def quadratic(self, a: int or float, b: int or float, c: int or float) -> tuple:
        print("Steps:")
        print()
        print("x = ( -b ± sqrt(b⁽²⁾ - 4(a)(c)) ) / 2(a)")
        print()
        print("a =", a)
        print("b =", b)
        print("c =", c)
        print()
        print("x = ( -({:}) ± sqrt({:}⁽²⁾ - 4({:})({:})) ) / 2({:})".format(b, b, a, c, a))
        b2 = b ** 2
        ac4 = 4 * a * c
        a2 = 2 * a
        print("x = ( -({:}) ± sqrt(({:}) - ({:})) ) / {:}".format(b, b2, ac4, a2))
        print("x = ( -({:}) ± sqrt({:}) ) / {:}".format(b, b2 - ac4, a2))
        discriminant = b2 - ac4
        if discriminant > 0:
            print("\nThe discriminant is positive and has 2 real and distinct roots\n")
        elif discriminant == 0:
            print("\nThe discriminant is zero and has 2 real and equal roots (or 1 real root)\n")
        elif discriminant < 0:
            print("\nThe discriminant is negative and has 2 complex roots\n")
        sq = (discriminant)**(1/2)
        print("x = ( -({:}) ± {:} ) / {:}".format(b, sq, a2))
        print("x1 = ( -({:}) - {:} ) / {:}".format(b, sq, a2))
        print("x2 = ( -({:}) + {:} ) / {:}".format(b, sq, a2))
        print("x1 = {:} / {:}".format((-b) - sq, a2))
        print("x2 = {:} / {:}".format((-b) + sq, a2))
        print()
        print("Solutions:")
        if discriminant == 0:
            print("X1 = X2")
        x1 = ((-b) - sq) / a2
        if abs(x1) == 0:
            x1 = 0
        print("x1 =", self.format_roots(x1))
        x2 = ((-b) + sq) / a2
        if abs(x2) == 0:
            x2 = 0
        print("x2 =", self.format_roots(x2))

    def reduce_term(self, term: tuple) -> tuple:
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

    def poly_dictionary(self, ast: list) -> dict:
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
            ast[0][t] = self.reduce_term(ast[0][t])

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
