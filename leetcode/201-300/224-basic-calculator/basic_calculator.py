"""LeetCode 224 — Basic Calculator (Python mirror / oracle).

One byte scan with a running result + current sign; '(' pushes (result, sign)
and resets, ')' folds the sub-result back. Mirrors the Kara version.
"""


def calculate(s):
    b = s.encode()
    n = len(b)
    result = 0
    sign = 1
    stack = []
    i = 0
    zero = ord('0')
    while i < n:
        ch = b[i]
        if zero <= ch <= zero + 9:
            num = 0
            while i < n and zero <= b[i] <= zero + 9:
                num = num * 10 + (b[i] - zero)
                i += 1
            result = result + sign * num
        elif ch == ord('+'):
            sign = 1
            i += 1
        elif ch == ord('-'):
            sign = -1
            i += 1
        elif ch == ord('('):
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1
            i += 1
        elif ch == ord(')'):
            saved_sign = stack.pop() if stack else 1
            saved_result = stack.pop() if stack else 0
            result = saved_result + saved_sign * result
            i += 1
        else:
            i += 1
    return result


def report(s):
    print(calculate(s))


def main():
    report("1 + 1")
    report(" 2-1 + 2 ")
    report("(1+(4+5+2)-3)+(6+8)")
    report("2147483647")
    report("-2+ 1")
    report("- (3 + (4 + 5))")
    report("1-(     -2)")
    report("10 - (2 + 3) - 1")
    report("0")


main()
