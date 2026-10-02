# 325. Maximum Size Subarray Sum Equals k

Given an integer array `nums` and an integer `k`, return the length of the
longest contiguous subarray whose sum is exactly `k`, or `0` if there is
none. `1 <= n <= 2 * 10^5`, values in `-10^4..10^4`, `k` in `-10^9..10^9`.

```
nums = [1, -1, 5, -2, 3], k = 3  ->  4    ([1, -1, 5, -2])
nums = [-2, -1, 2, 1],    k = 1  ->  2    ([-1, 2])
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `max_sub_len.kara` ★ | prefix sums, `Map` of each sum's first index: `get`, then `entry(p).or_insert(i)` | expected `O(n)` time, `O(n)` space |
| `max_sub_len_contains.kara` | the same, spelled `contains_key` / index / `insert` | expected `O(n)` time, `O(n)` space |
| `max_sub_len_sorted.kara` | the same over a `SortedMap`: `if let` lookup, insert-then-restore | `O(n log n)` time, `O(n)` space |
| `max_sub_len_brute.kara` | every start, every end, running sum | `O(n^2)` time, `O(1)` space |
| `differential.kara` | the four arms, a span-returning fifth, eight properties | — |
| `bench/max_sub_len.kara` | 60 re-scans of 200,000-value arrays by the ★ arm | — |

Every arm prints the same 27 lines: the two examples, nine edge cases, four
small random inputs, and four `k` values on each of three larger inputs (500,
2,000 and 3,000 values, small enough for the quadratic arm). The four arms'
output is byte-identical, and `max_sub_len.py` mirrors both the ★ arm and,
with `--brute`, the quadratic one.

## The first index, never the last

Let `p(i)` be the sum of the first `i` values. The subarray `nums[j..i]` sums
to `p(i) - p(j)`, so a subarray ending at `i` sums to `k` exactly when some
earlier prefix equals `p(i) - k`, and the LONGEST one starts right after the
EARLIEST such prefix. The map therefore records each prefix sum the first
time it appears and never overwrites it. The empty prefix (sum `0`, at index
`-1`) is seeded so that a subarray starting at index 0 is found.

Both details are load-bearing, and the edge cases pin each one:

- `[1, -1, 1, -1, 1, -1], k = 0` is `6`. The prefix sums alternate `1, 0, 1,
  0, ...`, so every sum repeats; overwriting with the latest index gives `2`.
- `[5], k = 5` is `1`, and `[1, 2, 3], k = 6` is `3`. Both answers start at
  index 0 and are only found through the seeded empty prefix.

The three map arms differ only in how they spell the two map steps. The ★ arm
uses `get` and `entry(p).or_insert(i)`, which is one hash per step. The
`contains_key` arm tests, then indexes or inserts, which costs a third hash
per element. The `SortedMap` arm reads with `if let Some(j) = first.get(..)`
and keeps the first index by putting back whatever `insert` returned, so it
also exercises `Option` of a map value on the ordered map.

## Differential

`differential.kara` runs all four arms on the same inputs, and adds `span`,
which returns WHERE the longest subarray is, as `Option[(start, len)]`, so
an answer can be checked against the input rather than only against another
arm. Six edge cases (including the empty array) are followed by 1,000 random
rounds of 0 to 39 values within ±1 to ±6, with `k` drawn near zero so that
most rounds find something.

| | property |
|---|---|
| P1 | all four lengths agree |
| P2 | `0 <= length <= n` |
| P3 | `span` agrees with the length, and is `None` exactly when it is 0 |
| P4 | the values `span` points at really sum to `k` |
| P5 | reversing the input does not change the length |
| P6 | negating every value and `k` does not change the length |
| P7 | `k` = the whole array's sum gives length `n` |
| P8 | appending a `0` never shortens the answer |

`rounds 1006, found 824, longest 39`, and all properties hold, on every
surface.

## Mutation testing

Six edits to the ★ arm's copy inside `differential.kara`, each built and run.

| # | mutation | outcome | first properties to fire |
|---|---|---|---|
| M1 | overwrite: `insert(p, i)` instead of `entry(p).or_insert(i)` | **killed** | P1, P3 |
| M2 | no seeded empty prefix | **killed** | P1, P3 |
| M3 | length off by one, `i - j + 1` | **killed** | P1, P2 |
| M4 | look up `p + k` instead of `p - k` | **killed** | P1, P3 |
| M5 | `>=` instead of `>` when keeping the best | silent (equivalent) | — |
| M6 | seed the empty prefix at index `0` instead of `-1` | **killed** | P1, P3 |

M5 is equivalent: on a tie it stores the same length it already had. P3 and
P4 do not depend on the other arms, so a mutation shared by every arm would
still be caught there.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`. `scripts/surface-sweep.py --filter
325- --timeout 400` reports `5 programs · 5 clean · 0 DIVERGENCES`. All five programs
are valgrind-clean at `-O0`. The four arms' output is byte-identical to
`max_sub_len.py` and `max_sub_len.py --brute`.

None of these programs observes a `Map`'s iteration order: the maps are only
looked up, never walked, so the output does not depend on the per-process
hash seed.

The benchmark kernel's sink matches all four language twins and Python
(`sink 343512294`), and `karac run --interp` prints the same sink.

## Benchmarks

`bench/max_sub_len.kara` and its four mirrors time the ★ arm as written: a
fresh map per call, a lookup, and a first-occurrence insert. Three arrays of
200,000 values are built once, with values within ±1, ±100 and ±10,000. The
range decides how many distinct prefix sums a scan meets, and so how big the
map grows: a few hundred keys, tens of thousands, or nearly one per element.
Each of 60 punches takes the next array in turn, changes one value at a
random position, draws a `k` near zero scaled to the range, and re-runs the
whole scan. Every length is folded into a rolling hash, which is the sink.

The mirrors use each language's own map, which makes this a comparison of
hash tables as much as of compilers:

- **Rust** `HashMap`: SipHash-1-3 under a random key, the same hash Kāra's
  default `Map` uses, over hashbrown's grouped table.
- **C** has no standard map, so `max_sub_len.c` carries one shaped like the
  Kāra runtime's: linear probing, 75% load, doubling, SipHash-1-3 over the
  key (checked against Rust's SipHash-2-4 with the round counts swapped).
- **Go** uses its built-in map and its own hash, and **Python** its dict.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container, karac
`0.1.0-dev.10181+gf2907d370`, measured 2026-10-02. Python is its own lane at
3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| rust `-O -C overflow-checks=on` (equal-safety) | 520.6 ms ± 14.3 | 1.00× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 523.9 ms ± 13.0 | 1.01× |
| rust `-O` | 524.2 ms ± 18.7 | 1.01× |
| go `go build` | 662.0 ms ± 16.6 | 1.27× |
| c `clang -O3` | 802.2 ms ± 14.6 | 1.54× |
| c `-march=x86-64-v3` (matched-ISA) | 816.9 ms ± 21.7 | 1.57× |
| **kāra `karac build`** | **857.5 ms ± 23.6** | **1.65×** |
| python 3 | 2110 ms ± 47 | 4.05× |

**Kāra is 1.65× behind Rust, and within 7% of a C table of its own design.**
Both run SipHash-1-3, so the hash function is not the difference; the C
row, which hashes the same way into the same kind of table, lands next to
Kāra. That points at the table, not at the code the compiler emits around
it. Filed as
[`B-2026-10-02-39`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)
(perf, low) with a profile: 46% of Kāra's instructions are in the hash
itself (93 per call, not inlinable because the hasher is chosen when the map
is constructed), and resizing costs twice hashbrown's instruction count. Python is
unusually close because nearly all of its time is in the dict, which is C.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 129.8 ms ± 2.1 | 15.8 KiB | 21.9 MiB |
| rust | 204.1 ms ± 2.7 | 3887.3 KiB | 14.8 MiB |
| kāra | 352.1 ms ± 13.4 | 353.9 KiB | 19.9 MiB |
| go | — | 2179.1 KiB | 21.7 MiB |
| python | — | — | 53.3 MiB |

Rust's peak RSS is the smallest. hashbrown's higher load factor (7/8
against 3/4) would give its largest table fewer buckets, which is the likely
reason, but that was not measured. `karac build` is 2.7× clang's cold compile and 1.7×
rustc's. Its binary is 22× clang's and 11× smaller than rustc's. Raw numbers
are in `bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**No correctness gaps.** All five programs were byte-identical on every
surface from the first run.

- **[`B-2026-10-02-39`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) (perf, low, open): Kāra's `Map` is 1.65× Rust's
  `HashMap` on this growth-heavy workload**, at equal hashing, while a C
  table of the runtime's design is within 7% of Kāra. A monomorphized
  `entry(k).or_insert(v)` was prototyped (the claim currently takes the
  runtime's type-erased path) and ran 6% SLOWER, because the runtime's path
  already uses a grouped scan that the inline byte walk loses to on branch
  mispredicts. The row records the profile and the question for whoever owns
  `Map` performance.

`karac check` reported no diagnostics on any file, so the Mend loop had
nothing to apply. That says little about the diagnostics: the author already
knows the language, which is why authoring like this never counts toward the
machine-fix rate.
