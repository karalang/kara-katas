# LeetCode #1370: Increasing Decreasing String -- Python mirror of the ★
# arm: the letters counted, then sweeps up from a to z and down from z
# to a, each taking one of every letter still left, until none is.


def sort_string(s):
    counts = [0] * 26
    for b in s.encode():
        counts[b - 97] += 1
    out = []
    left = len(s)
    while left > 0:
        for i in list(range(26)) + list(range(25, -1, -1)):
            if counts[i] > 0:
                out.append(chr(97 + i))
                counts[i] -= 1
                left -= 1
    return "".join(out)


seed = 1370


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    print(" ".join(sort_string(s) for s in ["aaaabbbbcccc", "rat", "leetcode", "ggggggg", "spo"]))
    check = 0
    same = 0
    for _ in range(2000):
        n = 1 + next_random() % 500
        letters = 1 + next_random() % 26
        s = "".join(chr(97 + next_random() % letters) for _ in range(n))
        got = sort_string(s)
        if got == s:
            same += 1
        for b in got.encode():
            check = (check * 31 + b) % 1000000007
    print(f"2000 random strings: {same} unchanged, checksum {check}")


main()
