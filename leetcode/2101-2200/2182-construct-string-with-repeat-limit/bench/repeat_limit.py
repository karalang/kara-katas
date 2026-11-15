# LeetCode #2182: Construct String With Repeat Limit -- the benchmark's
# Python mirror of repeat_limit.kara.


def repeat_limited_string(s, repeat_limit):
    counts = [0] * 26
    for c in s:
        counts[ord(c) - 97] += 1
    out = []
    big = 25
    while True:
        while big >= 0 and counts[big] == 0:
            big -= 1
        if big < 0:
            break
        take = min(counts[big], repeat_limit)
        for _ in range(take):
            out.append(chr(97 + big))
        counts[big] -= take
        if counts[big] == 0:
            continue
        small = big - 1
        while small >= 0 and counts[small] == 0:
            small -= 1
        if small < 0:
            break
        out.append(chr(97 + small))
        counts[small] -= 1
    return "".join(out)


seed = 2182


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    row = "".join(chr(97 + next_random() % 26) for _ in range(1000000))
    check = 0
    for _ in range(400):
        start = (next_random() * 32768 + next_random()) % 900001
        k = next_random() % 3 + 1
        t = repeat_limited_string(row[start:start + 100000], k)
        for c in t:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"400 solves: checksum {check}")


main()
