# 1585. Check If String Is Transformable With Substring Sort Operations

Given two strings `s` and `t`, transform string `s` into string `t` using
the following operation any number of times:

- Choose a non-empty substring in `s` and sort it in place so the
  characters are in ascending order. For example, applying the operation
  on the underlined substring in `"14234"` results in `"12344"`.

Return `true` if it is possible to transform `s` into `t`. Otherwise,
return `false`.

A substring is a contiguous sequence of characters within a string.

```
s = "84532", t = "34852"  ->  true
s = "34521", t = "23415"  ->  true
s = "12345", t = "12435"  ->  false
```

**Constraints:** `s.length == t.length`; `1 <= s.length <= 10^5`; `s`
and `t` consist of only digits.

## Approaches

A sort is a run of swaps of a neighbouring larger-then-smaller pair, so
a digit can only ever move left past larger digits, and two equal digits
never change order.

| file | mechanism |
|---|---|
| `sortable.kara` ★ | `t` read left to right, each digit matched to the first unused copy of it in `s` (a `Vec[VecDeque[i64]]` of positions per digit); the match fails when a smaller digit's first unused copy lies before it, since nothing can move that copy past it. O(10 n) |
| `sortable_counts.kara` | the k-th copy of a digit can only gain smaller digits in front of it: for each copy in `s`, the ten running counts in front of it (`seen.to_vec()`), compared with the running counts of `t` at its k-th copy. O(10 n) |
| `sortable_pairs.kara` | with the digit counts equal (two `Map[char, i64]` compared with `!=`), for every pair `lo < hi` the k-th `hi` of `t` must have at least as many `lo` in front of it as the k-th `hi` of `s`, by a walk over the chars and a `zip(..).all(..)`. O(45 n) |
| `sortable_solution.kara` | LeetCode's Rust template (ten `Vec<usize>` of positions with a cursor each), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's three examples and five
more, then the count that are transformable and a checksum for 3000
random problems of up to 8 digits from 0 to 2, 300 of up to 1000 digits
and 10 of up to 100000; each `t` is made from `s` by random substring
sorts, and half the time two places swapped. `sortable.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every string reached from `s` by sorting any substring, any
number of times, found by a breadth-first search over a `Set[String]`,
and `t` looked for among them. It checks 3000 problems of 1 to 6 digits
from 0 to 2, each `t` drawn from `s` by up to two random sorts, half the
time a random swap and a quarter of the time one digit redrawn, every
random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | each digit `d` made `9 - d` and both strings reversed leave the answer |
| P3 | a 9 added at the end of both leaves the answer |
| P4 | a 0 added at the front of both leaves the answer |
| P5 | every digit raised by 5 leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 464198907, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

It first wrote `String.from_utf8(s.bytes().iter().map(|c| f(c)).collect())`,
Rust's `String::from_utf8(iter.collect())`, which `karac check` refused:
the collect took its target from `from_utf8`'s `Slice[u8]` parameter,
and no `Slice` is a `FromIterator`. That is kara `B-2026-11-15-21`, fixed
at `bae463436e`: a `collect()` passed where a call takes a `Slice[T]` now
collects into a `Vec[T]`. The line is written as it was first written.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

On the first run three survived (M3, M6, M7): each only changes what
happens when `t` has a digit `s` lacks, and every `t` was then a
rearrangement of `s`. The differential now redraws one digit of `t` a
quarter of the time, and all three are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: fails when a smaller digit's copy is after, not before | P1 1231, P2 51, P6 1231 |
| M2 | ★: the largest smaller digit never checked | P1 159, P6 159 |
| M3 | ★: a digit with no copy left in `s` passes | P1 369, P2 168, P6 369 |
| M4 | counts: fails when `t` has more smaller digits in front, not fewer | P1 822, P6 822 |
| M5 | counts: `t`'s running counts never grow | P1 1263, P3 985, P4 771, P6 1263 |
| M6 | counts: a digit with no copy left in `s` passes | P1 369, P2 168, P6 369 |
| M7 | pairs: the digit counts never compared | P1 329, P2 206, P3 329, P6 329 |
| M8 | pairs: the count of `lo` restarts after each `hi` | P1 214, P2 265, P6 214 |
| M9 | template: a smaller digit just before still lets it pass | P1 143, P6 143 |
| M10 | template: the cursor never moves | P1 1142, P2 572, P3 1394, P4 1203, P6 1142 |

## Benchmarks

The bench draws 40 problems of 100000 digits first, each `t` made from
`s` by 2000 sorts of substrings of 1 to 50 digits, and every other one
then given a random swap; then answers each by the ★ arm, in all five
languages. Every implementation prints `40 problems of 100000 digits: 23
transformable, checksum 193805455`. The C mirror keeps each digit's
queue as a growable array with a head index, allocated per call as the
Kāra `VecDeque`s are, and sorts each short run by insertion.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `bae463436e` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.087 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.091 s |
| C (`clang -O3`) | 0.095 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.099 s |
| Rust (`rustc -O`) | 0.103 s |
| Go | 0.149 s |
| Python | 2.3 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.071 s and 0.084 s on one run).

Kāra is 0.92x Rust under overflow checks by median. Most of the time in
every lane is drawing the strings and their 80000 short sorts; a `t`
that cannot be reached is usually refused early, which is why Python
takes only 2.3 s.

## Verification

All four arms print the same output as `sortable.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`bae463436e`.

## Writing it

The counts and pairs arms were written in Kāra and checked as written.
The ★ arm wrote `at[(c - b'0') as i64]`, and `karac fix` dropped the
cast, which a `u8` index does not need.

The Rust template took three rounds of `karac fix`:

1. six edits: the `Vec<Vec<usize>>` type to `Vec[Vec[usize]]`,
   `Vec::new()` to `Vec.new()`, `&&` to `and`, and `Solution::` to
   `Solution.`;
2. six edits: `vec![Vec.new(); 10]` to `Vec.filled(10, Vec.new())`,
   `s.bytes().enumerate()` to `s.bytes().iter().enumerate()`, the
   `usize` types and casts to `i64`, and `[0usize; 10]` to `[0; 10]`;
3. the now redundant `as i64` on the index dropped.

It then checks and agrees with no hand edit.
