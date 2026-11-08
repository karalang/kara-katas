# 2005. Subtree Removal Game with Fibonacci Tree

A Fibonacci tree is a binary tree created using the order function
`order(n)`: `order(0)` is the empty tree; `order(1)` is a binary tree with
only one node; `order(n)` is a binary tree that consists of a root node with
the left subtree as `order(n - 2)` and the right subtree as `order(n - 1)`.

Alice and Bob are playing a game with a Fibonacci tree with Alice starting
first. On each turn, a player selects a node and removes that node and its
subtree. The player that is forced to delete `root` loses. Given the integer
`n`, return `true` if Alice wins the game or `false` if Bob wins, assuming
both players play optimally.

```
n = 3  ->  true    (Alice takes node 1 in the right subtree; Bob is left to
                    take one of two nodes, and Alice the other)
n = 1  ->  false   (Alice must delete the root)
n = 2  ->  true    (Alice takes node 1; Bob must delete the root)
```

**Constraints:** `1 <= n <= 100`.

`order(100)` has about `10^21` nodes, so no arm builds the tree.

## Approaches

Removing a node with its subtree is cutting the edge above it, so the game
is Green Hackenbush on a rooted tree, played until the root stands alone. By
the colon principle a rooted tree is worth the nim-sum, over the root's
children, of each child's value plus one, and the player to move wins
exactly when the value is not 0. `order(k)` is worth `(v(k - 2) + 1) xor
(v(k - 1) + 1)`, the left term absent for `k = 2`; the values run 0, 1, 3,
6, 3, 3, 0, 5, 7, ... and are 0 exactly at `n = 1, 7, 13, ...`.

| file | mechanism |
|---|---|
| `fibtree.kara` ★ | the values of `order(2)` to `order(n)` in a `Vec`, each from the two before it with `^`. O(n) |
| `fibtree_mod.kara` | the closed form: Bob wins exactly when `n % 6 == 1`. O(1) |
| `fibtree_memo.kara` | the same recurrence top down, recursive, memoised in a `Vec[Option[i64]]`, with no tree worth -1 so its "plus one" adds nothing. O(n) |
| `fibtree_iter.kara` | `successors` over the pairs (value of `order(k - 1)`, value of `order(k)`) from (-1, 0), and `nth(n - 1)`. O(n) |
| `fibtree_nim.kara` | the nim-sum by hand, one binary digit at a time, into a fixed `Array[i64, 101]`. O(n log v) |
| `fibtree_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `n as usize`, `vec![0i32; n + 1]`, a `::` path in the wrapper), carried to Kāra by `karac fix`. O(n) |
| `differential.kara` | the six arms against the game played literally, six properties |

Every arm prints the same 5 lines: LeetCode's three examples; who wins for
every `n` from 1 to 100 as a line of `A` and `B`; and how many of 50000
random `n` Alice wins, with a checksum. `fibtree.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and two readings of the
statement that build the tree: the game played out on `order(n)`'s nodes,
a position being the set of nodes left (as a bit mask, memoised in a
`Map`), won by the player to move when some removal leaves a lost one; and
the colon principle worked recursively over the nodes themselves. It checks
every `n` from 1 to 100.

| | property |
|---|---|
| P1 | the answer is the game played out on the tree (`n` up to 6, 20 nodes and 3410 positions) |
| P2 | the answer for `n` is the answer for `n + 6` |
| P3 | the answer is the colon principle over the tree's own nodes (`n` up to 16, 2583 nodes) |
| P4 | in every six consecutive `n` Bob wins exactly once |
| P5 | LeetCode's examples: Alice wins at 3 and 2, Bob at 1 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `100 problems: checksum 551614178, 1884 checks over
6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The problem has no
input but `n`, so there is nothing random to draw.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `order(0)` counted as a node | P1 5, P3 13, P4 95, P5 2, P6 83 |
| M2 | ★: the right child's plus one dropped | P1 2, P2 1, P3 4, P4 95, P5 1, P6 18 |
| M3 | ★: Alice read as winning on value 1 | P1 2, P2 1, P3 4, P4 93, P5 2, P6 18 |
| M4 | mod: a period of 5 | P1 1, P2 37, P3 5, P4 19, P6 29 |
| M5 | mod: Alice at `n = 1` | P1 1, P2 1, P3 1, P4 1, P5 1, P6 1 |
| M6 | mod: a period of 7 | P2 28, P3 4, P4 14, P6 26 |
| M7 | memo: `order(1)` worth 1 | P1 2, P3 5, P5 1, P6 33 |
| M8 | memo: the memo holding one more | P2 1, P3 2, P4 94, P6 16 |
| M9 | memo: the answer read from `order(n - 1)` | P1 2, P3 6, P5 2, P6 34 |
| M10 | iter: the left value's plus one dropped | P1 1, P3 2, P4 95, P6 16 |
| M11 | iter: Alice read as winning on an odd value | P1 1, P3 3, P4 95, P6 17 |
| M12 | nim: `order(2)`'s left child counted | P1 1, P2 1, P3 4, P4 1, P6 32 |
| M13 | nim: the second number halved twice | P2 3, P3 3, P4 88, P6 17 |
| M14 | solution: the right child's one taken away | P2 16, P3 1, P4 48, P6 8 |
| M15 | solution: the answer read from `order(n - 1)` | P1 1, P2 1, P3 5, P4 1, P5 1, P6 33 |

P3 and P6 kill all fifteen, P4 thirteen, P1 eleven, P2 ten and P5 seven.
P1 reaches only `n <= 6`, where the values have not yet grown, so it misses
the edits that go wrong only once a value passes 3 (M6, M8, M13, M14); P3,
the same reading carried to `n = 16`, sees them all. P4 misses only M7 and
M9, which shift the answers by one `n` and so keep one Bob in every six. P2
misses those two and three more whose wrong answers still repeat every six
(M1, M10, M11). P5 is LeetCode's three examples, and seven edits change one
of them.

The other fifteen fail as a kept one does. Four fail as M1, each losing
`order(2)`'s value: the ★ arm's loop starting at 3, the memo arm's no tree
worth 0, the iterator arm's walk started at (0, 0), and the nim arm's digits
stopped at the shorter number. Three fail as M7: the closed form's Bob at
multiples of 6, the iterator arm one step too far, and the Rust arm's
values all starting at 1. Four fail as M8: the ★ arm's nim-sum as a
bitwise or, the iterator arm's older value kept, and the nim arm's digits
combined by or and its plus one outside the nim-sum. Three fail as M10: the
closed form's Bob at multiples of 6 as well, and the memo and Rust arms'
left plus one dropped. The Rust wrapper asking for `n - 1` fails as M15.
Two first drafts crashed on an integer overflow and were replaced (the
iterator arm's values added rather than nim-summed, and the nim arm's
places worth three times the last): the values grow past `i64`, and a
program stopped by an overflow counts as no kill.

## Verification

Every arm prints the same output as `fibtree.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.16 s (mod) to 5.8 s (nim) and the
differential 0.21 s.

The five arms were written in Kāra. Four checked clean; the nim arm's
fixed array was first typed `[i64; 101]`, Rust's spelling, which `karac
fix` turns into `Array[i64, 101]`. The Rust arm was written as LeetCode's
Rust template and reaches a clean check through `karac fix` alone, in three
rounds (two edits, then one, then one): `struct Solution;` to `struct
Solution {}` and the `::` path to `.`, then `vec![0i32; n + 1]` to
`Vec.filled(n + 1, 0i32)`, then `let n = n as usize;` over the `i32`
parameter to `let n = n as i64;`. That last edit came from kata 2003's fix
for a narrower integer's `as usize`, but its message still said to drop the
cast, which over an `i32` would leave `n` an `i32` and `Vec.filled(n + 1,
..)` refused; the message now names the edit it makes (kara c2c1c98fa5,
`tests/kata_2003_check_gaps.rs`).

## Benchmarks

The bench draws 500000 values of `n` from 1 to 100 once in all five
languages and runs the ★ arm on each, 10 rounds: five million calls, each
allocating its `n + 1` values and filling them. Every implementation prints
`5000000 calls: Alice wins 4149470, checksum 764284119`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.470 to 0.615 s | 0.475 s |
| C (`clang -O3`) | 0.472 to 0.498 s | 0.487 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.470 to 0.589 s | 0.496 s |
| Rust (`rustc -O`) | 0.744 to 1.003 s | 0.761 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.833 to 0.898 s | 0.857 s |
| Go | 1.157 to 1.273 s | 1.196 s |
| Python | 18.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.468 s) is not above its real time (0.475 s).

The sequential Kāra program is 0.58x Rust under overflow checks and 1.02x
C.