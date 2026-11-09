# LeetCode #1086: High Five -- mirrors high_five.kara (the ★ arm): the
# scores grouped by student, the ids walked in order, each student's
# scores sorted high to low and the first five summed and divided by 5.


def high_five(items):
    scores = {}
    for sid, score in items:
        scores.setdefault(sid, []).append(score)
    out = []
    for sid in sorted(scores):
        top = sorted(scores[sid], reverse=True)
        out.append([sid, sum(top[:5]) // 5])
    return out


# ---- test harness ---------------------------------------------------------

class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def written(pairs):
    return "[" + ",".join(f"[{p[0]},{p[1]}]" for p in pairs) + "]"


# k students with ids drawn from 1 to `ids`, each with 5 to 9 scores,
# the items shuffled.
def random_items(rng, k, ids):
    chosen = []
    while len(chosen) < k:
        sid = rng.next() % ids + 1
        if sid not in chosen:
            chosen.append(sid)
    items = []
    for sid in chosen:
        n = rng.next() % 5 + 5
        for _ in range(n):
            items.append([sid, rng.next() % 101])
    for i in range(len(items) - 1, 0, -1):
        j = rng.next() % (i + 1)
        items[i], items[j] = items[j], items[i]
    return items


def fold(h, text):
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    cases = [
        [[1, 91], [1, 92], [2, 93], [2, 97], [1, 60], [2, 77], [1, 65], [1, 87], [1, 100], [2, 100], [2, 76]],
        [[1, 100], [7, 100], [1, 100], [7, 100], [1, 100], [7, 100], [1, 100], [7, 100], [1, 100], [7, 100]],
        [[3, 0], [3, 0], [3, 0], [3, 0], [3, 1]],
        [[1000, 4], [1000, 4], [1000, 4], [1000, 4], [1000, 3], [1000, 100], [2, 9], [2, 9], [2, 9], [2, 9], [2, 9]],
    ]
    for items in cases:
        print(f"{written(items)} -> {written(high_five(items))}")
    rng = Rng(1086)
    students = 0
    h = 0
    for _ in range(300):
        k = rng.next() % 40 + 1
        items = random_items(rng, k, 1000)
        out = high_five(items)
        students += len(out)
        h = fold(h, written(out))
    print(f"300 random lists: {students} students, checksum {h}")


main()
