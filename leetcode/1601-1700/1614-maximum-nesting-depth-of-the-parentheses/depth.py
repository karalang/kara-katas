# LeetCode #1614: Maximum Nesting Depth of the Parentheses -- the Python
# mirror of depth.kara: one pass counting the parentheses open, keeping the
# most.


def max_depth(s):
    open_ = most = 0
    for c in s:
        if c == "(":
            open_ += 1
            most = max(most, open_)
        elif c == ")":
            open_ -= 1
    return most


seed = 1614


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def expression(size, out):
    left = size
    while True:
        if left > 1 and next_random() % 3 == 0:
            inner = next_random() % left + 1
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


def batch(count, most):
    check = chars = deepest = 0
    for _ in range(count):
        a = next_random()
        size = (a * 32768 + next_random()) % most + 1
        out = []
        expression(size, out)
        s = "".join(out)
        depth = max_depth(s)
        check = mix(check, depth)
        deepest = max(deepest, depth)
        chars += len(s)
    print(f"{count} expressions of up to {most} terms: {chars} characters, deepest {deepest}, checksum {check}")


for s in ["(1+(2*3)+((8)/4))+1", "(1)+((2))+(((3)))", "7", "(5)", "((((((9))))))", "(1)*(2)"]:
    print(max_depth(s))
batch(3000, 6)
batch(300, 1000)
batch(3, 100000)
