"""Benchmark workload for LeetCode #224 — Basic Calculator (Python; scale lane)."""


# ASCII: '+'=43 '-'=45 '('=40 ')'=41 '0'=48 '9'=57
def calculate(bytes_, n):
    result = 0
    sign = 1
    stack = []
    i = 0
    while i < n:
        b = bytes_[i]
        if 48 <= b <= 57:
            num = 0
            while i < n and 48 <= bytes_[i] <= 57:
                num = num * 10 + (bytes_[i] - 48)
                i += 1
            result = result + sign * num
        elif b == 43:
            sign = 1
            i += 1
        elif b == 45:
            sign = -1
            i += 1
        elif b == 40:
            stack.append(result)
            stack.append(sign)
            result = 0
            sign = 1
            i += 1
        elif b == 41:
            saved_sign = stack.pop() if stack else 1
            saved_result = stack.pop() if stack else 0
            result = saved_result + saved_sign * result
            i += 1
        else:
            i += 1
    return result


def push_number(buf, num):
    if num >= 100:
        buf.append(48 + num // 100)
        buf.append(48 + (num // 10) % 10)
        buf.append(48 + num % 10)
    elif num >= 10:
        buf.append(48 + num // 10)
        buf.append(48 + num % 10)
    else:
        buf.append(48 + num)


def main():
    nums = 250000
    passes = 80
    max_depth = 16
    modulus = 1000000007

    buf = []
    state = 12345
    depth = 0

    state = (state * 1103515245 + 12345) & 2147483647
    push_number(buf, state % 1000)

    t = 1
    while t < nums:
        state = (state * 1103515245 + 12345) & 2147483647
        buf.append(43 if state % 2 == 0 else 45)

        state = (state * 1103515245 + 12345) & 2147483647
        opens = state % 3
        opened_here = False
        o = 0
        while o < opens:
            if depth < max_depth:
                buf.append(40)
                depth += 1
                opened_here = True
            o += 1

        if opened_here:
            state = (state * 1103515245 + 12345) & 2147483647
            if state % 4 == 0:
                buf.append(45)

        state = (state * 1103515245 + 12345) & 2147483647
        push_number(buf, state % 1000)

        state = (state * 1103515245 + 12345) & 2147483647
        closes = state % 3
        c = 0
        while c < closes:
            if depth > 0:
                buf.append(41)
                depth -= 1
            c += 1
        t += 1
    while depth > 0:
        buf.append(41)
        depth -= 1

    n = len(buf)
    sink = 0
    for p in range(passes):
        buf[0] = 48 + (p % 10)
        r = calculate(buf, n)
        sink = ((sink + r) % modulus + modulus) % modulus
    print(sink)


main()
