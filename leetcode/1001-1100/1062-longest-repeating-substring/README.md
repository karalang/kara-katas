# 1062. Longest Repeating Substring

Given a string `s`, return the length of the longest repeating substring:
the longest substring that occurs at least twice. Return `0` if no
substring repeats. The two occurrences may overlap.

```
s = "abcd"         ->  0
s = "abbaba"       ->  2     ("ab" and "ba" each occur twice)
s = "aabcaabdaab"  ->  3     ("aab" occurs three times)
```

**Constraints:** `1 <= s.length <= 2000`; `s` is lowercase English
letters.

A length has a repeat only if every shorter one does (the repeat's
prefixes repeat too), so the answer can be found by a binary search on the
length, or read off a table of common runs.

## Approaches

| file | mechanism |
|---|---|
| `lrs.kara` ★ | a binary search on the length, each step a rolling hash over the windows of that length in a `Map[i64, Vec[i64]]` from hash to starts, each match checked byte for byte. O(n log n) expected |
| `lrs_dp.kara` | the common run ending at each pair of ends, one longer than the run ending one byte before when the bytes match, keeping one row. O(n^2) time, O(n) space |
| `lrs_set.kara` | the same binary search, each step putting every window of that length into a `Set[String]` until one is already there. O(n^2 log n) |
| `lrs_z.kara` | the Z-function of every suffix, whose largest value is the longest substring starting there that occurs again later. O(n^2) |
| `lrs_suffix.kara` | the suffixes' starts sorted by the suffixes (`b[x..].cmp(b[y..])`), and the longest common prefix of two neighbours. O(n^2 log n) worst case |
| `lrs_solution.kara` | LeetCode's Rust template (`struct Solution;`, a full `vec![vec![0i32; n + 1]; n + 1]` table, `as_bytes()`, `std::cmp::max`, `Solution::`), carried to Kāra by `karac fix`. O(n^2) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 17 lines: the answers for LeetCode's three
examples and seven more; the sum and a checksum of the answers for 3000
strings of 1 to 12 letters over 1 to 3 of them, and for 300 strings of 50
to 300 letters over 2 to 26; and the answers for strings of 2000 letters
over 2, 4 and 26 letters, a Fibonacci word of 2000 letters (1013) and 2000
`z`s (1999). `lrs.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from the string's length less one down to 1, the first length
at which two different starts hold the same substring, compared as
`String`s, or 0. It checks 2000 strings: 1000 of 1 to 12 letters over 1 to
3, and 1000 of 1 to 30 over 2 to 26. Every random choice of a problem is
drawn before any arm answers, so a wrong arm cannot change the problems
the others see.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer lies between 0 and the length less one, and when it is not 0 two different starts hold the same substring of that length |
| P3 | the string reversed, and its letters renamed by a random permutation of the alphabet, leave the answer |
| P4 | the string written twice is answered by at least its own length |
| P5 | a letter added at the end leaves the answer or raises it by one, and the string cut in two answers each half with no more than the whole |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 945189114, 96000 checks
over 6 arms: 0 failures` under every lane in Verification; a Python
reading of the same 2000 strings gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks. A
first Z-function edit, dropping the box's `l = k`, survived: with `l` at 0
the box reads `z[k]`, still 0, and the match is extended by hand, which is
slower but right. It was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search capped one short of the length | P1 326, P4 98, P6 326 |
| M2 | ★: the first window never recorded | P1 595, P3 352, P4 1657, P6 595 |
| M3 | ★: overlapping repeats refused | P1 548, P6 548 |
| M4 | dp: the row not cleared between rows | P1 822, P2 822, P3 742, P6 822 |
| M5 | dp: adjacent starts never extended | P1 459, P6 459 |
| M6 | set: length 1 assumed to repeat | P1 243, P2 243, P6 243 |
| M7 | set: the search stops one step early | P1 984, P4 98, P5 435, P6 984 |
| M8 | set: a failed length's lower neighbour dropped too | P1 507, P5 411, P6 507 |
| M9 | Z: the box's bound taken as a max | P1 258, P2 258, P3 346, P6 258 |
| M10 | Z: the box's right end one past its match | P1 177, P2 177, P3 272, P6 177 |
| M11 | suffix: sorted by the first letter only | P1 233, P3 168, P4 1118, P6 233 |
| M12 | suffix: the shortest neighbour prefix taken | P1 1711, P4 1902, P5 410, P6 1711 |
| M13 | suffix: the starts left in text order | P1 814, P4 1576, P6 814 |
| M14 | solution: the second end read one letter early | P1 1576, P2 1576, P6 1576 |
| M15 | solution: the best read off the run before | P1 1757, P4 1657, P6 1757 |

P1 and P6 kill all fifteen, P4 seven, P2 and P3 five each, and P5 three.
P2 sees an answer no repeat backs (M4, M6, M9, M10, M14). P4 sees an
answer below the string's length on the string written twice, which every
edit that loses the longest repeats does (M1, M2, M7, M11 to M13, M15).
P5 sees a search that stops short or skips a length (M7, M8), and the
shortest neighbour prefix (M12). Two edits are caught only by the literal
reading and the vote: M3 and M5 both refuse an overlapping repeat, which
no other property asks about.

Of the fifteen not kept, four edits that never count the last window or
the last position (set, Z, suffix, solution) fail alike, and the suffix
arm leaving out the whole string fails as M2. The DP and solution arms'
edits pairing a start with itself fail alike, as do their edits extending
the run from the wrong cell. The other six each fail in a way of their
own.

## Verification

Every arm prints the same output as `lrs.py` under `karac __mir-run` (the
v2 MIR interpreter), `karac __mir-llvm-run`, and `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer) with no error. `karac run` and a
`karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any file.
Under `karac __mir-run` the arms take 0.6 s (set) to 26.6 s (Z-function)
and the differential 12.8 s.

Two of the Kāra arms met a gap, each fixed in the compiler rather than
written around (kara `acf4607cbd`, `tests/kata_1062_check_gaps.rs`):

- The ★ arm's `s[other..other + len]`, with `other` read from
  `starts.iter()`, was refused: the range's start was the `ref i64` and
  its end the `i64` that `+` read through it, two different types. A
  range bound that borrows an integer now reads it, as an operator's
  operand does.
- The suffix arm's `b[x..].cmp(b[y..])` had no method to call: a `Slice`
  is ordered lexicographically (collections.md), and `<` on two slices
  already compared them that way, but `Slice` had no `cmp`. It has one
  now, lowered through the same comparator.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` in three rounds: the syntax (`struct
Solution {}`, `max`, `Solution.`), then `as_bytes`, the outer `vec!` and
the `as i64` the return no longer needs, then the inner `vec!`. One error has no fix: Rust infers
`let mut best = 0` as `i32` from the return, and Kāra types the literal
`i64` on the spot, so returning it as `i32` narrows. design.md § Type
inference says a literal defaults last, after every use has had its
chance to fix it; that is kara B-2026-11-07-3 (open), and until it is
fixed the arm writes `let mut best: i32 = 0`.

## Benchmarks

The bench builds 60 strings of 20000 letters, over 2 to 26 of them, once
in all five languages, then answers each with the ★ arm's binary search
and rolling hash: about fifteen passes per string, each 20000 map
lookups. Rust uses `HashMap<i64, Vec<usize>>`, Go `map[int64][]int`,
Python a `dict` of lists, and C an open-addressed table whose slots keep a
chain of starts. Every implementation prints `60 calls: answers sum 554,
checksum 668545290`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `acf4607cbd` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.190 to 0.234 s | 0.210 s |
| Kāra (`karac build`) | 1.192 to 1.425 s | 1.233 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.253 to 1.451 s | 1.350 s |
| Rust (`rustc -O`) | 1.356 to 1.717 s | 1.446 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.380 to 1.645 s | 1.519 s |
| Go | 2.145 to 2.510 s | 2.253 s |
| Python | 6.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.215 s) is below its real time.

Kāra is 0.89x Rust under overflow checks. Both spend most of the time in
a SipHash map of growable vectors, one vector allocated for each new
hash. C's table is the same algorithm without either cost: a
multiplicative hash into a flat array and a chain of starts threaded
through one more array, allocated once per string, which is most of its
lead (inferred from the shapes, not measured).
