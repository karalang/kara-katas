# 1151. Minimum Swaps to Group All 1's Together

Given a binary array `data`, return the minimum number of swaps required
to group all `1`'s present in the array together in **any place** in the
array.

```
data = [1,0,1,0,1]              ->  1
data = [0,0,0,1,0]              ->  0
data = [1,0,1,0,1,0,0,1,1,0,1]  ->  3
```

**Constraints:** `1 <= data.length <= 10^5`; `data[i]` is either `0` or
`1`.

The arms are `fn min_swaps(data: Vec[i64]) -> i64`.

## Approaches

The ones end up filling some window as long as their count `k`. A swap
can bring one outside one into the window for one zero inside it, so a
window costs as many swaps as it holds zeros, and the answer is `k` less
the most ones any window of length `k` already holds.

| file | mechanism |
|---|---|
| `min_swaps.kara` ★ | a sliding window of length `k`, gaining a bit on the right and losing one on the left, the most ones kept. O(n) |
| `min_swaps_prefix.kara` | prefix sums built with `scan`, each window's ones read as a difference of two of them, the most kept with `max`. O(n) |
| `min_swaps_positions.kara` | over the places of the ones: a best window can start at a one, and a second pointer counts the ones within `k` places of each. O(n) |
| `min_swaps_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `data: Vec<i32>`, the ones counted with `sum`, the first window summed from `data[..k]` and slid in `usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 15 lines: LeetCode's three examples; one zero
(0) and one one (0); three ones (0); ones at both ends of
`[1, 0, 0, 0, 1]` (1) and `[1, 1, 0, 0, 1, 1]` (2); and
`[0, 1, 0, 1, 1, 0, 1, 0]` (1). Then 2000 random lists of 1 to 60 bits,
each bit 1 with a chance of 0 to 8 in 8 drawn per list, the answers summed
and a checksum (`2000 random lists: swaps total 6413, checksum
279054312`), and five lists at the constraints' end: 100,000 bits
alternating 1 and 0 (25000), all ones (0), 25,000 ones at each end
(25000), all zeros (0), and random bits 3 in 8 ones (23390).
`min_swaps.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a swap exchanges any two bits, and a breadth-first search over
the arrangements of the list finds the fewest swaps that leave the ones
together. It checks 2000 lists of 1 to 10 bits in four kinds of 500: each
bit 1 with chance 4 in 8 and 6 in 8; runs of ones and zeros of 1 to 3
bits; and a run of 1 to 4 ones at each end with zeros between, one bit
then flipped in half of them, so that the ones lie far apart. P3's end is
drawn before any arm answers. The answers run from 0 to 3: 778 lists need
no swap, 919 one, 292 two and 11 three.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the list reversed gives the same answer |
| P3 | a zero at one end gives the same answer |
| P4 | every bit twice gives twice the answer |
| P5 | the answer is 0 exactly when the ones are already one run |
| P6 | the answer is at most the number of zeros, and at most the ones outside the longest run of ones |

P4 holds because a window of length `2k` in the doubled list holds twice
the ones of a window of the list when it starts at an even place, and the
ones of two neighbouring windows when it starts at an odd one. All 48,000
checks pass on every arm: `2000 lists: checksum 916507137, 48000 checks
over 4 arms: 0 failures`. A Python reading of the same lists, by the same
search, with the six properties asserted against the ★ arm's mirror,
gives the same line.

## Mutation testing

Twenty-eight edits to the differential, seven to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-seven are caught; one is
equivalent: the positions arm restarting its second pointer at each one,
which only repeats the counting the pointer had already done. Twenty-two
are kept, no two failing the same checks; one of them stops the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first window one bit short | P1 1130, P2 689, P3 423, P4 1130, P5 511, P6 917 |
| M2 | ★: the last window never reached | P1 295, P2 647, P3 270, P4 295, P5 132, P6 232 |
| M3 | ★: the window loses the bit after its first | P1 702, P2 967, P3 556, P4 702, P5 477, P6 241 |
| M4 | ★: the first window never counted | P1 603, P2 647, P3 379, P4 352, P5 415, P6 532 |
| M5 | ★: the last window wins | P1 669, P2 978, P3 555, P5 273, P6 537 |
| M6 | ★: the window never loses a bit | P1 1222, P5 1222 |
| M7 | ★: the second window skipped | P1 478, P2 649, P3 615, P4 478, P5 272, P6 235 |
| M8 | prefix: each sum before its bit, not after | P1 410, P2 548, P3 194, P4 410, P5 271 |
| M9 | prefix: the window's first bit dropped | stops: index out of bounds |
| M10 | prefix: no window counted as all ones | P1 778, P4 778, P5 778, P6 778 |
| M11 | prefix: the last bit left out of the count | P1 615, P2 278, P3 299, P4 615, P5 412 |
| M12 | prefix: the fewest ones kept | P1 1228, P3 754, P5 405, P6 1008 |
| M13 | prefix: windows at odd starts skipped | P1 254, P2 432, P3 475, P4 254, P5 176, P6 208 |
| M14 | positions: the window one bit longer | P1 634, P4 634, P5 434 |
| M15 | positions: the window one bit shorter | P1 1076, P4 1076, P5 656, P6 815 |
| M16 | positions: the starting one not counted | P1 1878, P4 1878, P5 656, P6 1564 |
| M17 | positions: no window starts at the last one | P1 256, P4 256, P5 256, P6 256 |
| M18 | positions: a one at the front ignored | P1 386, P2 548, P3 180, P4 386, P5 236 |
| M19 | positions: the last start wins | P1 1469, P4 1878, P5 400, P6 1422 |
| M20 | solution: the first window without its first bit | P1 1361, P2 697, P3 671, P4 1361, P5 415, P6 1133 |
| M21 | solution: the window loses the bit before the new one | P1 737, P2 952, P3 485, P4 748, P5 386, P6 275 |
| M22 | solution: the last `k` windows never reached | P1 482, P2 928, P3 515, P5 178, P6 366 |

P1 and P5 catch all twenty-six edits that let the run finish: the lists
already in one run are 778 of the 2000, and nearly every edit miscounts
some of them. P6 catches twenty; the five kept edits it misses (M6, M8,
M11, M14, M18) answer wrongly within both of its bounds. P4 catches
nineteen; it misses M5, M6, M12 and M22 and their three duplicates.
P2 catches sixteen, the edits that treat the front and the back unlike;
the edits that change every window alike (M6, M10, M12, M14 to M17, M19)
answer the reversed list the same. P3 catches eighteen. It misses M6,
M10 and every edit to the positions arm but M18: that arm reads only the
places of the ones relative to each other, which a zero at either end
does not move, so its edits answer the padded list as wrongly as the
list. The edit that stops the run reads `before[i + 1]` at the last
window, one past the sums when the list has no ones.

Of the five caught and not kept, each fails exactly as a kept one: the
solution arm never reaching the last window, as M2; keeping the fewest
ones, as M12; answering the last window's count, as M5; skipping the
second window, as M7; and the prefix arm keeping the bits rather than
their sums, as M6.

Two edits first written for the prefix and solution arms did not
typecheck and were replaced. The solution arm's `let mut best = 0;`
against an `i32` window is refused because the literal keeps the default
`i64`, as design.md §8 says, and `karac fix` writes the `best: i32` that
makes it run. The other was a gap: a `scan` closure whose next state is
not computed from the state while its item is, `scan(0, |prev, x|
Some((*x, (prev, *x))))` among them, was refused with two types that
unify, "expected 'Option[(i64, _)]', found 'Option[(i64, (i64, i64))]'".
A number met in the state's slot now fixes the state's literal
(B-2026-11-13-35, fixed).

## Verification

Every arm prints the same output as `min_swaps.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The ★ and positions arms were written as Kāra and checked clean as
written. The prefix arm was written with Rust's `scan`, which writes the
state in place (`*sum += x; Some(*sum)`); `karac fix` rewrote it to
Kāra's, which takes the state by value and returns `Some((next, item))`,
on one line, and the line is laid out here as `karac fmt` lays it out.
`karac fix` carried the solution arm in four rounds: `Vec<i32>` to
`Vec[i32]`, the adapter's `&Vec<i64>` to `ref Vec[i64]`, `|&x|` to `|x|`
and `Solution::` to `Solution.`; then `struct Solution {}` declared; then
`ones as usize` to `ones as i64`, Kāra indexing with `i64`, and the
adapter's `as i64` dropped; then the adapter's `ref` dropped, a parameter
borrowing by default.

The kata found one gap, B-2026-11-13-35 (see Mutation testing).

## Benchmarks

`bench/` times the ★ arm against the same window in C, Rust, Go and
Python. 16 lists of 100,000 bits, LeetCode's longest, each bit 1 with a
chance of 1 to 7 in 8 by list, are built once; then each of 3000 rounds
flips 64 bits of one list, in turn, and answers it. Every program prints
`3000 rounds over 16 lists of 100000 bits: swaps total 58132285,
checksum 582025310`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `d59535f2bc`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.191 to 0.263 s | 0.222 s |
| C (`clang -O3`) | 0.246 to 0.324 s | 0.282 s |
| Rust (`rustc -O`) | 0.284 to 0.351 s | 0.313 s |
| Go | 0.348 to 0.468 s | 0.386 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.375 to 0.716 s | 0.423 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.383 to 0.539 s | 0.431 s |
| Kāra (`karac build`) | 0.391 to 0.565 s | 0.438 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.397 to 0.566 s | 0.470 s |
| Python | 17.8 s | |

The two Kāra builds are the same binary, so the gap between their
medians is the noise in these runs. Kāra ties overflow-checked Rust, the
equal-safety comparison: both check every `+` and `-` of the window for
overflow. C and unchecked Rust, which do not, lead by about a third.
