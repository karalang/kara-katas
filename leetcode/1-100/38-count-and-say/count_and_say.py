"""LeetCode #38: Count and Say — known-correct reference oracle.

The count-and-say sequence starts at countAndSay(1) = "1"; each later term is the
**run-length encoding** (RLE) of the previous one — read it as "<count><digit>" for each
maximal run of equal digits. "3322251" → "23"(two 3s) "32"(three 2s) "15"(one 5)
"11"(one 1) = "23321511". So 1, 11, 21, 1211, 111221, … each term *says* the one before.

Three styles, all producing the identical string for every n (cross-checked below), each
mirroring one Kāra pedagogical file:

  - Style 1 (streaming state-machine RLE, ★) — mirror of count_and_say.kara
  - Style 2 (recursive unfolding)            — mirror of count_and_say_rec.kara
  - Style 3 (indexed two-pointer grouping)   — mirror of count_and_say_indexed.kara

The output is `f"{n}: {term}"` for n = 1..N, line-for-line diffable against each Kāra
mirror's stdout under both `karac run` and `karac build`.
"""

from __future__ import annotations

N = 12


# --- Style 1: streaming state-machine RLE (mirrors count_and_say.kara, ★) -------
#
# Encode one term in a single left-to-right pass: carry the current run's digit and its
# length; on each character, extend the run if it matches, else FLUSH "<len><digit>" and
# start a new run. Flush the final run at the end. Unfold n by iterating the encode n-1
# times from the seed "1".

def say_stream(s: str) -> str:
    out = []
    run_digit = ""
    run_len = 0
    for ch in s:
        if ch == run_digit:
            run_len += 1
        else:
            if run_len != 0:
                out.append(str(run_len))
                out.append(run_digit)
            run_digit = ch
            run_len = 1
    if run_len != 0:
        out.append(str(run_len))
        out.append(run_digit)
    return "".join(out)


def count_and_say_stream(n: int) -> str:
    s = "1"
    for _ in range(n - 1):
        s = say_stream(s)
    return s


# --- Style 2: recursive unfolding (mirrors count_and_say_rec.kara) --------------
#
# The sequence's definition spelled out literally: countAndSay(1) = "1", and
# countAndSay(n) = say(countAndSay(n-1)). The encode is the same streaming RLE; only the
# n-fold unfolding changes — recursion down to the "1" base case instead of a loop.

def count_and_say_rec(n: int) -> str:
    if n == 1:
        return "1"
    return say_stream(count_and_say_rec(n - 1))


# --- Style 3: indexed two-pointer grouping (mirrors count_and_say_indexed.kara) --
#
# Same iterative unfolding, but the RLE groups runs with explicit indices: a left pointer
# i sits at a run's first character; a right pointer j advances while s[j] == s[i]; the
# run length is j - i. Emits "<j-i><s[i]>" and jumps i to j. The random-access reading of
# the same encoding the state machine streams.

def say_indexed(s: str) -> str:
    out = []
    n = len(s)
    i = 0
    while i < n:
        j = i
        while j < n and s[j] == s[i]:
            j += 1
        out.append(str(j - i))
        out.append(s[i])
        i = j
    return "".join(out)


def count_and_say_indexed(n: int) -> str:
    s = "1"
    for _ in range(n - 1):
        s = say_indexed(s)
    return s


def main() -> None:
    for n in range(1, N + 1):
        a = count_and_say_stream(n)
        b = count_and_say_rec(n)
        c = count_and_say_indexed(n)
        assert a == b == c, (n, a, b, c)
        print(f"{n}: {a}")


if __name__ == "__main__":
    main()
