# LeetCode #2255: Count Prefixes of a Given String -- the benchmark's
# Python mirror of prefixes.kara: each word tested with s.startswith(word)
# and the ones that hold counted.


def count_prefixes(words, s):
    return sum(1 for w in words if s.startswith(w))


seed = 2255


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(longest, letters):
    length = next_random() % longest + 1
    data = bytearray()
    for _ in range(length):
        data.append(ord("a") + next_random() % letters)
    return data.decode()


def main():
    check = 0
    for c in range(500):
        letters = c % 5 + 1
        words = [random_word(10, letters) for _ in range(1000)]
        s = random_word(10, letters)
        check = (check * 31 + count_prefixes(words, s) + 1) % 1000000007
    print(f"500 cases of 1000 words: checksum {check}")


main()
