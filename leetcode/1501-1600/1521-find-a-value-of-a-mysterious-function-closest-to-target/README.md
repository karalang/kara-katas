# 1521. Find a Value of a Mysterious Function Closest to Target

Winston has a function `func(arr, l, r)` that returns the bitwise AND of
`arr[l..=r]`. Given an integer array `arr` and an integer `target`, return
the minimum possible value of `|func(arr, l, r) - target|` over all
`0 <= l, r < arr.length` with `l <= r`.

```
arr = [9,12,3,7,15],          target = 5  ->  2
arr = [1000000,1000000,1000000], target = 1  ->  999999
arr = [1,2,4,8,16],           target = 0  ->  0
```

**Constraints:** `1 <= arr.length <= 10^5`; `1 <= arr[i] <= 10^6`;
`0 <= target <= 10^7`.

## Approaches

| file | mechanism |
|---|---|
| `closest.kara` ★ | the ANDs of every range ending at `r` are those ending at `r - 1`, each ANDed with `arr[r]`, and `arr[r]` itself. A bit can only be lost, so there are at most 21 distinct values, kept in order without repeats. O(n log max) |
| `closest_sparse.kara` | a sparse table of ANDs over power-of-two ranges answers any range in two lookups. The AND from `l` never grows as `r` moves right, so a binary search from each `l` finds the last range still at least the target; it and the next are the only candidates. O(n log n) |
| `closest_bits.kara` | walking `l` from the right, each bit keeps the nearest place at or after `l` where it is 0. Those places, sorted, are every place the AND from `l` changes. O(21 n log 21) |
| `closest_iter.kara` | the ★ arm with iterator adapters: `scan` carries the list of ANDs, `map` and `dedup` build the next one, `flat_map` and `min` take the distance |
| `closest_solution.kara` | LeetCode's Rust template (`Vec<i32>`, `i32::MAX`, `for &x in`, `vec![x]`, `*next.last().unwrap()`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's three examples, a single
number far below the target, then checksums of the answers for 3000
random arrays of 1 to 12 numbers and 20 of 1 to 20000. Half the numbers
are a shared base with random bits cleared, so ANDs fall slowly, and half
the targets sit next to a number in the array. `closest.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the AND of every range `l..=r`, computed from scratch, and the
least distance. It checks 3000 arrays of 1 to 10 numbers from 1 to 31,
with targets from 0 to 40, every random choice drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the array reversed has the same answer |
| P3 | every number and the target doubled double the answer |
| P4 | the answer is at least 0 and at most each number's own distance |
| P5 | 2^21 - 1 appended changes the answer only to that number's own distance, when it is closer |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 692525420, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Nine are killed, each the
same way under both backends; six survive, and all six are equivalent.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a range's AND not extended by the new number | P1 415, P6 415 |
| M3 | ★: only the single number carried to the next place | P1 67, P6 67 |
| M5 | sparse: the first range below the target not a candidate | P1 1074, P2 1072, P4 1008, P6 1074 |
| M8 | bits: only the low 4 bits tracked | P1 53, P2 88, P3 74, P6 53 |
| M9 | bits: the places the AND changes not sorted | P1 91, P2 132, P6 91 |
| M11 | iter: only the single number carried | P1 67, P6 67 |
| M12 | iter: `max` for `min` | P1 2674, P4 2674, P5 3000, P6 2674 |
| M13 | template: `ans.max` for `ans.min` | P1, P3, P4, P5, P6 3000 each |
| M15 | template: `ends = next` dropped | P1 415, P6 415 |

The survivors: the ★ arm pushing repeats (M1), the iterator arm without
`dedup` (M10), and the template comparing with the list's first value
rather than its last (M14), since a repeated value never changes the
least distance; `>` for `>=` in the sparse arm's search (M4), since a
range equal to the target is then the next candidate instead and still
scores 0; `<` for `<=` in the sparse arm's level choice (M6), since a
range of exactly `2^(k+1)` is then covered by two halves of `2^k`; and
the bits arm counting `l` itself as a change (M7), since `arr[l] & arr[l]`
is `arr[l]`.

One first draft of M11, `Some((Vec.new(), next))`, did not check: a
closure returning `Some((Vec.new(), x))` to a generic `Fn(S) ->
Option[(S, O)]` leaves `O` uninferred. That is kara `B-2026-11-08-58`.
A first draft of M13, `let mut ans = 0;`, was refused by design
(`B-2026-11-07-57`: a literal is not fixed by a method receiver).

## Benchmarks

The bench builds 2000 random arrays of 1 to 4000 numbers below 10^6 once
and answers each 3 times by the ★ arm, in all five languages. Each place's
list of ANDs is a fresh allocation, as the arm writes it (`malloc` and
`free` in C). Every implementation prints `3 passes over 2000 arrays of up
to 4000 numbers: distances sum to 10022793, checksum 230450745`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `218952d3b` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.309 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.532 s |
| Kāra (`karac build`) | 0.537 s |
| Rust (`rustc -O`) | 0.543 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.595 s |
| Go | 0.836 s |
| Python | 6.10 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.51 s and 0.54 s on one run).

Kāra is 0.89x Rust under overflow checks by median. C is ahead of all of
them because it allocates each list at its final size: Kāra, Rust and Go
start it at one element and grow it as values are pushed. Rust built with
`Vec::with_capacity(ends.len() + 1)` instead ran in about 0.34 s (five
runs, not committed), so most of the gap is the regrowth.

## Verification

All five arms print the same output as `closest.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The ★, sparse and bits arms were written in Kāra and `karac fix` had
nothing to change. The iterator arm's first draft wrote Rust's `scan`,
with the state as `mut ref` and only the output returned; Kāra's `scan`
takes the state by value and returns it with the output, and the closure
was rewritten by hand to that shape.

The Rust template took 11 edits and 1 edit over two rounds: `Vec<..>` to
`Vec[..]`, `::` paths to `.`, the `&` before each `for` pattern dropped,
then `vec![x]` to `[x]`. It checks and agrees with no hand edit.
