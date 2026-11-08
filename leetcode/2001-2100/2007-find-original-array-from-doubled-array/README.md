# 2007. Find Original Array From Doubled Array

An integer array `original` is turned into a doubled array `changed` by
appending twice the value of every element of `original`, then shuffling
the result. Given `changed`, return `original` if `changed` is a doubled
array, and an empty array otherwise. The elements of `original` may be
returned in any order.

```
changed = [1,3,4,2,6,8]  ->  [1,3,4]
changed = [6,3,0,1]      ->  []
changed = [1]            ->  []
```

**Constraints:** `1 <= changed.length <= 10^5`; `0 <= changed[i] <= 10^5`.

Any order of `original` is an answer, so every arm's answer is shown, and
compared, sorted. Zero is its own double: an even number of zeros pairs
among themselves.

## Approaches

| file | mechanism |
|---|---|
| `doubled.kara` ★ | a count of each value in a `Vec`, walked upward: the smallest value left cannot be anyone's double, so every copy of `v` takes a copy of `2v` at once; zeros pair among themselves. O(n + max) |
| `doubled_queue.kara` | sorted; each value either settles the oldest double still owed or is an original that now owes its double, the doubles owed in a `VecDeque` whose front is the only one ever due. O(n log n) |
| `doubled_map.kara` | the values counted in a `SortedMap`, walked from the smallest: each key's remaining copies take as many copies of twice the key. O(n log n) |
| `doubled_pointers.kara` | sorted; the first value not yet used is an original, and a second pointer that only moves forward finds the first unused copy of its double and marks it. O(n log n) |
| `doubled_halves.kara` | from the other end: the largest value left is a double, and its half, counted in a `Map`, must be there to take it; walked with `iter().rev()`. O(n log n) |
| `doubled_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<i32>`, a `HashMap` of counts, `for &x in &changed`, `vec![]`), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for 3000
doubled arrays of 2 to 16 values up to 11, one in three with a value
nudged, and for 6 arrays of 40000 values up to 3, 100 or 50000.
`doubled.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to choose half the values, kept when their doubles
are exactly the other half. It checks 1500 problems of up to 5 pairs of
values up to 10, a quarter of them with a value nudged and a quarter with a
stray value appended. Every random choice of a problem (the values, a
shuffle, a pair to append) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values shuffled leave the answer |
| P3 | every value tripled triples the answer |
| P4 | a non-empty answer, with each value's double added, is the input |
| P5 | a pair `(x, 2x)` appended to an input that has an answer adds `x` to it |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 problems: checksum 278879069, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every zero an original | P1 307, P4 307, P5 164, P6 307 |
| M2 | ★: the walk starting at 2 | P1 267, P3 267, P5 42, P6 267 |
| M3 | ★: each value counted once | P1 479, P4 90, P5 150, P6 479 |
| M4 | queue: the newest double settled | P1 189, P5 85, P6 189 |
| M5 | queue: the values never sorted | P1 442, P2 133, P6 442 |
| M6 | map: an even count of zeros refused | P1 347, P4 40, P5 53, P6 347 |
| M7 | map: a single copy skipped | P1 668, P4 404, P5 318, P6 668 |
| M8 | pointers: a used double found again | P1 213, P4 30, P5 123, P6 213 |
| M9 | pointers: the double looked for one short | P1 619, P3 2, P4 2, P5 2, P6 619 |
| M10 | halves: an odd value's half taken | P1 235, P3 235, P4 235, P6 235 |
| M11 | halves: the double never used up | P1 402, P4 253, P5 209, P6 402 |
| M12 | halves: a used-up value walked again | P1 617, P4 76, P5 20, P6 617 |
| M13 | Rust: the values never sorted | P1 399, P2 162, P5 43, P6 399 |
| M14 | Rust: the value never used up | P1 397, P4 248, P5 205, P6 397 |
| M15 | Rust: a missing double allowed | P1 252, P4 252, P5 67, P6 252 |

P1 and P6 kill all fifteen, P5 thirteen, P4 eleven, P3 three and P2 two.
P5 misses the queue arm left unsorted and the halves arm halving an odd
value (M5, M10). P4 rebuilds the input from a non-empty answer, so it sees
every edit that returns a wrong original, and misses the four whose wrong
answers here are all empty (M2, M4, M5, M13). P3 sees the edits that treat
a value by its size or its parity, which tripling changes: the walk
skipping 1 (M2), an odd value halved (M10), and a double looked for one
short (M9, which P3, P4 and P5 each see only twice). P2 sees only the
edits that read the input in its given order: the two arms that sort, left
unsorted (M5, M13).

The other fifteen fail as a kept one does, or with counts of their own
that add nothing. Keeping the double rather than the original fails alike
in the queue, pointers and Rust arms (P1 541, P4 541, P5 453). The map arm
refusing exactly enough doubles, its doubles never used up, and the halves
arm walked from the smallest fail alike (P1 541, P5 20). The pointers arm
never marking a double used, the halves arm never using up a half and the
Rust arm never using up a double fail alike, on P1 and P6 alone. The queue
arm owing a double at the front fails as the newest double settled. The
★ arm taking one double for all the copies, its largest value never looked
at (9 problems in 1500: only an input whose largest value is an original
it pairs with nothing), the queue arm allowing one double left owing, the
map arm keeping one copy fewer and the pointers arm taking any value as the
double fail with counts of their own. Four drafts were replaced as
equivalent: the ★ arm refusing only a count of doubles of 0 rather than
fewer than needed (the walk upward has used every smaller copy already),
the ★ arm allowing a single zero (the length check refuses it first), the
map arm rounding an odd count of zeros up, and the map arm accepting one
copy of the double for many.

## Verification

Every arm prints the same output as `doubled.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any of
them. ARM_TIMES

The ★ arm found a backend gap. `let top = changed.iter().max().unwrap();`
is a `ref i64`, and `for v in 1..=top` reads it as its value (core
semantics §5.10), so the arm checked clean; but both backends refused to
build it ("scalar constant of a non-scalar type"), because MIR typed the
loop's counter as the reference. The counter is now the integer (kara
cdb6382000, `tests/kata_2007_check_gaps.rs`). The queue arm compared
`owed.front() == Some(x)`, an `Option[ref i64]` against an `Option[i64]`;
`karac fix` adds the `.cloned()`. The map, pointers and halves arms checked
clean as written.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (24, 2, 3 and 1 edits).
The first round carries the `use`, the struct, the `Vec<..>` and
`HashMap<..>` types, `vec![]`, the `&` patterns and borrows and the `::`
paths, and turns `sort_unstable` into `sort`. The last round settles
Rust's `let mut changed = changed;`, how Rust changes an owned argument:
a bare Kāra parameter borrows, so `changed.sort()` cannot write it. The
fix declared the parameter `mut ref`, which changes the caller's value and
needs `mut` at each call; that version checked clean but printed wrong
answers, through a second gap: a `mut` argument that is a temporary,
`f(mut xs.iter().map(..).collect())`, is passed as if it were already a
reference, so `__mir-llvm-run` read a wrong length and `__mir-run`
stopped ("deref of non-reference Box"). That is B-2026-11-08-43. The fix now
declares the parameter `own`, which keeps Rust's meaning, and the arm runs
(kara bdd59137e1, `tests/kata_2007_check_gaps.rs`).

## Benchmarks

The bench builds 2000 doubled arrays of 1000 values up to 10000 once in
all five languages, one in three with a value nudged, and runs the ★ arm
on each for 25 rounds: 50000 calls, each counting into a `Vec` as long as
the largest value and walking it. The answer's length and values are
summed. Every implementation prints `50000 calls: sum 39153046825, checksum
631609953`. Every language allocates the counts and the answer per call,
as the Kāra program does; the C mirror grows the answer by doubling.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.710 to 0.807 s | 0.747 s |
| Kāra (`karac build`) | 0.768 to 0.870 s | 0.783 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.757 to 0.892 s | 0.809 s |
| Rust (`rustc -O`) | 1.072 to 1.158 s | 1.074 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.089 to 1.139 s | 1.121 s |
| Go | 1.129 to 1.214 s | 1.161 s |
| Python | 18.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.767 s) is not above its real time (0.783 s).

The sequential Kāra program is 0.72x Rust under overflow checks and 1.08x
C.