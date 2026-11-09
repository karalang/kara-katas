# LeetCode #2053: Kth Distinct String in an Array -- Python mirror of the
# ★ arm (distinct.kara): every string counted, then the array walked in
# its own order, counting down k over the strings seen once. Output is
# byte-identical to the Kāra arms.


def kth_distinct(arr, k):
    counts = {}
    for s in arr:
        counts[s] = counts.get(s, 0) + 1
    left = k
    for s in arr:
        if counts[s] == 1:
            left -= 1
            if left == 0:
                return s
    return ""


# ---- test harness ---------------------------------------------------------

seed = 2053


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, longest, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    arr = []
    for _ in range(n):
        length = next_random() % longest + 1
        arr.append("".join(alphabet[next_random() % letters] for _ in range(length)))
    return arr


def fold(check, answer):
    c = check
    for ch in answer:
        c = (c * 31 + ord(ch)) % 1000000007
    return (c * 31 + len(answer) + 1) % 1000000007


def main():
    examples = [
        (["d", "b", "c", "b", "c", "a"], 2),
        (["aaa", "aa", "a"], 1),
        (["a", "b", "a"], 3),
        (["a", "b", "a"], 1),
        (["x"], 1),
        (["p", "p", "q", "q"], 1),
        (["ab", "ba", "ab", "c", "ba", "d", "c", "e"], 2),
    ]
    for arr, k in examples:
        print(f"[{', '.join(arr)}], k {k} -> \"{kth_distinct(arr, k)}\"")
    found = check = 0
    for _ in range(2000):
        n = next_random() % 30 + 1
        longest = next_random() % 3 + 1
        letters = next_random() % 4 + 2
        arr = draw(n, longest, letters)
        k = next_random() % n + 1
        answer = kth_distinct(arr, k)
        if answer:
            found += 1
        check = fold(check, answer)
    print(f"2000 arrays: {found} answers found, checksum {check}")
    found = check = 0
    for t in range(200):
        letters = 2 + t % 25
        arr = draw(1000, 5, letters)
        answer = kth_distinct(arr, t * 5 + 1)
        if answer:
            found += 1
        check = fold(check, answer)
    print(f"200 arrays of 1000: {found} answers found, checksum {check}")


main()
