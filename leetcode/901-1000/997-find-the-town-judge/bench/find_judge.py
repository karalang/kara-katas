# Benchmark: LeetCode #997 Find the Town Judge -- the ★ arm, one score
# per person, on random towns of 1000 people and 10000 trusts,
# LeetCode's largest. Mirrors find_judge.kara, .rs, .c and go-seq/.


def find_judge(n, trust):
    score = [0] * (n + 1)
    for t in trust:
        score[t[0]] -= 1
        score[t[1]] += 1
    for person in range(1, n + 1):
        if score[person] == n - 1:
            return person
    return -1


seed = 997


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# 1000 people and 10000 different trusts: in even towns 999 of them are
# everyone else trusting a judge, and the rest are at random
def random_town(a):
    pairs = []
    seen = [False] * (2000 * 1001)
    judge = 0
    if a % 2 == 0:
        judge = 1 + next_random() % 1000
        for p in range(1, 1001):
            if p != judge:
                seen[p * 2000 + judge] = True
                pairs.append([p, judge])
    while len(pairs) < 10000:
        x = 1 + next_random() % 1000
        y = 1 + next_random() % 1000
        if x != y and x != judge and not seen[x * 2000 + y]:
            seen[x * 2000 + y] = True
            pairs.append([x, y])
    return pairs


def main():
    rounds = 1000
    towns = [random_town(a) for a in range(20)]
    judges = 0
    check = 0
    for r in range(rounds):
        for i in range(20):
            got = find_judge(1000, towns[(r + i) % 20])
            if got > 0:
                judges += 1
            check = (check * 31 + got + 2) % 1000000007
    print(f"{rounds} rounds over 20 towns of 1000 people: {judges} judges, checksum {check}")


main()
