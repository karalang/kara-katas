# 2412. Minimum Money Required Before Transactions

You are given a **0-indexed** 2D integer array `transactions`, where
`transactions[i] = [cost_i, cashback_i]`.

The array describes transactions, where each transaction must be
completed exactly once in **some order**. At any given moment, you have
a certain amount of `money`. In order to complete transaction `i`,
`money >= cost_i` must hold true. After performing a transaction,
`money` becomes `money - cost_i + cashback_i`.

Return *the minimum amount of* `money` *required before any transaction
so that all of the transactions can be completed **regardless of the
order** of the transactions.*

```
transactions = [[2,1],[5,0],[4,2]]   ->  10
transactions = [[3,0],[0,3]]         ->  3
```

**Constraints:** `1 <= transactions.length <= 10^5`; `0 <= cost_i,
cashback_i <= 10^9`.

The worst order spends every losing transaction's loss before the one
transaction that needs the most beyond what is left: a losing one needs
its cashback on top of the losses, since its own loss is already among
them, and a gaining one its whole cost. The answer is the total loss
plus the largest of those.

## Approaches

| file | mechanism |
|---|---|
| `money.kara` ★ | the total loss, and the largest of the losing transactions' cashbacks and the gaining ones' costs. O(n) |
| `money_each.kara` | each transaction as the one that needs the most: the total loss less its own, plus its cost, the largest over all. O(n) |
| `money_worst.kara` | the worst order simulated: the losing transactions by cashback upward, then the gaining ones by cost downward, the most any cost exceeds what is left. O(n log n) |
| `money_binary.kara` | binary search on the money: an amount is enough when it survives the worst order, the least found by halving up to the sum of every cost. O(n log n + n log S) |
| `money_iter.kara` | iterators: the total loss by `filter`, `map` and `sum`, the need beyond it by `map(min)` and `max`. O(n) |
| `money_solution.kara` | LeetCode's Rust template: `Vec<Vec<i32>>` rows read by index, the loss summed as `i64` through `as` casts, the largest need kept as `i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one free
transaction; one losing and one gaining; only gains; `10^5`
transactions up to `10^9` and `10^5` up to 10; then 2000 random cases of
up to 12 transactions up to 20, with a checksum and the total of the
answers. `money.py` mirrors the ★ arm and its output is byte-identical,
and the mirror was checked on 5000 random cases of up to 6 transactions
against walking every order.

`check` first reports 2 errors on the template, and `karac fix` carries
it in one call, reporting 7 edits: `Vec<Vec<i32>>` given its brackets;
`struct Solution;` given its braces; and the `0i64` suffix and both `as
i64` casts removed, since an `i32` widens to `i64` implicitly. `let
(cost, back) = (t[0], t[1])` and `mx.max(back)` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every order of the transactions tried, each order walked for
the money it needs at the start, and the most any order needs. No worst
order and no formula. It checks 300 random cases of 1 to 6 transactions
up to 20, which the literal reading answers; then 30 of up to 3000 up to
`10^9`; then 30 of up to 3000 up to 10. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | up to 6 transactions, the answer is the literal reading's |
| P2 | at least every cost and the total loss, and at most the total loss plus the largest cost |
| P3 | the transactions in reverse: the same answer |
| P4 | a free transaction, `(0, 0)`, added: the same answer |
| P5 | every cost and cashback doubled: the answer doubled |
| P6 | each arm agrees with at least three of the other five |

P2 holds because each transaction must be affordable in an order that
puts it first, every loss must be paid from the start, and no
transaction needs more than its cost on top of the losses. P3 holds
because every order is considered anyway, P4 because a free transaction
needs nothing and changes nothing, and P5 because doubling every amount
doubles what every order needs.

The differential prints `360 cases: checksum 576415575, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and walks every permutation. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a loss of 1 taken as none | P1 27, P2 27, P5 57, P6 57 |
| M5 | ★: the larger of loss and need | P1 240, P2 111, P6 300 |
| M6 | ★: the first transaction skipped | P1 216, P2 119, P3 267, P6 256 |
| M7 | each: each transaction's own loss spent before it | P1 200, P6 235 |
| M9 | each: gains offsetting losses | P1 241, P2 240, P6 301 |
| M10 | each: only the last transaction's need | P1 168, P2 67, P3 290, P4 324, P6 228 |
| M13 | worst: the smallest gaining cost first | P1 96, P2 36, P6 132 |
| M14 | worst: the gaining transactions first | P1 193, P2 179, P6 253 |
| M15 | worst: a transaction's own cost not needed | P1 297, P2 218, P3 2, P4 47, P6 357 |
| M17 | binary: exact money refused | P1 239, P2 86, P5 299, P6 299 |
| M18 | binary: the losses by cashback downward | P1 103, P6 122 |
| M21 | binary: no cashback ever paid | P1 239, P2 268, P6 299 |
| M24 | iter: the smallest need taken | P1 246, P2 128, P4 240, P6 306 |
| M25 | iter: each loss counted one short | P1 243, P2 71, P5 303, P6 303 |
| M26 | iter: every transaction needing its cashback | P1 202, P2 150, P6 237 |
| M29 | solution: the need beyond the loss dropped | P1 294, P2 200, P6 354 |
| M31 | solution: cost and cashback swapped | P1 293, P2 281, P6 353 |

P1 and P6 kill all seventeen, P2 fifteen, and P3, P4 and P5 three
each. The two P2 misses, each transaction's own loss spent before it
(M7) and the binary arm's losses taken by cashback downward (M18), give
an answer inside P2's bounds but not the least one. P3, P4 and P5 hold
for most wrong answers too, since a mutant that orders or counts the
transactions wrongly usually does so the same way after the
transactions are reversed, a free one is added or everything is
doubled.

Of the thirty-one, fourteen were not kept. Five fail the same checks as
a kept one: a losing transaction needing its cost in the ★ arm and the
template (M2, M28) as the each arm's own loss spent before it (M7); the
★ arm's gaining transaction needing its cashback (M3) as the iter arm's
every transaction needing its cashback (M26); the worst arm's largest
cashback first (M12) as the binary arm's losses by cashback downward
(M18); and the binary arm's gains by cost upward (M19) as the worst
arm's smallest gaining cost first (M13). Eight fail apart from every
kept one and were left out because those arms keep their share
already: only the largest loss counted in the ★ and iter arms (M4,
M22), which fail alike; the each arm's transaction needing its cashback
(M8) and every transaction losing at least 1 (M11); the binary arm's
failed amount raising the bound by two (M20); the iter arm's larger of
cost and cashback needed (M23); and the template's gaining transactions
taken as losing (M27) and whole cost counted as loss (M30). The worst
arm's even transaction in both lists (M16) is not killed and cannot be:
a transaction whose cost equals its cashback changes nothing spent, and
its second visit, among the gains after every loss, needs at least as
much as its first.

## Verification

Every arm prints the same output as `money.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.3 to 2.7 s. The differential
takes 8.9 s there, 2.9 s under `karac __mir-llvm-asan` and 0.9 s under
`karac run`.

## Benchmarks

The bench builds 10 lists of `10^5` transactions, list `i`'s costs and
cashbacks up to `7^(i + 1)`, once from the harness's generator, then
makes 100 passes, answering every list and folding each answer plus the
pass into the checksum, with the ★ arm in all five languages. Every
implementation prints `100 passes over 10 lists of 10^5 transactions:
checksum 722290812`. The loop is one branch and two additions per
transaction; Kāra checks both additions for overflow, as `rustc -O -C
overflow-checks=on` does, and on this container the two ran in about
the same time, several times slower than plain `rustc -O` and C, which
do not check.

BENCHTAB
