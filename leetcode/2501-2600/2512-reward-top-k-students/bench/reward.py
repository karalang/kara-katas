# LeetCode #2512: Reward Top K Students -- benchmark mirror of the ★ arm
# (reward.kara): 100 cases of 1000 reports built once from its own
# generator, then the passes; each copies one report of every case over
# another, chosen by the checksum so far, asks, and puts it back.


def top_students(positive, negative, report, student_id, k):
    good = set(positive)
    bad = set(negative)
    ranked = []
    for i in range(len(report)):
        score = 0
        for word in report[i].split(" "):
            if word in good:
                score += 3
            elif word in bad:
                score -= 1
        ranked.append((-score, student_id[i]))
    ranked.sort()
    return [i for _, i in ranked[:k]]


seed = 2512


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(w):
    digits = []
    v = w + 5
    while v > 0:
        digits.append(v % 5)
        v //= 5
    return "".join(chr(ord("a") + d) for d in reversed(digits))


def main():
    cases = []
    for c in range(100):
        p = next_random() % 200 + 1
        q = next_random() % 200 + 1
        positive = [word(w) for w in range(p)]
        negative = [word(w) for w in range(p, p + q)]
        report = []
        for _ in range(1000):
            length = next_random() % 20 + 1
            report.append(" ".join(word(next_random() % 600) for _ in range(length)))
        ids = [(r * 7919 + c) % 1000003 + 1 for r in range(1000)]
        cases.append((positive, negative, report, ids, c * 10 + 1))
    passes = 50
    check = 0
    for p in range(passes):
        for positive, negative, report, ids, k in cases:
            at = check % 1000
            kept = report[at]
            report[at] = report[(check // 1000 + p) % 1000]
            for i in top_students(positive, negative, report, ids, k):
                check = (check * 31 + i + p) % 1000000007
            report[at] = kept
    print(f"{passes} passes over 100 cases of 1000 reports: checksum {check}")


main()
