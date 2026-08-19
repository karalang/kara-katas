# 285. Inorder Successor in BST

Given a BST and a key, return the smallest key strictly greater than it — or
nothing, if it's the largest.

```
tree from [20,9,25,5,12,11,14]      sorted: 5 9 11 12 14 20 25

successor of 11 -> Some(12)
successor of 13 -> Some(14)     13 isn't in the tree; the answer still is
successor of 25 -> None         the maximum has none
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `inorder_successor.kara` ★ | descend, remembering the last left turn | O(h) |
| `inorder_successor_recursive.kara` | the same descent, with `??` as its fallback | O(h) |
| `inorder_successor_inorder.kara` | walk in order, take the first key greater | O(n) |
| `differential.kara` | 432 trees, 8424 probes, three shapes | — |

## The answer is optional by nature

The successor of the maximum **doesn't exist**, and that isn't an error — it's a
legitimate answer the type has to carry. Every solver returns `Option[i64]`, and
a `-1` sentinel would be quietly wrong the moment `-1` is a real key.

That's also why the harness counts the `None` answers separately: **909 of 8424
probes have no successor.** If that count ever went to zero, the generator would
have stopped exercising the case the type exists for.

## Descend, remembering the last left turn

```kara
cur = root; best = None
while cur exists:
    if cur.key > target:  best = cur.key;  cur = cur.left   // a candidate
    else:                                  cur = cur.right  // too small
```

Every left turn has just passed a key greater than the target, and every later
left turn passes a smaller such key — so the last one recorded is the smallest
key greater than the target.

**The `else` branch deliberately takes no candidate.** When `cur.key <= target`
the entire left subtree is smaller still, so nothing there can be the answer.
Recording a candidate there looks symmetric and is wrong — 4523 disagreements.

## Where `??` earns its place

Written recursively, the mutable `best` disappears — the recursion *is* the
state:

```kara
if t.key[node] <= target { return successor_from(t, t.right[node], target); }
return Some(successor_from(t, t.left[node], target) ?? t.key[node]);
```

This node is a candidate, but a better one may live in its left subtree — so ask
there first and fall back to this node only if the subtree has nothing. `??` says
exactly that, and the fallback is the entire semantic content of the line. A
three-line `match` around it would bury that.

The two descents are the same algorithm, so their **slips have no counterpart in
each other**: updating `best` on the wrong branch is an assignment bug with no
recursive analogue, and dropping the `?? node.key` is a fallback bug with no
iterative analogue — 7515 disagreements, the largest in the table.

## What the injected bugs did

| injection | iter vs def | rec vs def | probes with no successor |
|---|---:|---:|---:|
| iterative: also take a candidate going right | 4523 | 0 | 909 |
| iterative: `>=` instead of `>` | 3076 | 0 | 909 |
| **recursive: drop the `?? node.key` fallback** | 0 | **7515** | 909 |
| recursive: `<` instead of `<=` | 0 | 3076 | 909 |
| **oracle: inorder walk uses `>=`** | **3076** | **3076** | **445** |

The last row is the symmetric check: breaking the *definition* implicates both
descents at once. It also halves the `None` count — with `>=`, the maximum
becomes its own successor — so a second, independent counter moves. That's the
signature of a broken oracle rather than a broken solver, and it's worth being
able to tell apart.

## Tree shapes are generated, not sampled

Random insertion orders give balanced-ish trees where the descent is short and
every solver looks the same. The harness also builds **ascending** and
**descending** insertion sequences, which degenerate the BST into a linked list —
where an O(h) descent is O(n), a recursive solver is deepest, and an off-by-one
in the left/right choice stops being masked by a short path.

Probes cover every key **and both its neighbours**: the successor of an absent
key is a different code path from that of a present one, decided by `<=` versus
`<`, and a solver using the wrong one is right on absent keys and wrong on
present ones.

```
trees 432, probes 8424, deepest tree 12 nodes
probes with NO successor 909
digest 336056404
iterative vs the inorder definition 0
recursive vs the inorder definition 0
```

## Newly-landed surface, deliberately

This kata was aimed at features days old, after two consecutive katas found no
compiler bugs while re-using the same `Vec`/`i64`/`mut ref` vocabulary the
previous 280 katas already cover. `?.` and `??` are both used here because the
problem genuinely wants them, not as decoration.

The aim paid off before the kata existed: probing `?.` turned up
**`B-2026-08-18-39`**, a high-severity miscompile where two let-bound
`Option`-returning calls under auto-par returned freed memory that varied between
runs. It's fixed (`f3fb56b` — the branch→parent slot transfer was missing
`BoxedEnumDrop`), and `?.` is correct on all four surfaces here.

Probed clean in the same pass: default arguments, and `PartialEq` derived through
a `Vec` field.

## Kāra features exercised

- **`Option[i64]` as a real return type**, with `?.` and `??` at the use sites.
- **A flat-arena BST** — three parallel `Vec[i64]`s with `-1` for absent — so the
  kata is about the algorithm rather than about `shared` node graphs.
- **An explicit-stack inorder walk**, so the definitional solver is also the one
  that can't blow the stack on the degenerate trees the generator builds.

## Running

```bash
karac run inorder_successor.kara
karac run inorder_successor_recursive.kara
karac run inorder_successor_inorder.kara

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in inorder_successor inorder_successor_recursive inorder_successor_inorder differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
