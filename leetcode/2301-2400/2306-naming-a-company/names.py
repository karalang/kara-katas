# LeetCode #2306: Naming a Company -- the ★ arm in Python. Group the
# suffixes by first letter. Two ideas can swap first letters exactly when
# neither one's suffix is in the other's group, so for each pair of
# letters the valid names are the suffixes of each group not shared with
# the other, multiplied, twice for the two orders.


def distinct_names(ideas):
    groups = [set() for _ in range(26)]
    for idea in ideas:
        groups[ord(idea[0]) - ord("a")].add(idea[1:])
    names = 0
    for a in range(26):
        for b in range(a + 1, 26):
            shared = sum(1 for suffix in groups[a] if suffix in groups[b])
            names += 2 * (len(groups[a]) - shared) * (len(groups[b]) - shared)
    return names


seed = 2306


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def make(count, heads, tails, longest):
    letters = "abcdefghijklmnopqrstuvwxyz"
    seen = set()
    ideas = []
    while len(ideas) < count:
        idea = letters[next_random() % heads]
        for _ in range(next_random() % longest):
            idea += letters[next_random() % tails]
        if idea not in seen:
            seen.add(idea)
            ideas.append(idea)
    return ideas


def main():
    fixed = [
        ["coffee", "donuts", "time", "toffee"],
        ["lack", "back"],
        ["a", "b"],
        ["ax", "bx", "cx", "dx"],
        ["ab", "ac", "bd", "be", "bf"],
    ]
    for ideas in fixed:
        print(distinct_names(ideas))
    print(distinct_names(make(600, 26, 26, 4)))
    check = 0
    total = 0
    for _ in range(300):
        count = next_random() % 39 + 2
        heads = next_random() % 5 + 2
        ideas = make(min(count, heads * 13), heads, 3, 3)
        names = distinct_names(ideas)
        check = (check * 31 + names) % 1000000007
        total += names
    print(f"300 cases: checksum {check}, {total} in all")


main()
