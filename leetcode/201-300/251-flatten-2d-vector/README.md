# 251. Flatten 2D Vector

Design an iterator over a 2D vector. `has_next` reports whether anything is
left; `next` yields the next element in row-major order.

```
[[1,2],[3],[4]]            -> 1 2 3 4
[[],[],[7,8],[],[9],[]]    -> 7 8 9
[[],[],[]]                 -> (nothing)
```

**Rows may be empty** — at the front, at the back, several in a row, or all of
them — and that is the entire problem. Everything else about this kata is
bookkeeping.

**Constraints:** `0 ≤ rows ≤ 200`; `0 ≤ row length ≤ 500`; values fit in `i64`.

## Approaches

| file | state | per-element cost | extra space |
|---|---|---|---|
| `flatten_2d.kara` ★ | `(row, col)` cursor, skip-empty on demand | amortized O(1) | O(1) |
| `flatten_2d_eager.kara` | one flat `Vec[i64]` copied up front | O(1) | O(total) |
| `flatten_2d_offset.kara` | prefix-sum table + linear position `k` | O(log rows) | O(rows) |
| `differential.kara` | 4,000 randomized inputs, all three must agree | — | — |

## The mechanism

**Three ways to not trip over an empty row.**

The ★ **cursor** keeps the invariant "the cursor is at a real element, or past
the end", restored by `skip_empty` at the top of *both* entry points — `has_next`
must be idempotent because callers poll it, and `next` must be correct when
called without a preceding `has_next`. Empty rows are handled by a loop that
steps over them.

The **eager** copy makes the problem vanish: empty rows contribute nothing to
the flat vector, so there is no cursor left to strand. It pays O(total) space
and does all the work up front — an iterator abandoned after one `next` has
still flattened everything.

The **offset** table is the most interesting answer: a zero-length row
contributes a *zero-width span* to the prefix sums, so no linear position `k`
ever lands inside one. The state machine the ★ file spends `skip_empty` on is
replaced by an interval that is simply empty. It also buys random access —
`seek(k)` is O(log rows) here, O(k) for the cursor, and impossible for the eager
copy without rebuilding the same table.

One subtlety in the binary search: consecutive empty rows produce **equal**
consecutive prefix entries, so the search must be the upper-bound form (first
prefix greater than `k`, step back) rather than a plain lower bound, which would
stop on the first row of a run of empties and index a zero-length row.

## `and` runs the other way here than in #250

[#250](../250-count-univalue-subtrees/) is broken *by* short-circuit evaluation:
a recursion called for its side effect gets skipped, and the count comes out
wrong. Here the same operator is a **bounds guard**:

```kara
while v.row < v.data.len() and v.col >= v.data[v.row].len() {
```

When `row == data.len()` the right operand would index one past the end. The
left test is not a condition being combined — it is a guard, and short-circuit
is what makes the loop safe.

Verified rather than assumed, by swapping the operands so the guard no longer
runs first. That probe did not merely fault: it exposed an interpreter ICE, and
then a second one after the first was fixed — kara `B-2026-08-09-18` and
`B-2026-08-09-19`.

## What it found

**Three compiler bugs, all from negative probes or the natural spelling.**

**kara `B-2026-08-09-18`** — the interpreter ICE'd (`internal error: entered
unreachable code`) on a method call whose *receiver* faulted, instead of
reporting the fault. `v[3].len()` on an empty `Vec` panicked; bare `v[3]`
reported correctly. Fixed upstream in `bb46a68d`.

**kara `B-2026-08-09-19`** — re-running the *original* probe after that fix
landed showed three more sites with the same root cause: the short-circuit
operator's LHS (`and` and `or`) and the enclosing `if` condition all consume the
same poison value without checking. The minimised repro filed with `-18` was
fixed; the kata-shaped case that found it was not. Open.

**kara `B-2026-08-09-21`** — and this one is why the kata is only partly
verified. A nested index rooted at a **struct field** — `v.data[v.row][v.col]`,
the canonical spelling of this entire problem — is rejected by codegen:

```
codegen: nested indexed read requires the outer container to be a
named variable in v1 (got non-identifier inner expression)
```

Boundary, probed: `d[i][j]` on a named local builds; `h.data[i][j]` fails;
`let row = h.data[i]; row[j]` builds; `h.data[i].len()` builds; the nested
*write* `h.data[i][j] = v` fails the same way. So it is specifically the double
index rooted at a field, read and write alike.

**The natural spelling is kept.** Rewriting the solvers to bind an intermediate
row would make them build, and would also delete the finding — so per the corpus
policy the kata stays idiomatic and this README records the blocked leg instead.

## Verification status — partial, and deliberately so

| file | interp | JIT | build | auto-par | Python |
|---|---|---|---|---|---|
| `flatten_2d.kara` ★ | ✅ | ⛔ `-21` | ⛔ `-21` | ⛔ `-21` | ✅ |
| `flatten_2d_eager.kara` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `flatten_2d_offset.kara` | ✅ | ⛔ `-21` | ⛔ `-21` | ⛔ `-21` | — |
| `differential.kara` | ✅ | ⛔ `-21` | ⛔ `-21` | ⛔ `-21` | ✅ |

All three solvers produce byte-identical output under the interpreter, and
`flatten_2d_eager.kara` — the one that reaches every surface — is byte-identical
across all four plus Python. **The A/B run-vs-build guarantee this corpus
requires is therefore NOT yet established for three of the four programs.** When
`B-2026-08-09-21` is fixed, re-run the matrix below; nothing else should need to
change.

## Generator design

`differential.kara` regenerates its input from the same seed once per solver
rather than cloning, so each of the three gets an identical but independent
value — no shared mutable state between the runs being compared. It compares the
full emitted **sequence** via a positional checksum, not the element count: two
iterators can agree on how many elements they yield and still disagree on the
order, and row-major order is the contract.

Empty rows are drawn at ~45%, independently per row, so runs of consecutive
empties occur constantly instead of rarely. Over 4,000 cases that yields **24,102
rows of which 10,698 are empty**, 46,353 elements, and **620 inputs that yield
nothing at all** — the "runs off the end without ever yielding" path exercised in
bulk rather than once.

## Kāra features exercised

- **Struct holding a `Vec[Vec[i64]]`**, consumed by value at construction —
  three different iterator states over the same input type.
- **`mut ref Struct` free functions** as the design-kata idiom (as in
  [#232](../232-implement-queue-using-stacks/)), not methods.
- **Short-circuit `and` as a bounds guard**, load-bearing and verified as such.
- **Upper-bound binary search** over a table with equal consecutive keys.
- **Nested indexing through a field** — `v.data[v.row][v.col]` — which is the
  construct `B-2026-08-09-21` is about.
- **`gen` is a reserved word**; the generator is `make_data`. The parse
  diagnostic named the reason directly.

## No benchmark

The whole input is bounded at 200×500 and every approach is one pass; the
measurement would be startup-dominated. `differential.kara` is the load-bearing
artifact.

## Running

```bash
karac run --interp flatten_2d.kara
karac run --interp flatten_2d_eager.kara
karac run --interp flatten_2d_offset.kara

# the three solvers agree with each other and with the Python oracle
diff <(karac run --interp flatten_2d.kara) <(python3 flatten_2d.py) && echo OK
diff <(karac run --interp flatten_2d.kara) <(karac run --interp flatten_2d_eager.kara) && echo OK
diff <(karac run --interp flatten_2d.kara) <(karac run --interp flatten_2d_offset.kara) && echo OK

# 4,000 randomized inputs, three solvers cross-checked, mirrored in Python
diff <(karac run --interp differential.kara) <(python3 differential.py) && echo "differential OK"

# the one program that currently reaches every surface
karac build flatten_2d_eager.kara && ./flatten_2d_eager
KARAC_AUTO_PAR=0 karac build flatten_2d_eager.kara && ./flatten_2d_eager
```
