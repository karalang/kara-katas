# LeetCode #1003: Check If Word Is Valid After Substitutions -- a stack
#
# Mirrors is_valid.kara, the ★ arm, and its test harness; its output is
# byte-identical.


def is_valid(s):
    stack = []
    for c in s:
        stack.append(c)
        k = len(stack)
        if k >= 3 and stack[k - 3] == 'a' and stack[k - 2] == 'b' \
                and stack[k - 1] == 'c':
            del stack[k - 3:]
    return not stack


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_string(most, seed):
    xs = []
    for _ in range(1 + next_random(seed) % most):
        at = next_random(seed) % (len(xs) + 1)
        xs[at:at] = ['a', 'b', 'c']
    letters = ['a', 'b', 'c']
    edit = next_random(seed) % 8
    at = next_random(seed) % len(xs)
    if edit == 0:
        xs[at] = letters[(next_random(seed) % 2 + 1 + ord(xs[at]) - 97) % 3]
    elif edit == 1 and at + 1 < len(xs):
        xs[at], xs[at + 1] = xs[at + 1], xs[at]
    elif edit == 2 and len(xs) > 1:
        del xs[at]
    elif edit == 3:
        xs.insert(at, letters[next_random(seed) % 3])
    return "".join(xs)


def text(b):
    return "true" if b else "false"


def main():
    examples = ["aabcbc", "abcabcababcc", "abccba", "abc", "a", "cba",
                "aabbcc", "ababcc", "abcabcabc", "abacbc"]
    for s in examples:
        print(f's = "{s}" -> {text(is_valid(s))}')
    flat = "abc" * 6666
    nested = "a" * 6666 + "bc" * 6666
    short = nested[:19997]
    blocks = "a" * 6666 + "b" * 6666 + "c" * 6666
    large = [("abc 6666 times", flat),
             ("a 6666 times, then bc 6666 times", nested),
             ("the same less its last c", short),
             ("a, b and c 6666 times each in turn", blocks)]
    for name, s in large:
        print(f"{name} -> {text(is_valid(s))}")
    seed = [1003]
    for count, most in [(300, 4), (3000, 20), (300, 200), (3, 6666)]:
        letters = 0
        valid = 0
        check = 0
        for _ in range(count):
            s = random_string(most, seed)
            letters += len(s)
            v = 1 if is_valid(s) else 0
            valid += v
            check = (check * 31 + v + 1) % 1000000007
        print(f"{count} random strings of {letters} letters: {valid} valid, "
              f"checksum {check}")


main()
