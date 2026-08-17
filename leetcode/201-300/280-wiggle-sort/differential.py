#!/usr/bin/env python3
"""LeetCode 280 — differential harness. Mirror of differential.kara.

The answer is not unique, so validity is checked rather than compared, and it
is TWO conditions: the wiggle property AND the same multiset as the input.
"""


def wiggles(v):
    for i in range(1, len(v)):
        if i % 2 == 1:
            if v[i] < v[i - 1]:
                return False
        else:
            if v[i] > v[i - 1]:
                return False
    return True


def greedy(nums):
    for i in range(1, len(nums)):
        odd = i % 2 == 1
        if odd:
            if nums[i] < nums[i - 1]:
                nums[i], nums[i - 1] = nums[i - 1], nums[i]
        else:
            if nums[i] > nums[i - 1]:
                nums[i], nums[i - 1] = nums[i - 1], nums[i]


def sorted_pairs(nums):
    a = 1
    while a < len(nums):
        b = a
        while b > 0 and nums[b - 1] > nums[b]:
            nums[b - 1], nums[b] = nums[b], nums[b - 1]
            b -= 1
        a += 1
    i = 1
    while i + 1 < len(nums):
        nums[i], nums[i + 1] = nums[i + 1], nums[i]
        i += 2


def brute(nums):
    a = 1
    while a < len(nums):
        b = a
        while b > 0 and nums[b - 1] > nums[b]:
            nums[b - 1], nums[b] = nums[b], nums[b - 1]
            b -= 1
        a += 1
    while True:
        if wiggles(nums):
            return
        p = len(nums) - 2
        while p >= 0 and nums[p] >= nums[p + 1]:
            p -= 1
        if p < 0:
            return
        s = len(nums) - 1
        while nums[s] <= nums[p]:
            s -= 1
        nums[p], nums[s] = nums[s], nums[p]
        nums[p + 1:] = reversed(nums[p + 1:])


def same_multiset(a, b):
    return len(a) == len(b) and sorted(a) == sorted(b)


def lex_cmp(a, b):
    for i in range(min(len(a), len(b))):
        if a[i] < b[i]:
            return -1
        if a[i] > b[i]:
            return 1
    return 0


def main():
    cases = greedy_invalid = sorted_invalid = brute_invalid = 0
    greedy_below = sorted_below = greedy_differed = sorted_equalled = 0
    with_duplicates = digest = 0

    seed = 20260818
    for n in range(1, 8):
        for t in range(240):
            alpha = 2 + (t % 4)
            base = []
            for _ in range(n):
                seed = (seed * 1103515245 + 12345) % 2147483648
                base.append((seed // 13) % alpha)
            if len(set(base)) < len(base):
                with_duplicates += 1

            g, s, b = list(base), list(base), list(base)
            greedy(g)
            sorted_pairs(s)
            brute(b)

            if not wiggles(g) or not same_multiset(base, g):
                greedy_invalid += 1
            if not wiggles(s) or not same_multiset(base, s):
                sorted_invalid += 1
            if not wiggles(b) or not same_multiset(base, b):
                brute_invalid += 1

            if lex_cmp(g, b) < 0:
                greedy_below += 1
            if lex_cmp(s, b) < 0:
                sorted_below += 1
            if lex_cmp(g, b) != 0:
                greedy_differed += 1
            if lex_cmp(s, b) == 0:
                sorted_equalled += 1

            for v in b:
                digest = (digest * 131 + v + 1) % 1000000007
            cases += 1

    print(f"cases {cases}, of which contain a duplicate {with_duplicates}")
    print(f"greedy answers differing from the lex-smallest {greedy_differed}")
    print(f"sort-then-pair answers EQUAL to the lex-smallest {sorted_equalled}")
    print(f"answers lexicographically BELOW the brute-force minimum: greedy {greedy_below}, sorted {sorted_below}")
    print(f"digest {digest}")
    print(f"invalid (wiggle or multiset): greedy {greedy_invalid}, sorted {sorted_invalid}, brute {brute_invalid}")


main()
