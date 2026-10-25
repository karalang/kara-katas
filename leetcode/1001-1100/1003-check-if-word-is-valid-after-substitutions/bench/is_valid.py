# Benchmark: LeetCode #1003 Check If Word Is Valid After Substitutions --
# the ★ arm, a stack, on strings of 19998 letters, LeetCode's longest.
# Mirrors is_valid.kara, .c, .rs and go-seq/.


def is_valid(s):
    stack = []
    for c in s:
        stack.append(c)
        k = len(stack)
        if k >= 3 and stack[k - 3] == 'a' and stack[k - 2] == 'b' \
                and stack[k - 1] == 'c':
            del stack[k - 3:]
    return not stack


seed = 1003


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# a valid string of `pieces` pieces, made left to right: each step
# either begins a new piece with its a or writes the next letter of the
# latest piece begun, at random
def random_valid(pieces):
    xs = []
    waiting = []
    left = pieces
    while left > 0 or waiting:
        if left > 0 and (not waiting or next_random() % 2 == 0):
            xs.append('a')
            waiting.append('b')
            left -= 1
        else:
            c = waiting[-1]
            xs.append(c)
            if c == 'b':
                waiting[-1] = 'c'
            else:
                waiting.pop()
    return xs


def main():
    rounds = 250
    # 20 strings of 6666 pieces, 19998 letters; the odd ones with one
    # letter changed
    letters = ['a', 'b', 'c']
    strings = []
    for t in range(20):
        xs = random_valid(6666)
        if t % 2 == 1:
            at = next_random() % len(xs)
            xs[at] = letters[(next_random() % 2 + 1 + ord(xs[at]) - 97) % 3]
        strings.append("".join(xs))
    valid = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            v = 1 if is_valid(strings[(r + i) % 20]) else 0
            valid += v
            check = (check * 31 + v + i + 1) % 1000000007
    print(f"{rounds} rounds over 20 strings of 19998 letters: {valid} valid, "
          f"checksum {check}")


main()
