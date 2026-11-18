# LeetCode #2306: Naming a Company -- the bench, the ★ arm in Python.
# Group the suffixes by first letter, and for each pair of letters
# multiply the suffixes each group does not share with the other, twice.

seed = 2306


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def distinct_names(ideas):
    groups = [set() for _ in range(26)]
    for idea in ideas:
        groups[ord(idea[0]) - 97].add(idea[1:])
    names = 0
    for a in range(26):
        for b in range(a + 1, 26):
            shared = 0
            other = groups[b]
            for suffix in groups[a]:
                if suffix in other:
                    shared += 1
            names += 2 * (len(groups[a]) - shared) * (len(groups[b]) - shared)
    return names


def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    lists = []
    for _ in range(10):
        seen = set()
        ideas = []
        while len(ideas) < 50000:
            idea = letters[next_random() % 26]
            for _ in range(next_random() % 7):
                idea += letters[next_random() % 6]
            if idea not in seen:
                seen.add(idea)
                ideas.append(idea)
        lists.append(ideas)
    check = 0
    for _ in range(4):
        for ideas in lists:
            check = (check * 31 + distinct_names(ideas)) % 1000000007
    print(f"4 passes over 10 lists of 5 * 10^4 ideas: checksum {check}")


main()
