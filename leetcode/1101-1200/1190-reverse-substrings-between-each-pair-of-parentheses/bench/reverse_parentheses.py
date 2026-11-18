# LeetCode #1190 bench: the ★ arm in Python, over the same 200 strings of
# about 2000 characters and 200 rounds as the Kāra bench.


def reverse_parentheses(s):
    n = len(s)
    pair = [0] * n
    open_ = []
    for i in range(n):
        c = s[i]
        if c == "(":
            open_.append(i)
        elif c == ")":
            j = open_.pop()
            pair[i] = j
            pair[j] = i
    out = []
    i, step = 0, 1
    while i < n:
        c = s[i]
        if c == "(" or c == ")":
            i = pair[i]
            step = -step
        else:
            out.append(c)
        i += step
    return "".join(out)


seed = 1190


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_case(n, letters):
    s = []
    open_ = 0
    for _ in range(n):
        r = next_random() % 4
        if r == 0:
            s.append("(")
            open_ += 1
        elif r == 1 and open_ > 0:
            s.append(")")
            open_ -= 1
        else:
            s.append(letters[next_random() % len(letters)])
    s.append(")" * open_)
    return "".join(s)


def nested(depth, letters):
    s = []
    for _ in range(depth):
        s.append(letters[next_random() % len(letters)])
        s.append("(")
    for _ in range(depth):
        s.append(letters[next_random() % len(letters)])
        s.append(")")
    return "".join(s)


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


letters = "abcdefghijklmnopqrstuvwxyz"
cases = [random_case(2000, letters) if i % 2 == 0 else nested(500, letters) for i in range(200)]
check = 0
for _ in range(200):
    for s in cases:
        check = (check * 131 + digest(reverse_parentheses(s))) % 1000000007
print(f"200 rounds of 200 strings of about 2000 characters: checksum {check}")
