# 1754. Largest Merge Of Two Strings

You are given two strings `word1` and `word2`. You want to construct a
string `merge` in the following way: while either `word1` or `word2` are
non-empty, choose **one** of the following options:

- If `word1` is non-empty, append the **first** character in `word1` to
  `merge` and delete it from `word1`.
- If `word2` is non-empty, append the **first** character in `word2` to
  `merge` and delete it from `word2`.

Return *the lexicographically **largest*** `merge` *you can construct*.

```
word1 = "cabaa", word2 = "bcaaa"       ->  "cbcabaaaaa"
word1 = "abcabc", word2 = "abdcaba"    ->  "abdcabcabcaba"
```

**Constraints:** `1 <= word1.length, word2.length <= 3000`; both consist
only of lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `merge.kara` ★ | the letter is taken from the word whose rest, from the current letter to its end, is larger: different first letters decide at once, and a tie is broken by the first place the rests differ, an exhausted rest counting as smaller. The rests are compared as `Str` slices. O((m + n)^2) |
| `merge_chars.kara` | both words as `Vec[char]`, and the comparison written out in a helper: at the first place the rests differ the larger letter wins, and otherwise the rest that outlasts the other. O((m + n)^2) |
| `merge_deque.kara` | each word a `VecDeque[u8]`; the front is popped from the queue that compares larger, element by element, an empty queue being the smallest. O((m + n)^2) |
| `merge_solution.kara` | a Rust solution as LeetCode's Rust users write it, two byte slices from `as_bytes()` compared as slices and a `String::with_capacity` result pushed a `char` at a time, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's two examples, then one
letter each, equal words, one word a prefix of the other, and a tie
broken far ahead; then how many merges start with `a` and a checksum
over every merge's letters for 3000 random pairs of words of up to 6
letters from 2, 1000 of up to 100 from 3, and 10 of up to 3000,
LeetCode's limit, from 2. `merge.py` mirrors the ★ arm and its output
is byte-identical.

```
cbcabaaaaa
abdcabcabcaba
ba
abcabc
bbaba
aaaacaaaab
3000 pairs of up to 6 letters from 2: 753 start with a, checksum 117975929
1000 pairs of up to 100 letters from 3: 121 start with a, checksum 186728675
10 pairs of up to 3000 letters from 2: 1 start with a, checksum 792802533
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every merge, each step taking the first letter of one word or
the other, built out in full by recursion, and the largest of them. It
checks 3000 random pairs of words of 1 to 5 letters from the first 1 to
3. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words given in the other order give the same answer |
| P3 | the answer holds exactly the two words' letters |
| P4 | the answer is at least either word followed by the other |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 689215408, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, the same search over every merge, gives the same checksum. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Four first edits were replaced: three
that read past a word's end and stopped with a slice or index panic
rather than a wrong answer, and one equivalent, the chars helper no
longer asking whether the second rest ran out, which is the only way the
loop can end with the first rest left.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rests compared on their first two letters only | P1 98, P2 196, P4 43, P5 98 |
| M2 | ★: the first letter always taken from the first word | P1 787, P2 1515, P4 787, P5 787 |
| M3 | ★: the first word's rest compared with the second's one letter on | P1 1334, P2 1656, P4 1116, P5 1334 |
| M4 | chars: the rests compared on their first letter only | P1 326, P2 599, P4 185, P5 326 |
| M5 | chars: the smaller differing letter taken as larger | P1 1915, P4 1900, P5 1915 |
| M6 | chars: every other letter of the rests compared | P1 476, P2 621, P4 263, P5 476 |
| M7 | deque: the queues compared by their fronts only | P1 532, P2 937, P4 258, P5 532 |
| M8 | deque: the second word's letters taken from its back | P1 1209, P2 1647, P4 609, P5 1209 |
| M9 | solution: the first word's last letter left until the second word is empty | P1 791, P2 1543, P4 544, P5 791 |
| M10 | solution: the merge stops once either word is empty | P1 3000, P3 3000, P4 2383, P5 3000 |

## Benchmarks

The bench draws 200 pairs of words of 3000 letters, LeetCode's longest,
each letter `a` but for a `b` one time in 300, so that the two rests
often tie for hundreds of letters, all of them first, then merges each
pair 20 times by the ★ arm in all five languages and folds every merge's
letters into a checksum. Kāra and Go compare the rests as string
slices, Rust as `str` slices and C with `memcmp`; Python's `word1[i:]`
copies each rest before comparing it. Every implementation prints `200
pairs of 3000 letters, 20 rounds: checksum 530536625`. The C build also
runs clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.308 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.310 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.311 s |
| Kāra (`karac build`) | 0.320 s |
| Go | 0.366 s |
| C (`clang -O3`) | 0.417 s |
| Python | 6.6 s |

The sequential Kāra build is level with Rust and level with Rust with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.315 s and
0.315 s on one run).

## Verification

All four arms print the same output as `merge.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★, chars and deque arms checked clean as first written; the deque
arm's `a > b` on two `VecDeque[u8]` compares them element by element,
as Rust's does.

LeetCode's Rust template took one `karac fix` of 9 edits: `struct
Solution {}` added, `as_bytes()` written `bytes()`, `let (mut i, mut j)`
written `let mut (i, j)`, `String::with_capacity` written
`String.with_capacity`, `||` written `or`, and `Solution::largest_merge`
written `Solution.largest_merge`. The slice comparison `w1[i..] >
w2[j..]` and `w1[i] as char` carried over as written.

The differential and the bench checked clean as generated.
