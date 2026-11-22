# 2847. Smallest Number With Given Digit Product

Given a **positive** integer `n`, return *a string representing the
**smallest positive** integer such that the product of its digits is
equal to* `n`*, or* `"-1"` *if no such number exists*.

```
n = 105  ->  "357"
n = 7    ->  "7"
n = 44   ->  "-1"
```

**Constraints:** `1 <= n <= 10^18`.

## Approaches

| file | mechanism |
|---|---|
| `product.kara` ★ | the fewest digits make the smallest number, and taking the largest digit that divides what is left, 9 down to 2, makes the fewest; the digits then go smallest first, by `char.from_digit` and `iter().rev().collect()`; anything left over but 1 has a prime factor above 7 |
| `product_primes.kara` | by the exponents of 2, 3, 5 and 7 in a `SortedMap`: every pair of 3s a 9, every three 2s an 8, each 5 and 7 its own digit, and what is left, at most one 3 and two 2s, made the fewest and smallest digits by a `match` on a tuple; the digits counted out smallest first |
| `product_memo.kara` | a search over what is left to make, remembered in a `Map[i64, Option[String]]`: the best digits for m over every digit d dividing m, the best for m / d with d sorted in, the shortest and then the smallest winning |
| `product_peel.kara` | the greedy written as recursion over `Option` with `?`: the largest digit that divides n, found by `find` over `(2..10).rev()`, is the number's last, and the rest is the smallest number for n over it |
| `product_solution.kara` | a Rust solution as LeetCode's Rust users write it: a `mut n: i64` parameter divided by 9 down to 2 over `(2..=9).rev()`, the digits pushed as `(b'0' + d as u8) as char` and the string reversed with `chars().rev().collect()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's three examples and 1;
10^18, LeetCode's most; 2^59 and 3^37, the largest powers of 2 and 3
in range, and the prime 10^9 + 7; then 3000 random products of up to
12 of 2, 3, 5 and 7, a fifth of them times 11 or 13, and 300 of up to
40 as many as stay within 10^18, as a count with none and a checksum.
`product.py` mirrors the ★ arm and its output is byte-identical.

```
357 7 -1 1
555555555555555555888888
48888888888888888888 3999999999999999999 -1
3000 short products: 616 with none, checksum 482329875
300 long products: 0 with none, checksum 445977246
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every number from 1 to 99999 in order, each digit
product's first number kept in a `Map`, so a product some number of up
to 5 digits makes has its smallest one, and for any other the answer
must be -1 or longer than 5 digits. It draws 2000 random products of
up to 4 digits from 2 to 9, a sixth of them times 11 or 13, then 50
products of 2, 3, 5 and 7 up to 10^17, all before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's, or past its reach |
| P2 | the answer's digits multiply to n |
| P3 | n times 7: the same digits with a 7 sorted in (7 for n = 1), or -1 again |
| P4 | n times 11: -1 |
| P5 | the answer's digits run smallest first, with no 0, and no 1 but for n = 1 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 985898797, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Eight are killed, each the same
way under both backends. M6 and M7 survive and are equivalent: the
answer with its smallest digit taken off is the best string for what is
left, so the search reaches it at that digit, the first one tried that
gives the shortest length, and any other last digit tried first would
start a smaller string, which cannot be; and with the digits left
unsorted the answer is still built, as that best string with the largest
digit appended, which the search also tries.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the digits left largest first | P1 953, P3 1315, P5 992, P6 992 |
| M2 | ★: 9 never tried | P1 497, P6 532 |
| M3 | primes: a 3 and two 2s made 3 and 4 | P1 101, P6 107 |
| M4 | primes: pairs of 3s left as 3s | P1 497, P6 532 |
| M5 | primes: a left-over 2 dropped | P1 217, P2 224, P6 224 |
| M6 | memo: the smaller of equal lengths not preferred | survives: equivalent (above) |
| M7 | memo: the digits not sorted | survives: equivalent (above) |
| M8 | peel: the smallest dividing digit taken | P1 1148, P3 1315, P5 978, P6 1187 |
| M9 | peel: the digit put in front | P1 953, P3 1315, P5 992, P6 992 |
| M10 | solution: a remainder above 7 not caught | P1 375, P2 375, P4 2050, P6 375 |

## Benchmarks

The bench draws 10^5 random products of up to 40 of 2, 3, 5 and 7
within 10^18, a tenth of them times 11, all of them first, then
answers each 20 times by the ★ arm in all five languages; C writes
each answer into a fresh buffer. Every implementation prints `100000
numbers, 20 rounds: 26197600 digits, checksum 137199790`.

BENCHTAB

## Verification

All five arms print the same output as `product.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The harness, as first written, folded the answer's bytes with `(check
* 31 + (b as i64))`, and `karac check` reported `lossless_cast`, "'u8'
widens to 'i64' implicitly here"; `karac fix` took the cast and, since
kara 0d28296389, its parentheses, leaving `check * 31 + b`. The memo arm's
`match winner { .., Some(w) => .. }` moved the `String` out, and
`karac check` reported E0500 at the later `winner.clone()`, "a binding
in that pattern moves its part out; bind it as `ref name`", as Rust's
E0382 would; `karac fix` wrote `Some(ref w)`. The other arms checked
clean. The harness's second batch first drew products of up to 60
primes, 3000 of them, which the memo arm, with up to some 10^4 states a
number, took minutes to answer under the interpreter; it draws 300 of
up to 40.

LeetCode's Rust template took 5 `karac fix` edits in one run:
`struct Solution {}` added for the `impl`; the `mut n: i64` parameter
became a plain one rebound with `let mut n = n;`; `String::new()`
became `String.new()`, and `Solution::` took `.`. The inclusive
`(2..=9).rev()` and `(b'0' + d as u8) as char` were accepted as
written.
