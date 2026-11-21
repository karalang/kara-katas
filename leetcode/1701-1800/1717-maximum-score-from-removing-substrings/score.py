# LeetCode #1717: Maximum Score From Removing Substrings -- the Python
# mirror of the ★ arm (score.kara): the pair worth more removed first with
# a stack, then the other pair from what is left.


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
    if x >= y:
        rest, a = remove(s, "a", "b", x)
        _, b = remove(rest, "b", "a", y)
    else:
        rest, a = remove(s, "b", "a", y)
        _, b = remove(rest, "a", "b", x)
    return a + b


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def batch(count, most, other, top, seed):
    total = 0
    check = 0
    for _ in range(count):
        n = (next_random(seed) * 32768 + next_random(seed)) % most + 1
        s = []
        for _ in range(n):
            if next_random(seed) % other == 0:
                s.append(chr(ord("c") + next_random(seed) % 24))
            elif next_random(seed) % 2 == 0:
                s.append("a")
            else:
                s.append("b")
        x = next_random(seed) % top + 1
        y = next_random(seed) % top + 1
        answer = maximum_gain("".join(s), x, y)
        total += answer
        check = (check * 31 + answer + n) % 1000000007
    print(f"{count} strings of up to {most} letters: answers sum to {total}, checksum {check}")


def main():
    # LeetCode's two examples, then no pair, equal points, and pairs that
    # only appear once others are gone
    print(maximum_gain("cdbcbbaaabab", 4, 5))
    print(maximum_gain("aabbaaxybbaabb", 5, 4))
    print(maximum_gain("xyz", 1, 1))
    print(maximum_gain("abab", 3, 3))
    print(maximum_gain("aabbba", 1, 10))
    seed = [1717]
    batch(3000, 12, 6, 5, seed)
    batch(300, 1000, 20, 10000, seed)
    batch(10, 100000, 1000, 10000, seed)


main()
