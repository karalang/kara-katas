# 257. Binary Tree Paths

Every root-to-leaf path, rendered as `"1->2->5"`.

```
[1,2,3,null,5]  ->  ["1->2->5", "1->3"]
[1,2]           ->  ["1->2"]        the root has ONE child, so it is not a leaf
[]              ->  []
```

**Constraints:** `0 ≤ n ≤ 100`; `-100 ≤ Node.val ≤ 100`.

## Approaches

| file | what the path is carried as | copying cost |
|---|---|---|
| `binary_tree_paths.kara` ★ | a `String` extended at every node | O(n · depth) bytes |
| `binary_tree_paths_join.kara` | a `Vec[i64]`, rendered once per leaf | O(leaves · depth) |
| `binary_tree_paths_iter.kara` | explicit `Vec[Frame]`, prefix per frame | O(n · depth) |
| `differential.kara` | 4,000 randomized trees, all three agree | — |

## The mechanism

**A node with exactly one child is not a leaf.** That is the only rule here that
is easy to get wrong, and `[1,2]` yields one path rather than two because of it.

**The ★ file's cost is where the interest is.** It copies its accumulated prefix
at every node, so it moves O(n · depth) bytes to produce an answer that is only
O(leaves · depth). On a balanced tree those are within a constant of each other.
On a path-shaped tree — depth n, a single leaf — the ★ file does O(n²) byte
copying to produce one string, and `..._join.kara` does O(n). Same algorithm,
copying moved to where the output actually is; `bench/` measures the gap.

The join file pays for that with state: its `Vec[i64]` is shared across the whole
walk, so the `pop` on the way back up is **mandatory**. The ★ file needs no undo
because each recursion owns its own prefix. Cheaper bytes, more careful state.

## Ownership shaped two of these files

Both were `perf[rc-fallback]` diagnostics — not errors, and not silenced.

**★:** `prefix: String` was consumed by the left recursion and re-used by the
right. The fix was to say what was meant — `prefix: ref String`. The walker never
keeps a prefix, it only reads one to build the next; the single owned copy
happens at the **leaf**, which is exactly where a new string comes into being.

**Iterative:** `f.prefix` read twice moved the field out of the owned frame
twice. Binding it to a local did *not* help — `push_str` accepts an owned value
or a borrow, and an owned local passed to it counts as a **consume** even though
the callee only copies bytes. The intended spelling routes through a `ref`
parameter, so the extension became a helper:

```kara
fn extend(prefix: ref String, v: i64) -> String { … }
```

which removed the RC and the duplication together. The compiler's own
`is_str_like` exists to allow exactly this, and its comment cites kata #722,
where the same call was rejected under `build` while `run` only warned.

### That second one turned out to be a compiler issue — kara `B-2026-08-13-1`

Investigating the diagnostic rather than silencing it (the help text offers
`#[allow(rc_fallback)]` first) showed the ownership checker is **inconsistent
across the three methods the compiler documents together as read-only**:

| call, on an owned argument | ownership |
|---|---|
| `a.push_str(s)` twice | **MOVED** |
| `s.starts_with(t)` twice | **MOVED** |
| `s.contains(t)` twice | clean |
| receiver reuse, `s.contains(lit)` twice | clean |
| argument via a `ref String` parameter | clean |

`is_str_like`'s own comment names all three as methods where *"the callee only
copies/scans the bytes, so there is no ownership reason to demand a move"* — the
typechecker was widened to accept a borrow, but the ownership checker still
classifies the owned-argument case as a consume for two of the three.

It is **not** a correctness bug: the value really is still readable afterwards,
and the same program prints identically under `run` and `build`. The cost is a
spurious move report, an unnecessary RC in harder shapes, and — as here — a
helper function existing purely to turn two owned reads into two borrows.

## Order is part of the answer

The iterative file must push the **right** child before the left, because the
stack is LIFO. Getting it backwards produces the right *set* of paths in fully
reversed order — measured, not assumed:

```
correct        [1->2->4, 1->2->5, 1->3->6, 1->3->7]
pushes swapped [1->3->7, 1->3->6, 1->2->5, 1->2->4]
```

So `differential.kara` compares an **order-sensitive positional digest**, not a
set or a sorted list. A sorted-set comparison would call those two identical and
the bug would ship.

## Generator design

A uniformly random tree is bushy: every path is short, and the ★ file's
O(n · depth) copying never diverges from the join file's O(leaves · depth) — the
distinction the kata exists to show goes untested. So the generator draws a high
null rate per side and makes **one case in three a pure spine**, producing trees
of depth near n with one or two leaves.

Over 4,000 cases: **18,146 nodes, 5,200 paths, longest rendered path 57 chars.**

## Kāra features exercised

- **`ref String` parameters** threaded through a recursion, and the contrast with
  an owned one — the subject of both rc-fallback diagnostics above.
- **A struct carrying a `String`** (`Frame { node, prefix }`) pushed onto a
  `Vec[Frame]` worklist, each frame owning its own prefix.
- **`Vec[i64]` push/pop backtracking** with a mandatory undo.
- **`String.bytes()`** for the positional digest, and `f"{…}"` rendering of
  negative values.
- **Index-pool tree from a level-order array**, shared with
  [#199](../../101-200/199-binary-tree-right-side-view/) and
  [#250](../250-count-univalue-subtrees/).

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the two with
mirrors match Python. All four are **rc-fallback clean**.

No compiler bugs found. Both diagnostics encountered were the ownership checker
working correctly on code that deserved restructuring.

## Running

```bash
karac run binary_tree_paths.kara
karac run binary_tree_paths_join.kara
karac run binary_tree_paths_iter.kara

diff <(karac run binary_tree_paths.kara) <(python3 binary_tree_paths.py) && echo OK
diff <(karac run binary_tree_paths.kara) <(karac run binary_tree_paths_join.kara) && echo OK
diff <(karac run binary_tree_paths.kara) <(karac run binary_tree_paths_iter.kara) && echo OK

# 4,000 randomized trees, three builders cross-checked order-sensitively
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in binary_tree_paths binary_tree_paths_join binary_tree_paths_iter differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
