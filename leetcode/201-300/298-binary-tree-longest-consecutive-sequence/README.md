# 298. Binary Tree Longest Consecutive Sequence

Find the longest path down a binary tree whose values increase by exactly one at
every step. The path may start anywhere and end anywhere, but it runs **parent
to child only** — it may never turn around.

```
   1              longest is 3-4-5, length 3
    \
     3
    / \
   2   4
        \
         5
```

## Approaches

| file | mechanism | shape |
|---|---|---|
| `longest_consecutive.kara` ★ | bottom-up: each node returns the run *starting* at it | recursive, return value + accumulator |
| `longest_consecutive_topdown.kara` | top-down: each node is handed the run *arriving* at it | recursive, accumulator only |
| `longest_consecutive_iter.kara` | the top-down walk with an explicit stack | `Vec[(Option[TreeNode], bool, i64, i64)]` |
| `differential.kara` | 700 trees, three arms, an independent oracle, five properties | — |
| `bench/consecpath.kara` | depth-20 tree, 40 passes | benchmark lane |
| `longest_consecutive.py` | mirror of the ★ arm | — |

## The direction rule is the whole problem

Drop it and this becomes the tree-diameter problem: you would join a chain
coming **up** the left subtree to one going **down** the right and get a path
through the node. Here you cannot. Every legal path is a suffix of some
root-to-leaf walk, so each has exactly one topmost node, and the answer is the
best over all of them.

```
   2              longest is 2, not 3
    \             the 3-2-1 chain DESCENDS; only 2-3 ascends
     3
    /
   2
  /
 1
```

The ★ arm asks each node one local question — *how long is the run whose first
node is me?* — which its children's answers settle:

```
down(n) = 1 + max( down(l)  if l.val == n.val + 1  else 0,
                   down(r)  if r.val == n.val + 1  else 0 )
```

A child whose value is not exactly one more contributes nothing, so the `else 0`
is where the direction rule lives.

### Local and global are different quantities

`down(n)` is the run **starting at** `n`; the answer is the best run **anywhere
in the tree**. Conflating them is the classic wrong solution — returning
`max(down(n), best_in_subtree)` up the tree lets a parent extend a chain that
does not touch it. Threading a `mut ref` best alongside the return value keeps
them apart, and that separation is really what the shape of the function is
about. P5 has a fixture that catches exactly this: a best run of 3 buried in one
subtree, under a root that would report 5 if the two were mixed.

## Three arms, and honesty about what they prove

| arm | how it can be wrong |
|---|---|
| **A** bottom-up | it compares a node against its **children's** values |
| **B** top-down | it compares a node against the value it was **handed** |
| **C** iterative | B with the call stack made explicit |

A and B put the same rule at opposite ends of the edge, so an off-by-one in the
`+ 1` lands on a different edge in each. **C is deliberately *not* independent
of B** — it is the same algorithm with the frames moved onto the heap — and
saying otherwise would overstate what their agreement proves. C is in the set to
exercise a different *ownership* shape: a `shared` handle nested inside a tuple
inside a `Vec`, pushed and popped across a loop, which neither recursive arm
builds at all.

The genuinely independent opinion is the **oracle**:

> Collect every root-to-leaf path as a flat `Vec[i64]`, then scan each for its
> longest run of consecutive values. That is an **array** problem, not a tree
> problem — no shared traversal, no accumulator, no comparison with any arm. It
> is correct because every downward path in a tree is a contiguous slice of some
> root-to-leaf path.

The oracle is quadratic in the shape the arms handle in linear time, which is
why the arms exist; at these sizes it is affordable, and it is the only member
of the set whose correctness needs no argument.

### The five properties

| | what it checks |
|---|---|
| P1 | the three arms agree with each other |
| P2 | and with the path-enumeration oracle |
| P3 | structural bounds — 0 when empty, else `1 ≤ answer ≤ min(nodes, height)` |
| P4 | invariances the rule implies — mirroring changes nothing, adding a constant to every value changes nothing |
| P5 | plateaus, descending spines, a best run buried in one subtree, values crossing zero |

**P4 is the one that catches a left/right asymmetry.** P1 and P2 would both pass
an implementation that only ever looked at left children, as long as the
generator happened to put the best run on the left. Mirroring every tree and
demanding the same answer removes that luck. The shift invariance is the same
idea for the values: the rule is about *differences*, so `+1000` must not move
the answer.

## Compiler bugs this kata found

| id | what | status |
|---|---|---|
| [`B-2026-08-29-39`](../../../../kara/docs/bug-ledger.md) | an annotated `let` recorded the *literal's* uninstantiated type rather than the binding's, so a `None`-initialized `Option[shared T]` scored non-`Copy` and its reuse was wrongly reported as a move | fixed (`c793ad0`) |

The differential's P5 block builds spines with the standard accumulator:

```kara
let mut up_l: Option[TreeNode] = None;
while k < s { up_l = node(s - k, up_l, None); k = k + 1; }
if arm_a(up_l) != s or arm_b(up_l) != s or arm_c(up_l) != s { p5 = p5 + 1; }
```

That warned. Four programs differing only in their initializer isolated it:

| binding | result |
|---|---|
| `let mut x: Option[Node] = None;` then `x = make(1);` | **warned** |
| `let mut x: Option[Node] = None;` | **warned** |
| `let mut x = make(0);` then `x = make(1);` | clean |
| `let mut x: Option[Node] = make(0);` then `x = make(1);` | clean |

Same type, same callee, same two uses — and later reassignment never
rehabilitated the binding, which is what pointed at the declaration rather than
the dataflow.

The cause turned out to be one step upstream of the ownership pass, which had
decided nothing. `check_expr(value, &declared)` verifies a bare `None` against
the annotation but did not re-record it, so the typechecker stored
`Option[TypeParam("T")]` where the binding is `Option[shared Node]`. The
classifier reads that RHS type *as* the binding's type, and `is_copy_type`
answers `Option[T]` by asking whether every argument is `Copy` — a bare type
parameter is not. `Option[shared T]` **is** `Copy`, since a use bumps a
refcount rather than moving the binding, which is why the same annotation
spelled `= Some(..)` was always clean.

> **One claim in the original report was wrong and is corrected in the ledger
> row.** It asserted that `karac check` exits 1 on the warning. It does not —
> an ownership warning prints and still reports "All checks passed" with exit
> 0. The exit 1 seen while filing came from two unrelated `mut`-marker
> typecheck errors in the same file. The finding stands on being a false
> positive on an idiomatic shape that reaches `karac check --output=json`, not
> on a broken gate.

## Benchmarks

Build one perfect depth-20 tree (1,048,575 nodes) once, then make 40 full
passes. Pass `d` asks for the longest downward path rising by exactly `d` —
`d = 1` is the kata's problem, and `d = 2..40` is the same traversal with a
different constant in one comparison. Without that the sink would be one number
repeated 40 times; with it, the work per pass is unchanged and the sink reads
every answer. All five languages produce `checksum 782785867`.

Values are assigned top-down as parent-plus-a-small-delta, so consecutive runs
actually occur — a balanced build over a shuffled array would relate no node to
its children, every run would have length 1, and the `run = arriving + 1` branch
the algorithm is *about* would never be taken.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json).
See [BENCHMARKS.md](../../../../BENCHMARKS.md) for methodology and caveats.

| | mean | vs C |
|---|---:|---:|
| c (`-O3`) | 703 ms | 1.00× |
| go | 713 ms | 1.01× |
| rust (`-O`) | 1.127 s | 1.60× |
| rust (`-O -C overflow-checks=on`, equal safety) | 1.162 s | 1.65× |
| **kara** (codegen, seq) | **1.201 s** | **1.71×** |
| python | 12.096 s | 17.2× |

Cross-checked by interleaving all four binaries 10 times each (medians): C 0.714
s, Go 0.748 s, Rust 1.225 s, Kāra 1.240 s. **Kāra and Rust are a dead tie —
1.01× — and both trail C and Go by 1.7×.** Whatever costs Rust that 1.7× costs
Kāra the same amount, and it cannot be reference counting, because Rust has
none.

### The C mirror was 1.7× faster for a reason that had nothing to do with C

The first run of this lane had C at 345 ms against Rust's 1.17 s — a 3.4× gap on
what is meant to be the same algorithm, which is exactly the shape
[BENCHMARKS.md](../../../../BENCHMARKS.md) warns about. It was a **mirror
asymmetry, and the fault was mine**:

```c
Node *n = malloc(...);              /* parent FIRST  — the obvious C spelling */
n->left  = build(depth - 1, ...);
n->right = build(depth - 1, ...);
```

Rust, Go, Kāra and Python all construct a node **from already-built children**,
so the parent is necessarily the *last* allocation in its subtree. C's version
allocated the parent *first*, which lays each node adjacent to its left child
and hands the traversal a much friendlier cache layout. Rewriting the C build to
children-first — same binary otherwise — moved it from **0.34 s to 0.58 s, a
1.7× swing from allocation order alone.** The published table uses the
children-first C.

Ruled out before landing on it, each measured: the work is real and scales
linearly in both languages (40 vs 80 passes doubles both); the Rust signature is
not the cause (`Option<&Node>`, a plain nullable reference like C's, measures
identically to `&Option<Box<Node>>`); inlining is not the cause (`noinline` on
both leaves the ratio unchanged); optimization level is not the cause (`clang
-O1` matches `-O3` at 0.34 s, and `rustc -C opt-level=3` matches `-O`); and
overflow checks are not the cause (the equal-safety twin is within noise of
plain `-O`).

**The residual 1.7× of Rust-and-Kāra behind C-and-Go is unattributed.** What has
been established is that it survives all six of those controls — not its cause.

### Elsewhere

| | kara | c | rust | go |
|---|---:|---:|---:|---:|
| binary size | 337.4 KiB | 15.8 KiB | 3863.7 KiB | 2178.6 KiB |
| peak RSS | 50.5 MiB | 33.5 MiB | 34.1 MiB | 27.3 MiB |
| compile (cold) | 380 ms | 99 ms | 121 ms | — |

Kāra's 50.5 MiB against 34 MiB for C and Rust is the refcount word: a
`shared TreeNode` carries a control block that a `Node *` and a `Box<Node>` do
not, across 1,048,575 nodes.

## Running it

```bash
karac run  longest_consecutive.kara
karac build longest_consecutive.kara && ./longest_consecutive
karac run  --interp differential.kara
python3 longest_consecutive.py
bash bench/bench.sh
```
