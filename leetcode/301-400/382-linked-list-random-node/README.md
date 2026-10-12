# 382. Linked List Random Node

Given a singly linked list, return a random node's value; every node
must be equally likely.

- `Solution(head)` keeps the list;
- `get_random()` returns the value of a node chosen uniformly at random.

```
Solution([1, 2, 3])
get_random() -> 1, 2 or 3, each with probability 1/3
```

**Constraints:** `1 <= number of nodes <= 10^4`;
`-10^4 <= Node.val <= 10^4`; at most `10^4` calls to `get_random`.
**Follow-up:** the list is too long to copy and its length is not known
in advance.

## Approaches

Every arm uses `shared struct ListNode { val: i64, next:
Option[ListNode] }` and draws its random numbers from the same seeded
LCG, as `below(n)`, a number from 0 to n - 1.

| file | mechanism | per draw | extra space |
|---|---|---|---|
| `linked_list_random.kara` ★ | reservoir sampling: the i-th node replaces the kept value with probability 1/i, so after one walk every node was kept with probability 1/n; answers the follow-up | O(n) | O(1) |
| `linked_list_random_vec.kara` | copy the values into a `Vec` once, then draw one position | O(1) | O(n) |
| `linked_list_random_count.kara` | count the nodes once, then walk to a random index | O(n) | O(1) |
| `linked_list_random_recursive.kara` | the ★ arm's walk as a recursion that passes the kept value along | O(n) | O(n) stack |
| `differential.kara` | the four arms against the list's own values, 300 random lists, five properties | — | — |

The arms spend their random numbers differently (one per node for the
reservoir arms, one per draw for the others), so they draw different
values. Every arm therefore prints the same 6 lines of properties
rather than the draws: a chi-square test of 30,000 draws from the
LeetCode example, a one-node list that always gives its value, lists
with repeated and negative values, a list of 1,000 nodes over 37
values, and how many of 200 random lists of 1 to 60 nodes pass the
test. The test (`fair`) checks that every draw is in the list and that
the chi-square statistic against the list's own counts is below
`dof + 6 * sqrt(2 * dof) + 12`, far in the tail for its degrees of
freedom. `linked_list_random.py` mirrors the ★ arm, draws the same
values, and prints the same lines.

The recursive arm's `get_random` first copies the head handle,
`let head = self.head;`, and passes that to the recursion. Passing
`self.head` directly lends from `self` while `pick` changes the seed
through `mut ref self`, and the MIR borrow checker refuses it (E0516),
as Rust would; see Compiler findings.

## Differential

`differential.kara` holds copies of the four arms behind one enum. It
builds 300 random lists of 1 to 12 nodes with values from -3 to 3, so
that values repeat, and gives each list to all four arms.

| | property |
|---|---|
| P1 | every draw is a value of the list |
| P2 | a one-node list always gives its value |
| P3 | every value in the list comes up within 60 draws per node |
| P4 | over 100 draws per node, the chi-square statistic against the list's own counts is below the bound above |
| P5 | drawing leaves the list as it was |

It prints `300 lists, 510828 checks, 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`. The legacy backends cannot run it; see
Compiler findings.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | reservoir: keeps the i-th node with probability 1/(i+1) | P1, P2 and P4, 5170 failures |
| M2 | reservoir: never replaces a value once kept | P3 and P4, 1119 failures |
| M3 | copy: never draws the last position | P3 and P4, 359 failures |
| M4 | copy: keeps each value's absolute value | P1 to P4, 19884 failures |
| M5 | count: counts one node too many | P1, P2 and P4, 5371 failures |
| M6 | count: walks only half as far | P3 and P4, 677 failures |
| M7 | recursive: the node number does not advance | P3 and P4, 1271 failures |
| M8 | recursive: numbers the first node 2 | P1, P2 and P4, 5170 failures |

M1 and M8 are the same mistake in two arms, and give the same counts:
with the first node numbered 2, nothing may be kept, and the draw is the
starting value 0.

## Verification

All four arms print the same output as `linked_list_random.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`
(the same MIR compiled to LLVM), and `karac check` passes on every
file. The legacy backends (`karac run --interp`, LLJIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build`) refuse every arm before running;
see Compiler findings.

## Benchmarks

The bench program uses the ★ arm on one list of 10,000 nodes, the
problem's largest, with values from an LCG, and folds 20,000 draws into
a checksum: 200,000,000 node visits. The Rust mirror uses `Rc` nodes,
as Kāra's `shared struct` is reference-counted, and clones the handle
at each step as the Kāra walk does; C and Go use plain pointers. All
five mirrors, `karac __mir-llvm-run` and the legacy `karac build` print
`checksum 480076171`. Spot timings on a shared 4-core container: C
0.79 s, Rust 0.73 s, Go 1.0 s, Python 49 s, the legacy `karac build`
0.49 s, and `karac __mir-llvm-run` 5.0 s with a debug-built `karac`'s
compile included. `karac __mir-llvm-run` JITs the IR without LLVM's optimization
passes, through a debug-built runner, so its times show that the new
backend runs the program, not how fast it will be. `bench.sh` timings need a quiet
machine.

## Compiler findings

Nothing filed. One check gap already reported, and one in the legacy
backends, which are frozen:

- **`karac check` accepts the borrow conflict the MIR borrow checker
  refuses.** `self.pick(self.head, 1, 0)` inside a `mut ref self`
  method passes `check` and stops `karac __mir-run` with `mutable borrow
  of (*_1) while it is borrowed`. Thread A has this class of gap (check
  not running the MIR borrow checker) in hand.
- **The legacy typechecker refuses `*v` on the items of
  `values.iter()`.** Every arm's test harness walks a `ref Vec[i64]`
  with `for v in values.iter()` and reads `*v`, and `karac run --interp`
  and LLJIT stop with `unary '*' requires 'ref T' ... found 'i64'`; the
  native builds fail the same way. `karac check` and both MIR backends
  accept it. The bench program has no such loop, and the legacy
  `karac build` runs it correctly.
