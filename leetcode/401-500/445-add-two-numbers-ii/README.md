# 445. Add Two Numbers II

You are given two non-empty linked lists representing two non-negative
integers. The most significant digit comes first and each node holds
one digit. Add the two numbers and return the sum as a linked list in
the same form. Neither number has a leading zero, except the number 0
itself.

```
l1 = [7,2,4,3], l2 = [5,6,4]  ->  [7,8,0,7]
l1 = [2,4,3],   l2 = [5,6,4]  ->  [8,0,7]
l1 = [0],       l2 = [0]      ->  [0]
```

**Constraints:** each list has 1 to 100 nodes; `0 <= Node.val <= 9`.
**Follow-up:** could you solve it without reversing the input lists?

## Approaches

Every arm is `fn add_two_numbers(l1: Option[ListNode], l2:
Option[ListNode]) -> Option[ListNode]` over `shared struct ListNode {
mut val: i64, mut next: Option[ListNode] }`. Addition starts at the
least significant digit, which the lists give last.

| file | mechanism |
|---|---|
| `add_two_numbers.kara` ★ | two stacks: push each list's digits, pop both together adding with a carry, and put each digit of the sum in front of those already made. O(m + n) time and extra space |
| `add_two_numbers_reverse.kara` | reverse both lists in place, add them as in #2 while putting each digit in front of the sum, then reverse the lists back. O(1) extra space besides the sum; it is the one arm the follow-up rules out |
| `add_two_numbers_recursive.kara` | count both lengths, then recurse down the longer list, stepping the shorter only once the digits left are equal in number; each call returns its carry and the sum after it. O(max(m, n)) stack |
| `add_two_numbers_nines.kara` | build the sum most significant first, remembering the last digit below 9: a place that carries raises that digit and turns the 9s after it into 0s. O(1) extra space besides the sum |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, five
edge cases (carries that make the sum one digit longer from either
side, 5 + 5, adding 0, and a carry through four 9s), and for 300 random
pairs of 1 to 100 digits, each digit a 9 half the time, the total
number of digits in the sums and a checksum. `add_two_numbers.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases of three numbers a, b and c of 1 to 40 digits (1 to
100 one time in ten), each digit a 9 half the time so that carries run
far. Each arm gets its own fresh lists, so an arm that changed its
inputs fails only its own checks.

| | property |
|---|---|
| P1 | a + b is the schoolbook sum of the two digit lists |
| P2 | b + a is the same |
| P3 | a and b are unchanged afterwards |
| P4 | a + 0 is a, and 0 + b is b |
| P5 | (a + b) + c is a + (b + c), and the schoolbook sum of a + b and c |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | stacks: a carry out of the top place is dropped | P1 98, P2 98, P5 238 |
| M2 | stacks: a place summing to exactly 10 does not carry | P1 1167, P2 1167, P5 1458 |
| M3 | reverse: the first list is not reversed back | P2 1458, P3 1497, P4 1497, P5 1497 |
| M4 | reverse: the carry is not added to the next place | P1 1482, P2 1482, P5 1499 |
| M5 | recursive: a carry of 1 out of the top place is dropped | P1 98, P2 98, P5 238 |
| M6 | recursive: a 9 in the shorter list adds as 0 | P1 1444, P2 1443, P4 16, P5 1496 |
| M7 | nines: only the first 9 after the raised digit becomes 0 | P1 441, P2 441, P5 863 |
| M8 | nines: an 8 also counts as a 9 | P1 1271, P2 1271, P5 1471 |

P3 sees only M3, the one mutant that leaves an input changed, and P1
does not see it at all: the sum M3 returns is right, and the damage
shows from the next call on the same list. P4 adds a single 0, which
never carries, so it misses every carry mutant; it catches M6 only
when b is the single digit 9 and so the shorter list. M1 and M5 fail
the same 98 cases, those whose sum is one digit longer than either
number. P5 kills every mutant, since it adds a sum that is itself the
result of the arm under test.

## Verification

All four arms print the same output as `add_two_numbers.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

On the frozen legacy backends the stacks, reverse and nines arms match
under `karac run --interp`, LLJIT and `karac build` (with and without
`KARAC_AUTO_PAR=1`). The recursive arm matches only under
`karac run --interp`: LLJIT segfaults, the `karac build` binary grows
past 5 GB without finishing, and the `KARAC_AUTO_PAR=1` build's output
differs. The differential prints `0 failures` under
`karac run --interp`, and its `karac build` binary runs out of memory.
Legacy is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random numbers of
1,000 to 2,000 digits once (each digit a 9 half the time), then 60
times over adds each number to the next. Every implementation prints
`60 rounds on 100 numbers: 10050120 digits, checksum 854674664`, the
Kāra program under `karac __mir-run` included (in 69 s).

The mirrors keep the ★ arm's structure. C frees each sum after reading
it, as Kāra drops it; Rust uses LeetCode's `Option<Box<ListNode>>` with
an iterative `Drop`. Spot timings on a shared 4-core container, three
runs each (two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.24 to 0.32 s |
| Rust (`rustc -O`) | 0.29 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.31 to 0.37 s |
| Go | 0.67 to 0.70 s |
| Python | 3.8 to 4.2 s |
| Kāra (legacy `karac build`) | 0.35 to 0.46 s |

The legacy build here is the bench program with its `.clone()`
workaround, on the frozen legacy compiler. The Kāra program prints the
same line under `karac __mir-llvm-run` in 2.4 s, compile included; that
JITs the MIR's IR without optimization passes, so it is not a
benchmark.

## Compiler findings

One new finding, filed as kara B-2026-10-12-26.

- **B-2026-10-12-26.** The bench program first added
  `add_two_numbers(numbers[i], numbers[(i + 1) % count])` over a
  `Vec[Option[ListNode]]`. `karac check` and both MIR backends refuse
  it with `E_INDEX_MOVE_NON_COPY`, as a move out of the vector, though
  a bare parameter borrows. The same index of a `Vec[Vec[T]]`,
  `Vec[String]` or `Vec[ListNode]` is accepted: D5 passes an `Option`
  of a `shared` type as a counted handle, and the index rule's
  exemption for handles covers the bare `shared` type only. The bench
  passes `numbers[i].clone()`; revert it to the plain index when the
  row is fixed.
