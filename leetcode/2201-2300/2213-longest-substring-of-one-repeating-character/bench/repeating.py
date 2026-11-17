# LeetCode #2213: Longest Substring of One Repeating Character -- bench
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


# a draw of 30 bits, since one draw stops at 32767
def wide_random():
    return next_random() * 32768 + next_random()


def main():
    words = []
    for w in range(6):
        # 10^5 letters from 2, 3 and 26 in turn, with 10^5 queries
        letters = [2, 3, 26][w % 3]
        s = random_word(100000, letters)
        query_characters = random_word(100000, letters)
        query_indices = [wide_random() % 100000 for _ in range(100000)]
        words.append((s, query_characters, query_indices))
    check = 0
    for s, query_characters, query_indices in words:
        for length in longest_repeating(s, query_characters, query_indices):
            check = (check * 31 + length) % 1000000007
    print(f"6 words of 10^5: checksum {check}")


main()
