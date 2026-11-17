# LeetCode #1593: Split a String Into the Max Number of Unique Substrings
# -- the Python mirror of unique_split.kara: backtracking over a set of
# pieces used, with the same bound.


def split_from(s, at, used, best):
    if at == len(s):
        best[0] = max(best[0], len(used))
        return
    if len(used) + (len(s) - at) <= best[0]:
        return
    for end in range(at + 1, len(s) + 1):
        piece = s[at:end]
        if piece not in used:
            used.add(piece)
            split_from(s, end, used, best)
            used.remove(piece)


def max_unique_split(s):
    best = [0]
    split_from(s, 0, set(), best)
    return best[0]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, least, most, letters, rng):
    check = 0
    total = 0
    for _ in range(count):
        n = least + rng.next() % (most - least + 1)
        s = "".join(chr(ord("a") + rng.next() % letters) for _ in range(n))
        answer = max_unique_split(s)
        total += answer
        check = mix(check, answer)
    print(f"{count} strings of {least} to {most} letters from {letters}: total {total}, checksum {check}")


def main():
    examples = ["ababccc", "aba", "aa", "a", "abcdefghijklmnop", "aaaaaaaaaaaaaaaa", "abab", "wwwzfvedwfvhsww"]
    for s in examples:
        print(f'"{s}" -> {max_unique_split(s)}')
    rng = Rng(1593)
    batch(3000, 1, 8, 2, rng)
    batch(300, 1, 12, 3, rng)
    batch(30, 16, 16, 2, rng)


main()
