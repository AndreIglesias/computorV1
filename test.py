
def gcd(x, y):
    while(y):
        x, y = y, x % y
    return abs(x)

def float_fraction(s):
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
    gd = gcd(numerator, denominator)
    print(numerator // gd, "/", denominator // gd)

if __name__ == '__main__':
	float_fraction("0.2")
