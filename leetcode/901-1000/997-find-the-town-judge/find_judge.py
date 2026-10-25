# LeetCode #997: Find the Town Judge -- mirror of the ★ arm
# (find_judge.kara), one score per person.


def find_judge(n, trust):
    score = [0] * (n + 1)
    for a, b in trust:
        score[a] -= 1
        score[b] += 1
    for person in range(1, n + 1):
        if score[person] == n - 1:
            return person
    return -1


seed = 997


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# n people and a list of trusts: half the time a judge everyone else
# trusts, with a third of those spoiled by one trust taken away or one
# trust from the judge, and other trusts at random, in random order
def random_town(n, extra):
    pairs = []
    seen = set()

    def add(a, b):
        if a != b and (a, b) not in seen:
            seen.add((a, b))
            pairs.append((a, b))

    judge = 0
    if next_random() % 2 == 0:
        judge = 1 + next_random() % n
        for p in range(1, n + 1):
            add(p, judge)
    for _ in range(extra):
        a = 1 + next_random() % n
        b = 1 + next_random() % n
        if a != judge:
            add(a, b)
    if judge > 0 and n > 1:
        spoil = next_random() % 6
        if spoil == 0:
            pairs.pop(next_random() % (n - 1))
        elif spoil == 1:
            other = 1 + next_random() % n
            if other != judge:
                pairs.append((judge, other))
    for i in range(len(pairs) - 1, 0, -1):
        j = next_random() % (i + 1)
        pairs[i], pairs[j] = pairs[j], pairs[i]
    return pairs


def main():
    cases = [
        (2, [(1, 2)]),
        (3, [(1, 3), (2, 3)]),
        (3, [(1, 3), (2, 3), (3, 1)]),
        (1, []),
        (2, []),
        (2, [(1, 2), (2, 1)]),
        (4, [(1, 3), (1, 4), (2, 3), (2, 4), (4, 3)]),
        (3, [(1, 2), (2, 3)]),
        (4, [(1, 4), (2, 4)]),
        (3, [(1, 2), (3, 2), (1, 3)]),
    ]
    for n, trust in cases:
        text = "[" + ",".join(f"[{a},{b}]" for a, b in trust) + "]"
        print(f"n = {n}, trust = {text} -> {find_judge(n, trust)}")
    everyone = [(p, 500) for p in range(1, 1001) if p != 500]
    print(f"1000 people, all trusting 500: {find_judge(1000, everyone)}")
    print(f"1000 people, all trusting 500, and 500 trusting 1: {find_judge(1000, everyone + [(500, 1)])}")
    print(f"1000 people, no trust: {find_judge(1000, [])}")
    print(f"1000 people, all but person 1000 trusting 500: {find_judge(1000, everyone[:-1])}")
    ring = [(p, p % 1000 + 1) for p in range(1, 1001)]
    print(f"1000 people in a ring of trust: {find_judge(1000, ring)}")
    for count, most, extra in ((300, 4, 3), (3000, 30, 40), (300, 1000, 9000)):
        people = 0
        judges = 0
        check = 0
        for _ in range(count):
            n = 1 + next_random() % most
            trust = random_town(n, next_random() % (extra + 1))
            people += n
            got = find_judge(n, trust)
            if got > 0:
                judges += 1
            check = (check * 31 + got + 2) % 1000000007
        print(f"{count} random towns of {people} people: {judges} judges, checksum {check}")


main()
