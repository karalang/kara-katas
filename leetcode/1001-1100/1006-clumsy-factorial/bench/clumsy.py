# Benchmark: LeetCode #1006 Clumsy Factorial -- the ★ arm, a stack, on
# every n up to 10000, LeetCode's largest.
# Mirrors clumsy.kara, .c, .rs and go-seq/. Kāra's `/` truncates toward
# zero, so `div` does too.


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


def main():
    rounds = 4
    total = 0
    check = 0
    for r in range(rounds):
        for i in range(10000):
            n = i + 1 if r % 2 == 0 else 10000 - i
            got = clumsy(n)
            total += got
            check = (check * 31 + got) % 1000000007
    print(f"{rounds} rounds over every n up to 10000: answers sum to {total}, checksum {check}")


main()
