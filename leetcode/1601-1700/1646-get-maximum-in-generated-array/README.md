# 1646. Get Maximum in Generated Array

You are given an integer `n`. A **0-indexed** integer array `nums` of
length `n + 1` is generated in the following way:

- `nums[0] = 0`
- `nums[1] = 1`
- `nums[2 * i] = nums[i]` when `2 <= 2 * i <= n`
- `nums[2 * i + 1] = nums[i] + nums[i + 1]` when `2 <= 2 * i + 1 <= n`

*Return **the maximum** integer in the array* `nums`.

```
n = 7  ->  3
n = 2  ->  1
n = 3  ->  2
```

**Constraints:** `0 <= n <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `generated.kara` ★ | the array built as the statement does, each entry from the ones at half its index, keeping the largest seen. O(n) |
| `generated_fusc.kara` | the array is Stern's diatomic sequence, and any one entry follows from the bits of its index alone (Dijkstra's fusc); the largest over `0..=n` by an iterator `max`. O(n log n) |
| `generated_recursive.kara` | the two rules read as a recursion on the index, each entry worked out afresh with no array. O(n log n) |
| `generated_solution.kara` | LeetCode's Rust template: the array in a `vec![0; n + 1]`, then `*nums.iter().max().unwrap()`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally on every n it allows, five properties |

Every arm prints the same 10 lines: LeetCode's three examples, `n = 0`,
`n = 1` and `n = 100` (21), the answer for every n from 0 to 100 on one
line, and the maxima summed and a checksum for 3000 random n.
`generated.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the array filled for i counting up, `nums[2 * i]` and
`nums[2 * i + 1]` each set when its index lies in `2..=n`, as the
statement writes them, rather than each entry from the ones at half its
index as the arms do. It checks every n LeetCode allows, 0 to 100, so
the whole input space.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer never falls as n grows by one |
| P3 | for n of L bits the answer lies between the Fibonacci numbers `F(L)` and `F(L + 1)` |
| P4 | an even n gives the same answer as `n - 1` |
| P5 | each arm agrees with at least two of the other three |

P3 holds because the entries from `2^(L-1)` to `2^L` peak at `F(L + 1)`,
and those before peak at `F(L)`. P4 holds because an even entry repeats
the one at half its index, which is already counted.

The differential prints `101 problems: checksum 119976594, 2020 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The ★ arm starting its maximum at 0
(M2) and the recursive arm's `entry(0)` returning 1 (M6) fail on `n = 1`
and `n = 0` alone, which is why the differential takes every n rather
than a random few.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an odd entry from the entries at half its index and one before | P1 98, P3 57, P5 98 |
| M2 | ★: the maximum starts at 0 | P1 1, P3 1, P4 1, P5 1 |
| M3 | ★: the last entry never built | P1 14, P4 14, P5 14 |
| M4 | fusc: the two running values swap roles | P1 96, P3 17, P4 10, P5 96 |
| M5 | fusc: the running values start as `(0, 1)` | P1 15, P4 14, P5 15 |
| M6 | recursive: `entry(0)` is 1 | P1 1, P5 1 |
| M7 | recursive: an odd entry from the entry at half its index twice | P1 84, P3 72, P5 84 |
| M8 | template: `nums[1]` left 0 | P1 100, P3 100, P5 100 |
| M9 | template: the two rules swapped | P1 81, P4 12, P5 81 |
| M10 | template: the last entry returned, not the largest | P1 78, P2 49, P3 47, P4 49, P5 78 |

## Benchmarks

The bench draws 4000000 random n from 0 to 100, all of them first, then
answers each by the ★ arm in all five languages, the array allocated per
call in each. Every implementation prints `4000000 random n up to 100:
maxima sum to 48199784, checksum 16921775`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.453 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.495 s |
| Kāra (`karac build`) | 0.506 s |
| Rust (`rustc -O`) | 0.582 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.649 s |
| Go | 0.734 s |
| Python | 20 s |

The sequential Kāra build is 15% faster than Rust and 24% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C is the fastest here at 0.453 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.486 s and
0.498 s on one run).

## Verification

All four arms print the same output as `generated.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The ★ arm filled its array with `Vec.filled(n + 1, 0)` and returned its
`best` as the `i32` the signature asks for; both took the default `i64`,
and `karac fix` made them `0i32` and `best: i32`. The fusc and recursive
arms checked clean as first written.

LeetCode's Rust template takes one `karac fix` of 4 edits: `struct
Solution;` to `struct Solution {}`, `n as usize` to `n as i64`, and
`vec![0; n + 1]` to `Vec.filled(n + 1, 0i32)`. The arm then checks
and agrees with no hand edit.
