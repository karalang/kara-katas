# 2241. Design an ATM Machine

There is an ATM machine that stores banknotes of `5` denominations:
`20`, `50`, `100`, `200` and `500` dollars. Initially the ATM is empty.
The user can use the machine to deposit or withdraw any amount of
money.

When withdrawing, the machine prioritizes using banknotes of **larger**
values. For example, if you want to withdraw `$300` and there are `2`
`$50` banknotes, `1` `$100` banknote and `1` `$200` banknote, the
machine will use the `$100` and `$200` banknotes. However, if you try to
withdraw `$600` and there are `3` `$200` banknotes and `1` `$500`
banknote, the request will be rejected, because the machine will first
try to use the `$500` banknote and then be unable to complete the
remaining `$100`. The machine is **not** allowed to use the `$200`
banknotes instead of the `$500` banknote.

Implement the ATM class:

- `ATM()` initializes the ATM object.
- `void deposit(int[] banknotesCount)` deposits new banknotes in the
  order `$20`, `$50`, `$100`, `$200` and `$500`.
- `int[] withdraw(int amount)` returns an array of length `5` of the
  number of `$20`, `$50`, `$100`, `$200` and `$500` banknotes that will
  be handed to the user, in that order, and updates the number of
  banknotes in the ATM after withdrawing. Returns `[-1]` if it is not
  possible, and does **not** withdraw any banknotes in this case.

```
deposit([0,0,1,2,1]), withdraw(600), deposit([0,1,0,1,1]), withdraw(600), withdraw(550)
    ->  [0,0,1,0,1], [-1], [0,1,0,0,1]
```

**Constraints:** `banknotesCount.length == 5`; `0 <= banknotesCount[i]
<= 10^9`; `1 <= amount <= 10^9`; at most `5000` calls in total to
`withdraw` and `deposit`; at least one call to each.

A withdrawal takes as many of each banknote as fit, largest first, into
a plan; only when the plan pays the whole amount is it taken from the
counts. O(1) a call. The counts can reach 2.5 * 10^12, so they are
`i64`.

## Approaches

| file | mechanism |
|---|---|
| `atm.kara` ★ | `struct Atm { counts: Vec[i64] }`, smallest first; `withdraw` fills a separate `plan` with `(left / values[i]).min(self.counts[i])` from the largest down and subtracts it from the counts only when nothing is left |
| `atm_map.kara` | a `SortedMap[i64, i64]` from each banknote's value to its count, walked from the top with `iter().rev()`; the plan a `SortedMap` of the same keys, written back over the counts by key and answered as `plan.values().collect()` |
| `atm_result.kara` | refusal as a value: a `const VALUES: Array[i64, 5]`, the counts an `Array[i64, 5]`, `plan` (`ref self`) returning `Result[Vec[i64], Unpaid]`, and `withdraw` a `match` that takes the plan on `Ok` and answers `[-1]` on `Err` |
| `atm_enum.kara` | an `enum Note` of the five banknotes with `value` and `slot`, listed largest first by `Note.largest_first()`; a `struct Drawer` of a note and how many are held, `take` saying how many of it go toward an amount; deposits and refunds through `iter_mut` over the drawers |
| `atm_iter.kara` | iterator chains: a deposit `zip`s the counts with the banknotes and `map`s them to sums; a withdrawal `scan`s the banknotes from the largest down carrying the amount left, `rev`s what it takes into the answer's order, and `zip`s, `map`s and `sum`s it to see whether it pays |
| `atm_solution.kara` | LeetCode's Rust template: `struct ATM { cnt: [i64; 5] }` beside `const VAL: [i64; 5]`, `&mut self` methods taking `Vec<i32>` and `i32`, `std::cmp::min`, `vec![0; 5]` and `vec![-1]`, the counts cast between `i32` and `i64`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's example and five more
call sequences (one of each banknote short of 890, an empty machine, the
greedy `$500` that leaves `$100` unpaid though three `$200`s would do,
refusals that must leave the machine as it was, and every banknote at
the constraints' largest count), each with its answers; then how many
withdrawals are paid, with a checksum of the answers, for 3000 machines
of 1 to 30 calls (up to 1 to 6 of each banknote a deposit, amounts up to
10 to 3000), and for 4 machines of 5000 calls, the most the constraints
allow (up to 10^9 of each banknote, amounts up to 10^9, 10^6, 10^4 and
10^3). Three amounts in four are a multiple of 10. `atm.py` mirrors the
★ arm and its output is byte-identical.

`karac fix` carries the template in one round of 19 edits: `[i64; 5]`
to `Array[i64, 5]`, `ATM` to `Atm` (a type name is UpperCamelCase),
`&mut self` to `mut ref self`, `Vec<i32>` to `Vec[i32]`, `vec![0; 5]` to
`Vec.filled(5, 0)`, `vec![-1]` to `[-1]`, `std::cmp::min` to `min`, and
the two `as i64` removed, since an `i32` added to or taken from an `i64`
widens implicitly. The `take as i32` stays: it narrows.

Two arms were first written otherwise and `karac fix` mended them. The
enum arm listed its notes with `.to_vec()` and moved a `for` element of
them into a `Drawer`; `karac check` asked for `#[derive(Copy, Clone)]`
on `Note`, and the fix wrote it. The iter arm's `scan` closure wrote its
state through `*left -= ...`, as Rust's does; Kāra's `scan` takes the
state by value and returns `Some((next_state, item))`, and the fix
rewrote the closure that way.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the machine's banknotes handed out one at a time, always the
largest that is held and not more than the amount left, and all of them
put back if the amount is not reached; no division. It checks 300
random call sequences of 1 to 12 calls, up to 3 of each banknote a
deposit and amounts up to 1500; then 30 that deposit only `$200`s and
`$500`s; then 30 whose withdrawals ask for sums of banknotes from the
last deposit. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the banknotes handed out, read literally |
| P2 | each answer is `[-1]` or five counts, none negative, worth the amount |
| P3 | the refused withdrawals left out: the same answers for the rest |
| P4 | each deposit split in two, half and the rest: the same answers |
| P5 | no answer hands out more of a banknote than was deposited and not yet handed out |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 180142519, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that takes
each banknote by `divmod` from the largest down on a copy of the counts,
kept only when nothing is left over. On a failure it prints the first
ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under `karac __mir-llvm-run`, and the kept
ones under `karac __mir-run` too. Seventeen are kept, three to each
Kāra arm and two to the Rust-template arm. Each kept one is killed,
fails the same way under both backends and not by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a refusal still takes the plan from the counts | P1 52, P3 9, P6 52 |
| M4 | ★: a fifty worth forty | P1 166, P2 108, P6 166 |
| M6 | ★: a deposit replacing the counts | P1 110, P4 56, P6 110 |
| M8 | map: a banknote not taken left out of the answer | P1 174, P2 174, P6 174 |
| M10 | map: a deposit put in the drawers reversed | P1 87, P5 59, P6 87 |
| M11 | map: one banknote more than held | P1 138, P5 137, P6 138 |
| M12 | result: less than a twenty left counted as paid | P1 191, P2 191, P6 191 |
| M13 | result: a two hundred worth two fifty | P1 122, P2 103, P6 122 |
| M14 | result: the twenties never taken from the counts | P1 7, P5 7, P6 7 |
| M17 | enum: ten dollars short paid anyway | P1 175, P2 175, P6 175 |
| M18 | enum: the two hundreds before the five hundreds | P1 115, P6 115 |
| M19 | enum: the fifties in the twenties' slot | P1 201, P2 200, P6 201 |
| M22 | iter: the amount left cut by the count, not the money | P1 169, P6 169 |
| M23 | iter: the plan never reversed | P1 164, P5 1, P6 164 |
| M25 | iter: a banknote extra in each deposit | P1 109, P4 42, P5 108, P6 109 |
| M27 | solution: half of each count answered | P1 178, P2 178, P6 178 |
| M30 | solution: the five hundreds never taken from the counts | P1 9, P5 9, P6 9 |

P1 and P6 kill all seventeen, P2 seven, P5 six, P4 two and P3 one.
P3, which replays a sequence without its refusals, is there for the
one mistake a design like this invites, a refusal that still changes
the machine (M1). P4 splits every deposit in two, which a machine that
adds deposits cannot tell apart; only the kept edits whose deposit does
not add up, one that replaces the counts (M6) and one that adds a
banknote a call (M25), fail it. P5 tracks the banknotes from the answers
alone and so catches every edit that hands out what was never put in.

Of the thirty-one, fourteen were not kept, and none survives, crashes or
differs between the backends. One fails as a kept one does: the enum
arm's drawer handing out one more than it holds (M20) as the map arm's
(M11). Eight fail alike in groups of their own: the banknotes taken
smallest first in the ★, map and template arms (M2, M7, M29); half the
plan taken from the counts in the ★ and iter arms (M3, M26); and only an
overpaid amount refused in the map, iter and template arms (M9, M24,
M28). Five fail their own way and are left out for the count of three
(two for the template): the ★ arm's banknotes taken that are not held
(M5), the result arm's five hundreds never planned and its deposit
counted twice (M15, M16), the enum arm's hundred worth a hundred and
twenty (M21), and the template's five hundred worth a thousand (M31).

## Verification

Every arm prints the same output as `atm.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, enum and result arms take 0.8 s to
0.9 s, the template 1.3 s, the map arm 1.7 s, the iter arm 2.5 s, and
the differential 1.2 s.

## Benchmarks

The bench runs 200 machines of 5000 calls each, half deposits of up to
10^9 of each banknote and half withdrawals of a multiple of 10 up to
10^9, with the ★ arm in all five languages. A withdrawal's plan is a
fresh list in every language but C, which writes it into an array the
caller passes. Every implementation prints `200 machines of 5000 calls:
299908 withdrawals paid, checksum 114129197`.

BENCHTAB
