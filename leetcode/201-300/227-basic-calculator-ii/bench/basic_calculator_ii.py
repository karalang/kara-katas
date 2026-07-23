"""Benchmark workload for LeetCode #227 — Basic Calculator II (Python; scale lane)."""


# ASCII: '+'=43 '-'=45 '*'=42 '/'=47 '0'=48 '9'=57
def calculate(bytes_, n):
    stack = []
    num = 0
    op = 43  # '+'
    i = 0
    while i < n:
        b = bytes_[i]
        if 48 <= b <= 57:
            num = num * 10 + (b - 48)
        is_op = b == 43 or b == 45 or b == 42 or b == 47
        if is_op or i == n - 1:
            if op == 43:
                stack.append(num)
            elif op == 45:
                stack.append(-num)
            elif op == 42:
                t = stack.pop() if stack else 0
                stack.append(t * num)
            else:  # '/'
                t = stack.pop() if stack else 0
                # truncate toward zero (Python // floors)
                q = abs(t) // abs(num)
                if (t < 0) != (num < 0):
                    q = -q
                stack.append(q)
            op = b
            num = 0
        i += 1
    return sum(stack)


def push_number(buf, num):
    if num >= 10:
        buf.append(48 + num // 10)
        buf.append(48 + num % 10)
    else:
        buf.append(48 + num)


def main():
    tokens = 200000
    passes = 250
    modulus = 1000000007

    buf = []
    state = 12345

    state = (state * 1103515245 + 12345) & 2147483647
    push_number(buf, (state % 99) + 1)

    prev_high = False
    t = 1
    while t < tokens:
        state = (state * 1103515245 + 12345) & 2147483647
        opsel = (state % 2) if prev_high else (state % 4)
        if opsel == 0:
            buf.append(43)
            prev_high = False
        elif opsel == 1:
            buf.append(45)
            prev_high = False
        elif opsel == 2:
            buf.append(42)
            prev_high = True
        else:
            buf.append(47)
            prev_high = True
        state = (state * 1103515245 + 12345) & 2147483647
        push_number(buf, (state % 99) + 1)
        t += 1

    n = len(buf)
    sink = 0
    for p in range(passes):
        buf[0] = 49 + (p % 9)
        r = calculate(buf, n)
        sink = ((sink + r) % modulus + modulus) % modulus
    print(sink)


main()
