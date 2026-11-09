# Benchmark: LeetCode #1087 Brace Expansion -- mirrors brace_expansion.kara:
# the pattern read into sorted groups and the words built by a depth-first
# walk, over 2000 patterns built once.


def groups_of(s):
    groups = []
    open_group = None
    for c in s:
        if c == '{':
            open_group = []
        elif c == '}':
            open_group.sort()
            groups.append(open_group)
            open_group = None
        elif c == ',':
            pass
        elif open_group is not None:
            open_group.append(c)
        else:
            groups.append([c])
    return groups


def walk(groups, at, word, out):
    if at == len(groups):
        out.append("".join(word))
        return
    for c in groups[at]:
        word.append(c)
        walk(groups, at + 1, word, out)
        word.pop()


def expand(s):
    out = []
    walk(groups_of(s), 0, [], out)
    return out


seed = 1087


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_pattern(most, k):
    s = ""
    parts = next_random() % 8 + 1
    for _ in range(parts):
        if next_random() % 2 == 0:
            c = chr(ord('a') + next_random() % k)
            if len(s) + 1 <= most:
                s += c
        else:
            want = next_random() % k + 1
            letters = []
            while len(letters) < want:
                c = chr(ord('a') + next_random() % k)
                if c not in letters:
                    letters.append(c)
            group = "{" + ",".join(letters) + "}"
            if len(s) + len(group) <= most:
                s += group
    if s == "":
        s = "a"
    return s


def main():
    rounds = 400
    patterns = [random_pattern(50, t % 6 + 1) for t in range(2000)]
    words = 0
    check = 0
    for r in range(rounds):
        for i in range(2000):
            out = expand(patterns[(r * 7 + i) % 2000])
            words += len(out)
            mid = out[len(out) // 2]
            check = (check * 31 + len(out) + ord(mid[-1])) % 1000000007
    print(f"{rounds} rounds over 2000 patterns: {words} words, checksum {check}")


main()
