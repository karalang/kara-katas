# LeetCode #2185: Counting Words With a Given Prefix -- the benchmark's
# Python mirror of prefix_count.kara: each word asked whether it starts
# with the prefix.


def prefix_count(words, pref):
    count = 0
    for w in words:
        if w.startswith(pref):
            count += 1
    return count


seed = 2185


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n):
    return "".join(chr(97 + next_random() % 2) for _ in range(n))


def main():
    words = []
    for _ in range(100):
        length = next_random() % 100 + 1
        words.append(random_word(length))
    check = 0
    for _ in range(100000):
        length = next_random() % 8 + 1
        pref = random_word(length)
        check = (check * 31 + prefix_count(words, pref)) % 1000000007
    print(f"100000 solves: checksum {check}")


main()
