# LeetCode #2052: Minimum Cost to Separate Sentence Into Rows -- Python
# mirror of the ★ arm's benchmark (separate.kara): the same 600 sentences,
# the same dynamic programming from the end.

seed = 2052


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    total = check = 0
    for t in range(600):
        parts = []
        length = 0
        while length < 4990:
            if length > 0:
                length += 1
            w = next_random() % 10 + 1
            word = "".join(letters[next_random() % 26] for _ in range(w))
            parts.append(word)
            length += w
        text = " ".join(parts)
        k = 20 + t % 200 * 20
        cost = minimum_cost(text, k)
        total += cost
        check = (check * 31 + cost) % 1000000007
    print(f"600 sentences: sum {total}, checksum {check}")


main()
