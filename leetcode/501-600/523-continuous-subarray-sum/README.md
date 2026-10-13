# 523. Continuous Subarray Sum

Given an integer array `nums` and an integer `k`, return `true` if
`nums` has a good subarray, or `false` otherwise. A good subarray is
one whose length is at least two and whose sum is a multiple of `k`.
A subarray is a contiguous part of the array, and `0` is always a
multiple of `k`.

```
nums = [23,2,4,6,7],  k = 6   ->  true   ([2,4] sums to 6)
nums = [23,2,6,4,7],  k = 6   ->  true   (the whole array sums to 42)
nums = [23,2,6,4,7],  k = 13  ->  false
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <= 10^9`;
`0 <= sum(nums[i]) <= 2^31 - 1`; `1 <= k <= 2^31 - 1`.

## Approaches

Every arm is `fn check_subarray_sum(nums: Vec[i64], k: i64) -> bool`.
A run `nums[j+1..=i]` sums to a multiple of `k` exactly when the
prefix sums up to `j` and up to `i` leave the same remainder, so every
arm looks for two prefixes, at least two numbers apart, with the same
remainder; the empty prefix counts, with remainder 0.

| file | mechanism |
|---|---|
| `check_subarray_sum.kara` ★ | a `Map` from each remainder to the first index it was seen at (the empty prefix at -1); true as soon as a remainder comes back at least two places later |
| `check_subarray_sum_lag.kara` | a `Set` that takes each prefix's remainder one step after it is made, so a remainder found in it is at least two places back |
| `check_subarray_sum_sorted.kara` | every prefix's (remainder, length) pair, the empty prefix included, sorted; each group of equal remainders spans from its first to its last |
| `check_subarray_sum_span.kara` | one pass records the first and the last prefix length for each remainder in two `Map`s; a second pass looks for one whose last is two past its first |
| `differential.kara` | the four arms against a brute force over every run, five properties |

Every arm prints the same 13 lines: the answer for eleven arrays (the
three examples, two zeros and one zero with `k = 1`, zeros after a
number, a run of one that is a multiple and a run of two that is not,
a single number equal to `k`, and two numbers of `10^9` with `k =
2^31 - 1`), then for 3,000 random arrays of 1 to 30 numbers up to 999
with `k` up to 1,000 how many are true and a checksum over which, and
last the largest case: 100,000 numbers from 1 to 20,000 with `k =
2^31 - 1` (false) and with `k` the sum of the middle 50,000 (true).
`check_subarray_sum.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a brute force
that sums every run of two or more numbers. Each arm is held to the
properties below on 2,000 cases: a short array of 1 to 12 numbers up
to 30 with `k` up to 60 for P1, and a longer one of 1 to 60 numbers up
to 999 with `k` up to 1,000 for the rest.

| | property |
|---|---|
| P1 | the answer is the brute force's, on the short array |
| P2 | the array back to front gives the same answer |
| P3 | every number and `k` times `c` (2 to 5) give the same answer |
| P4 | two zeros put in side by side, anywhere, make it true |
| P5 | with `k = 1` it is true exactly when there are two or more numbers |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run of one number counts (`>= 1`) | P1 234, P5 36 |
| M2 | ★: the empty prefix put at 0, not -1 | P1 38, P2 3, P4 67, P5 33 |
| M3 | lag: the set takes each remainder at once, not a step late | P1 275, P2 54 |
| M4 | lag: the remainder held back never moves on from 0 | P1 486, P2 282, P4 1653 |
| M5 | sorted: the empty prefix left out | P1 146, P2 56, P4 67, P5 33 |
| M6 | sorted: the pairs reversed, not sorted | P1 990, P4 2000, P5 1964 |
| M7 | span: the first length overwritten too, so first is last | P1 990, P4 2000, P5 1964 |
| M8 | span: a run of three or more needed (`>= 3`) | P1 125, P4 863, P5 33 |
| E1 | ★: the gap tested as `i >= j + 2` | 0 |
| E2 | lag: each number reduced before it is added | 0 |
| E3 | sorted: the gap tested as `last >= first + 2` | 0 |
| E4 | span: the last length stored by index assignment | 0 |

M6 and M7 fail the same checks because both always answer false:
reversing the pairs leaves no group with a first before its last, and
a first that is overwritten is always the last. M2 and M5 lose the
empty prefix's place in the same way, so a run that starts at the
array's front must be three long (M2) or is never seen (M5); they
differ on P1 and P2 only because M5 also loses the remainder 0 group's
first member. M3 is both too eager, taking a run of one number that is
a multiple of `k`, and too late, never holding the empty prefix; the
two errors depend on where the run sits, which is why P2, the array
back to front, catches it 54 times.

## Verification

Every arm prints the same output as `check_subarray_sum.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `40000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

On the frozen legacy backends, the sorted arm prints the same output
under `karac run --interp`, LLJIT and `karac build`, and under a
`KARAC_AUTO_PAR=1` build. The other three arms, the differential and
the bench program are refused at type checking, "unary '*' requires
'ref T' ... found 'i64'": legacy types the payload of a `Map`'s
`get`, the items of a `Vec`'s `iter()` and the values of a `Map`'s
`iter()` by value, so it refuses `*j`, `*x` and `*a`. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 random arrays of 100,000
numbers (the problem's longest) from 1 to 20,000 once, so every sum
stays under `2^31`; then checks every array in each of 10 rounds
against a fresh `k` from 10,000 to about `2^30`, which keeps most
answers false and the whole array walked. Every implementation prints
`20 arrays of 100000, 10 rounds: 143 true, checksum 7701`, the Kāra
program under `karac __mir-run` included (in 22.7 s).

Each mirror makes a fresh map for every call, as the ★ arm's
`Map.new()` does: Rust's `HashMap` with its default hasher, Go's
built-in map, Python's dict. C has no map of its own, so its mirror is
an open-addressing table with linear probing that doubles at half
full. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.92 to 0.93 s |
| Rust (`rustc -O`) | 0.73 to 0.79 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.80 to 0.90 s |
| Go | 0.89 to 0.92 s |
| Python | 2.56 to 2.67 s |
| Kāra (`karac build --mir`) | 0.89 to 1.06 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`df61cbfff6`. Under `karac __mir-llvm-run` the program prints the same
line in 9.8 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
