# 254. Factor Combinations

Every way to write `n` as a product of factors, each factor in `[2, n-1]` — so
the trivial `[n]` is excluded.

```
12 -> [[2,2,3],[2,6],[3,4]]
32 -> [[2,2,2,2,2],[2,2,2,4],[2,2,8],[2,4,4],[2,16],[4,8]]
37 -> []            (prime)
 1 -> []
```

**Constraints:** `1 ≤ n ≤ 2³¹ - 1`.

## Approaches

| file | how a combination is completed | emits `[2,6]` … |
|---|---|---|
| `factor_combinations.kara` ★ | split at each divisor: `path + [i, n/i]` | before `[2,2,3]` |
| `factor_combinations_close.kara` | recurse first, then close with the remainder | after `[2,2,3]` |
| `factor_combinations_iter.kara` | explicit stack of frames, LIFO | in a third order |
| `differential.kara` | exhaustive sweep 2..10,000, all three agree | — |

## The mechanism

**The non-decreasing rule is the whole algorithm.** Each level may only use
divisors at least as large as the one above it. Without it `[2,6]` and `[6,2]`
are both generated and must be de-duplicated afterwards, which costs far more
than never producing the duplicate.

**The `i * i <= remaining` bound is that same rule, not an optimisation.** Past
that point the cofactor `remaining / i` would be *smaller* than `i`, which the
ordering has already forbidden — so the loop condition and the rule are one
thing said twice.

**The three files differ in when a combination is finished.** The ★ file emits
the two-factor split the moment it finds a divisor, then recurses to split the
cofactor further. The close-the-tail file emits nothing at a divisor — it
recurses first and completes a combination by appending whatever is left, guarded
by `remaining >= start` (the ordering rule applied to the last element) and a
non-empty path (which is what excludes the trivial `[n]`). The worklist is the ★
recursion with the call stack made explicit.

**The worklist pays for its own iteration.** A recursion can push a divisor,
recurse, and pop on the way back because the undo point is known; a worklist has
none — the child frame is consumed long after the parent moved on — so each frame
gets its **own copy** of the path. `path.push(i)` / `path.pop()` in the ★ file
becomes a fresh `Vec[i64]` per frame here, which is the real cost of going
iterative and the kind of thing worth seeing in a language with explicit
ownership.

## What it found: two layered codegen gaps

The three solvers generate in three different orders, so their shared `render`
sorts the `Vec[Vec[i64]]` lexicographically before printing — comparing lengths
and elements, which is the natural way to canonicalise a list of lists. **That
comparator cannot be compiled.**

```
codegen: no handler for method 'len' on variable 'x'
(method dispatch fell through; this is a codegen bug — add a dispatcher arm
 in `compile_method_call` …)
```

The diagnostic names itself a codegen bug, so this is a dispatch fall-through
rather than a deliberate deferral. Boundary, probed:

| inside a `sort_by` comparator | build |
|---|---|
| `x.len()` on `Vec[Vec[i64]]` | ❌ |
| `x.len()` on `Vec[String]` | ❌ |
| `x[0]` index | ❌ |
| tuple field `x.0` | ✅ |
| element `.len()` **outside** any closure | ✅ |

So the comparator's parameters reach codegen with no element type attached:
field access needs no type lookup and works, while method dispatch and index
lowering both need one and fall through. It is a whole family — sorting a
`Vec[Vec[T]]` or a `Vec[String]` by *any* content-derived key cannot be built.

Every earlier `sort_by` in the corpus compares **tuple fields**
([#56](../../1-100/56-merge-intervals/), [#252](../252-meeting-rooms/),
[#253](../253-meeting-rooms-ii/)), which is why nothing has hit this before.

**Fixed upstream in `b90027e`** — and fixing it exposed a second one underneath.

### kara `B-2026-08-10-16` — `return` inside a comparator

Re-checking the fix against **this kata's own comparator** rather than the 8-line
repro that was filed showed the repro fixed and the kata still broken, now at a
different site:

```
Module verification failed: "Function return type does not match operand
type of return inst!  ret { i64 } %ord / i64"
```

Boundary, probed on `Vec[(i64,i64)]` so the element type is held fixed:

| comparator body | build |
|---|---|
| single expression `\|x,y\| x.0.cmp(y.0)` | ✅ |
| block, **implicit** tail | ✅ |
| if-expression tail (what [#253](../253-meeting-rooms-ii/) uses) | ✅ |
| block with explicit **`return`** | ❌ |

So it is the `return` *keyword* in comparator position, independent of element
type: the implicit-tail path unwraps the `Ordering` struct and the explicit-return
path does not.

**Not a regression from the first fix.** That commit touches no return-type
logic, its tests are all single-expression comparators, and #254 is the only
program in the corpus with a block-bodied comparator — so nothing else could have
exercised this path before or after. It is a pre-existing gap the first one was
masking: previously this kata failed *earlier*, at method dispatch, and never
reached module verification.

This kata's comparator needs an **early return from inside a while loop** —
compare element by element, exit at the first difference — which cannot be
written as an implicit tail without restructuring into a sentinel-and-flag shape.
**The natural spelling is kept** rather than contorted, so three of the four
programs are interpreter-only until `B-2026-08-10-16` is fixed.

## Verification status — partial

| file | interp | JIT | build | auto-par | Python |
|---|---|---|---|---|---|
| `factor_combinations.kara` ★ | ✅ | ⛔ `-16` | ⛔ `-16` | ⛔ `-16` | ✅ |
| `factor_combinations_close.kara` | ✅ | ⛔ `-16` | ⛔ `-16` | ⛔ `-16` | — |
| `factor_combinations_iter.kara` | ✅ | ⛔ `-16` | ⛔ `-16` | ⛔ `-16` | — |
| `differential.kara` | ✅ | ✅ | ✅ | ✅ | ✅ |

All three solvers agree with each other and with Python under the interpreter.
`differential.kara` reaches every surface — it compares by an order-independent
digest and never sorts, so it never touches the broken construct. **The A/B
run==build guarantee is therefore NOT established for the three solvers.**
`B-2026-08-10-13` is already fixed; when `B-2026-08-10-16` follows, re-run the
matrix — nothing else should need to change.

## The differential compares without sorting

Because the three generate in different orders, the harness hashes each
combination and **sums** the hashes. Addition is commutative, so the digest
depends on the multiset of combinations and not on generation order — no sort,
and no risk of a sort quietly hiding a disagreement about content.

An exhaustive sweep beats random sampling here: the interesting inputs are highly
composite numbers, which are rare under a uniform draw and dense in a contiguous
range. Over `2..10,000` — **8,770 factorable, 129,813 combinations, worst case
661 combinations at n=8,640, deepest 13 factors.**

**The harness was tested against a known defect rather than trusted.** Breaking
the worklist's non-decreasing rule (child frames restarting from 2 instead of
`i`) makes it report **965 mismatches** over `2..2,000`; restored, `0`.

## Kāra features exercised

- **`Vec[Vec[i64]]` built by backtracking** with push/pop path management.
- **A struct carrying a `Vec`** (`Frame { remaining, start, path }`) pushed onto
  a `Vec[Frame]` worklist — per-frame owned copies, no shared mutable path.
- **A multi-statement `sort_by` comparator** with a loop and early returns — the
  construct `B-2026-08-10-13` is about.
- **Overflow-safe `i * i <= remaining`** rather than `i <= remaining / i`; Kāra
  traps on overflow by default, so the multiplication form is a deliberate choice
  the LeetCode bound makes safe.

## Running

```bash
karac run --interp factor_combinations.kara
karac run --interp factor_combinations_close.kara
karac run --interp factor_combinations_iter.kara

diff <(karac run --interp factor_combinations.kara) <(python3 factor_combinations.py) && echo OK
diff <(karac run --interp factor_combinations.kara) <(karac run --interp factor_combinations_close.kara) && echo OK
diff <(karac run --interp factor_combinations.kara) <(karac run --interp factor_combinations_iter.kara) && echo OK

# exhaustive sweep 2..10,000, three generators cross-checked, mirrored in Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

# the one program that currently reaches every surface
karac build differential.kara && ./differential
```
