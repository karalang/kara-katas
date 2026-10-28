# LeetCode #1006: Clumsy Factorial -- a stack
#
# Mirrors clumsy.kara, the ★ arm, and its test harness; its output is
# byte-identical. Kāra's `/` truncates toward zero, so `div` does too.


def div(a, b):
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def clumsy(n):
    stack = [n]
    op = 0
    x = n - 1
    while x > 0:
        if op == 0:
            stack[-1] = stack[-1] * x
        elif op == 1:
            stack[-1] = div(stack[-1], x)
        elif op == 2:
            stack.append(x)
        else:
            stack.append(-x)
        op = (op + 1) % 4
        x -= 1
    return sum(stack)


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    print(f"n = 4 -> {clumsy(4)}")
    print(f"n = 10 -> {clumsy(10)}")
    print(f"n = 1..16 -> {' '.join(str(clumsy(n)) for n in range(1, 17))}")
    for n in [10000, 9999, 9998, 9997]:
        print(f"n = {n} -> {clumsy(n)}")
    total = 0
    check = 0
    for n in range(1, 1001):
        got = clumsy(n)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"n = 1..1000: answers sum to {total}, checksum {check}")
    seed = [1006]
    total = 0
    check = 0
    for _ in range(200):
        n = 1 + next_random(seed) % 10000
        got = clumsy(n)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"200 random n up to 10000: answers sum to {total}, checksum {check}")


main()
