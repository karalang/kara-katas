# LeetCode #1446 Consecutive Characters: the bench, a mirror of
# max_power.kara.


def max_power(s):
    # the length of the run the letter so far ends, and the longest run
    best = 0
    run = 0
    last = " "
    for ch in s:
        if ch == last:
            run += 1
        else:
            run = 1
            last = ch
        best = max(best, run)
    return best


def main():
    # 200 strings of 10^5 letters, each drawn from the first 2 to 4 of the
    # alphabet, each string's power asked 10 times, the powers folded to a
    # checksum
    seed = 1446
    strings = []
    for j in range(200):
        k = 2 + j % 3
        letters = []
        for _ in range(100000):
            seed = (seed * 1103515245 + 12345) % 2147483648
            letters.append(chr(97 + seed // 65536 % k))
        strings.append("".join(letters))
    check = 0
    for _ in range(10):
        for s in strings:
            check = (check * 131 + max_power(s)) % 1000000007
    print(f"2000 strings of 10^5 letters: checksum {check}")


main()
