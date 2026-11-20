# 1750. Minimum Length of String After Deleting Similar Ends

Given a string `s` consisting only of characters `'a'`, `'b'`, and
`'c'`. You are asked to apply the following algorithm on the string any
number of times:

1. Pick a **non-empty** prefix from the string `s` where all the
   characters in the prefix are equal.
2. Pick a **non-empty** suffix from the string `s` where all the
   characters in this suffix are equal.
3. The prefix and the suffix should not intersect at any index.
4. The characters from the prefix and suffix must be the same.
5. Delete both the prefix and the suffix.

Return *the **minimum length** of* `s` *after performing the above
operation any number of times (possibly zero times)*.

```
s = "ca"          ->  2
s = "cabaabac"    ->  0    "c" and "c", "a" and "a", "b" and "b", "a" and "a"
s = "aabccabba"   ->  3    "aa" and "a", "b" and "bb", leaving "cca"
```

**Constraints:** `1 <= s.length <= 10^5`; `s` only consists of
characters `'a'`, `'b'`, and `'c'`.

## Approaches

| file | mechanism |
|---|---|
| `ends.kara` ★ | two pointers over `s.bytes()`: while the ends hold the same letter, every copy of it at the front and at the back comes off; the front's sweep may run through a middle made of that letter alone, so the back's stops where the front got to. O(n) |
| `ends_runs.kara` | the string cut into runs of one letter with their lengths; matching outer runs come off in pairs, and what is left is either several runs, kept whole, or one run, which comes off too when it has two letters or more. O(n) |
| `ends_trim.kara` | the string shortened one layer at a time as a `Str` view: while its ends match, `strip_prefix` and `strip_suffix` take that letter off each end until neither finds it. O(n) |
| `ends_solution.kara` | a Rust solution as LeetCode's Rust users write it, two `usize` pointers over `s.as_bytes()` with the back's sweep held above the front so that it never passes below 0, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 10 lines: LeetCode's three examples, then one
letter, two equal letters, an odd palindrome that leaves its middle, and
100000 of one letter; then the sum of the answers and a checksum for
3000 random strings of up to 10 letters from 2, 1000 of up to 100 from
3, and 20 of up to 100000, LeetCode's limit, from 3. Half of each batch
is plain random and half a short random middle wrapped in layers of one
letter on both sides, so that whole layers come off. `ends.py` mirrors
the ★ arm and its output is byte-identical.

```
2
0
3
1
0
1
0
3000 strings of up to 10 letters from 2: lengths add to 5070, checksum 797901456
1000 strings of up to 100 letters from 3: lengths add to 25531, checksum 7245651
20 strings of up to 100000 letters from 3: lengths add to 171166, checksum 462230405
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: from the string, every operation the statement allows, a
non-empty prefix and a non-empty suffix of one letter that do not meet,
is tried, recursively, and the shortest length any sequence of them
reaches is the answer. It checks 3000 random strings of up to 10
letters, or a little more when wrapped, from the first 1 to 3 letters,
drawn as in the arms. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed gives the same answer |
| P3 | the letters renamed one for one give the same answer |
| P4 | the string between two `z`s gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 347758411, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading, the same search over every allowed prefix and suffix, memoized,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the front's sweep takes one letter, not every copy | P1 963, P2 818, P5 963 |
| M2 | ★: the back's sweep takes one letter, not every copy | P1 958, P2 818, P5 958 |
| M3 | ★: the ends compared only while three letters or more are left | P1 257, P5 257 |
| M4 | runs: one run left kept whole, whatever its length | P1 1694, P5 1694 |
| M5 | runs: one run left taken off only from three letters | P1 257, P5 257 |
| M6 | runs: a run cut at two letters | P1 679, P2 561, P5 679 |
| M7 | trim: one letter stripped from the back, not every copy | P1 958, P2 818, P5 958 |
| M8 | trim: the ends compared only while three letters or more are left | P1 257, P5 257 |
| M9 | solution: the back's sweep held two above the front | P1 500, P4 157, P5 500 |
| M10 | solution: the front's sweep stopped before it meets the back | P1 1694, P5 1694 |

Two first edits were equivalent and replaced: the ★ arm's front sweep
stopping before it meets the back, where the back's sweep then takes
the last letter instead; and the runs arm answering 1 when the pairs
cross, which they never do, since neighbouring runs never share a
letter. The second found a dead `if i > j { return 0; }` in the runs
arm, since removed.

## Benchmarks

The bench draws 50 strings of about 100000 letters, LeetCode's longest,
each a random middle of up to 1000 letters from `a` and `b` wrapped in
layers of one letter on both sides, all of them first, then answers
each 40 times by the ★ arm in all five languages; nearly every answer
walks the whole string. Every implementation prints `50 strings of about
100000 letters, 40 rounds: lengths add to 920, checksum 329514737`. The C
build also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `21cdf88b69` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.567 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.625 s |
| Rust (`rustc -O`) | 0.692 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.733 s |
| Kāra (`karac build`) | 0.736 s |
| Go | 0.759 s |
| Python | 12 s |

The sequential Kāra build takes 1.06x Rust's time and 1.17x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
The 17% over Rust with overflow checks on is not explained yet. C is the
fastest here at 0.567 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.732 s and
0.748 s on one run).

## Verification

All four arms print the same output as `ends.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ arm checked clean as first written.

The runs arm first extended the last run through Rust's `match
runs.last_mut() { Some((d, n)) if d == c => n += 1, _ => runs.push((c,
1)) }`. Kāra has no `last_mut`, and `karac check` named the index form;
one `karac fix` wrote it, `if runs.len() > 0 and runs[runs.len() - 1].0
== c { runs[runs.len() - 1].1 += 1; } else { .. }`.

The trim arm was first written with Rust's `trim_start_matches(c)` and
`trim_end_matches(c)`. Kāra has neither, and `karac check` named
`strip_prefix` and `strip_suffix` in a loop, which the arm then used. It
started its view as `let mut rest: Str = s;` with `s` the borrowed
`String` parameter, and `karac check` refused that with a bare
`expected 'Str', found 'ref String'` and no fix: the check that writes
`.as_str()` for a `String` read as a `Str` looked at the parameter's
type without resolving what its borrow pointed to. Since kara `21cdf88b69`
(B-2026-11-20-105) it resolves it, and one `karac fix` wrote `s.as_str()`.

LeetCode's Rust template took one `karac fix` of 9 edits: `struct
Solution {}` added, `s.as_bytes()` written `s.bytes()`, `let (mut i, mut
j)` written `let mut (i, j)`, `&&` written `and`, and
`Solution::minimum_length` written `Solution.minimum_length`. The
`j as i32 - i as i32 + 1` tail carried over as written.

The differential and the bench checked clean as generated.
