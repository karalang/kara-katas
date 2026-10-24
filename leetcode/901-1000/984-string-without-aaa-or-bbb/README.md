# 984. String Without AAA or BBB

Given two integers `a` and `b`, return any string `s` such that:

- `s` has length `a + b` and contains exactly `a` `'a'` letters, and
  exactly `b` `'b'` letters,
- the substring `'aaa'` does not occur in `s`, and
- the substring `'bbb'` does not occur in `s`.

```
a = 1, b = 2  ->  "abb"    ("bab" and "bba" are also correct)
a = 4, b = 1  ->  "aabaa"
```

**Constraints:** `0 <= a, b <= 100`; it is guaranteed such an `s`
exists for the given `a` and `b`.

## Approaches

Every arm makes the answer of one greedy rule: after two of one letter
the other comes next; otherwise the letter with more left to write goes
next, `a` when the counts are even. Writing the more numerous letter
first never strands it, so the rule finds an answer whenever one exists.

| file | mechanism |
|---|---|
| `str_without_3a3b.kara` ★ | greedy, reading the tail: the answer is written a letter at a time, and `ends_with("aa")` and `ends_with("bb")` on the string so far say when the other letter is forced. O(a + b) |
| `str_without_3a3b_blocks.kara` | the greedy answer in closed form: with a >= b it opens with min(a - b, b) blocks of `aab`, then either the last one or two a's or `ab` in turn; with more b's, min(b - a - 1, a) blocks of `bba`, then the last b's or `b` and `ab` in turn, since the rule writes `a` as soon as the counts are even. O(a + b) |
| `str_without_3a3b_index.kara` | each letter from its place: the closed form read at place i alone, so no letter depends on the letters before it, and the answer is `(0..a + b).map(...).collect()` into a `String`. O(a + b) |
| `str_without_3a3b_recursive.kara` | the first block, then the rest: the answer opens with a block after which the rule has nothing to remember, `aab` with more a's, `ab` when even, `ba` with one more b and `bba` with more, followed by the answer for what is left. O((a + b)^2) for the copying |
| `str_without_3a3b_runs.kara` | the run so far as a state: an enum of nothing or a run of one or two of a letter, advanced by one `match` per letter, with the letters gathered in a `Vec[char]`. O(a + b) |
| `differential.kara` | the five arms against the statement read literally, six properties |

LeetCode accepts any answer and gives `"abb"` for its first example;
the rule writes `"bab"`. Every arm prints the same 13 lines. The first
ten are LeetCode's two examples and eight more: one letter (`a`); two
of one letter (`bb`); even counts (`ababab`); the most a's and the
most b's that two letters fit around (6 and 2, `aabaabaa`, and 2 and 6,
`bbabbabb`); one letter ahead by two either way (`aabaabab` and
`bbababab`); and LeetCode's largest, 100 of each, which alternates.
Then totals over random pairs that have an answer, 300 up to 10 and
3,000 up to 100, and over all 5,300 such pairs up to 100: the letters,
how many repeat the letter before them, and a checksum of every letter.
`str_without_3a3b.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a + b letters, exactly a of them `a` and b of them `b`, each
counted as the letters are read, and no three letters in a row the same.
It checks 3,200 pairs, each with an answer: 3,000 of up to 8 of each
letter against the statement, and 200 of up to LeetCode's 100 against
the other properties.

| | property |
|---|---|
| P1 | the statement, on the first 3,000 pairs |
| P2 | the rest after a free place is the answer for what is left: cut at a random place, moved back to one where a run starts and the two letters before differ, the letters after it are the arm's own answer for the a's and b's they hold |
| P3 | the shape: the less numerous letter (b when they are even) never doubles, and the runs of the other never grow |
| P4 | one more of each letter, when a <= 2b and b <= 2a + 1, adds `ab` at the end |
| P5 | every letter is the one the rule picks from the letters left and the two before it |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 pairs of 48454 letters: 7337 doubled, checksum
822918301, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (2.9 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-eight edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two a's in a row do not force a b | P1 789, P5 878, P6 878 |
| M2 | ★: ties go to b | P4 2527, P5 2300, P6 2300 |
| M3 | ★: two b's in a row do not force an a | P1 463, P5 555, P6 555 |
| M4 | blocks: one `aab` block too many | P1 1731, P2 663, P5 1399, P6 1829 |
| M5 | blocks: `bba` blocks written `bab` | P1 180, P2 419, P3 888, P5 888, P6 888 |
| M6 | blocks: one `bba` block too many | P1 805, P2 584, P4 227, P5 901, P6 901 |
| M7 | index: `aab` blocks read as `aba` | P1 152, P2 655, P3 1223, P5 1282, P6 1282 |
| M8 | index: the even tail starts with b | P2 458, P3 746, P4 1399, P5 1181, P6 1181 |
| M9 | index: one place short | P1 3000, P4 2527, P6 3200 |
| M10 | recursive: one more b opens with `bba` | P2 466, P3 1014, P4 767, P5 1066, P6 1066 |
| M11 | recursive: the last b's dropped | P1 1269, P2 623, P4 1128, P6 1371 |
| M12 | recursive: one more b opens with `ab` | P2 390, P3 849, P4 1128, P5 901, P6 901 |
| M13 | runs: a run of two a's goes on | P1 1189, P3 345, P4 59, P5 1282, P6 1282 |
| M14 | runs: ties go to b at the start | P2 544, P5 435, P6 435 |
| M15 | runs: after a b, ties go to b | P3 1840, P4 1356, P5 2026, P6 2026 |

P6 kills all fifteen, P5 thirteen (all but M9 and M11), P1, P2 and P4
nine each, and P3 seven. Six of the fifteen make answers LeetCode
would accept, M2, M8, M10, M12, M14 and M15, so P1 cannot see them:
they write another letter where the rule has a choice, and only the
properties of the rule's own answer catch them. M9 and M11 lose letters
at the end, which leaves every letter they do write as the rule would,
so P5 passes them; P1 counts the letters. The rule remembers only
whether the last two letters are equal. At P2's free place they are
not, and the next letter starts a new run, so the runs after the cut
are the same whether or not the letters before it are there.

Thirteen other edits were tried and set aside. Four failed exactly the
same checks as a kept one: recursive opening more a's with `aba`, as
M7; recursive opening even counts with `ba`, as M8; recursive opening
more b's with `bab`, as M5; and runs never growing a run of a's, as M1.
Seven were sound but beyond three an arm: ★ writing the fewer letter
next; ★ letting one a force a b; blocks writing `aab` as `aba`; blocks
leaving out the lone b before the tail; index with one `bba` block too
few; recursive dropping the last a's; runs letting two b's force
another b. One survived and is equivalent: index reading the tail as
`b` and `ab` in turn also when b = 2a + 1, where the tail is a single
b either way. One crashed in both lanes: recursive taking two b's with
each `aab` drives b below zero, never meets its base case, and
overflows the stack.

## Verification

Every arm prints the same output as `str_without_3a3b.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 1.8 s (blocks) to 5.3 s (index,
which builds each answer through an iterator), the ★ arm 2.6 s, and the
differential 2.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. In each of 100 rounds
it makes the answer for every one of the 5,300 pairs up to LeetCode's
100 that have one, each round starting from a different pair, and
folds every answer's length and middle letter into a checksum. Every
implementation prints `100 rounds over 5300 pairs up to 100: 61095000
letters, checksum 501637177`. Each call builds a fresh string of up to
200 letters a letter at a time, and looks at its last two letters
before each one.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.084 to 0.099 s | 0.095 s |
| Rust (`rustc -O`) | 0.424 to 0.490 s | 0.459 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.425 to 0.481 s | 0.469 s |
| Go | 0.693 to 0.841 s | 0.750 s |
| Python | 6.3 s | |
| Kāra (`karac build --mir`) | 0.367 to 0.412 s | 0.394 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 16 times
Kāra's.

v2 took 0.84 times Rust's median time under overflow checks and 4.1
times C's. Under valgrind's cachegrind v2 ran 1,917 million
instructions and 507 million branches with 15.9 million mispredicted,
Rust with overflow checks 2,449 million, 506 million and 18.6 million,
and C 974 million, 249 million and 2.4 million. The C program differs from
the others in one way: it allocates the a + b letters it needs
once and writes into them, where Rust's `String`, Go's
`strings.Builder` and Kāra's `String` start empty and grow as letters
are pushed, which fits its fewer instructions and far fewer
mispredicted branches (inferred, not traced).
