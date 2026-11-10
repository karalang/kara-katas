# 2057. Smallest Index With Equal Value

Given a 0-indexed integer array `nums`, return the smallest index `i` of
`nums` such that `i mod 10 == nums[i]`, or `-1` if there is no such index.

```
nums = [0, 1, 2]                        ->  0
nums = [4, 3, 2, 1]                     ->  2
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]   ->  -1
```

**Constraints:** `1 <= nums.length <= 100`; `0 <= nums[i] <= 9`.

The indices are tried from the front and the first that matches is the
answer; the approaches differ in how they walk and how they stop.

## Approaches

| file | mechanism |
|---|---|
| `equal.kara` ★ | the indices walked from the front with a `for`, the first match returned, `-1` after the loop |
| `equal_brute.kara` | the statement read directly: every matching index gathered with `filter`, the smallest taken with `min`, `unwrap_or(-1)` for none |
| `equal_position.kara` | the elements `enumerate`d and the first match found with `position`, which stops there, and `match`ed to `-1` for none |
| `equal_chunks.kara` | the array cut into `chunks(10)`, one for each run of indices sharing their tens: an index's last digit is its place in its chunk, so the first element equal to its place, in the first chunk that has one, is the answer |
| `equal_recursive.kara` | the answer from index `i` on is `i` when it matches, else the answer from `i + 1` on, and `-1` past the end; at most 100 calls deep |
| `equal_solution.kara` | LeetCode's Rust template (`nums.iter().enumerate().find(\|&(i, &x)\| i % 10 == x as usize)` and `map_or(-1, \|(i, _)\| i as i32)`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and four
more, each array and its answer; then, for 5000 random arrays of 1 to
100 digits, the constraints' limit, how many have a match, the sum of
the answers and a checksum. A digit that would match its index is drawn
again, most of the time, so that about two arrays in five have a match
and the first one is often far in. `equal.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each index kept as the answer when it matches and no index
before it does, its last digit found as `i - i / 10 * 10` rather than
`%`. It checks 2000 random arrays, drawn as the harness draws them,
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is -1 or an index of the array whose last digit is its element |
| P3 | no index before the answer matches; with -1, no index matches |
| P4 | the array with digits appended answers the same when it found one; when it found none, -1 or an index among the appended |
| P5 | one element set to its index's last digit answers the smaller of that index and the old answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 arrays: checksum 604601366, 72000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-three edits to the differential, five to six to each of its
arms, each run under `karac __mir-run` and `karac __mir-llvm-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last digit taken mod 9 | P1 1506, P2 1499, P3 114, P5 218, P6 1506 |
| M2 | ★: the index after the match returned | P1 854, P2 839, P3 854, P5 1462, P6 854 |
| M3 | ★: the tens digit compared | P1 1796, P2 1766, P3 221, P5 439, P6 1796 |
| M4 | brute: the largest match taken | P1 413, P3 413, P4 570, P5 836, P6 413 |
| M5 | brute: the indices that do not match kept | P1 2000, P2 2000, P3 40, P5 105, P6 2000 |
| M6 | brute: an element at least its last digit a match | P1 1960, P2 1960, P6 1960 |
| M7 | position: the search from index 1, counted from there | P1 851, P2 841, P3 37, P4 121, P5 1461, P6 851 |
| M8 | position: the search from the back | P1 838, P2 823, P3 423, P4 1539, P5 1602, P6 838 |
| M9 | position: the length for no match | P1 1146, P2 1146, P4 1026, P6 1146 |
| M10 | chunks: the chunk's number added, not its tens | P1 566, P2 566, P4 679, P5 911, P6 566 |
| M11 | chunks: each chunk's first place left out | P1 127, P3 127, P5 235, P6 127 |
| M12 | chunks: the last match in a chunk | P1 107, P3 107, P4 14, P5 145, P6 107 |
| M13 | recursive: the walk from index 1 | P1 40, P3 40, P5 103, P6 40 |
| M14 | recursive: the digit returned, not the index | P1 566, P2 566, P4 689, P5 912, P6 566 |
| M15 | recursive: only even indices a match | P1 407, P3 407, P5 767, P6 407 |
| M16 | solution: the adapter adding one to each digit | P1 1820, P2 1794, P3 276, P5 623, P6 1820 |
| M17 | solution: the adapter dropping the first digit | P1 1780, P2 1748, P3 230, P4 20, P5 560, P6 1780 |

P1 and P6 kill all seventeen, P5 fifteen, P3 thirteen, P2 twelve and P4
eight. P2 and P3 split the work between them. An arm that answers a real
match, only not the first (M4, M11 to M13, M15), passes P2 and fails
P3; an arm that answers something that is not a match, but never past
the first one (M6's first index whose element is at least its digit,
M9's length for none, M10's and M14's numbers smaller than the index),
passes P3, since no match comes before what it answers, and fails P2. P4 appends digits, so it
catches the arms whose answer can move when later digits do (the
largest match, the search from the back, the last match in a chunk) and
the ones that answer something other than -1 for none. P5 makes one
index match, and misses only M6 and M9: index `k` made a match is one
for M6 too, which answers the smaller of `k` and its old answer as the
property asks, and M9 answers wrongly only when nothing matches, which
P5 never leaves.

Of the thirty-three, sixteen were not kept. None is equivalent and none
crashes. Three fail as M13, each a way of never answering index 0: the ★
arm's walk from 1, the position arm's index 0 never a match, and the
Rust arm's search from index 1. Four answer 0 for no match, in the ★,
brute, chunks and Rust arms, and fail alike. The ★ and recursive arms'
last index never looked at fail alike, as do the brute arm's first ten
indices only and the position arm's element's last digit compared with
the index: either way only an index under ten can match. Three fail as a
kept one does: the recursive arm's length for no match as M9, and the
Rust arm's last match as M4 and its element returned as M14. The chunks
arm's chunks of nine and its place compared with the chunk's number
added fail on checks of their own, and were left out because that arm
keeps three.

M8 was first written as Rust writes it, `nums.iter().enumerate().rev()`,
and the check refused it: see Verification.

## Verification

Every arm prints the same output as `equal.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.
Under `karac __mir-run` the arms take 0.4 s (★) to 1.0 s (Rust), and the
differential 4.6 s.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template, and met one gap.
`karac fix` carries it in two rounds of 5 and 1 edits: `struct
Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`, the two `&`
patterns in `|&(i, &x)|` dropped, and `x as usize` to `x as i64`. The
check then refused `map_or(-1, |(i, _)| i as i32)` returned as `i32`, as
a narrowing from `i64`, though `map_or(0, ..)` passed. A literal argument
for the parameter a generic call returns is left open, for a later
argument such as the closure to fix, but `-1` is a negation of a
literal, not a literal node, so it took the default `i64` at once. kara
`91f116f430` lets a negated literal stay open the same way (tests in
`tests/kata_2057_negative_literal_arg.rs`). The adapter hands the
harness's digits to it as `Vec[i32]` and widens the answer back.

A mutation met a second gap. The position arm searched from the back as
`nums.iter().enumerate().rev().position(..)`, and the check refused it,
"no method 'rev' on type 'IterEnumerate'": only the collections' own
iterators walked from the back, so `map(..).rev()`, `filter(..).rev()`
and `zip(..).rev()` were refused too. kara `8c8926d207` lets `map`, `filter`,
`cloned`, `enumerate` and `zip` walk from the back when what they wrap
can, with a new `ExactSizeIterator` that gives `enumerate` the index of
an item taken from the back and lets `zip` trim its longer side first,
as Rust's do (tests in `tests/kata_2057_adapter_rev.rs`).

Writing the library's `match_indices` beside that fix met one more gap,
open as B-2026-11-10-7: a user iterator over a `Str` field whose `next`
spells its return `Option[Str]` rather than `Option[Self.Item]` passes
`karac check`, and `collect()` on it is then refused by the borrow check
inside the library's `ItemValues.next`. The library's iterator is written
`Option[Self.Item]`, which runs.

## Benchmarks

The bench answers 1000000 arrays of 1 to 100 digits, the constraints'
limit, drawn as the harness draws them into one buffer that each array
reuses, with the ★ arm in all five languages: about 50 million digits
drawn and walked. Drawing the digits is part of the work timed, and is
most of it, since a walk stops at its first match. Every implementation
prints `1000000 arrays: 428037 found, sum 9290173, checksum 562373466`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `0142335972` and the fixes from
katas 2054 to 2057, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.225 to 0.297 s | 0.230 s |
| Kāra (`karac build`) | 0.226 to 0.291 s | 0.233 s |
| C (`clang -O3`) | 0.237 to 0.266 s | 0.238 s |
| Rust (`rustc -O`) | 0.264 to 0.271 s | 0.265 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.262 to 0.312 s | 0.272 s |
| Go | 0.501 to 0.537 s | 0.505 s |
| Python | 14.6 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.229 s) is not above its real time (0.233 s).

The sequential Kāra program is 0.84x Rust under overflow checks and 0.96x
C. Drawing the digits is most of the work: C, Rust and Kāra are within
a fifth of each other, and Go takes about twice as long.
