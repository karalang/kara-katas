"""LeetCode #131: Palindrome Partitioning — Python oracle.

All ways to cut s so every piece is a palindrome. Backtrack: try each palindromic
prefix, recurse on the rest. Deterministic report: count of partitions + an
order-independent digest (sum of per-partition hashes), plus a global sink.
"""

MOD = 1000000007


def is_pal(s, lo, hi):           # inclusive [lo, hi]
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def partition(s):
    res = []
    path = []

    def bt(start):
        if start == len(s):
            res.append(list(path))
            return
        for end in range(start, len(s)):
            if is_pal(s, start, end):
                path.append(s[start:end + 1])
                bt(end + 1)
                path.pop()

    bt(0)
    return res


def part_hash(parts):
    h = 0
    for piece in parts:
        for ch in piece:
            h = (h * 131 + (ord(ch) - ord('a') + 1)) % MOD
        h = (h * 131 + 27) % MOD
    return h


def summarize(s):
    ps = partition(s)
    count = len(ps)
    digest = 0
    for p in ps:
        digest = (digest + part_hash(p)) % MOD
    return count, digest


def main():
    sink = 0
    cases = ["aab", "a", "aba", "aabaa", "abccba", "racecar", "bananas", "aaaa", "abcde"]
    for s in cases:
        count, digest = summarize(s)
        print(f"{s}: count={count} hash={digest}")
        sink = (sink * 1000003 + count * 13 + digest) % MOD
    print(f"sink: {sink}")


if __name__ == "__main__":
    main()
