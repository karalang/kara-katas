# LeetCode #2262: Total Appeal of A String -- Python mirror of the ★ arm
# (appeal.kara): each position counted in the substrings where its letter
# first appears, (i - last) * (n - i). Output is byte-identical to the
# Kara arms.


def appeal_sum(s):
    n = len(s)
    last = [-1] * 26
    total = 0
    for i in range(n):
        c = ord(s[i]) - ord("a")
        total += (i - last[c]) * (n - i)
        last[c] = i
    return total


# ---- test harness ---------------------------------------------------------

seed = 2262


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(length, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(length))


def main():
    for s in ["abbca", "code", "z", "aaa", "abcdefghijklmnopqrstuvwxyz", "racecar"]:
        print(f"{s} -> {appeal_sum(s)}")
    check = 0
    for t in range(3000):
        length = next_random() % 40 + 1
        s = word(length, [1, 2, 3, 5, 26][t % 5])
        check = (check * 31 + appeal_sum(s)) % 1000000007
    print(f"3000 strings: checksum {check}")
    all_a = "a" * 100000
    cycle = ("abc" * 33334)[:100000]
    random = word(100000, 26)
    answers = [appeal_sum(all_a), appeal_sum(cycle), appeal_sum(random)]
    print(f"10^5 letters: {answers}")


main()
