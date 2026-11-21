# 2521. Distinct Prime Factors of Product of Array

Given an array of positive integers `nums`, return *the number of
**distinct prime factors** in the product of the elements of* `nums`.

**Note** that:

- A number greater than `1` is called **prime** if it is divisible by
  only `1` and itself.
- An integer `val1` is a factor of another integer `val2` if `val2 /
  val1` is an integer.

```
nums = [2,4,3,7,10,6]  ->  4
nums = [2,4,8,16]      ->  1
```

**Constraints:** `1 <= nums.length <= 10^4`; `2 <= nums[i] <= 1000`.

The product of `10^4` numbers to 1000 is far beyond any machine word,
but it never has to be formed: a prime divides a product exactly when it
divides one of its factors, so the answer is the number of distinct
primes among the numbers' own prime factors. The approaches differ in
how the numbers are split and the primes kept.

## Approaches

| file | mechanism |
|---|---|
| `primes.kara` ★ | each number split by trial division up to its square root, every prime it gives into a `Set`, the leftover above 1 a prime too; the answer the Set's size. O(n sqrt(max)) |
| `primes_sieve.kara` | the smallest prime factor of every number to 1000 sieved once, then each number split by dividing out its smallest prime factor again and again, each prime marked in a table of 1001 flags |
| `primes_multiples.kara` | which numbers to 1000 appear at all, then for every prime to 1000 a walk over its multiples, the prime counted when one of them appears. No number is divided |
| `primes_rec.kara` | recursion: a number split by a recursion that tries the divisor `d`, dividing it out when it divides and moving to `d + 1` when it does not; the primes in a `SortedSet`. At most 32 deep |
| `primes_iter.kara` | iterators: the primes to 1000 a `filter` keeping the numbers no smaller number to their square root divides (`take_while`, `all`), then those that divide `any` number, `count`ed |
| `primes_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; each number split by trial division, every prime into a `HashSet`, and its `len()` cast back; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and six
more; then 2000 random lists of 1 to 10 numbers from 2 to 50 and 2000
of 1 to 100 from 2 to 1000, as the sum and a checksum; then the
constraints' largest, `10^4` numbers: 2 to 1000 in turn, all 1000, and
random from 2 to 1000. `primes.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3000 random lists of 1 to
12 numbers to 20 or to 1000 against the primes to 1000 that divide the
whole product, formed as a Python integer, and the two agreed on every
list.

`check` reports 2 errors on the recursion arm as first written: the
recursive calls passed the `mut ref SortedSet` binding on without the
call-site `mut` marker. `karac fix` applied both markers.

`check` first reports 7 errors on the template: the `use
std::collections::HashSet` line, `struct Solution;`, `Vec<i32>` in
angle brackets, the paths `HashSet::new` and
`Solution::distinct_prime_factors`, the `&n` pattern, and the `&nums`
borrow. `karac fix` carries it in one call, reporting 11 edits: the
`use` line deleted; `struct Solution {}`; the brackets; `HashSet.new`
written `Set.new`, the prelude's set; the `&` pattern dropped; `for n in
ref nums`; `p` annotated `i32` to match the number it divides;
`Solution.distinct_prime_factors`; and the wrapper's lossless `as i64`
dropped.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the primes to 1000 found by counting divisors, a prime being
a number with exactly two; then the product of the numbers taken modulo
each prime, the prime counted when the product leaves 0. No number is
split. It checks 300 random lists of 1 to 10 numbers from 2 to 50; then
30 of 1 to 30 from 2 to 1000, the last 15 with a 1000 added; and 30 of
one prime repeated 1 to 5 times. Every list keeps the constraints. All
360 are drawn before any arm answers, and 47 of them have one prime.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | from 1 to 4 for each number, no number to 1000 having five |
| P3 | the numbers in the reverse order: the same answer |
| P4 | the first number appended once more: the same answer |
| P5 | the list joined to the next case's: from the larger of the two answers to their sum |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the five smallest primes multiply to 2310, past 1000.

The differential prints `360 cases, 47 with one prime: checksum
841674608, 12960 checks over 6 arms: 0 failures` under every lane in
Verification; the checksum of the literal answers was checked against a
Python reading that builds the same cases, forms each whole product and
tries every prime to 1000. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the square root bound strict | P1 137, P6 137 |
| M3 | ★: each prime divided out once | P1 226, P6 226 |
| M5 | ★: the last number skipped | P1 179, P2 36, P3 161, P4 179, P5 45, P6 179 |
| M7 | sieve: the prime divided out squared | P1 216, P6 216 |
| M9 | sieve: a prime counted every time | P1 318, P2 3, P4 360, P6 318 |
| M11 | sieve: the first number skipped | P1 203, P2 36, P3 161, P4 203, P5 55, P6 203 |
| M13 | multiples: only the prime itself looked for | P1 316, P2 71, P6 316 |
| M14 | multiples: the primes from 3 | P1 63, P6 63 |
| M15 | multiples: the hit reset at each multiple | P1 343, P2 317, P6 343 |
| M17 | rec: the leftover dropped | P1 347, P2 43, P6 347 |
| M19 | rec: the recursion begun at 3 | P1 211, P6 211 |
| M20 | rec: the divisor stepped by 2 | P1 183, P6 183 |
| M22 | iter: the primes from 3 | P1 300, P2 2, P6 300 |
| M23 | iter: a prime only when it divides every number | P1 299, P2 273, P5 134, P6 299 |
| M24 | iter: the square root bound strict | P1 277, P6 277 |
| M29 | solution: the divisors from 3 | P1 210, P6 210 |
| M30 | solution: one more than the size | P1 360, P6 360 |

P1 and P6 kill all seventeen, P2 eight, P4 and P5 three each, and P3
two.

The first run of the thirty-one found a gap in the differential: no
case held a 1000, so the multiples arm's 1000 never present and the
template's each number cut to 999 (M16, M31) survived, as did the sieve
arm's sieve to 999. The last 15 of the lists to 1000 now end in a 1000,
and M16 and M31 are killed. The sieve to 999 was replaced, since on a
1000 it leaves the smallest factor 0 and divides by it. Four more were
replaced. Two survived as equivalent: the sieve arm's later prime
overwriting the smallest factor, which still divides the number, and
the multiples arm's prime marked composite, read only before it is
marked. The iter arm's primes to 999 is equivalent too, 1000 not being
prime. The sieve arm's sieve from the square crashed, leaving the
primes above 31 with no smallest factor. They became the sieve arm's
prime divided out squared, count begun at 1 and sieve stepping by `2 p`
(M7, M8, M10), the multiples arm's only the prime itself looked for
(M13), and the iter arm's primes from 3 (M22).

Fourteen are not kept, and none survives. Eight fail exactly as a kept
one. The ★ arm's and the template's leftover dropped (M2, M27) fail as
the rec arm's (M17); the ★ arm's divisors from 3 (M4) as the
template's (M29); the ★ arm's leftover counted though 1 and the rec
arm's divisor moved on after a hit (M6, M18) as the ★ arm's each prime
divided out once (M3); the sieve arm's count begun at 1 (M8) as the
template's one more than the size (M30); the iter arm's first number
skipped (M26) as the sieve arm's (M11); and the template's square root
bound strict (M28) as the ★ arm's (M1). The other six each fail in a
way of their own, but their arms already hold their kept edits: the
sieve arm's sieve stepping by `2 p` (M10), the multiples arm's prime
itself not walked and 1000 never present (M12, M16), the rec arm's
bound `d * d` at least (M21), the iter arm's composites kept (M25), and
the template's each number cut to 999 (M31).

## Verification

Every arm prints the same output as `primes.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 to 40.5 s and the differential 19.8 s; under `karac __mir-llvm-asan` the arms take 0.6 to 13.0 s and the differential 6.8 s; and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds 200 random lists of 1000 numbers from 2 to 1000 once
from its own generator, then makes 110 passes. Each pass asks every
list cut to its first `check % 1000 + 1` numbers, folding each answer
plus the pass into the checksum. The bench uses the ★ arm in all five
languages; the C mirror holds its set in a small open-addressing hash
table, cleared for every call. Every implementation prints `110 passes
over 200 lists of 1000 numbers: checksum 135715239`.

BENCHTAB
