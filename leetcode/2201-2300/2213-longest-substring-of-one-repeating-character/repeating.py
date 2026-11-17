# LeetCode #2213: Longest Substring of One Repeating Character -- the
# mirror of repeating.kara: a segment tree keeping, for each range, the
# longest run that starts it, the longest that ends it and the longest
# inside it; each query changes one letter and mends the nodes above it.
import sys

sys.setrecursionlimit(10000)


def longest_repeating(s, query_characters, query_indices):
    letters = list(s)
    n = len(letters)
    prefix = [0] * (4 * n)
    suffix = [0] * (4 * n)
    best = [0] * (4 * n)

    def pull(node, lo, hi):
        mid = (lo + hi) // 2
        left, right = 2 * node, 2 * node + 1
        joined = letters[mid] == letters[mid + 1]
        prefix[node] = prefix[left] + prefix[right] if joined and prefix[left] == mid - lo + 1 else prefix[left]
        suffix[node] = suffix[right] + suffix[left] if joined and suffix[right] == hi - mid else suffix[right]
        best[node] = max(best[left], best[right])
        if joined:
            best[node] = max(best[node], suffix[left] + prefix[right])

    def build(node, lo, hi):
        if lo == hi:
            prefix[node] = suffix[node] = best[node] = 1
            return
        mid = (lo + hi) // 2
        build(2 * node, lo, mid)
        build(2 * node + 1, mid + 1, hi)
        pull(node, lo, hi)

    def update(node, lo, hi, at):
        if lo == hi:
            return
        mid = (lo + hi) // 2
        if at <= mid:
            update(2 * node, lo, mid, at)
        else:
            update(2 * node + 1, mid + 1, hi, at)
        pull(node, lo, hi)

    build(1, 0, n - 1)
    lengths = []
    for letter, at in zip(query_characters, query_indices):
        letters[at] = letter
        update(1, 0, n - 1, at)
        lengths.append(best[1])
    return lengths


seed = 2213


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join("abcdefghijklmnopqrstuvwxyz"[next_random() % letters] for _ in range(n))


def random_indices(k, n):
    return [next_random() % n for _ in range(k)]


def show(s, query_characters, query_indices):
    print(f'"{s}" with "{query_characters}" at {query_indices} -> {longest_repeating(s, query_characters, query_indices)}'.replace("'", ""))


def main():
    # LeetCode's two examples, then four more: one letter, a run broken in
    # the middle, two runs joined, and a letter set to what it was
    show("babacc", "bcb", [1, 3, 3])
    show("abyzz", "aa", [2, 1])
    show("a", "b", [0])
    show("aaaaaaa", "ba", [3, 3])
    show("aabaa", "a", [2])
    show("abcabc", "aab", [0, 0, 4])
    # 3000 random words of 1 to 30 letters, each with 1 to 30 queries,
    # the letters drawn from 2, 3 and 26 in turn
    check = 0
    for t in range(3000):
        letters = [2, 3, 26][t % 3]
        n = next_random() % 30 + 1
        k = next_random() % 30 + 1
        s = random_word(n, letters)
        query_characters = random_word(k, letters)
        query_indices = random_indices(k, n)
        for length in longest_repeating(s, query_characters, query_indices):
            check = (check * 31 + length) % 1000000007
    print(f"3000 words: checksum {check}")
    # the constraints' largest: 10^5 letters of 'a' and 'b' with 10^5
    # random queries, then 10^5 'a's with the middle letter broken and
    # mended in turn
    s = random_word(100000, 2)
    query_characters = random_word(100000, 2)
    query_indices = random_indices(100000, 100000)
    lengths = longest_repeating(s, query_characters, query_indices)
    print(f"10^5 random: total {sum(lengths)}, last {lengths[99999]}")
    plain = "a" * 100000
    flips = "".join("b" if i % 2 == 0 else "a" for i in range(100000))
    lengths = longest_repeating(plain, flips, [50000] * 100000)
    print(f"10^5 alike: first {lengths[0]}, last {lengths[99999]}, total {sum(lengths)}")


main()
