"""LeetCode 227 — Basic Calculator II (Python mirror / oracle).

Term stack with operator precedence: '*' and '/' fold into the stack top
immediately, '+'/'-' push signed terms; sum the stack. Division truncates toward
zero to match Kara's `/` (Python's // floors, so a trunc helper is used).
Mirrors the Kara version.
"""


def trunc_div(a, b):
    q = abs(a) // abs(b)
    if (a < 0) != (b < 0):
        q = -q
    return q


def calculate(s):
    b = s.encode()
    n = len(b)
    stack = []
    num = 0
    op = ord('+')
    zero = ord('0')
    i = 0
    while i < n:
        ch = b[i]
        if zero <= ch <= zero + 9:
            num = num * 10 + (ch - zero)
        is_op = ch in (ord('+'), ord('-'), ord('*'), ord('/'))
        if is_op or i == n - 1:
            if op == ord('+'):
                stack.append(num)
            elif op == ord('-'):
                stack.append(-num)
            elif op == ord('*'):
                t = stack.pop() if stack else 0
                stack.append(t * num)
            else:  # '/'
                t = stack.pop() if stack else 0
                stack.append(trunc_div(t, num))
            op = ch
            num = 0
        i += 1
    return sum(stack)


def report(s):
    print(calculate(s))


def main():
    report("3+2*2")
    report(" 3/2 ")
    report(" 3+5 / 2 ")
    report("1-1+1")
    report("14-3/2")
    report("2*3+4")
    report("100000000/1/2")
    report("0")
    report("6-4/2")
    report("1*2-3/4+5*6-7*8+9/10")


main()
