# Benchmark for #439: mirror of parse_ternary.kara (a stack, scanning
# from the right) on 200 random expressions of 2,499 ternaries each,
# built once and evaluated 20 times over.
import sys

sys.setrecursionlimit(100000)


def parse_ternary(expression):
    e = expression.encode()
    stack = []
    i = len(e)
    while i > 0:
        i -= 1
        if stack and stack[-1] == 63:  # '?'
            stack.pop()
            yes = stack.pop()
            stack.pop()
            no = stack.pop()
            stack.append(yes if e[i] == 84 else no)  # 'T'
        else:
            stack.append(e[i])
    return chr(stack[0])


seed = 439


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# Appends a random expression of exactly n ternaries to out: a random
# split of the n - 1 below the root between its two branches.
def random_expression(n, out):
    if n == 0:
        r = next_random() % 12
        out.append(chr(48 + r) if r < 10 else ("T" if r == 10 else "F"))
        return
    out.append("T" if next_random() % 2 == 0 else "F")
    out.append("?")
    left = next_random() % n
    random_expression(left, out)
    out.append(":")
    random_expression(n - 1 - left, out)


def main():
    count, ternaries, rounds = 200, 2499, 20
    expressions = []
    for _ in range(count):
        out = []
        random_expression(ternaries, out)
        expressions.append("".join(out))
    digits = 0
    checksum = 0
    for round in range(rounds):
        for e in expressions:
            value = parse_ternary(e)
            if value != "T" and value != "F":
                digits += 1
            checksum = (checksum * 31 + ord(value) + round) % 1000000007
    print(f"{count} expressions of {len(expressions[0])} characters, {rounds} rounds: {digits} digits, checksum {checksum}")


main()
