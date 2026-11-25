# 1362. Closest Divisors

Given an integer `num`, find the closest two integers in absolute
difference whose product equals `num + 1` or `num + 2`.

Return the two integers in any order.

```
num = 8    ->  [3,3]    (9 = 3 * 3; 10 = 2 * 5 is farther apart)
num = 123  ->  [5,25]
num = 999  ->  [40,25]
```

**Constraints:** `1 <= num <= 10^9`.

Each arm is `fn closest_divisors(num: i32) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `closest_divisors.kara` ★ | a divisor pair of m is closest when its smaller part is the largest divisor of m at most √m, so d counts down from √(num + 2), and the first d that divides num + 1 or num + 2 gives the answer; the two targets' best pairs cannot tie. O(√num) |
| `closest_divisors_separate.kara` | each target's own closest pair, its smaller part counted down from its own square root, and the pair of the two with the smaller difference. O(√num) |
| `closest_divisors_ascending.kara` | d counts up from 1 while d² is at most num + 2, the last divisor of each target seen kept; the closer of the two pairs is the answer. O(√num), always the whole way |
| `closest_divisors_divisors.kara` | each target factored by trial division, every divisor built from its prime powers, and the largest whose square is at most the target paired with its cofactor. O(√num) to factor, then the divisors, at most 1344 below 10^9 |
| `closest_divisors_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let mut i = ((num + 2) as f64).sqrt() as i32;` counted down, `vec![i, (num + 1) / i]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

The answer goes either way round, so every arm's pair is printed
smaller first. Every arm prints the same 2 lines: LeetCode's three
examples, the constraints' two ends, num + 2 a square (23), and num + 1
twice a prime with num + 2 the prime 10^9 + 7 (`[3,3] [5,25] [25,40]
[1,2] [23658,42269] [5,5] [2,500000003]`); and 500 random numbers up to
10^9 folded into a checksum (`500 random numbers: checksum 891886220`).
`closest_divisors.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, separate, ascending and divisors arms check
clean. The Rust solution takes 6 fixes: `struct Solution;` becomes
`struct Solution {}`, `Vec<i32>` becomes `Vec[i32]`, the two `vec![..]`
returns become list literals and `vec![]` becomes `Vec.new()`. Its
`(num + 2) as f64` stays an `i32` sum, which fits for every num up to
10^9. Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every pair of positive integers whose product is num +
1 or num + 2, the first factor tried from 1 to the product, and the
pair of least difference kept. That reading takes O(num), so it answers
num up to 2000; the other properties cover the constraints' last ten
and 200 random numbers up to 10^9 as well.

| | property |
|---|---|
| P1 | the statement read literally, for num up to 2000 |
| P2 | the product is num + 1 or num + 2 |
| P3 | the closest pair for its own product: nothing from the smaller part up to the product's square root divides it |
| P4 | a neighbour's answer on a shared target is no closer: num - 1 may answer for num + 1, and num + 1 for num + 2 |
| P5 | num + 1 or num + 2 a square k², for a k drawn from num, the answer (k, k) |
| P6 | the ★ arm's answer |

All 76,255 checks pass on every arm: `2210 cases: checksum 50577951,
76255 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, trying every factor up to each
target's square root, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: d counted down by twos | P1 931, P3 503, P6 4156 |
| M2 | ★: num + 2's divisor paired with num + 1's cofactor | P1 1012, P2 1128, P3 565, P4 43, P5 2210, P6 4512 |
| M3 | separate: num + 2 never tried | P1 1012, P4 1127, P5 2210, P6 1128 |
| M4 | separate: the count down stopped at 2 | P1 35, P2 35, P3 33, P6 35 |
| M5 | ascending: the farther pair chosen | P1 2000, P4 702, P5 4420, P6 2210 |
| M6 | ascending: only odd d tried | P1 1029, P3 716, P5 2226, P6 1124 |
| M7 | divisors: a prime factor above the square root dropped | P1 457, P3 425, P6 512 |
| M8 | divisors: a square's root not taken | P1 86, P3 25, P5 4420, P6 86 |
| M9 | solution: counted down from the square root of num + 1 | P1 43, P4 43, P5 2210, P6 43 |
| M10 | solution: num tried in place of num + 1 | P1 1307, P2 1072, P3 61, P4 574, P5 2210, P6 1445 |

P1 and P6 kill all ten, P3 and P5 seven, P4 five and P2 three. The
product (P2) catches the edits that pair a part with the wrong
cofactor: num + 1's cofactor for num + 2 (M2), a count down stopped
at 2 on an odd prime (M4), and num's divisor paired as num + 1's
(M10). The closest pair for its own product (P3) catches the edits
that pass over the best divisor of a product they still answer for:
odd d only (M6), a missing prime factor (M7), a square's root (M8), and
d by twos (M1). The neighbours (P4) catch the edits that answer for
the wrong target when the other was closer: num + 2 never tried (M3),
the farther pair (M5) and a count from √(num + 1), which passes over
num + 2 when it is a square (M9). The squares (P5) catch all three of
those, and every edit that can miss a pair (k, k).

## Benchmarks

The bench asks 10^4 questions, each num up to 10^9 drawn from the
checksum so far, so no answer carries over, answered by the ★ arm and
folded into the checksum. Every implementation prints `10000 questions:
checksum 594990387`. The work is two 64-bit remainders for each d from
√(num + 2) down to the answer, the same in every language.

BENCHTAB
