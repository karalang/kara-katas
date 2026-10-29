# 1019. Next Greater Node In Linked List

Given the head of a linked list with `n` nodes, find for each node the
value of the first node after it whose value is strictly larger. Return
the answers as an array, with 0 for a node that has no such next greater
node.

```
head = [2, 1, 5]        ->  [5, 5, 0]
head = [2, 7, 4, 3, 5]  ->  [7, 0, 5, 5, 0]
```

**Constraints:** `1 <= n <= 10^4`, `1 <= Node.val <= 10^9`.

## Approaches

The node type is a `shared struct`, Kāra's reference-counted form, as
in kata 876.

| file | mechanism |
|---|---|
| `next_greater.kara` ★ | a stack of waiting nodes: walk the list once, keeping the positions still waiting for a greater value on a stack whose values fall from bottom to top; each new value answers and pops every waiting position below it, then waits itself. O(n) |
| `next_greater_backward.kara` | from the back: copy the values out and go from last to first with a stack of candidates, popping those no greater than the current value; the top is its answer. O(n) |
| `next_greater_scan.kara` | a walk from each node: the statement as written, walking on from each node until a greater value or the end. O(n^2) on a falling list |
| `next_greater_reverse.kara` | reversing the list: turn the list around in place, answer it from its old last node with the candidate stack, turn it back to leave it as it was, and put the answers in order. O(n), no copy of the values |
| `next_greater_recursive.kara` | recursion to the end: recurse to the last node, and as the recursion unwinds give each node the top of the candidate stack its successors left. O(n), recursion as deep as the list |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for eight lists,
LeetCode's two examples among them; for five groups of random lists (10
to 3,000 nodes, values up to 3, 10, 1,000 or `10^9`), the sum of the
answers, how many are 0 and a checksum; and the answer sums for a
falling and a rising list of 3,000 nodes. `next_greater.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and checks 6,070
lists: every list of 1 to 6 values from 1 to 4 (5,460, so ties are
common), 600 random lists of 7 to 100 values and 10 of 1,000, with
values up to 3, 100 or `10^9`. Each arm gets a list of its own, built
from the values, and each list is also asked with a value above all of
them added at the end and with every value `v` made `3v + 1`.

| | property |
|---|---|
| P1 | the statement read literally, on the values |
| P2 | one answer per node, and the list left as the arm found it |
| P3 | an answer is 0 exactly when no later value is greater, and otherwise is greater than its node's value |
| P4 | a value above all of them at the end answers every 0 and changes no other answer |
| P5 | `v -> 3v + 1` keeps the order, so it maps the answers the same way |
| P6 | each arm agrees with at least two of the other four |

An arm that fails P2 is not checked for P3 to P6 on that list. The
differential prints `6070 lists: checksum 462257511, 182100 checks over
5 arms: 0 failures` under `karac __mir-run` (17 s) and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Thirty edits to the differential, each run under `karac __mir-run` and
`karac __mir-llvm-run`; fifteen are kept, three to each arm, all
fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal value taken as greater | P1 5402, P3 5402, P6 5402 |
| M2 | ★: the bottom of the stack compared | P1 4308, P3 3886, P6 4308 |
| M3 | ★: every value read one high | P1 5861, P4 6070, P5 5861, P6 5861 |
| M4 | backward: the first node skipped | P1 4204, P3 4204, P4 6070, P6 4204 |
| M5 | backward: one pop per node | P1 4308, P3 4308, P6 4308 |
| M6 | backward: the last node skipped | P1 2329, P3 2329, P4 6070, P6 2329 |
| M7 | scan: the last greater value kept, not the first | P1 3361, P4 5861, P6 3361 |
| M8 | scan: only the next node looked at | P1 3801, P3 3801, P4 6055, P6 3801 |
| M9 | scan: greater by 2 or more | P1 4460, P3 4088, P4 6070, P5 4460, P6 4460 |
| M10 | reverse: the list not put back | P2 6066 |
| M11 | reverse: the answers left backwards | P1 5629, P3 5584, P4 6070, P6 5629 |
| M12 | reverse: the list never turned | P1 5782, P2 6066, P4 4 |
| M13 | recursive: the bottom of the stack taken | P1 2476, P4 5861, P6 2476 |
| M14 | recursive: the position never advanced | P1 5566, P3 5566, P4 6066, P6 5566 |
| M15 | recursive: the answer's slot added on the way back | index out of bounds panic, exit 101 |

P1 kills thirteen, P6 twelve, P4 ten, P3 nine, and P2 and P5 two each;
M15 is killed by its bounds check. P2 alone catches M10, which answers
correctly but leaves the list reversed; only the four one-node lists,
which read the same either way, get past P2 to the later checks. M12
turns the list around once, at the end, so it answers the list forwards
with a stack that expects it backwards. The checks draw no random
number that depends on an answer, so every mutant sees the same lists
and their counts can be compared.

Fifteen other edits were tried and set aside, none of them equivalent.
Seven failed exactly the same checks as a kept one: backward, scan,
reverse and recursive taking an equal value as greater (as M1); ★
answering one waiting node per value (as M8); and backward and reverse
taking the bottom of the stack (as M13). The other eight were killed
too, beyond three per arm, in two families that fail alike: five that
miss every greater value (★ with nothing waiting and backward, reverse
and recursive pushing nothing, which answer 0 throughout, and scan
taking the node's own value where it finds a greater one), and three
that answer a node's own value when nothing is greater (★, scan and
recursive).

## Verification

Every arm prints the same output as `next_greater.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error; the differential prints its line under all three. `karac
check --output=json` reports no diagnostic for the five arms, the
differential and the bench program, so `karac fix` had nothing to do.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. The release build is kara `56c60bdf7c`, with
runtime archives rebuilt at `ce706dd131`, the last commit before it to
change the runtime. Under `karac __mir-run` the arms take 1.1 s
(backward) to 18.6 s (scan, on the falling list of 3,000).

The reverse arm first ended with a bare `reversed(tail_first);`, and
`karac check` warned that a discarded `Option` is `#[must_use]`, with a
hint to write `let _ = ...`; the arm does that now, with a comment on
why the result is not needed. No compiler gap turned up.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench builds 500 random lists of 1 to 10,000 nodes (LeetCode's
sizes, 2,403,221 nodes in all) once in all five languages and answers
each list 10 times, folding the answers into a sum and a checksum. The
Rust version uses `Option<Box<ListNode>>`, LeetCode's Rust signature,
walked by reference, and C a `malloc` per node. Every implementation
prints `500 lists, 2403221 nodes, 10 rounds: answer sum 524976783,
checksum 766902419`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with karac as above:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.565 to 0.676 s | 0.636 s |
| Rust (`rustc -O`) | 0.668 to 0.873 s | 0.715 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.697 to 0.839 s | 0.724 s |
| Go | 1.290 to 1.445 s | 1.381 s |
| Python | 10.3 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.675 to 0.795 s | 0.742 s |
| Kāra (`karac build`) | 0.662 to 0.741 s | 0.710 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time stays below its real time) and runs as fast as the
sequential one.

v2 took 1.02 times Rust's median time under overflow checks and 1.17
times C's. The walk is one dependent load after another in every
language, and each node in Kāra is reference-counted, so its walk also
touches each node's count (kata 876 read that from the disassembly; not
re-read here). Go's user time is twice its real time, its collector
running beside the program; we did not measure how much of its time
that is.
