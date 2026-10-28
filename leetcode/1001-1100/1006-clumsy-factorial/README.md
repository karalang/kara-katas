# 1006. Clumsy Factorial

The factorial of a positive integer `n` is the product of all positive
integers less than or equal to `n`. We make a *clumsy factorial* using
the integers in decreasing order by swapping out the multiply
operations for a fixed rotation of operations: multiply `*`, divide
`/`, add `+`, and subtract `-`, in this order. For example,
`clumsy(10) = 10 * 9 / 8 + 7 - 6 * 5 / 4 + 3 - 2 * 1`.

The usual order of operations of arithmetic applies: all
multiplication and division steps are done before any addition or
subtraction, and multiplication and division are processed left to
right. The division is floor division, so `10 * 9 / 8 = 90 / 8 = 11`.

Given an integer `n`, return *the clumsy factorial of* `n`.

```
n = 4    ->  7       (4 * 3 / 2 + 1)
n = 10   ->  12      (10 * 9 / 8 + 7 - 6 * 5 / 4 + 3 - 2 * 1)
```

**Constraints:** `1 <= n <= 10^4`.

Every product and quotient is of positive numbers, so floor division
and Kāra's `/`, which truncates toward zero, agree. The stack arm
divides a negated term, and truncating it gives what dividing the
positive term and negating it gives, which is how the expression
reads.

## Approaches

The operators repeat every four numbers, so the expression is a first
group `n * (n-1) / (n-2) + (n-3)` followed by groups that subtract
their product-quotient and add their fourth number. Two arms evaluate
it as a stack and as groups, one recurses over the groups, one writes
the expression out as text and parses it, and one uses a closed form.

| file | mechanism |
|---|---|
| `clumsy.kara` ★ | a stack of terms: `*` and `/` fold the next number into the top term, `+` pushes it and `-` pushes its negation; the answer is the sum of the stack. O(n) |
| `clumsy_groups.kara` | groups of four: each group's product-quotient is added for the first group and subtracted after, and its fourth number added; the last group may stop after one, two or three numbers. O(n) |
| `clumsy_formula.kara` | a closed form: for `a >= 5`, `a * (a-1) / (a-2)` is `a + 1`, so every later full group adds -4 and the answer depends only on `n % 4`, with the first four `n` listed. O(1) |
| `clumsy_recursive.kara` | recursion over groups: one call takes a group and leaves the expression from `x - 4`, its first group subtracted, to the next. O(n) time, `n / 4` calls deep |
| `clumsy_parse.kara` | write it out and parse it: the text `10*9/8+7-6*5/4+3-2*1`, evaluated with a stack of numbers and a stack of waiting operators, each operator first applying every waiting one of the same or higher precedence. O(n) in the text's length |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; every `n`
from 1 to 16 on one line, which covers the four cases of `n % 4` and
the four small `n` the closed form lists; LeetCode's largest, 10,000,
and the three below it; and totals over every `n` up to 1,000 and over
200 random `n` up to 10,000. `clumsy.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: it writes out the numbers and operators, then applies
the leftmost `*` or `/` while there is one, and then the leftmost `+`
or `-` while there is one, each time replacing two numbers and their
operator by the result. It checks every `n` from 1 to 300 against the
statement and 60 random `n` up to 10,000 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, for every `n` up to 300 |
| P2 | from `n = 9` on, the answer is the answer for `n - 4` plus 4 |
| P3 | from `n = 5` on, the answer is `n - 1`, `n + 1` or `n + 2` |
| P4 | at most the first group alone, and exactly it when `n <= 4` |
| P5 | always positive |
| P6 | each arm agrees with at least two of the other four |

P2 holds because four more numbers at the front make one more full
group, `-(a+1) + (a-3)` once its product-quotient is taken whole, and
P4 because every later group subtracts more than it adds. P2 starts at
9, not 8, because `4 * 3 / 2` is 6, not 5: the closed form's `a + 1`
needs `a >= 5`.

It prints `360 values of n: answers sum to 322986, checksum 298040534,
10440 checks over 5 arms: 0 failures` under `karac __mir-run` (11.7 s,
most of it the parse arm's long texts) and `karac __mir-llvm-run`, and
the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-seven edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `-` pushes the number, not its negation | P1 296, P2 352, P3 356, P4 356, P6 356 |
| M2 | ★: `/` undone by a `*` | P1 297, P2 352, P3 356, P4 15, P5 341, P6 357 |
| M3 | ★: the operators repeat every three | P1 296, P2 352, P3 356, P4 355, P6 356 |
| M4 | groups: the fourth number subtracted | P1 297, P2 352, P3 356, P4 1, P5 354, P6 357 |
| M5 | groups: divided by the number before | P1 296, P2 352, P3 349, P4 2, P6 356 |
| M6 | groups: `*` read as `+` | P1 298, P2 352, P3 352, P4 343, P6 358 |
| M7 | formula: `n % 4 == 3` gives `n + 1` | P1 74, P6 91 |
| M8 | formula: `n = 4` gives 5 | P1 1, P4 1, P6 1 |
| M9 | formula: `n % 4 == 0` gives `n + 2` | P1 74, P6 86 |
| M10 | recursive: a short group's number added again | P1 225, P3 179, P4 3, P6 273 |
| M11 | recursive: groups of three | P1 295, P2 123, P3 353, P4 1, P6 355 |
| M12 | recursive: a last lone number dropped | P1 75, P3 86, P4 1, P5 1, P6 87 |
| M13 | parse: the text one number short | P1 298, P2 352, P3 356, P4 2, P5 91, P6 358 |
| M14 | parse: `/` at `+`'s precedence | P1 293, P2 352, P3 353, P5 352, P6 353 |
| M15 | parse: equals right to left | P1 260, P2 352, P3 226, P4 1, P6 315 |

P1 and P6 kill all fifteen, P3 and P4 twelve each, P2 ten and P5 five.
The checks draw no random number that depends on an answer, so every
mutant sees the same `n` and their counts can be compared. The closed
form's edits are the hardest to see: each is wrong on one residue of
`n % 4`, or on one small `n`, and keeps the answer within one or two of
`n`, so only the statement and the other arms catch M7 and M9, and M8
fails P4 only because `n = 4` is the one place P4 asks for equality.
P2 fails all 352 of its checks on most edits that break the general
case, since it compares an arm with itself four numbers on and those
edits break that relation at every `n`; M11's groups of three fail it
on 123.

Twelve other edits were tried and set aside. Two change no answer: the
groups arm skipping the multiply when the next number is 1, and the
recursive arm skipping the divide when it is 1. Five failed exactly
the same checks as a kept one: the groups arm adding later groups, or
adding every group's term, and the recursive arm carrying its sign,
all as M1; and the closed form's `n = 2` falling to the general case
and `n = 3` giving 5, as M8. Five were killed but beyond three an arm:
the ★ operators starting at `/` and the ★ last number left out, the
groups arm subtracting its first group and adding later ones, and the
parse arm's `-` backwards and its operators starting at `/`, the last
failing the same checks as the ★ arm's own.

## Verification

Every arm prints the same output as `clumsy.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build was kara `f03a023547` with the fix that
landed as `f59be6dac3` (below), and the runtime archives were rebuilt at
`f03a023547`. Under `karac __mir-run` the arms take 0.2 s (formula) to
24 s (parse).

The parse arm found B-2026-10-28-30 in kara: `text = text + ops[i] +
(n - x).to_string()` copied `text` on every add, because the overflow
check on `n - x` sits between the borrow of `text` and the add, and
kara's pass that lets an add take its left string stopped at the
check's branch. Built, the arm took 1.05 s before the fix and 0.13 s
with it; under `karac __mir-run` it takes 23.7 s either
way, since the interpreter's add copies regardless.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages: four rounds over every
`n` from 1 to 10,000, LeetCode's largest, the even rounds upward and
the odd ones downward, folding every answer into a checksum. Every
implementation prints `4 rounds over every n up to 10000: answers sum
to 200060008, checksum 798503022`. A call for `n` pushes about `n / 2`
terms onto a fresh stack and divides `n / 4` times, so the run does
about 200 million steps, a quarter of them 64-bit divisions.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with the same karac:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.539 to 0.579 s | 0.553 s |
| Rust (`rustc -O`) | 0.537 to 0.582 s | 0.549 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.554 to 0.597 s | 0.572 s |
| Go | 1.418 to 1.651 s | 1.549 s |
| Python | 36.1 s | |
| Kāra (`karac build`) | 0.555 to 0.666 s | 0.566 s |

`bench.sh` builds the Kāra program with `karac build`, which is the v2
compiled backend since M3. Python's run is about 64 times Kāra's.

v2 took 0.99 times Rust's median time under overflow checks and 1.02
times C's: the divisions dominate every compiled version. Under
valgrind's cachegrind v2 ran 6,058 million instructions, Rust with
overflow checks 5,483 million, Rust without them 5,209 million and C
4,820 million. Go took 2.8 times C's time; we did not look into why.
