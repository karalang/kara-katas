# 1390. Four Divisors

Given an integer array `nums`, return the sum of divisors of the
integers in that array that have exactly four divisors. If there is no
such integer in the array, return `0`.

```
nums = [21, 4, 7]       ->  32
nums = [21, 21]         ->  64
nums = [1, 2, 3, 4, 5]  ->  0
```

**Constraints:** `1 <= nums.length <= 10^4` and `1 <= nums[i] <= 10^5`.

Each arm is `fn sum_four_divisors(nums: Vec[i32]) -> i32`. A value v
with four divisors is p q or p^3, and its divisors sum to at most 1.5 v
+ 3, so 10^4 such values up to 10^5 stay under 1.6 × 10^9, inside an
`i32`.

## Approaches

| file | mechanism |
|---|---|
| `sum_four_divisors.kara` ★ | each value's divisors found in pairs, d and v / d, by trial division up to its square root, a count and a sum kept, the search given up once the count passes four. O(n sqrt(m)) for n values up to m |
| `sum_four_divisors_sieve.kara` | a smallest-prime-factor sieve up to the largest value: a value has four divisors when it is p q for two different primes, or p^3, and they are 1, p, q and p q, or 1, p, p^2 and p^3. O(m log log m + n) |
| `sum_four_divisors_counts.kara` | every divisor laid down at once: each d up to the largest value added to the count and the sum of each of its multiples, and the values whose count is four give their sums. O(m log m + n) |
| `sum_four_divisors_memo.kara` | each distinct value worked out once: its divisors collected into a `Vec` up to its square root, and what it gives, their sum when there are four and else 0, kept in a `Map` for the next time it comes. O(u sqrt(m) + n) for u distinct values |
| `sum_four_divisors_solution.kara` | a Rust solution as LeetCode's Rust users write it (`for &n in nums.iter()`, `break` once past four, and `ans` returned), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples, the cube
of a prime with the cube of another, the square of a prime, which has
three divisors, and the constraints' largest value (`32 64 0 55 0 0`);
the constraints' most, 10^4 values up to 10^5, and the 10^4 largest
(`10^4 values: 137186108, and 251384194 for 90001 to 10^5`); and 2000
random lists of 1 to 50 values, half up to 10^5 and half up to 100
(`2000 random lists: 122882897 in all, checksum 589529702`).
`sum_four_divisors.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: in four of the five arms a sum begun with `let mut total
= 0;`, added to from `i32` values and returned as the `i32` answer,
keeps its literal's `i64`, which the return refuses; `karac fix`
declares it `let mut total: i32 = 0;`. The same fix goes with it to the
running sums and divisors whose literals feed the same `i32`s: in the ★
arm `sum` and `d`, in the memo arm `d`, which is pushed onto a
`Vec[i32]`, and in the counts arm the `Vec.filled(most + 1, 0)` of sums,
which becomes `Vec.filled(most + 1, 0i32)`; the counts, compared only
with 4, keep their `i64`. The sieve arm's `Vec.filled(most + 1, 0)`
takes `i32` from the primes stored in it, with no fix. The Rust solution
takes one round of 8 fixes by `karac fix`'s count, from 4 errors:
`struct Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`,
the pattern `&n` to `n`, `Solution::` to `Solution.`, and `ans`, `sum`
and `i` declared `i32`; the `break` stays. Its output matches on the
first run.

The sieve arm as first written tested for a cube with `q == p * p`;
under `karac run` the harness's 10^4 values stopped it with `runtime
error: integer overflow`, since a prime near 10^5 squared passes 2^31 in
`i32`. The arm now asks `q % p == 0 and q / p == p`. Kāra checks integer
arithmetic by default, and that check caught a mistake in the kata, not
in the compiler.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number from 1 to the value tried as a divisor, and the
divisors of each value with exactly four of them summed. LeetCode's
three examples and 2000 lists of 1 to 12 values, half anywhere up to
3000 and half up to 60 with cubes and squares of primes and 16, 81 and
625 thrown in, so that four divisors, three and five are all common.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the values in reverse order: the same |
| P3 | the values written twice: twice as much |
| P4 | a 6 added, whose divisors 1, 2, 3 and 6 make 12: 12 more |
| P5 | the front half and the back half answered apart: the same in sum |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 lists: checksum 699399498,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, listing every
divisor, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search stopped below the square root | P1 415, P6 1660 |
| M2 | ★: the square root of a square counted twice | P1 665, P6 2660 |
| M3 | sieve: the square of a prime taken for p q | P1 584, P6 584 |
| M4 | sieve: a cube's p^2 left out of its sum | P1 649, P6 649 |
| M5 | counts: 1 not counted as a divisor | P1 1685, P4 2003, P6 1685 |
| M6 | counts: the largest value left out as a multiple, so it has no divisors | P1 806, P4 10, P5 575, P6 806 |
| M7 | memo: a value given up at four divisors, not past four | P1 1647, P4 2003, P6 1647 |
| M8 | memo: the search stopped below the square root | P1 415, P6 415 |
| M9 | solution: the search broken off at four divisors, not past four | P1 1732, P6 1732 |
| M10 | solution: the larger of each pair summed as the value itself | P1 1647, P4 2003, P6 1647 |

P1 and P6 kill all ten, P4 four, P5 one, and P2 and P3 none. The answer
is a sum over the values, each value's part its own, so an edit that
gets a value wrong still gets it wrong the same way in any order and as
often as the value comes: reversing the list (P2) and writing it twice
(P3) cannot tell. P4 kills the edits that get 6 itself wrong: M5 gives 6
three divisors, M7 gives up on it at its fourth, M10 sums 1 + 6 + 2 + 6,
and M6 drops it when 6 is the largest value of a short list. Only M6
makes one value's part depend on the others, through the largest value,
which the two halves of P5 do not share.

## Benchmarks

The bench draws 10^4 values up to 10^5, the constraints' most, once.
Then 300 rounds, each giving one value a new one and folding the answer
into the checksum, all drawn from the checksum so far. Every
implementation prints `300 rounds over 10^4 values up to 10^5: checksum
229042424`. The work is the trial division of 10^4 values, a round, each
up to its square root unless it passes four divisors first. Each
language runs the same loop on 32-bit integers.

BENCHTAB
