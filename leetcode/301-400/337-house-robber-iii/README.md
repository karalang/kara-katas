# 337. House Robber III

The houses form a binary tree, each holding some money. Robbing two houses
joined by an edge sets off the alarm. Return the most money that can be
taken without robbing a house and its parent.

```
[3,2,3,null,3,null,1]  ->  7   (3 + 3 + 1)
[3,4,5,1,3,null,1]     ->  9   (4 + 5)
```

## Approaches

Every arm answers each subtree once. A subtree has two best totals, one with
its root robbed and one without. Robbing the root adds its money to both
children's "not robbed" totals. Leaving it takes the better of each child's
two totals.

| file | mechanism | cost |
|---|---|---|
| `house_robber_iii.kara` ★ | post-order over an index pool (`Vec[Node]`, child indices, -1 = none). Each call returns the `(robbed, not robbed)` tuple for its subtree | `O(n)` time, `O(height)` stack |
| `house_robber_iii_shared.kara` | the same post-order over linked `shared struct TreeNode`s with `Option` children, as LeetCode hands the tree over, matching on each child | `O(n)` time, `O(height)` stack |
| `house_robber_iii_memo.kara` | one best per subtree: rob the root plus the best of its four grandchildren's subtrees, or skip it and take its two children's. A grandchild is reached from two places, so the bests are memoised in a `Map` from node index | `O(n)` time and memo |
| `house_robber_iii_iter.kara` | no recursion. A breadth-first walk lists every house after its parent, so walking that list backwards reaches every house after its children, and the two totals are filled into two arrays | `O(n)` time and memory |
| `differential.kara` | the four arms, a brute-force oracle and eight properties on 11,797 trees | — |
| `bench/house_robber_iii.kara` | 100 solves of a 500,000-house tree, by the ★ arm | — |

Every arm prints the same 19 lines: the two examples, ten edge cases (the
empty tree, one house with and without money, two and three houses, a
chain going left, one whose best robs a house and its uncle, a tree of empty
houses, and one whose best skips a whole level), six random trees of 3 to 28 houses, a random tree of 10,000
houses and a chain of 10,000. The chain is as deep as LeetCode allows, so it
is also the deepest recursion the arms meet. The four arms' output is
byte-identical, and `house_robber_iii.py` mirrors the ★ arm.

## Differential

`differential.kara` checks every tree shape with at most five houses, with
every assignment of money from `{0, 1, 3}` (11,497 trees), then 300 random
trees of 1 to 12 houses holding 0 to 20. The oracle tries every set of
houses as a bit mask and keeps the sets that rob no house together with its
child.

| | property |
|---|---|
| P1 | the four arms agree |
| P2 | they equal the oracle |
| P3 | the answer is at least the richest house and at most the total |
| P4 | mirroring the tree keeps the answer |
| P5 | doubling every house's money doubles the answer |
| P6 | the answer is at least the money on the even depths, and at least the money on the odd depths, since neither set holds a house and its child |
| P7 | a new root holding nothing above the tree keeps the answer |
| P8 | a new root holding more than the whole tree answers that root plus the answers for the old root's two subtrees |

`11497 exhaustive trees (answers sum to 53825)`, `300 random trees (answers
sum to 12817), 0 failures`, on every surface.

## Mutation testing

Fourteen edits to the copies inside `differential.kara`, each run with every
failure printed rather than the first ten.

| # | mutation | outcome | how |
|---|---|---|---|
| M1 | ★: robbing a house adds its left child's robbed total | **killed** | P1, P2, P4, P6, P8 |
| M2 | ★: leaving a house takes only its children's not-robbed totals | **killed** | P1, P2, P3, P6, P7, P8 |
| M3 | ★: the answer is the robbed total | **killed** | P1, P2, P3, P6, P7, P8 |
| M4 | ★: an absent child counts 1 when robbed | **killed** | P1, P2, P3, P5, P7, P8 |
| M5 | shared: robbing a house adds its right child's robbed total | **killed** | P1 |
| M6 | shared: the linking swaps every house's children | silent (equivalent) | — |
| M7 | memo: the memo is never written | silent (equivalent) | — |
| M8 | memo: robbing a house leaves out its right child's children | **killed** | P1 |
| M9 | memo: every best is stored under the root's index | silent (equivalent) | — |
| M10 | iter: the list is walked forwards | **killed** | P1 |
| M11 | iter: leaving a house takes only its children's not-robbed totals | **killed** | P1 |
| M12 | oracle: a robbed house's right child is not checked | **killed** | P2 |
| M13 | oracle: the last house is never robbed | **killed** | P2 |
| M14 | oracle: the empty set is never tried | silent (equivalent) | — |

All four silent mutations are equivalent. M6 solves the mirror image, which
has the same answer (that is P4). M7 recomputes every subtree, which is
exponential but gives the same bests. M9 is M7 in disguise: the root is
never reached again, so no lookup ever finds what was stored. M14: the empty
set is worth 0, which the oracle's starting best already is. P1 catches
everything the non-★ mutations do, because each arm is compared against the
★ arm's answer first.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and all five programs are
valgrind-clean at `-O0` with `KARAC_AUTO_PAR=0` and `KARAC_BUF_CACHE=0`
(`All heap blocks were freed`, no errors). The four arms' output is
byte-identical to `house_robber_iii.py`. The memo arm keeps its bests in a
`Map`, but only looks them up, so the output does not depend on the hash
order. The 10,000-house chain recurses 10,000 deep on every surface,
including the interpreter.

With a release karac the arms take 1.5 to 11.8 s under `--interp` against
about 0.3 s on the JIT, and the differential 47 s against 0.4 s. The
slowest arm under the interpreter is the linked one, which builds a
`shared struct` per house before solving. Every arm here is a recursion of
small calls, so most of that time is probably the interpreter's per-call
cost, filed from kata 336 as B-2026-10-03-21; it was not profiled for this
kata.

## Benchmarks

`bench/house_robber_iii.kara` and its four mirrors time the ★ arm as
written. One random tree of 500,000 houses, each holding 0 to 10,000, is
built once: every new house walks down from the root, turning left or right
at random, and settles in the first empty place. Each of 100 punches gives
one random house new money, solves the whole tree, and puts the money back.
The sink is a rolling hash of the answers.

> **Host:** only the x86-64 Linux cloud container lane exists so far, in
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The
> canonical Apple M5 Pro lane (`bench/results.json`) is not measured yet, and
> `bench-lib.sh` refuses to write it from Linux. Absolute milliseconds are NOT
> comparable between hosts. Only the **within-file cross-language ratios** are.

30 runs each (Python: 3), on a 4-core x86-64 Linux container, karac built
from `main` at `b87830f19` with this thread's three unpushed fixes for
B-2026-10-03-23, -24 and -25 (none touches this kernel's code paths),
measured 2026-10-03. Python is its own lane.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 1600.3 ms ± 29.2 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 1640.8 ms ± 45.4 | 1.03× |
| rust `-O` | 1714.9 ms ± 46.9 | 1.07× |
| rust `-O -C overflow-checks=on` (equal-safety) | 1742.7 ms ± 44.8 | 1.09× |
| rust `-C target-cpu=x86-64-v3` (matched) | 1754.1 ms ± 51.0 | 1.10× |
| go `go build` | 1822.4 ms ± 35.7 | 1.14× |
| **kāra `karac build`** | **1908.8 ms ± 155.6** | **1.19×** |
| python 3 | 46025.5 ms ± 685.0 | 28.8× |

**Kāra is 9.5% behind equal-safety Rust here, and the whole gap is the
`ref Vec[Node]` parameter.** The build phase alone is a tie (121 ms against
130 ms for Rust with 0 punches). Changing `visit` to take `Slice[Node]` makes
Kāra 1.76 s against Rust's 1.77 s in the same hyperfine run. With `ref Vec`,
`visit` reloads the Vec's length and data pointer and repeats the bounds
check after each of its two recursive calls. The parameter carries LLVM
`readonly` but not `noalias`, so LLVM cannot assume the Vec is unchanged
across a call. Adding `noalias` by hand removes the reloads, but it would
not be sound yet; see B-2026-10-03-45 under Compiler findings. Filed as B-2026-10-03-46. The
kata keeps `ref Vec`, which is the natural way to write it.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 82.4 ms ± 2.1 | 15.8 KiB | 12.8 MiB |
| rust | 122.3 ms ± 9.2 | 3863.9 KiB | 13.4 MiB |
| kāra | 326.8 ms ± 18.0 | 341.6 KiB | 14.5 MiB |
| go | — | 2167.0 KiB | 13.3 MiB |
| python | — | — | 49.7 MiB |

`karac build` is 4.0× clang's cold compile and 2.7× rustc's. Kāra's binary is
22× clang's and 11× smaller than rustc's. Raw numbers are in
`bench/results.container-x86.json`. Methodology and caveats are in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

The benchmark kernel's sink matches all four language twins and Python
(`sink 637768311`).

## Compiler findings

- **B-2026-10-03-45 (use-after-free, high, open): iterating a `shared struct`'s `mut`
  Vec field while pushing to it through the same struct reads freed
  memory.** `for x in self.v.iter() { ... self.v.push(x + 1); }` in a
  `ref self` method gives a garbage total on every compiled surface, and
  valgrind shows the loop reading the block the push's reallocation freed.
  The language says a write to a field while it is being read must panic,
  and the compiled code has no check for it. Found while checking whether
  the bench's `ref Vec` parameter could carry `noalias`; the kata itself
  does not do this.
- **B-2026-10-03-46 (perf, low, open): a `ref Vec` parameter is reloaded after every
  call.** It costs this kernel its whole 9.5% gap to Rust. Details are under
  Benchmarks; it waits on B-2026-10-03-45.
- **B-2026-10-03-21 (perf, low, open)**, filed from kata 336: the
  interpreter's per-call cost, which is probably most of the 1.5 to 11.8 s
  the arms take under `--interp` (inferred, not profiled here).

Every arm was byte-identical on every surface and valgrind-clean from the
first run, and `karac check` reported no diagnostics on any of them. That
says little about the diagnostics overall: the author already knows the
language, which is why authoring like this never counts toward the
machine-fix rate.
