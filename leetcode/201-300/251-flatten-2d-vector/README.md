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

**Three compiler bugs, all from negative probes or the natural spelling — and a
fourth downstream of fixing one of them.** All are now closed.

**kara `B-2026-08-09-18`** — the interpreter ICE'd (`internal error: entered
unreachable code`) on a method call whose *receiver* faulted, instead of
reporting the fault. `v[3].len()` on an empty `Vec` panicked; bare `v[3]`
reported correctly. Fixed upstream in `bb46a68d`.

**kara `B-2026-08-09-19`** — re-running the *original* probe after that fix
landed showed three more sites with the same root cause: the short-circuit
operator's LHS (`and` and `or`) and the enclosing `if` condition all consume the
same poison value without checking. The minimised repro filed with `-18` was
fixed; the kata-shaped case that found it was not. Fixed in `512f59a`, and
re-checked against the original swapped-guard probe rather than the minimised
repro — the distinction that exposed the gap the first time.

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

**The natural spelling was kept.** Rewriting the solvers to bind an intermediate
row would have made them build, and would also have deleted the finding — so per
the corpus policy the kata stayed idiomatic and this README carried the blocked
leg instead. Fixed in `88da44e`, both halves; the fix in turn surfaced a leak in
the new store path (`B-2026-08-10-1`, `1b6ed41`), which a rewritten kata would
never have reached.

## Verification status

| file | interp | JIT | build | auto-par | Python |
|---|---|---|---|---|---|
| `flatten_2d.kara` ★ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `flatten_2d_eager.kara` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `flatten_2d_offset.kara` | ✅ | ✅ | ✅ | ✅ | — |
| `differential.kara` | ✅ | ✅ | ✅ | ✅ | ✅ |

Every program is byte-identical across all four surfaces, and the two with
mirrors match Python as well. The corpus A/B run==build guarantee holds.

This table was red on three of four rows when the kata landed, blocked by
`B-2026-08-09-21`. That row was fixed in `88da44e` and the matrix re-run
unchanged — no edit to any solver was needed, which is the outcome the original
note predicted and the reason the natural spelling was worth keeping.

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

## Benchmark

`bench/` builds **one ragged 2D input** (20,000 rows, ~45% of them empty), then
drains it from scratch **1,500 times** through the ★ lazy `(row, col)` iterator
— build-once + punch, ~58M `next()` calls.

The empty rows are what make it a benchmark rather than a memory scan: the
cursor advances unpredictably relative to the element stream, so `skip_empty`
is data-dependent and cannot be hoisted or vectorized away. The sink is a
**positional** checksum, so the yield ORDER is load-bearing — an implementation
that produced the right multiset in the wrong order would fail, which a plain
sum would not catch.

Sink `955071957`, reproduced exactly by the C, Rust, Go and Python mirrors.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 174.3 ± 3.1 ms | 0.93× |
| Rust `-O` | 174.9 ± 2.1 ms | 0.93× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 187.1 ± 2.9 ms | 1.00× |
| **Kāra (codegen)** | **187.3 ± 3.8 ms** | 1.00× |
| Go | 215.2 ± 2.4 ms | 1.15× |

**Kāra and equal-safety Rust are a dead tie — 187.3 against 187.1 ms, 0.2 ms
apart on σ of 3 ms.** That is the result this kata was built to produce: a
data-dependent `skip_empty` cursor that cannot be hoisted or vectorized, driven
58M times, is a pure test of how well each compiler handles an unpredictable
branch over a ragged structure, and Kāra lands exactly on the safety-matched
baseline. C and wrapping Rust share the lead at 0.93×, so the whole cost of
Kāra's guarantees on this shape is that 1.07×.

**The field compresses from the container**: Kāra was 1.17× behind C there and is
**1.08×** here. The reordering (Kāra moves from second to fourth) is not a
regression — it is the two rows above it, C and wrapping Rust, separating from
the checked builds on a host with enough out-of-order width to hide the
difference. Both hosts agree on the two claims that matter: C leads, and Kāra
tracks equal-safety Rust.

### The x86 corroboration run

Container x86-64, `bench/results.container-x86.json` — corroboration only
(BENCHMARKS.md § Hosts). That host separates the languages cleanly: C ahead,
Kāra level with `rustc -O` to within 0.3 ms and slightly ahead of the
equal-safety build, Go trailing.

## Running

```bash
karac run flatten_2d.kara
karac run flatten_2d_eager.kara
karac run flatten_2d_offset.kara

# the three solvers agree with each other and with the Python oracle
diff <(karac run flatten_2d.kara) <(python3 flatten_2d.py) && echo OK
diff <(karac run flatten_2d.kara) <(karac run flatten_2d_eager.kara) && echo OK
diff <(karac run flatten_2d.kara) <(karac run flatten_2d_offset.kara) && echo OK

# 4,000 randomized inputs, three solvers cross-checked, mirrored in Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

# run == build, on every program
for f in flatten_2d flatten_2d_eager flatten_2d_offset differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
