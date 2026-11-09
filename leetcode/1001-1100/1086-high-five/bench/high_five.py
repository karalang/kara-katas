# Benchmark: LeetCode #1086 High Five -- mirrors high_five.kara: the
# scores grouped by student, the ids walked in order, each student's
# sorted high to low and the first five averaged, over 200 lists of 1000
# items built once.


def high_five(items):
    scores = {}
    for sid, score in items:
        if sid in scores:
            scores[sid].append(score)
        else:
            scores[sid] = [score]
    out = []
    for sid in sorted(scores):
        top = sorted(scores[sid], reverse=True)
        out.append([sid, sum(top[:5]) // 5])
    return out


seed = 1086


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 50
    lists = []
    for t in range(200):
        k = 50 + t % 150
        ids = []
        taken = [False] * 1001
        while len(ids) < k:
            i = next_random() % 1000 + 1
            if not taken[i]:
                taken[i] = True
                ids.append(i)
        items = []
        for i in range(1000):
            sid = ids[i % k] if i < 5 * k else ids[next_random() % k]
            items.append([sid, next_random() % 101])
        for i in range(len(items) - 1, 0, -1):
            j = next_random() % (i + 1)
            items[i], items[j] = items[j], items[i]
        lists.append(items)
    students = 0
    check = 0
    for r in range(rounds):
        for i in range(200):
            out = high_five(lists[(r * 7 + i) % 200])
            students += len(out)
            for row in out:
                check = (check * 31 + row[0] * 101 + row[1]) % 1000000007
    print(f"{rounds} rounds over 200 lists of 1000 items: {students} students, checksum {check}")


main()
