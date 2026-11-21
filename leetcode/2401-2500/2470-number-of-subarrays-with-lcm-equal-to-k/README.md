# 2470. Number of Subarrays With LCM Equal to K

Given an integer array `nums` and an integer `k`, return *the number of
**subarrays** of* `nums` *where the least common multiple of the
subarray's elements is* `k`.

A **subarray** is a contiguous non-empty sequence of elements within an
array.

The **least common multiple of an array** is the smallest positive
integer that is divisible by all the array elements.

```
nums = [3,6,2,7,1], k = 6  ->  4
nums = [3], k = 2          ->  0
```

**Constraints:** `1 <= nums.length <= 1000`; `1 <= nums[i], k <= 1000`.

An LCM only grows, and only into multiples of itself, so once a
subarray's LCM no longer divides `k`, no longer subarray from the same
start can come back to it. A subarray's LCM is `k` exactly when every
number divides `k` and each prime power of `k` is held whole by some
number.

## Approaches

| file | mechanism |
|---|---|
| `lcm.kara` ★ | from each start, the running LCM extended one number at a time, the walk stopped once it no longer divides `k`. O(n^2 log k) at worst |
| `lcm_window.kara` | by prime powers: walking the ends, the last place each full prime power of `k` was seen and the start of the current run of divisors give, for each end, the starts that work, from the run's start to the earliest of those places. O(n * primes) |
| `lcm_sieve.kara` | inclusion and exclusion over the primes of `k`: the subarrays whose numbers all divide `k / d`, for `d` each product of distinct primes of `k`, counted from the runs of such numbers, with alternating signs. O(n * 2^primes) |
| `lcm_map.kara` | by the LCMs that end here: for each end, a `Map` from every LCM of a subarray ending there that divides `k` to how many subarrays have it, the next end's built from this one. O(n * divisors(k)) |
| `lcm_iter.kara` | iterators: for each start, the running LCMs by `scan`, `take_while` they divide `k`, those equal to `k` counted by `filter`, the starts summed by `map` and `sum`. O(n^2 log k) at worst |
| `lcm_solution.kara` | LeetCode's Rust template: the ★ arm's running LCM over an `i64`, the walk stopped once it passes `k`, with a `gcd` nested in the method; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples; then four
more, every number 1 with `k` 1, numbers that never divide `k`, a
prime `k`, and `k` 840 with its four prime powers spread apart; then
four lists of 1000 numbers, the constraints' longest, every number 997
with `k` 997, random divisors of 840, random divisors of 720, and any
numbers from 1 to 12 with `k` 12; and 3000 random lists of 1 to 30
numbers with `k` from 1 to 1000, as a checksum. The random lists draw
each number from the divisors of `k`, and one in eight from 1 to 1000.
`lcm.py` mirrors the ★ arm and its output is byte-identical, and the
mirror was checked on 20000 random lists of 1 to 9 numbers with `k`
from 1 to 60 against every subarray's `math.lcm`.

`check` first reports 2 errors on the template, and `karac fix`
carries it in one call, reporting 9 edits: the nested `fn gcd` moved to
the top level, an insertion and a deletion, since Kāra has no nested
items; the brackets of `Vec<i32>`, two edits; `struct Solution {}`
added; and the four `as i64` casts dropped, since an `i32` widens to an
`i64` by itself. The typed `let mut l: i64 = 1`, the nested loops and
`break` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every subarray, its least common multiple found by
trying the multiples of its first number in turn, up to `k`, for one
that every number divides, and the subarray counted when that least one
is `k`. No gcd stands in for the least common multiple. It checks 300
random lists of 1 to 10 numbers with `k` from 1 to 60, then 60 of up to
16 with `k` from 1 to 120; each number is a divisor of `k`, and one in
six any number to 500. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the list reversed: the same count |
| P3 | the list, a number that does not divide `k`, then the list again: twice the count |
| P4 | every number and `k` doubled: the same count |
| P5 | `k` appended: the count up by one more than the run of divisors of `k` that ends the list |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a subarray reversed has the same numbers. P3 holds
because `k + 1`, which never divides `k`, ends every walk, so no
subarray crosses it. P4 holds because `lcm(2a, 2b) = 2 lcm(a, b)`. P5
holds because a subarray ending on the new `k` has LCM `k` exactly when
every number in it divides `k`.

The differential prints `360 cases: checksum 107459982, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and takes every subarray's `math.lcm`. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the product for the LCM | P1 230, P4 209, P5 281, P6 230 |
| M4 | ★: the LCM carried across starts | P1 248, P2 218, P3 207, P5 235, P6 248 |
| M6 | ★: the last start skipped | P1 86, P2 118, P3 86, P5 274, P6 86 |
| M7 | window: each full power seen a place early | P1 270, P2 185, P4 4, P5 356, P6 270 |
| M8 | window: the run restarted on the breaker | P1 122, P2 150, P3 207, P5 218, P6 122 |
| M9 | window: one start short each end | P1 274, P2 185, P5 360, P6 274 |
| M12 | sieve: each run counted once a number | P1 254, P5 307, P6 254 |
| M14 | sieve: every term over k itself | P1 270, P4 4, P5 356, P6 270 |
| M15 | sieve: the last subset skipped | P1 294, P4 138, P5 4, P6 294 |
| M17 | map: each number alone counted twice | P1 274, P5 360, P6 274 |
| M18 | map: the new number never joined | P1 212, P2 184, P5 275, P6 212 |
| M19 | map: a joined count overwriting | P1 213, P2 185, P5 307, P6 213 |
| M24 | iter: each start counted once at most | P1 209, P2 185, P5 206, P6 209 |
| M25 | iter: the walk started at 2 | P1 188, P4 188, P5 166, P6 188 |
| M26 | iter: each LCM given a step late | P1 206, P2 218, P3 206, P4 4, P5 356, P6 206 |
| M29 | solution: the last end never reached | P1 206, P2 218, P3 206, P5 360, P6 206 |
| M31 | solution: the first number joined each time | P1 257, P2 57, P3 26, P5 279, P6 257 |

P1, P5 and P6 kill all seventeen, P2 eleven, and P3 and P4 six each.

Fourteen are not kept. Five fail exactly as a kept one: the map arm's
each end counted once at most (M20) as its joined count overwriting
(M19); the map arm's every map dropped after its end (M21) as the sieve
arm's each run counted once a number (M12), each counting only the
single numbers equal to `k`; and the iter arm's walk stopped below `k`,
and the template's walk stopped at `k` and each subarray counted twice
(M23, M27, M28), as the map arm's each number alone counted twice
(M17). Eight fail apart from every kept one: the ★ arm's every divisor
of `k` counted, the sieve arm's every sign plus and the template's walk
started at `k` (M3, M13, M30), alike; the ★ and iter arms' each start itself skipped (M2,
M22), alike; the window and sieve arms' leftover prime dropped (M11,
M16), alike; and the window arm's each prime power the prime alone
(M10). The ★ arm's gcd one too large (M5) ends in a division by zero:
the LCM falls to 0, and `k % lcm` divides by it. Every edit is killed by
some check.

## Verification

Every arm prints the same output as `lcm.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.0 to 1.6 s, the iter arm 4.5 s, and the differential 1.0 s; under `karac __mir-llvm-asan` the arms take 0.8 to 1.5 s and the differential 0.7 s, and under `karac run` the differential takes 0.6 s.

## Benchmarks

The bench builds 10 lists of 1000 numbers once from its own generator,
each a random divisor of 720 but one in 50 any number from 1 to 1000,
so a walk runs about 50 numbers before a number breaks it, then makes
90 passes; each sets one number of every list from the checksum so
far, so no answer carries over, then answers it with `k` 720, folding
the count plus the pass into the checksum. The bench uses the ★ arm in
all five languages, the gcd recursive in each. Every implementation
prints `90 passes over 10 lists of 1000: checksum 444064441`.

BENCHTAB
