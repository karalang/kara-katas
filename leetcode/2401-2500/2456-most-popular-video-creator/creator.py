# LeetCode #2456: Most Popular Video Creator -- Python mirror of
# creator.kara: one pass keeps each creator's total views and best video,
# the most viewed and on a tie the least id; then every creator whose
# total is the largest, with that best video, sorted.


def most_popular_creator(creators, ids, views):
    stats = {}
    for i in range(len(creators)):
        c = creators[i]
        if c in stats:
            total, top, vid = stats[c]
            better = views[i] > top or (views[i] == top and ids[i] < vid)
            stats[c] = (total + views[i], views[i], ids[i]) if better else (total + views[i], top, vid)
        else:
            stats[c] = (views[i], views[i], ids[i])
    most = 0
    for total, _, _ in stats.values():
        most = max(most, total)
    answer = [[c, vid] for c, (total, _, vid) in stats.items() if total == most]
    answer.sort()
    return answer


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_name(length, letters):
    n = 1 + next_random() % length
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def show(answer):
    return " ".join(f"{p[0]}/{p[1]}" for p in answer)


def summary(answer):
    check = 0
    for p in answer:
        for w in p:
            for b in w.encode():
                check = (check * 31 + b) % 1000000007
            check = (check * 31 + 1) % 1000000007
    return f"{len(answer)} pairs, checksum {check}"


def main():
    global seed
    print(show(most_popular_creator(["alice", "bob", "alice", "chris"], ["one", "two", "three", "four"], [5, 10, 5, 4])))
    print(show(most_popular_creator(["alice", "alice", "alice"], ["a", "b", "c"], [1, 2, 2])))
    print(show(most_popular_creator(["z"], ["q"], [0])))
    print(show(most_popular_creator(["x", "x", "x"], ["bb", "ab", "b"], [7, 7, 7])))
    print(show(most_popular_creator(["p", "q", "q", "p"], ["a", "b", "c", "d"], [6, 3, 3, 0])))
    print(show(most_popular_creator(["m", "m", "m", "n"], ["c", "b", "a", "z"], [1, 1, 1, 2])))
    seed = 2456
    for length, letters, top in [(3, 3, 100000), (1, 2, 3)]:
        creators = [random_name(length, letters) for _ in range(2000)]
        ids = [random_name(5, 26) for _ in range(2000)]
        views = [next_random() % (top + 1) for _ in range(2000)]
        print(f"2000 videos, names of {length} from {letters}: {summary(most_popular_creator(creators, ids, views))}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 8
        creators = [random_name(2, 3) for _ in range(n)]
        ids = [random_name(2, 3) for _ in range(n)]
        views = [next_random() % 6 for _ in range(n)]
        for p in most_popular_creator(creators, ids, views):
            for w in p:
                for b in w.encode():
                    check = (check * 31 + b) % 1000000007
                check = (check * 31 + 1) % 1000000007
        check = (check * 31 + 2) % 1000000007
    print(f"3000 random: checksum {check}")


main()
