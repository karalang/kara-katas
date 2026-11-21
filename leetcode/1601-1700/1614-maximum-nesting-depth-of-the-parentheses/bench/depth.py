# LeetCode #1614: Maximum Nesting Depth of the Parentheses -- the bench in
# Python, mirroring depth.kara: one pass counting the parentheses open,
# keeping the most.


def max_depth(s):
    open_ = most = 0
    for c in s:
        if c == "(":
            open_ += 1
            most = max(most, open_)
        elif c == ")":
            open_ -= 1
    return most


def main():
    seed = 1614

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    def expression(size, out):
        left = size
        while True:
            if left > 1 and next_random() % 3 == 0:
                inner = (next_random() * 32768 + next_random()) % left + 1
                out.append("(")
                expression(inner, out)
                out.append(")")
                left -= inner
            else:
                out.append(chr(48 + next_random() % 10))
                left -= 1
            if left <= 0:
                break
            out.append("+-*/"[next_random() % 4])

    expressions = []
    for _ in range(10):
        out = []
        expression(200000, out)
        expressions.append("".join(out))
    check = chars = 0
    for s in expressions:
        for _ in range(10):
            check = (check * 31 + max_depth(s) + 1) % 1000000007
            chars += len(s)
    print(f"10 expressions of 200000 terms, each read 10 times: {chars} characters, checksum {check}")


main()
