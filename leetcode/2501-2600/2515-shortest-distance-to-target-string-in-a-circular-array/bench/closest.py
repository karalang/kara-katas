# LeetCode #2515: Shortest Distance to Target String in a Circular Array
# -- benchmark mirror of the ★ arm (closest.kara): 2000 lists of 100
# words built once, then the passes, each asking every list for the word
# at a place the checksum picks, from a start it picks too.


def closet_target(words, target, start):
    n = len(words)
    best = -1
    for i in range(n):
        if words[i] == target:
            d = abs(i - start)
            shortest = min(d, n - d)
            if best == -1 or shortest < best:
                best = shortest
    return best


seed = 2515


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    lists = []
    for _ in range(2000):
        words = []
        for _ in range(100):
            length = next_random() % 3 + 1
            words.append("".join(chr(97 + next_random() % 3) for _ in range(length)))
        lists.append(words)
    passes = 900
    check = 0
    for p in range(passes):
        for words in lists:
            target = words[check // 100 % 100]
            check = (check * 31 + closet_target(words, target, check % 100) + p) % 1000000007
    print(f"{passes} passes over 2000 lists of 100 words: checksum {check}")


main()
