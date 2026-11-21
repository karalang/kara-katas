# LeetCode #2416: Sum of Prefix Scores of Strings -- the Python mirror of
# the ★ arm: a trie in flat arrays, `next[26 k + c]` node k's child by
# letter c and `count[k]` the words through it.

seed = 0


def sum_prefix_scores(words):
    nxt = [0] * 26
    count = [0]
    for w in words:
        at = 0
        for b in w.encode():
            c = b - 97
            if nxt[26 * at + c] == 0:
                nxt[26 * at + c] = len(count)
                count.append(0)
                nxt.extend([0] * 26)
            at = nxt[26 * at + c]
            count[at] += 1
    scores = []
    for w in words:
        at = 0
        score = 0
        for b in w.encode():
            at = nxt[26 * at + b - 97]
            score += count[at]
        scores.append(score)
    return scores


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_words(n, longest, kinds):
    words = []
    for _ in range(n):
        length = 1 + next_random() % longest
        words.append("".join(chr(97 + next_random() % kinds) for _ in range(length)))
    return words


def show(scores):
    return "[" + ",".join(str(s) for s in scores) + "]"


def digest(scores):
    h = 0
    for s in scores:
        h = (h * 31 + s) % 1000000007
    return f"{h} {sum(scores)}"


def main():
    global seed
    print(show(sum_prefix_scores(["abc", "ab", "bc", "b"])))
    print(show(sum_prefix_scores(["abcd"])))
    print(show(sum_prefix_scores(["a"])))
    print(show(sum_prefix_scores(["aa", "aa", "aa"])))
    print(show(sum_prefix_scores(["abcd", "abc", "ab", "a"])))
    print(show(sum_prefix_scores(["x", "yz", "zyx"])))
    seed = 2416
    print(digest(sum_prefix_scores(random_words(1000, 1000, 2))))
    print(digest(sum_prefix_scores(random_words(1000, 1000, 26))))
    check = 0
    total = 0
    for _ in range(2000):
        n = 1 + next_random() % 10
        longest = 1 + next_random() % 8
        kinds = 1 + next_random() % 4
        for s in sum_prefix_scores(random_words(n, longest, kinds)):
            total += s
            check = (check * 31 + s) % 1000000007
    print(f"2000 random: checksum {check}, total {total}")


if __name__ == "__main__":
    main()
