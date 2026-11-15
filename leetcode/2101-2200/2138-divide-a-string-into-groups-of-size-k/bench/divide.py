# LeetCode #2138: Divide a String Into Groups of Size k -- the benchmark,
# the same algorithm as divide.kara.


def divide_string(s, k, fill):
    n = len(s)
    groups = []
    start = 0
    while start < n:
        group = s[start:min(start + k, n)]
        while len(group) < k:
            group += fill
        groups.append(group)
        start += k
    return groups


seed = 2138


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    strings = []
    for _ in range(1000):
        strings.append([alphabet[next_random() % 26] for _ in range(100)])
    total = 0
    check = 0
    for _ in range(100):
        for i in range(1000):
            at = next_random() % 100
            strings[i][at] = alphabet[next_random() % 26]
            k = next_random() % 100 + 1
            fill = alphabet[next_random() % 26]
            groups = divide_string("".join(strings[i]), k, fill)
            total += len(groups)
            for b in groups[-1].encode():
                check = (check * 131 + b) % 1000000007
    print(f"100000 solves: {total} groups, checksum {check}")


main()
