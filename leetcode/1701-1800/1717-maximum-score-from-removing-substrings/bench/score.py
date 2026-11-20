# LeetCode #1717: Maximum Score From Removing Substrings -- the Python
# mirror of the bench (score.kara): the pair worth more removed first with
# a stack, then the other pair from what is left, on 20 random strings of
# 100000 letters, each answered 100 times.


def remove(chars, first, second, points):
    kept = []
    gained = 0
    for c in chars:
        if c == second and kept and kept[-1] == first:
            kept.pop()
            gained += points
        else:
            kept.append(c)
    return kept, gained


def maximum_gain(s, x, y):
    chars = list(s)
    if x >= y:
        first, second, more, less = "a", "b", x, y
    else:
        first, second, more, less = "b", "a", y, x
    rest, a = remove(chars, first, second, more)
    _, b = remove(rest, second, first, less)
    return a + b


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count = 20
    rounds = 100
    n = 100000
    seed = [1717]
    problems = []
    for _ in range(count):
        letters = []
        for _ in range(n):
            r = next_random(seed) % 200
            letters.append("c" if r < 2 else ("a" if r % 2 == 0 else "b"))
        x = next_random(seed) % 10000 + 1
        y = next_random(seed) % 10000 + 1
        problems.append(("".join(letters), x, y))
    total = 0
    check = 0
    for r in range(rounds):
        for s, x, y in problems:
            answer = maximum_gain(s, x, y)
            total += answer
            check = (check * 31 + answer + r) % 1000000007
    print(f"{count} strings of {n} letters, {rounds} rounds: answers sum to {total}, checksum {check}")


main()
