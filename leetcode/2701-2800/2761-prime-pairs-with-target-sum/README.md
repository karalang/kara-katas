# 2761. Prime Pairs With Target Sum

You are given an integer `n`. We say that two integers `x` and `y` form
a prime number pair if:

- `1 <= x <= y <= n`
- `x + y == n`
- `x` and `y` are prime numbers

Return *the 2D sorted list of prime number pairs* `[x_i, y_i]`. The list
should be sorted in **increasing** order of `x_i`. If there are no prime
number pairs at all, return *an empty array*.

**Note:** A prime number is a natural number greater than `1` with only
two factors, itself and `1`.

```
n = 10  ->  [[3, 7], [5, 5]]
n = 2   ->  []
```

**Constraints:** `1 <= n <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `primes.kara` ★ | a sieve of Eratosthenes up to n in a `Vec[bool]`, each prime from its square on crossing out its multiples; then each x up to n / 2 with x and n - x both prime, in rising x. O(n log log n) |
| `primes_trial.kara` | no sieve: each x up to n / 2 and its partner tested by trial division by 2 and the odd numbers up to the square root, by `filter` and `map` over the range. O(n sqrt n) |
| `primes_linear.kara` | a linear sieve, each composite crossed out once by its least prime factor, with the primes kept in a list as found; the pairs read off the primes by `take_while` and `filter`. O(n) |
| `primes_odd.kara` | only the odd numbers sieved, one bit each in a `Vec[u64]`, asked through a closure taking the bits as `ref`; 2 handled apart, since it pairs only with n - 2 for an odd n. O(n log log n) |
| `primes_solution.kara` | a Rust solution as LeetCode's Rust users write it, `n` shadowed `as usize`, the multiples crossed out by `(i * i..=n).step_by(i)` and each pair a `vec![x as i32, (n - x) as i32]`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; 4, the one
pair of 2 with itself; 9, an odd n paired with 2; 11, an odd n with no
pair; 100; every n from 1 to 2000; and 20 random n up to `10^6` with
`10^6` itself, LeetCode's most, the last two with the count of the pairs
and a checksum. `primes.py` mirrors the ★ arm and its output is
byte-identical.

```
[[3, 7], [5, 5]]
[]
[[2, 2]]
[[2, 7]]
[]
[[3, 97], [11, 89], [17, 83], [29, 71], [41, 59], [47, 53]]
n from 1 to 2000: 26852 pairs, checksum 755414380
21 n up to 10^6: 48121 pairs, checksum 118950477
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every x and y from 1 to n with x at most y and summing to n,
each kept when both have exactly two divisors, counted one by one; no
sieve. It takes every n from 1 to 200, then 30 random n up to `10^5`,
all before any arm answers; the literal reading is asked only of n up to
200.

| | property |
|---|---|
| P1 | n up to 200, the pairs are the literal reading's |
| P2 | each pair sums to n, its x at most its y, both prime by trial division, and the x strictly rising |
| P3 | an odd n: at most one pair, and that one `[2, n - 2]` |
| P4 | an even n from 4 on: at least one pair |
| P5 | for the first and the last pair `[x, y]`, the pairs of 2x hold `[x, x]` |
| P6 | each arm agrees with at least three of the other four |

P4 is Goldbach's conjecture, checked well past `10^5` long ago, so every
n drawn here stands within it.

The differential prints `230 cases: checksum 137181700, 6900 checks over
5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same count of divisors gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every other multiple left standing | P1 145, P2 168, P3 108, P6 168 |
| M2 | ★: 2 never paired | P1 45, P4 1, P6 49 |
| M3 | trial: a prime's square taken as prime | P1 92, P2 107, P6 107 |
| M4 | trial: 2 taken as no prime | P1 45, P4 1, P6 49 |
| M5 | linear: a prime's least factor never set | P1 143, P4 117, P6 165 |
| M6 | linear: the primes taken up to n, not n / 2 | P1 172, P2 196, P3 80, P6 196 |
| M7 | odd: even multiples crossed out too | P1 118, P2 8, P4 44, P6 138 |
| M8 | odd: [2, 2] never given for 4 | P1 1, P4 1, P5 48, P6 1 |
| M9 | solution: each pair written the larger first | P1 141, P2 163, P3 48, P6 163 |
| M10 | solution: the middle pair never reached | P1 26, P4 2, P5 162, P6 28 |

## Benchmarks

The bench draws 20 n from 900001 to `10^6`, near LeetCode's most, all of
them first, then answers each 3 times by the ★ arm in all five
languages. Every implementation prints `20 n near 10^6, 3 rounds: 255657
pairs, checksum 231340711`.

BENCHTAB

## Verification

All five arms print the same output as `primes.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, trial and linear arms checked clean as first written. The odd arm
gave its closure a `-> bool` return and passed the bits at each call as
`ref composite`; `karac check` warned on both, and `karac fix` took the
return type off and the four `ref`s, the parameter already borrowing.

LeetCode's Rust template took 13 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `Vec<Vec<i32>>` and
`Vec<Vec<i64>>` became `Vec[Vec[i32]]` and `Vec[Vec[i64]]`; `n as usize`
became `n as i64`; `vec![true; n + 1]` became `Vec.filled(n + 1, true)`,
`vec![]` became `Vec.new()`, and `vec![x as i32, (n - x) as i32]` an
array literal; `&&` became `and`; and `Solution::` became `Solution.`.
The `step_by` stayed as written.
