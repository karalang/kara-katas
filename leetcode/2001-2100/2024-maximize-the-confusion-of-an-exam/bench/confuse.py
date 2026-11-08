# LeetCode #2024: Maximize the Confusion of an Exam -- the ★ arm in Python,
# the same algorithm and workload as confuse.kara: a sliding window for each
# answer, the longer of the two.


def longest_run(key, c, k):
    best = left = other = 0
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


def main():
    keys = []
    ks = []
    for a in range(20):
        pct = [50, 70, 90, 97, 99][a % 5]
        keys.append("".join("T" if next_random() % 100 < pct else "F" for _ in range(100000)))
        ks.append([1, 10, 100, 1000, 10000][a // 4])
    calls = total = check = 0
    for _ in range(5):
        for a in range(20):
            best = max_consecutive_answers(keys[a], ks[a])
            calls += 1
            total += best
            check = (check * 31 + best) % 1000000007
    print(f"{calls} calls: total {total}, checksum {check}")


main()
