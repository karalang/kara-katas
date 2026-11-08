# LeetCode #2024: Maximize the Confusion of an Exam -- a Python mirror of the
# ★ arm (confuse.kara): for each answer, the longest sliding window holding at
# most k of the other one. Same output, byte for byte.


def longest_run(key, c, k):
    best = 0
    left = 0
    other = 0
    for right in range(len(key)):
        if key[right] != c:
            other += 1
        while other > k:
            if key[left] != c:
                other -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def max_consecutive_answers(answer_key, k):
    key = answer_key.encode()
    return max(longest_run(key, ord("T"), k), longest_run(key, ord("F"), k))


seed = 2024


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def key_of(length, t_in_100):
    return "".join("T" if next_random() % 100 < t_in_100 else "F" for _ in range(length))


def main():
    examples = [
        ("TTFF", 2),
        ("TFFT", 1),
        ("TTFTTFTT", 1),
        ("T", 1),
        ("TF", 1),
        ("FFFTFFF", 1),
        ("TFTFTFTF", 2),
        ("TTTTFFFF", 3),
    ]
    for key, k in examples:
        print(f"{key}, {k} -> {max_consecutive_answers(key, k)}")
    total = 0
    check = 0
    for _ in range(3000):
        length = next_random() % 30 + 1
        share = next_random() % 101
        key = key_of(length, share)
        k = next_random() % length + 1
        best = max_consecutive_answers(key, k)
        total += best
        check = (check * 31 + best) % 1000000007
    print(f"3000 keys of up to 30 answers: total {total}, checksum {check}")
    total = 0
    check = 0
    for a in range(6):
        key = key_of(1500, [50, 5, 95, 30, 70, 50][a])
        k = [1, 3, 10, 40, 100, 300][a]
        best = max_consecutive_answers(key, k)
        total += best
        check = (check * 31 + best) % 1000000007
    print(f"6 keys of 1500 answers: total {total}, checksum {check}")


main()
