# LeetCode #2052: Minimum Cost to Separate Sentence Into Rows -- Python
# mirror of the ★ arm (separate.kara): dynamic programming from the end,
# each first row grown word by word while it fits. Output is byte-identical
# to the Kāra arms.


def minimum_cost(sentence, k):
    lens = [len(w) for w in sentence.split(" ")]
    n = len(lens)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        width = -1
        least = 2**63 - 1
        j = i
        while j < n and width + 1 + lens[j] <= k:
            width += 1 + lens[j]
            j += 1
            if j == n:
                least = 0
            else:
                least = min(least, (k - width) * (k - width) + best[j])
        best[i] = least
    return best[0]


# ---- test harness ---------------------------------------------------------

seed = 2052


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def sentence(count, longest):
    letters = "abcdefghijklmnopqrstuvwxyz"
    words = []
    for _ in range(count):
        length = next_random() % longest + 1
        word = ""
        for _ in range(length):
            at = next_random() % 26
            word += letters[at]
        words.append(word)
    return " ".join(words)


def main():
    examples = [
        ("i love leetcode", 12),
        ("apples and bananas taste great", 7),
        ("a", 5),
        ("a b c d e f", 1),
        ("ab cd ef gh", 5),
        ("hello world", 11),
        ("the quick brown fox jumps over the lazy dog", 10),
    ]
    for text, k in examples:
        print(f'"{text}", k {k} -> {minimum_cost(text, k)}')
    total = check = 0
    for _ in range(2000):
        count = next_random() % 30 + 1
        longest = next_random() % 8 + 1
        text = sentence(count, longest)
        k = longest + next_random() % 20
        cost = minimum_cost(text, k)
        total += cost
        check = (check * 31 + cost) % 1000000007
    print(f"2000 sentences: sum {total}, checksum {check}")
    total = check = 0
    for count, longest, k in [(1000, 7, 200), (330, 14, 15), (2500, 1, 2)]:
        text = sentence(count, longest)
        cost = minimum_cost(text, k)
        total += cost
        check = (check * 31 + cost) % 1000000007
    print(f"3 long sentences: sum {total}, checksum {check}")


main()
