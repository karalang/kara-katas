# LeetCode #1054: Distant Barcodes -- the most common barcode first, every
# other place. The Python mirror of barcodes.kara; its output is
# byte-identical.


def rearrange_barcodes(barcodes):
    n = len(barcodes)
    top = max(barcodes)
    counts = [0] * (top + 1)
    for b in barcodes:
        counts[b] += 1
    most = 0
    for v in range(1, top + 1):
        if counts[v] > counts[most]:
            most = v
    answer = [0] * n
    place = 0
    v = most
    nxt = 1
    for _ in range(n):
        while counts[v] == 0:
            v = nxt
            nxt += 1
        answer[place] = v
        counts[v] -= 1
        place += 2
        if place >= n:
            place = 1
    return answer


# ---- test harness ----

class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def feasible(barcodes):
    counts = {}
    most = 0
    for b in barcodes:
        c = counts.get(b, 0) + 1
        counts[b] = c
        most = max(most, c)
    return most <= (len(barcodes) + 1) // 2


def valid(barcodes, answer):
    if sorted(barcodes) != sorted(answer):
        return False
    for i in range(1, len(answer)):
        if answer[i] == answer[i - 1]:
            return False
    return True


def trial(count, longest, largest, rng):
    possible = 0
    good = 0
    for _ in range(count):
        n = rng.next() % longest + 1
        barcodes = [rng.next() % largest + 1 for _ in range(n)]
        if not feasible(barcodes):
            continue
        possible += 1
        if valid(barcodes, rearrange_barcodes(barcodes)):
            good += 1
    return possible, good


def show(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def verdict(barcodes, answer):
    return "valid" if valid(barcodes, answer) else "INVALID"


def main():
    examples = [
        [1, 1, 1, 2, 2, 2],
        [1, 1, 1, 1, 2, 2, 3, 3],
        [7],
        [1, 2],
        [5, 5, 6],
        [3, 3, 3, 1, 2],
        [1, 1, 2, 2, 3, 3],
        [4, 4, 4, 4, 1, 2, 3],
        [9, 8, 7, 6],
        [2, 2, 1, 1, 1],
    ]
    for barcodes in examples:
        print(f"{show(barcodes)} -> {verdict(barcodes, rearrange_barcodes(barcodes))}")
    rng = Rng(1054)
    possible, good = trial(3000, 8, 3, rng)
    print(f"3000 random arrays of 1 to 8 barcodes of 1 to 3: {possible} possible, {good} valid")
    possible, good = trial(300, 2000, 50, rng)
    print(f"300 random arrays of 1 to 2000 barcodes of 1 to 50: {possible} possible, {good} valid")
    half = [7 if i < 5000 else i % 6 + 1 for i in range(10000)]
    print(f"10000 barcodes, 5000 of them 7, the rest 1 to 6: {verdict(half, rearrange_barcodes(half))}")
    runs = [1 if i < 5000 else 2 for i in range(10000)]
    print(f"10000 barcodes, 5000 of 1 then 5000 of 2: {verdict(runs, rearrange_barcodes(runs))}")


main()
