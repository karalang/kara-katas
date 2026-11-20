# 2338. Count the Number of Ideal Arrays

You are given two integers `n` and `maxValue`, which are used to
describe an **ideal** array.

A **0-indexed** integer array `arr` of length `n` is considered
**ideal** if the following conditions hold:

- Every `arr[i]` is a value from `1` to `maxValue`, for `0 <= i < n`.
- Every `arr[i]` is divisible by `arr[i - 1]`, for `0 < i < n`.

Return *the number of **distinct** ideal arrays of length* `n`. Since
the answer may be very large, return it modulo `10^9 + 7`.

```
n = 2, maxValue = 5   ->  10
n = 5, maxValue = 3   ->  11
```

**Constraints:** `2 <= n <= 10^4`; `1 <= maxValue <= 10^4`.

An ideal array never falls, and wherever it changes it moves to a
multiple, so its distinct values form a chain, each dividing the next,
and the array is that chain with each value held for one or more
places. A chain of `k + 1` values goes over the `n` places in
`C(n - 1, k)` ways, the choice of where each new value starts. A chain
at least doubles at each step, so it holds at most 14 values for
`maxValue` up to `10^4`, and the count is the sum over the chain
lengths of the chains of that length times its binomial. Equally, along
an ideal array each prime's exponent never falls, so the arrays ending
at `v` are, for each prime power `p^e` of `v`, the `C(n - 1 + e, e)`
ways to raise the exponent from 0 to `e`, all multiplied.

## Approaches

| file | mechanism |
|---|---|
| `ideal.kara` ★ | the chains ending at each value, level by level, each level pushing its counts on to every multiple; each level's total times `C(n - 1, k)`, the binomials from the one before by a modular inverse. O(maxValue log maxValue) a level |
| `ideal_naive.kara` | place by place: the arrays of each length ending at each value, each extended by every multiple of its last value. O(n maxValue log maxValue) |
| `ideal_primes.kara` | each value's prime exponents by trial division, the arrays ending at it the product of `C(n - 1 + e, e)`. O(maxValue sqrt maxValue) |
| `ideal_memo.kara` | the chains of `k` more values after `v` from the top down, through each multiple, memoized in a `Map` by `(v, k)`; the binomials as one row of Pascal's triangle |
| `ideal_iter.kara` | iterators: each value's proper divisors listed by a sieve with `step_by`, each level `map`ped from the one before by a `fold` over the divisors, the binomials threaded by `scan`, and the levels' totals `zip`ped with them and folded |
| `ideal_solution.kara` | LeetCode's Rust template: a `const` modulus inside the method, a `vec!` table of binomials by Pascal's rule over `usize` indices, and each value's prime exponents by trial division; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; a single
value allowed; ten thousand places of it; ten thousand places up to 60;
three places up to ten thousand; 300 places up to 3000; then 2000
random cases of 2 to 40 places and values up to 1 to 80, with a
checksum and the counts in all. `ideal.py` mirrors the ★ arm and its
output is byte-identical; the counts it prints were checked against
the prime-exponent formula with Python's exact `math.comb`.

The ★ arm was first written with its modulus and its longest chain as
module-level `let`s. `karac check` refuses a value at module scope that
is not a `const`, and `karac fix` rewrote both, two edits.

`karac fix` carries the template in one call, reporting 8 edits.
`check` first reports two errors and offers two edits for them:
`struct Solution;` to `struct Solution {}` and `Solution::` to
`Solution.` in the harness's wrapper. The other six follow from those:
the two `as usize` to `as i64`, since an index is an `i64`; the two
`vec!` to `Vec.filled`, with the `0i64`'s suffix dropped; and the
wrapper's `as i64` on the `i32` answer dropped, since it widens on its
own. The `const MOD` inside the method, its `1_000_000_007` and
`i.min(14)` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every array of `n` values from 1 to `maxValue`, made as the
digits of a counter, and those in which each value divides the next
counted. No chains, no binomials and no primes. It checks 300 random
cases of 2 to 4 places and values up to 1 to 8; then 30 of up to 60
places and values up to 300; then 30 of up to 3000 places and values up
to 12, whose counts pass the modulus. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | up to 4 places and values up to 8, the answer is the literal reading's |
| P2 | two places: the sum over `v` of `maxValue / v` |
| P3 | `maxValue` cut to the largest prime `p` it reaches: `p` adds `n` arrays to those up to `p - 1` |
| P4 | values up to 1, 2 and 3: 1, `n + 1` and `2n + 1` arrays |
| P5 | the arrays ending at `a * b`, for `a` and `b` coprime, number those ending at `a` times those ending at `b` |
| P6 | each arm agrees with at least three of the other five |

The arrays ending at `v` are read from any arm as its count up to `v`
less its count up to `v - 1`. P2 counts each first value with its
multiples. P3 holds because an array ending at a prime is ones and then
the prime, which starts at one of `n` places; P4 likewise counts the
ones and then twos, or ones and then threes, by where the change
comes. P5 is the prime-exponent product, which splits over coprime
factors. P3 to P5 hold modulo `10^9 + 7`, which the largest cases pass.

The differential prints `360 cases: checksum 174910301, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts over `itertools.product`. On a failure it
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
| M1 | ★: chains of at most three values | P1 12, P5 32, P6 57 |
| M4 | ★: the binomials never divided by k | P1 131, P5 130, P6 186 |
| M6 | ★: the chains ending at 1 never totalled | P1 300, P2 360, P4 360, P6 360 |
| M8 | naive: no value repeated | P1 300, P2 360, P3 316, P4 360, P5 62, P6 360 |
| M9 | naive: the arrays ending at maxValue left out | P1 300, P2 360, P3 244, P4 360, P5 33, P6 360 |
| M10 | naive: every other multiple skipped | P1 260, P2 316, P3 43, P4 360, P6 316 |
| M13 | primes: the rises over n places, not n - 1 | P1 260, P2 316, P3 316, P4 360, P6 316 |
| M15 | primes: each prime divided out once | P1 184, P2 233, P5 16, P6 239 |
| M16 | primes: the ways reset at each prime | P2 27, P5 22, P6 27 |
| M17 | memo: chains through every third multiple | P1 260, P2 316, P3 43, P4 360, P5 153, P6 316 |
| M18 | memo: a chain count read from the next length's | P1 183, P3 239, P4 269, P5 130, P6 239 |
| M19 | memo: Pascal's rule applied from the left | P1 184, P2 239, P5 156, P6 239 |
| M22 | iter: each value listed among its own divisors | P1 300, P2 360, P3 316, P4 360, P5 156, P6 360 |
| M23 | iter: the scan yielding the next binomial | P1 286, P2 316, P3 227, P4 360, P5 130, P6 346 |
| M26 | iter: divisors past half of maxValue never listed | P1 260, P2 316, P3 115, P4 360, P5 153, P6 316 |
| M27 | solution: Pascal's table only to two | P1 32, P2 77, P6 77 |
| M29 | solution: the rises over n places, not n - 1 | P1 184, P2 239, P5 137, P6 239 |

P6 kills all seventeen, P1 sixteen, P2 fourteen, P5 thirteen, P4 ten
and P3 nine. P1 misses only the primes arm's ways reset at each prime,
which needs a value with two primes found before the last one, 36 the
least, past the 8 that P1 reaches; P2 and P5 catch it on the larger
cases. P2, two places, misses the edits that only go wrong for chains
of three values or more, which two places never hold: chains cut to
three values, the binomials never divided by `k` (whose first two
divide by 1), and a chain count read from the next length's. P3, the
step at a prime, and P4, the values up to 3, fail where an edit
miscounts the arrays that end at a prime: a value never repeated, the
last value or every other multiple left out, the binomials or the
places off by one, the chains through every third multiple. They miss
the edits that only go wrong for chains of three values or more, which
no array ending at a prime or at 3 holds; P3 also misses the chains
ending at 1 never totalled, which cancels in its difference and which
P4's single value counts.

Of the thirty-one, fourteen were not kept. The ★ arm's binomials of
`n` places (M2) and the naive arm's one place too many (M7) fail as the
primes arm's rises over `n` places (M13). A value pushed on to itself
in the ★ arm (M3), no chain starting at 1 in the ★ (M5) and iter (M24)
arms, the naive arm's shorter arrays kept (M11) and the memo arm's
chains from 1 left out (M20) fail as the iter arm's value listed among
its own divisors (M22), and the iter arm's totals zipped a binomial on
(M25) as its scan yielding the next binomial (M23). The primes arm's
square of a prime taken for a prime (M14) fails as the template's
(M31), and its prime left over never counted (M12) as the template's
counted over `n - 1` places (M28); none of those four is kept. The memo
arm's chain of two values counted as one (M21) and the template's
trial division started at 3 (M30) fail apart from every kept one, and
were left out to keep three to an arm.

## Verification

Every arm prints the same output as `ideal.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ and template arms take about 1 s, the
primes arm 2 s, the naive arm 4.9 s, the iter arm 5.4 s and the memo
arm, which hashes every `(v, k)` it meets, 7.6 s. The differential
takes 17 s there and 0.7 s under `karac __mir-llvm-run`.

## Benchmarks

The bench answers 300 queries once, from a scramble that never repeats:
`n` from 2 to `10^4` and `maxValue` from 5000 to `10^4`, folding each
count into the checksum, with the ★ arm in all five languages. Every
implementation prints `300 queries of n up to 10^4 and maxValue 5000 to
10^4: checksum 938900772`. Each allocates its level of counts afresh
for every level of every query, `maxValue + 1` 64-bit integers, as the
arm does.

BENCHTAB
