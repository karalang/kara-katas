# LeetCode #1152 bench -- mirrors most_visited_pattern.kara: the same
# 64 problems, the same rounds, the ★ arm's maps and sets.


def most_visited_pattern(username, timestamp, website):
    order = sorted(range(len(username)), key=lambda i: timestamp[i])
    by_user = {}
    for i in order:
        by_user.setdefault(username[i], []).append(website[i])
    score = {}
    for sites in by_user.values():
        n = len(sites)
        seen = set()
        for a in range(n):
            for b in range(a + 1, n):
                for c in range(b + 1, n):
                    seen.add((sites[a], sites[b], sites[c]))
        for p in seen:
            score[p] = score.get(p, 0) + 1
    best = None
    for p, s in score.items():
        if best is None or s > best[1] or (s == best[1] and p < best[0]):
            best = (p, s)
    return list(best[0])


SEED = [1152]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    rounds = 5000
    site_names = [f"site{s}" for s in range(8)]
    problems = []
    for _ in range(64):
        username = [f"user{next_random() % 5}" for _ in range(50)]
        website = [site_names[next_random() % 8] for _ in range(50)]
        timestamp = list(range(1, 51))
        for j in range(49, 0, -1):
            k = next_random() % (j + 1)
            timestamp[j], timestamp[k] = timestamp[k], timestamp[j]
        problems.append((username, timestamp, website))
    distinct = 0
    check = 0
    for r in range(rounds):
        p = r % 64
        for _ in range(4):
            at = next_random() % 50
            problems[p][2][at] = site_names[next_random() % 8]
        answer = most_visited_pattern(*problems[p])
        if answer[0] != answer[1] and answer[1] != answer[2] and answer[0] != answer[2]:
            distinct += 1
        for w in answer:
            for c in w.encode():
                check = (check * 31 + c) % 1000000007
    print(f"{rounds} rounds over 64 problems of 50 visits: {distinct} patterns of three sites, checksum {check}")


main()
