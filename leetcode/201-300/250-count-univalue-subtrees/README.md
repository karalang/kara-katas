# 250. Count Univalue Subtrees

A **uni-value subtree** is one in which every node holds the same value. Given
the root of a binary tree, count them.

```
      5                     5                     1
     / \                   / \                   / \
    1   5                 5   5                 2   3
   / \   \               / \   \
  5   5   5             5   5   5

  -> 4                  -> 6                   -> 2
```

In the first tree the three `5`-leaves qualify, and so does the right child
(value `5`, only child a `5`). The `1` does not — its children are `5`s — and
neither does the root, because its left subtree is already broken.

**Constraints:** `0 ≤ n ≤ 1000`; node values fit in `i64`.

## Approaches

| file | shape | post-order comes from |
|---|---|---|
| `count_univalue.kara` ★ | recursion + `mut ref i64` accumulator | the call stack |
| `count_univalue_pair.kara` | recursion returning `Verdict { uni, count }` | the call stack |
| `count_univalue_iter.kara` | explicit stack with an `expanded` flag | spelled out by hand |
| `count_univalue_scan.kara` | descending scan over the node pool | the builder's index order |
| `differential.kara` | 4,000 randomized trees, all four must agree | — |

## The mechanism

**The decision is bottom-up and cannot be anything else.** A subtree is
uni-value iff both child subtrees are uni-value *and* every child that exists
holds the parent's value. The parent's answer is a function of its children's,
so children must be resolved first — every approach here is just a different way
of obtaining that ordering.

An absent child is **not** a failure: `null` never breaks its parent. That is
what makes a leaf uni-value (both children absent, vacuously fine) and it is the
rule the half-present cases exercise, which is why the generator produces ragged
trees rather than full ones.

## The trap: `and` is a short-circuit, and this recursion must not take it

The natural way to write the recursive combine is the wrong one:

```kara
let ok = is_uni(nodes, left, total) and is_uni(nodes, right, total);   // WRONG
```

`and` short-circuits. The moment the left subtree returns `false`, the right
recursion is **never called** — so every uni-value subtree hanging off the right
side goes uncounted. The recursion is not being used for its value alone; it is
being used for its side effect on `total`, and a short-circuit silently discards
that side effect.

The fix is to bind both results before combining, which is what the ★ file does:

```kara
let left_uni = is_uni(nodes, left, total);
let right_uni = is_uni(nodes, right, total);
let mut ok = left_uni and right_uni;
```

`[5,1,5,5,5,null,5]` — the LeetCode example — is precisely the shape that catches
it. The root's left subtree fails, so the right one is never walked, and it
contains **two** uni-value subtrees (the `5`-leaf and its parent). Short-circuit
answers **2** where the answer is **4** — measured, not reasoned about:
`[1,2,3,4,5,6,7]` drops from 4 to 2 the same way. Both are in the unit tests of
all four solvers for that reason.

`count_univalue_pair.kara` is immune **structurally** rather than by discipline:
it returns a `Verdict { uni, count }` upward instead of bumping an accumulator,
so both children have to be evaluated for their counts whatever their verdicts
say, and there is no `and` left for a shortcut to hide in. That is the same
out-parameter-versus-return-value contrast [#52](../../1-100/52-n-queens-ii/)
draws for a search tally — here one of the two forms has a trap and the other
cannot.

## The scan's hidden dependency

`count_univalue_scan.kara` walks `i` from `n-1` down to `0` and reads its
children's verdicts straight out of the memo, with no stack at all. That is
correct because of a property of the **builder**, not of the problem: `build`
fills the pool in level order and pushes each node's children after the node
itself, so **a child's index is always greater than its parent's**. Descending
the pool is therefore already a post-order.

Worth stating plainly because it is easy to inherit by accident: swap in a pool
built by BST insertion ([#230](../230-kth-smallest-element-in-a-bst/)) or by any
depth-first construction and the index invariant is gone, along with this file's
correctness. The other two approaches are indifferent to build order; this one
buys its speed by depending on it.

## Generator design

Two choices in `differential.kara` do real work, and both were made because the
obvious alternative measures nothing:

**A tiny value alphabet (2–3 distinct values).** Draw values uniformly from a
wide range and almost every internal node is broken by one of its children, so
the count collapses to "number of leaves" and the combining path — the entire
subject of this problem — barely executes. With the small alphabet, **5,070 of
the 29,899 uni-value subtrees found are non-leaf**: 17% of the count comes from
the branch that would otherwise be nearly dead.

**~28% nulls below the root.** Full trees never produce a node with exactly one
child, which is where the "absent child never breaks its parent" rule lives.

Over 4,000 trees / 63,001 nodes the four solvers agree on every case, and 547 of
the trees come out entirely uni-value.

## What it found

**Nothing — and that is the report.** All five programs passed `karac check` on
first authorship with no diagnostics, and every one is byte-identical across
`karac run --interp`, `karac run` (JIT), `karac build` (auto-par default) and
`KARAC_AUTO_PAR=0 karac build`, against the Python mirrors.

Worth recording rather than omitting: the surfaces this kata leans on —
`mut ref` scalar accumulators through recursion, `Vec[bool]` memos, by-value
struct returns from a recursive call, parallel stacks, descending index loops —
are all ones earlier katas have already driven bugs out of. A clean run over
known-exercised ground is a different signal from a clean run over new ground,
and this is the former.

## Kāra features exercised

- **`mut ref i64` out-parameter threaded through a recursion** — the accumulator
  form, as in [#52](../../1-100/52-n-queens-ii/)'s `marker_arrays.kara`; the
  recursive call forwards it unmarked, the owning caller passes `mut total`.
- **`Vec[bool]`** as a per-node memo, in two different roles (verdict table, and
  the iterative walker's `expanded` flags).
- **Parallel `Vec`s standing in for a stack of pairs** — `stack` + `expanded`
  popped in lockstep.
- **`match` on `Vec.pop()`'s `Option`** with a sentinel default.
- **Descending `while` loop** (`i = n-1; i >= 0; i = i - 1`) over an index pool.
- **By-value struct return from a recursion** (`Verdict { uni, count }`) — the
  pure alternative to the `mut ref` accumulator, same answer, no shared state.
- **Struct-of-i64 index-pool tree** with `-1` as the null child, shared by all
  three solvers and built by the same level-order walk as
  [#199](../../101-200/199-binary-tree-right-side-view/).

## Benchmark

`bench/` builds **one 2M-node level-order tree** from a 3-symbol alphabet, then
runs **40 full counting passes** over it — build-once + punch. The small alphabet
matters here for the same reason it does in the differential: it keeps uni-value
subtrees common, so the combining path is hot rather than the leaf case.

The pass cannot be reduced to a vectorized reduction — each node's verdict is
read back out of the memo by its parent, so the loop is carried through
`uni[]`.

**The kernel is the reverse index scan, not the ★ recursion.** A recursion here
would measure four languages' differing stack conventions rather than the
counting work, and the scan is expressible identically in all five mirrors. That
is a deliberate departure from "bench the ★ approach" and the reason is recorded
in the kernel header too.

Sink `42226040`, reproduced exactly by the C, Rust and Go mirrors.

**Published numbers await the Apple-silicon host.** The x86 container run in
`bench/results.container-x86.json` is corroboration that the lane works and the
mirrors agree (BENCHMARKS.md § Hosts), not a source of claims — and on that host
all five landed within a few percent of each other with Rust's own σ at 13% of
its mean, which is contention, not signal. Nothing here should be quoted until
`bench/results.json` exists.

## Running

```bash
karac run count_univalue.kara
karac run count_univalue_pair.kara
karac run count_univalue_iter.kara
karac run count_univalue_scan.kara

# each solver against the Python oracle
diff <(karac run count_univalue.kara) <(python3 count_univalue.py) && echo OK

# the three solvers against each other
diff <(karac run count_univalue.kara) <(karac run count_univalue_pair.kara) && echo OK
diff <(karac run count_univalue.kara) <(karac run count_univalue_iter.kara) && echo OK
diff <(karac run count_univalue.kara) <(karac run count_univalue_scan.kara) && echo OK

# 4,000 randomized trees, four solvers cross-checked, mirrored in Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"
```
