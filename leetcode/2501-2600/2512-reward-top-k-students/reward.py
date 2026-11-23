# LeetCode #2512: Reward Top K Students -- Python mirror of the ★ arm
# (reward.kara): the words in two sets, every report scored, the
# students sorted by (-score, id), and its harness, line for line.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def below(top):
    hi = next_random()
    return (hi * 32768 + next_random()) % top


def word(w):
    digits = []
    v = w + 5
    while v > 0:
        digits.append(v % 5)
        v //= 5
    return "".join(chr(ord("a") + d) for d in reversed(digits))


def random_case(size, most, n, top):
    p = next_random() % (size // 2) + 1
    q = next_random() % (size // 2) + 1
    positive = [word(w) for w in range(p)]
    negative = [word(w) for w in range(p, p + q)]
    report = []
    for _ in range(n):
        length = next_random() % most + 1
        report.append(" ".join(word(next_random() % size) for _ in range(length)))
    seen = set()
    ids = []
    while len(ids) < n:
        i = below(top) + 1
        if i not in seen:
            seen.add(i)
            ids.append(i)
    k = next_random() % n + 1
    return positive, negative, report, ids, k


def fold(check, answers):
    for a in answers:
        check = (check * 31 + a) % 1000000007
    return check


def fmt(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def main():
    global seed
    p = ["smart", "brilliant", "studious"]
    q = ["not"]
    print(fmt(top_students(p, q, ["this student is studious", "the student is smart"], [1, 2], 2)))
    print(fmt(top_students(p, q, ["this student is not studious", "the student is smart"], [1, 2], 2)))
    print(fmt(top_students(p, q, ["not not not", "a b c", "smart not"], [7, 3, 5], 3)))
    print(fmt(top_students(p, q, ["x", "x", "x", "x"], [40, 10, 30, 20], 2)))
    print(fmt(top_students(p, q, ["smart smart smart", "brilliant not studious not"], [1000000000, 1], 1)))
    print(fmt(top_students(["a"], ["b"], ["a b b b", "b b b b a", "a b b"], [5, 4, 6], 3)))
    seed = 2512
    for size, top in [(6, 30), (60, 1000000000)]:
        check = 0
        for _ in range(2000):
            n = next_random() % 12 + 1
            positive, negative, report, ids, k = random_case(size, 8, n, top)
            check = fold(check, top_students(positive, negative, report, ids, k))
        print(f"2000 random from {size} words, ids to {top}: checksum {check}")
    positive, negative, report, ids, _ = random_case(400, 20, 10000, 1000000000)
    print(f"10^4 reports: checksum {fold(0, top_students(positive, negative, report, ids, 10000))}")
    same = [report[0]] * 10000
    print(f"10^4 equal reports: checksum {fold(0, top_students(positive, negative, same, ids, 5000))}")


main()
