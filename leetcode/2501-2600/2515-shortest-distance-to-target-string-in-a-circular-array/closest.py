# LeetCode #2515: Shortest Distance to Target String in a Circular Array
# -- Python mirror of the ★ arm (closest.kara): every place holding the
# target a candidate, the shorter way round from the start; and its
# harness, line for line.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def word(most, letters):
    length = next_random() % most + 1
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    global seed
    cases = [
        (["hello", "i", "am", "leetcode", "hello"], "hello", 1),
        (["a", "b", "leetcode"], "leetcode", 0),
        (["i", "eat", "leetcode"], "ate", 0),
        (["a"], "a", 0),
        (["a", "b"], "b", 0),
        (["x", "y", "z", "w"], "z", 0),
        (["t", "o", "o", "o", "o", "t", "o"], "t", 3),
        (["ab", "a", "b", "ba"], "a", 3),
    ]
    for words, target, start in cases:
        print(f"[{', '.join(words)}] \"{target}\" from {start} -> {closet_target(words, target, start)}")
    seed = 2515
    for most_words, most, letters in [(10, 1, 3), (100, 3, 2)]:
        misses = 0
        total = 0
        check = 0
        for _ in range(2000):
            n = next_random() % most_words + 1
            words = [word(most, letters) for _ in range(n)]
            target = word(most, 4 if letters == 3 else letters)
            start = next_random() % n
            a = closet_target(words, target, start)
            if a == -1:
                misses += 1
            else:
                total += a
            check = (check * 31 + a + 1) % 1000000007
        print(f"2000 random of up to {most_words} words: {misses} misses, total {total}, checksum {check}")
    a = "a" * 100
    b = "b" * 100
    c = "c" * 100
    far = [b if i == 50 else a for i in range(100)]
    print(f"100 words, the target opposite: {closet_target(far, b, 0)}")
    print(f"100 words, the target to the left: {closet_target(far, b, 51)}")
    print(f"100 words, no target: {closet_target(far, c, 7)}")
    same = [a for _ in range(100)]
    print(f"100 words, all the target: {closet_target(same, a, 99)}")


main()
