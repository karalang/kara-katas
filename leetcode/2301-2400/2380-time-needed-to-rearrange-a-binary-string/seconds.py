# LeetCode #2380: Time Needed to Rearrange a Binary String -- Python
# mirror of the ★ arm, one pass.


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
    print(f"{seconds_to_remove_occurrences('0110101')} {seconds_to_remove_occurrences('11100')}")
    print(f"{seconds_to_remove_occurrences('0')}")
    ramp = "0" * 500 + "1" * 500
    pairs = "01" * 500
    ordered = "1" * 500 + "0" * 500
    print(f"{seconds_to_remove_occurrences(ramp)} {seconds_to_remove_occurrences(pairs)} {seconds_to_remove_occurrences(ordered)}")
    check = 0
    none = 0
    for _ in range(2000):
        n = 1 + next_random() % 60
        chance = next_random() % 11
        digits = "".join("1" if next_random() % 10 < chance else "0" for _ in range(n))
        t = seconds_to_remove_occurrences(digits)
        check = (check * 31 + t) % 1000000007
        if t == 0:
            none += 1
    print(f"2000 strings: checksum {check}, {none} take no time")


main()
