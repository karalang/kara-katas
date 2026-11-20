# 1737. Change Minimum Characters to Satisfy One of Three Conditions

You are given two strings `a` and `b` that consist of lowercase letters.
In one operation, you can change any character in `a` or `b` to **any
lowercase letter**.

Your goal is to satisfy **one** of the following three conditions:

- **Every** letter in `a` is **strictly less** than **every** letter in
  `b` in the alphabet.
- **Every** letter in `b` is **strictly less** than **every** letter in
  `a` in the alphabet.
- **Both** `a` and `b` consist of **only one** distinct letter.

Return *the **minimum** number of operations needed to achieve your
goal.*

```
a = "aba", b = "caa"         ->  2
a = "dabadd", b = "cda"      ->  3
```

**Constraints:** `1 <= a.length, b.length <= 10^5`; `a` and `b` consist
only of lowercase letters.

## Approaches

| file | mechanism |
|---|---|
| `minimum.kara` ★ | for "every letter of a below every letter of b" with the boundary between letters c - 1 and c, each letter of a from c up and each letter of b below c must change, for c from `b` to `z`; the second condition is the first with the strings swapped; for the third, every letter but the most common one across both strings must change. Each string's 26 counts and their running sums give every boundary's cost at once. O(m + n + 26) |
| `minimum_scan.kara` | each of the 25 boundaries, in each order, tried by walking both strings with `filter(..).count()` for the letters on the wrong side of it, and each of the 26 letters by counting the letters that differ from it. O(26 (m + n)) |
| `minimum_sorted.kara` | both strings' letters sorted, so a string's letters below a boundary are the prefix `partition_point` finds, and a letter's run lies between the searches for it and for what follows it. O((m + n) log(m + n)) |
| `minimum_solution.kara` | a Rust solution as LeetCode's Rust users write it, two `[0; 26]` count arrays over `a.bytes()`, the counts' running sums in a `let (mut pa, mut pb)`, and `ans.min(..).min(..)`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's two examples, then one
letter each, one letter in both, `z` against `a`, and `az` against
itself; then the changes summed and a checksum for 3000 random pairs of
up to 6 letters from `a` to `d`, 1000 pairs of up to 100 letters, and
10 pairs of up to `10^5` letters, LeetCode's longest. `minimum.py`
mirrors the ★ arm and its output is byte-identical.

```
2
3
0
0
0
2
3000 pairs of up to 6 letters from 4: changes sum to 5264, checksum 760829754
1000 pairs of up to 100 letters from 26: changes sum to 32296, checksum 973441487
10 pairs of up to 100000 letters from 26: changes sum to 83368, checksum 459354505
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every choice of which letters to keep, the rest changed, kept
when what is kept can be completed to one of the three conditions, and
the fewest changes of them. Kept letters complete to the first
condition when those of `a` are all below those of `b`, no changed
letter of `a` must go below a kept `a`, and no changed letter of `b`
above a kept `z`; to the third when they are all one letter. It checks
3000 random pairs of strings of 1 to 4 letters, each from `a`, `b`,
`c`, `x`, `y` and `z`, so that both ends of the alphabet are reached.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the strings swapped give the same answer |
| P3 | every letter mirrored, `a` for `z` and `z` for `a`, gives the same answer |
| P4 | each string reversed gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 36897557, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement another way, every pair of final strings over
`a`, `b`, `c`, `d`, `w`, `x`, `y` and `z` by `itertools.product`, kept
when it meets a condition, the fewest changes, gives the same checksum.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. No edit fails P4: every arm counts
letters without regard to their order. Three pairs make one change in
two arms and fail the very same checks: M1 and M8 leave b's letters out
of the third condition, M5 and M7 never try the boundary at `b`, and M6
and M10 never try b below a. M6 and M10 are the only edits that fail P2,
which swaps exactly the two orders.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the third condition's cost counts only a's letters of the common one | P1 61, P5 61 |
| M2 | ★: b below a costs b's letters from the boundary up, a's below it left out | P1 1696, P2 1063, P3 1115, P5 1696 |
| M3 | ★: the boundary at `z` never tried | P1 190, P3 414, P5 190 |
| M4 | scan: a's letters at the boundary left where they are | P1 1022, P3 279, P5 1022 |
| M5 | scan: the boundary at `b` never tried | P1 224, P3 414, P5 224 |
| M6 | scan: a below b tried twice, b below a never | P1 1066, P2 2115, P3 2115, P5 1066 |
| M7 | sorted: the boundary at `b` never tried | P1 224, P3 414, P5 224 |
| M8 | sorted: b's run of the common letter taken as empty | P1 61, P5 61 |
| M9 | solution: the running sums start at `b`, every `a` left out of them | P1 948, P3 879, P5 948 |
| M10 | solution: b below a never tried | P1 1066, P2 2115, P3 2115, P5 1066 |

## Benchmarks

The bench draws 20 random pairs of `10^5`-letter strings, LeetCode's
longest, all of them first, then answers each 200 times by the ★ arm in
all five languages. Every implementation prints `20 pairs of 100000
letters, 200 rounds: changes sum to 398884000, checksum 997550258`. C
walks the bytes of a string it has measured with `strlen`; Kāra, Rust
and Go walk the characters. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ad6400d909` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.311 s |
| Rust (`rustc -O`) | 0.388 s |
| Kāra (`karac build`) | 0.489 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.493 s |
| Go | 0.494 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.497 s |
| Python | 31 s |

The sequential Kāra build takes 1.27x Rust's time and 0.99x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).
With overflow checks on Rust is level, so the gap to plain Rust is the
cost of checked counting. C is the fastest here at 0.311 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.735 s and 0.735 s on one
run).

## Verification

All four arms print the same output as `minimum.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ad6400d909`.

## Writing it

The ★, scan and sorted arms checked clean as first written. The
harness first drew each letter with Rust's `char::from_u32(..)` written
`char.from_u32(..).unwrap()`; `karac check` named `char.try_from(n)`
and `.ok()`, and `karac fix` wrote `char.try_from(..).ok().unwrap()`.

LeetCode's Rust template took one `karac fix` of 8 edits: `struct
Solution {}` added, the two `[0; 26]` count arrays written `[0i32; 26]`
to meet the `i32` lengths, and `let (mut pa, mut pb) = (0, 0)` written
`let mut (pa, pb) = (0i32, 0i32)`. `a.bytes()`, `(c - b'a') as usize`
and `ans.min(..).min(..)` carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
