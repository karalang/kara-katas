# 456. 132 Pattern

Given an array of `n` integers `nums`, a 132 pattern is a subsequence
of three integers `nums[i]`, `nums[j]` and `nums[k]` such that
`i < j < k` and `nums[i] < nums[k] < nums[j]`. Return `true` if there
is a 132 pattern in `nums`, otherwise `false`.

```
nums = [1,2,3,4]   ->  false
nums = [3,1,4,2]   ->  true    (1, 4, 2)
nums = [-1,3,2,0]  ->  true    (-1, 3, 2), (-1, 3, 0), (-1, 2, 0)
```

**Constraints:** `1 <= n <= 2 * 10^5`; `-10^9 <= nums[i] <= 10^9`.

## Approaches

Every arm is `fn find132pattern(nums: Vec[i64]) -> bool`. Below, the
"1", "3" and "2" are `nums[i]`, `nums[j]` and `nums[k]`.

| file | mechanism |
|---|---|
| `pattern132.kara` ★ | one stack, from the right: keep the candidates for the "3" decreasing toward the top, and `third`, the largest value popped so far; a value is popped only by a larger one to its left, so it is a "2" with a "3" before it, and the pattern is complete when a value below `third` turns up. O(n) |
| `pattern132_prefix.kara` | prefix minimums give the best "1" for each "3"; walk the "3" from the right with a stack of values to its right, smallest on top, dropping those no larger than the current "1". O(n) |
| `pattern132_ordered.kara` | the values to the right of the "3" in a `SortedMap` of counts; `ceiling` finds the smallest one above the best "1", which must be below the "3". O(n log n) |
| `pattern132_scan.kara` | the plain reference: for each "3", the smallest value before it as the "1", and a scan of everything after it for a "2". O(n²) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 11 lines: the three LeetCode examples, one
number, two numbers, a "2" equal to the "3", a "2" equal to the "1",
a pattern that skips over a lower number, the two extremes, a falling
array, and for 300 random arrays of 1 to 200 numbers (over 2, 5, 50 or
every value from -10^9 to 10^9; the first 100 sorted upward with up to
two swaps, so that the answer is not always true) how many have the
pattern and a checksum. `pattern132.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 8 numbers within 0 to 4, the answer is brute force's over every triple |
| P2 | on 1 to 60 numbers over a mixed spread (sorted with a few swaps in a third of the cases), scaling by 1 to 5 and adding a constant keeps the answer |
| P3 | with a number below all of them put first, the pattern exists exactly when some pair is out of order |
| P4 | a number no larger than the smallest put last keeps the answer |
| P5 | a "1", a "3" and a "2" planted in that order always give `true` |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a candidate equal to the new value is popped | P1 193, P3 171 |
| M2 | ★: a value equal to `third` counts as the "1" | P1 204, P4 93 |
| M3 | prefix: a "2" equal to the "1" is kept | P1 47 |
| M4 | prefix: a "3" at index 1 is never tried | P1 85, P3 21, P5 5 |
| M5 | ordered: a "2" equal to the "1" is accepted | P1 204, P4 93 |
| M6 | ordered: nothing leaves the right side | P1 204, P3 225 |
| M7 | scan: a "2" equal to the "1" is accepted | P1 204, P4 93 |
| M8 | scan: the "1" is only the number just before the "3" | P1 48, P3 210 |

P1, the only property with an independent answer, sees all eight. P2
sees none: every arm only compares numbers, and scaling and shifting
keep every comparison. M2, M5 and M7 fail the same checks because they
all find the weaker pattern `nums[i] <= nums[k] < nums[j]`; P4's last
number, equal to the smallest, is just such a "2". M3 is the faintest:
it matters only when a value equal to the "1" is on the stack, which
needs repeated numbers, and only P1's small range makes those common.

## Verification

All four arms print the same output as `pattern132.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends the ★, prefix and scan arms match under
`karac run --interp`. LLJIT and `karac build` stop in the legacy code
generator on the harness's index into an array literal ("Index operator
applied to non-array type"). The ordered arm and the differential do
not type-check on legacy: its `SortedMap.ceiling` hands out the key by
value, so `*two` is rejected. Legacy `karac build` also rejects the
bench program (see Benchmarks). Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It builds 10 arrays of 1,000,000
numbers with no 132 pattern once: runs of 1 to 1,000 rising numbers,
each run below the one before it. Each of 5 rounds, for every array,
sets one number to a random value half the time (which nearly always
makes a pattern), checks the array, and puts the number back; a check
without a pattern walks the whole array, and one with a pattern stops
just left of the changed number. Every implementation prints `5 rounds
on 10 arrays of 1000000: 21 with the pattern, checksum 877319596`, the
Kāra program under `karac __mir-run` included (in 100 s).

The legacy `karac build` rejects the bench program (it moves `all[a]`
out of the index, where v2 borrows it), so `bench.sh` builds the Kāra
program with `karac build --mir`, the v2 compiled backend. That edit is
by hand, on top of the `scripts/new-bench.sh` output.

The mirrors keep the ★ arm's structure: one stack, from the right. The
C mirror allocates its stack once per check at full size; the others
grow theirs. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.13 s |
| Rust (`rustc -O`) | 0.14 to 0.15 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.13 to 0.16 s |
| Go | 0.43 to 0.56 s |
| Python | 5.7 to 6.3 s |
| Kāra (`karac build --mir`) | 0.99 to 1.09 s |

Most of Kāra's time goes to the ★ arm's
`stack.pop().expect("a candidate")`: the library's `expect` currently
takes its message as an owned `String`, so the literal is copied to the
heap on every pop (B-2026-10-12-31, below). With `.unwrap()` in its
place the same program takes 0.34 to 0.36 s. The kata keeps the natural
form. Under `karac __mir-llvm-run` the program prints the same line in
4.7 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-12-31** (stdlib, open, performance): `Option.expect` and
  `Result.expect` take `msg: own String` in the stdlib source, where the
  library spec says `msg: Str`, so every `.expect("...")` allocates its
  message even when nothing panics. A probe popping 50,000,000 values
  takes 1.14 s compiled with `.expect("x")` and 0.26 s with
  `.unwrap()`. The output is correct; only the time is off.
