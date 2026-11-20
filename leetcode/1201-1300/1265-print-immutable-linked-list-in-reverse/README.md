# 1265. Print Immutable Linked List in Reverse

You are given an immutable linked list. Print out all values of each node
in reverse with the help of the following interface:

- `ImmutableListNode`: an interface of an immutable linked list; you are
  given the head of the list.

You need to use the following functions to access the linked list (you
can't access the `ImmutableListNode` directly):

- `ImmutableListNode.printValue()`: print the value of the current node.
- `ImmutableListNode.getNext()`: return the next node.

The input is only given to initialize the linked list internally. You
must solve this problem without modifying the linked list: operate on it
using only the functions above.

```
head = [1,2,3,4]          ->  [4,3,2,1]
head = [0,-4,-1,3,-5]     ->  [-5,3,-1,-4,0]
head = [-2,0,6,4,4,-6]    ->  [-6,4,4,6,0,-2]
```

**Constraints:** the length of the list is between 1 and 1000; the value
of each node is between -1000 and 1000.

**Follow up:** could you solve it in constant space? In linear time and
less than linear space?

The judge's interface is `trait ImmutableListNode { fn print_value(self);
fn get_next(self) -> Option[dyn ImmutableListNode]; }`, and the arms are
`fn print_linked_list_in_reverse(head: dyn ImmutableListNode)`. The
harness's node is a `shared struct Node` holding its value, its next node
and a `shared` record of what has been printed, which `print_value`
appends to; `get_next` hands out the next node as a `dyn` value.

## Approaches

| file | mechanism |
|---|---|
| `print_linked_list_in_reverse.kara` ★ | by recursion: a node prints after everything after it has. O(n) time and O(n) stack |
| `print_linked_list_in_reverse_stack.kara` | by a stack: the nodes after the head kept in a `Vec[dyn ImmutableListNode]` on the way down, printed by `iter().rev()`, then the head |
| `print_linked_list_in_reverse_constant.kara` | in constant space, the first follow-up: the list counted, then for each place from the last a walk from the head to it. O(n^2) time |
| `print_linked_list_in_reverse_blocks.kara` | in blocks, the second follow-up: blocks of about sqrt(n) nodes, the first node of each kept on the way down, and each block printed from the last by a stack of its own. O(n) time and O(sqrt(n)) space |
| `print_linked_list_in_reverse_halves.kara` | by halves: a stretch prints its second half in reverse, then its first, the second half found by walking from the stretch's first node. O(n log n) time and O(log n) stack |
| `print_linked_list_in_reverse_solution.kara` | a Rust solution written against the interface as a Rust trait (`Box<dyn ImmutableListNode>`, `&self`), a stack popped to print, carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's three examples; 1000 random
lists of 1 to 60 values from -1000 to 1000 (`1000 random lists: 30003
values printed, checksum 605929418`); and the constraints' top, a list of
1000 nodes. `print_linked_list_in_reverse.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the stack, constant, blocks and halves arms checked clean
as first written, and so did the ★ arm once its harness did (below). The
solution arm takes one round of fixes, 13 by `karac fix`'s count: `&self`
to `self`, `Option<..>`, `Vec<..>` and `Box<..>` to brackets with
`Box<dyn ImmutableListNode>` to `dyn ImmutableListNode`, `struct
Solution;` to `struct Solution {}`, and `::` to `.`. Two repairs were by
hand. Rust's `head: Box<dyn ImmutableListNode>` is owned, and `let mut
cur = Some(head);` moves it; in Kāra a bare parameter borrows, so `cur`
was an `Option[ref dyn ImmutableListNode]` and `cur = node.get_next()`
got a bare E0200 that named neither the borrowed parameter nor the `own`
that fixes it (B-2026-11-20-85). And the method's `pub`, which Rust's
`impl Solution` carries, is dropped: a public method declares its effects,
and a call through the `dyn` nodes `get_next` hands out, whose type writes
no clause, has every effect; a private one infers them. The E0400 offered
a fix declaring `with allocates(*) blocks reads(*) ...`, which does not
parse, and `karac fix` refused its own edit (B-2026-11-20-84, fixed
now). All six check clean.

## Gaps

Three gaps were met; two are fixed now.

- **A `shared` handle read through a borrow could not become a `dyn`
  value** (B-2026-11-20-83, fixed at FIX2012). The judge's natural
  `get_next`, `match self.next { Some(n) => Some(n), None => None }` into
  an `Option[dyn ImmutableListNode]`, got E0313 ("cannot move 'n': it
  borrows its value ... This type has no `.clone()`"), though `Node` is a
  counted handle and the same `match` into an `Option[Node]` checked
  clean; past it, MIR made the `dyn` from the reference, and the borrow
  check refused it with E0509, as it did a borrowed `shared` parameter
  returned or pushed as a `dyn`. The `dyn` is now made from a counted copy.
  `self.next.map(|n| n)` is still refused: a closure's result is not a
  place a value becomes `dyn` (design.md § `dyn Trait` lists a `let`, an
  argument, a field, a return and an element), and the `match`, `if let`
  and `?` spellings check clean.
- **E0400's every-effect clause** (B-2026-11-20-84, fixed at FIX2013),
  above.
- **`Some(head)` over a borrowed parameter** (B-2026-11-20-85, open),
  above.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the values from the last node to the first. 2000 random lists,
a third of 1 to 8 nodes, a third of 1 to 120, and a third of 1 to 120
nodes holding only -1, 0 and 1; each node also records its place when it
prints.

| | property |
|---|---|
| P1 | the statement read literally: the values from the last node to the first |
| P2 | every node printed exactly once |
| P3 | the places printed run from the last to the first |
| P4 | printed twice, the same twice |
| P5 | the list cut in two at random prints the back's reverse, then the front's |
| P6 | the ★ arm's answer |

All 72,000 checks pass on every arm: `2000 lists: checksum 130693051,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the same
checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the head printed before the rest | P1 1909, P3 1912, P5 1706, P6 9545 |
| S2 | ★: the next node printed, not recursed into | P1 1797, P2 1797, P3 1797, P5 1645, P6 8985 |
| K1 | stack: the kept nodes printed first to last | P1 1790, P3 1797, P5 1640, P6 1790 |
| K2 | stack: the head never printed | P1 2000, P2 2000, P3 2000, P5 1709, P6 2000 |
| C1 | constant: the walks start at the second place | P1 1912, P2 1912, P3 1912, P5 1576, P6 1912 |
| C2 | constant: each walk one step short | P1 1793, P2 1797, P3 1797, P5 1555, P6 1793 |
| B1 | blocks: the blocks printed first to last | P1 1702, P3 1708, P5 1621, P6 1702 |
| B2 | blocks: each block after the head's one node short | P1 1335, P2 1335, P3 1335, P5 1254, P6 1335 |
| H1 | halves: the first half printed before the second | P1 1909, P3 1912, P5 1706, P6 1909 |
| H2 | halves: a stretch of two printed as its first node | P1 1912, P2 1912, P3 1912, P5 1529, P6 1912 |
| O1 | solution: every other node skipped on the way down | P1 1912, P2 1912, P3 1912, P5 925, P6 1912 |
| O2 | solution: the last node popped and dropped | P1 2000, P2 2000, P3 2000, P5 1709, P6 2000 |

All twelve are caught, every one by P1, the statement read literally, and
by P3, the places printed. P1 counts a little below P3 where the values
repeat: on the lists of only -1, 0 and 1, a wrong order can print the
right values. P2, every node printed once, sees the eight that drop or
repeat a node and none of the four that only reorder (S1, K1, B1, H1). P4,
printing twice, catches none: no arm keeps state between calls.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (by recursion: a node prints after everything after it has, every
call through the `dyn` interface) on 100 random lists of 1000 nodes
built once, 300 rounds; everything each round prints folded into a
checksum. Every program prints `300 rounds of 100 lists of 1000 nodes:
checksum 164974457`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.244 to 1.354 s | 1.265 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.227 to 1.326 s | 1.265 s |
| Rust (`rustc -O`) | 0.718 to 0.788 s | 0.730 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.694 to 0.749 s | 0.710 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.693 to 0.743 s | 0.707 s |
| C (`clang -O3`) | 0.632 to 0.682 s | 0.646 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.631 to 0.675 s | 0.643 s |
| Go | 0.667 to 0.707 s | 0.680 s |
| Python | 7.594 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.8x Rust with overflow checks on's time (1.265
s against 0.710 s). Kāra takes about 2.0x C's time (1.265 s against
0.646 s); Kāra takes about 1.9x Go's time (1.265 s against 0.680 s).
Python takes about 6x Kāra's time. No profile was taken.
