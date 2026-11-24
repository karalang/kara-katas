# LeetCode #2456: Most Popular Video Creator -- bench, Python mirror of
# creator.kara: one pass keeps each creator's total views and best video,
# then every creator at the largest total, sorted.


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


seed = 2456


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_name(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    lists = []
    for _ in range(10):
        creators = [random_name(3, 26) for _ in range(100000)]
        ids = [random_name(5, 26) for _ in range(100000)]
        views = [next_random() % 100001 for _ in range(100000)]
        lists.append((creators, ids, views))
    check = 0
    for p in range(16):
        for a in range(10):
            creators, ids, views = lists[a]
            views[(p * 7919 + a) % 100000] = check % 100001
            for pair in most_popular_creator(creators, ids, views):
                for w in pair:
                    for b in w.encode():
                        check = (check * 31 + b) % 1000000007
            check = (check + p) % 1000000007
    print(f"16 passes over 10 lists of 10^5 videos: checksum {check}")


main()
