# LeetCode #1152 -- mirrors most_visited_pattern.kara (the ★ arm): each
# user's visits in time order, the set of three-site patterns among them,
# each pattern's score the number of users whose set holds it, the best
# the highest score and the smallest pattern among ties.


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


SEED = [0]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def fmt(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def show(username, timestamp, website):
    p = most_visited_pattern(username, timestamp, website)
    print(f"{fmt(username)} {fmt(timestamp)} {fmt(website)}  ->  {fmt(p)}")


def visits(n, users, sites):
    username, website = [], []
    for i in range(n):
        u = 0 if i < 3 else next_random() % users
        username.append(f"u{u}")
        website.append(chr(ord("a") + next_random() % sites))
    timestamp = list(range(1, n + 1))
    for j in range(n - 1, 0, -1):
        k = next_random() % (j + 1)
        timestamp[j], timestamp[k] = timestamp[k], timestamp[j]
    return username, timestamp, website


def main():
    show("joe joe joe james james james james mary mary mary".split(), list(range(1, 11)),
         "home about career home cart maps home home about career".split())
    show("ua ua ua ub ub ub".split(), [1, 2, 3, 4, 5, 6], "a b a a b c".split())
    show(["x"] * 3, [3, 1, 2], ["c", "a", "b"])
    show("x y x y x y".split(), [6, 5, 4, 3, 2, 1], "p q r r q p".split())
    show("a a a a b b b".split(), [1, 2, 3, 4, 5, 6, 7], "z y x w x y z".split())

    SEED[0] = 1152
    check = 0
    first = [0] * 5
    for _ in range(2000):
        n = 3 + next_random() % 48
        users = 1 + next_random() % 6
        sites = 2 + next_random() % 4
        p = most_visited_pattern(*visits(n, users, sites))
        for w in p:
            for c in w.encode():
                check = (check * 31 + c) % 1000000007
        first[ord(p[0][0]) - ord("a")] += 1
    print(f"2000 random problems: first sites {fmt(first)}, checksum {check}")

    show(["solo"] * 50, list(range(1, 51)), [f"s{i + 10}" for i in range(50)])
    username = [f"u{i // 3}" for i in range(48)] + ["u0", "u0"]
    website = [["c", "a", "b"][i % 3] for i in range(48)] + ["a", "a"]
    show(username, list(range(1, 51)), website)


main()
