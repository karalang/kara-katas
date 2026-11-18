# LeetCode #2262: Total Appeal of A String -- Python mirror of the ★ arm
# (appeal.kara) on the bench workload: each position counts the substrings
# where its letter first appears, (i - last) * (n - i), with the last
# position kept per letter. Output is byte-identical to appeal.kara.


def appeal_sum(s):
    b = s.encode()
    n = len(b)
    last = [-1] * 26
    total = 0
    for i in range(n):
        c = b[i] - 97
        total += (i - last[c]) * (n - i)
        last[c] = i
    return total


# ---- bench harness ---------------------------------------------------------

seed = 2262


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for t in range(40):
        letters = t % 26 + 1
        s = "".join(chr(97 + next_random() % letters) for _ in range(100000))
        check = (check * 31 + appeal_sum(s)) % 1000000007
    print(f"40 strings of 10^5: checksum {check}")


main()
