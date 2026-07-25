"""LeetCode 387 — First Unique Character in a String (reference oracle).

Same two-pass tally as the Kara version.
"""


def first_uniq_char(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for j, ch in enumerate(s):
        if counts[ch] == 1:
            return j
    return -1


def unique_count(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return sum(1 for k in counts if counts[k] == 1)


def report(s):
    print(f"{s} -> {first_uniq_char(s)} (uniq={unique_count(s)})")


def main():
    report("leetcode")
    report("loveleetcode")
    report("aabb")
    report("z")
    report("")
    report("abcabcd")


if __name__ == "__main__":
    main()
