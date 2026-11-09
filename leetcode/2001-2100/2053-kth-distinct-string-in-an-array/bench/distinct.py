# LeetCode #2053: Kth Distinct String in an Array -- Python mirror of the
# ★ arm's benchmark (distinct.kara): the same 5000 arrays, the same count
# into a dict and walk of the array.

seed = 2053


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    found = check = 0
    for t in range(5000):
        letters = 2 + t % 25
        arr = []
        for _ in range(1000):
            n = next_random() % 5 + 1
            arr.append("".join(alphabet[next_random() % letters] for _ in range(n)))
        answer = kth_distinct(arr, t % 1000 + 1)
        if answer:
            found += 1
        for ch in answer:
            check = (check * 31 + ord(ch)) % 1000000007
        check = (check * 31 + len(answer) + 1) % 1000000007
    print(f"5000 arrays: {found} answers found, checksum {check}")


main()
