# LeetCode #2268: Minimum Number of Keypresses -- the Python mirror of
# the ★ arm, `keys.kara`, line for line. Its output is byte-identical.


def minimum_keypresses(s):
    count = [0] * 26
    for b in s.encode():
        count[b - ord('a')] += 1
    count.sort(reverse=True)
    total = 0
    for i, c in enumerate(count):
        total += c * (i // 9 + 1)
    return total


seed = 2268


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters(length, k):
    return "".join(chr(ord('a') + next_random() % k) for _ in range(length))


def main():
    examples = ["apple", "abcdefghijkl", "a", "abcdefghijklmnopqrstuvwxyz", "zzzzzzzzzz", "aaabbbcccdddeeefffggghhhiiij", "abcdefghijabcdefghij"]
    for s in examples:
        print(f"{s} -> {minimum_keypresses(s)}")
    check = 0
    for t in range(2000):
        length = next_random() % 60 + 1
        s = letters(length, [3, 10, 12, 26][t % 4])
        check = (check * 31 + minimum_keypresses(s)) % 1000000007
    print(f"2000 strings: checksum {check}")
    rand = letters(100000, 26)
    same = "a" * 100000
    weighted = []
    for _ in range(100000):
        r = next_random() % 351
        k = 0
        upto = 1
        while upto <= r:
            k += 1
            upto += k + 1
        weighted.append(chr(ord('a') + k))
    answers = [minimum_keypresses(rand), minimum_keypresses(same), minimum_keypresses("".join(weighted))]
    print(f"10^5 letters: [{', '.join(map(str, answers))}]")


main()
