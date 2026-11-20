# LeetCode #2380: Time Needed to Rearrange a Binary String -- the bench,
# the ★ arm in Python: one pass, each 1 after some 0 taking the larger of
# one more second than the 1 before it and the 0s before it.


def seconds_to_remove_occurrences(s):
    zeros = 0
    seconds = 0
    for c in s:
        if c == "0":
            zeros += 1
        elif zeros > 0:
            seconds = max(seconds + 1, zeros)
    return seconds


seed = 2380


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 100 strings of 1000 digits, string s 1 with a chance of 1 + s % 10
    # in 12; pass p asks for string (s + 7 p) % 100 in turn
    strings = []
    for s in range(100):
        strings.append("".join("1" if next_random() % 12 < 1 + s % 10 else "0" for _ in range(1000)))
    check = 0
    for p in range(500):
        for s in range(100):
            check = (check * 31 + seconds_to_remove_occurrences(strings[(s + 7 * p) % 100]) + p) % 1000000007
    print(f"500 passes over 100 strings of 1000 digits: checksum {check}")


main()
