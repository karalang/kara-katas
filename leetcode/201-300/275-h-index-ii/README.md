# 275. H-Index II

`citations` is sorted **ascending**. Return the h-index — the largest `h` such
that at least `h` papers have at least `h` citations each — in **O(log n)**.

```
[0,1,3,5,6]  -> 3        [0,0,0]      -> 0     nothing is cited
[1,2,100]    -> 2        [5,5,5]      -> 3     everything clears the bar
[100]        -> 1        [1,1,1,1,1]  -> 1     a wide flat plateau
[0]          -> 0        [0,1,2,3,4]  -> 2     the diagonal crossing
```

**Constraints:** `1 ≤ n ≤ 10⁵`; `0 ≤ citations[i] ≤ 1000`; sorted ascending.

[#274](../274-h-index/) is the same definition on **unsorted** input, where the
answer costs a sort or a counting pass. Handing the array over sorted changes the
problem entirely.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `h_index.kara` ★ | binary search on the index | O(log n) |
| `h_index_scan.kara` | backward linear scan from the most-cited end | O(n) |
| `h_index_bucket.kara` | counting buckets — uses no sortedness at all | O(n) |
| `differential.kara` | every sorted array of length ≤ 7, plus 3,000 random | — |
| `bench/hsearch.kara` | the ★ search as a benchmark kernel, five languages | — |

## Why the predicate is monotone, which is the whole problem

At index `i` the papers at `[i, n)` are the `n − i` most-cited. If
`citations[i] ≥ n − i`, each of those `n − i` papers has at least `n − i`
citations, so `n − i` is achievable. The predicate is false for a prefix and true
for a suffix — hence binary search.

It is worth being precise about *why* it is monotone, because it is not simply
"the array is sorted." Moving from `i` to `i + 1` **raises the left side**
(`citations` is non-decreasing) and **lowers the right side** (`n − i` shrinks by
one). Both movements favour the predicate, so once true it stays true. A
predicate where only one side moved would not be searchable this way.

## The off-by-one lives in the invariant, not in the comparison

```kara
let mut lo = 0i64;
let mut hi = n;                      // one PAST the last candidate
while lo < hi {
    let mid = lo + (hi - lo) / 2i64;
    if citations[mid] >= n - mid { hi = mid; }      // mid qualifies
    else                         { lo = mid + 1i64; }
}
return n - lo;                       // lo == n when nothing qualifies -> 0
```

`hi = mid` and not `mid - 1`: `mid` *qualifies*, so it is still a candidate. And
the all-uncited case needs no special handling — `lo` runs to `n` and `n - lo` is
0.

## The third solver uses no sortedness

Both other solvers are built on the array being non-decreasing — one
binary-searches a predicate that is monotone only because of it, the other stops
at the first failure because of it. If that assumption were ever violated they
would agree on a wrong answer.

The bucket solver is #274's algorithm, written for unsorted input, and it is the
one that would notice. Its trick is the **clamp**: a paper with 10,000 citations
is no more useful than one with `n`, because the h-index can never exceed the
paper count — so the histogram needs `n + 1` slots regardless of citation size.

## The exhaustive oracle, and the check that computes nothing

The small input space is **enumerated outright** rather than sampled: every
non-decreasing sequence of length 0..7 with values 0..7, all 6,435 of them. An
off-by-one lives at exactly one input, and a sampler can miss it forever. The
3,000 random arrays exist for *scale* — a binary search over four elements runs
two iterations — not for boundary coverage.

And every answer is checked against the **definition** directly: `h` is the
h-index iff at least `h` papers have `≥ h` citations *and* fewer than `h + 1`
have `≥ h + 1`. Two counting loops, no search, no sortedness, no arithmetic
shared with any solver. It does not compute an answer; it only refutes one.

```
cases 9435
of which EXHAUSTIVE (every sorted array, len 0..7, vals 0..7) 6435
answers at the floor (h = 0) 623
answers at the ceiling (h = n) 131
arrays with a citation count above n (the bucket clamp) 3213
answers refuted by the DEFINITION 0
digest 826433451
mismatches 0
```

## What the injected bugs did

| injection | mismatches | refuted by the definition |
|---|---:|---:|
| binary: `hi = mid - 1` (the classic skip-the-answer) | 4194 | 4194 |
| binary: `>` instead of `>=` in the predicate | 4114 | 4114 |
| binary: search `[0, n−1)` instead of `[0, n)` | 622 | 622 |
| scan: `>= h` instead of `>= h + 1` | 4752 | 0 |
| bucket: sweep from `n − 1` | 4492 | 0 |
| bucket: drop the clamp at `n` | *out-of-bounds crash* | — |
| both sortedness-dependent solvers lose the boundary | 6971 | 4194 |
| **all three return `h − 1`** | **0** | **9435** |

The last row is why the definitional check exists. All three solvers agree
perfectly, cross-checking reports **nothing**, and the definition refutes **every
single case**. That is the failure mode [#270](../270-closest-binary-search-tree-value/)
found and [#272](../272-closest-binary-search-tree-value-ii/) measured, taken one
step further: there, a third *mechanism* saved the harness; here even three
mechanisms would not, and only a check that computes no answer at all does.

Rows four and five show the other side honestly — the oracle validates the ★
solver's answer, so a bug in a non-★ solver surfaces as a mismatch and not as a
refutation. The two checks are complementary, not redundant.

## Benchmark

`bench/` builds one sorted **262,144-element** citation array once, then runs
**6,000,000** h-index binary searches over prefixes of varying length — so every
query has a different `n`, a different answer and a different path. Sink
`217993832`, reproduced by all four compiled mirrors and by Python.

**This is the corpus's flat-array search lane.** Per query the work is ~18
iterations of `mid = lo + (hi - lo) / 2`, one load at `mid`, and a data-dependent
branch, each load's address depending on the previous comparison. #272 is a tree
walk with stacks, #266 a byte scan, #271 a bulk memcpy; here the address chain is
*arithmetic* rather than a pointer dereference.

Sized at 2 MiB deliberately. [#261](../261-graph-valid-tree/) measured this
corpus's own limit — the same kata's σ went 1.3% → 2.0% → **22.8%** at working
sets of 1 MB, 3 MB and 13 MB. A larger array would be a purer memory-latency lane
and an unrankable one.

### What the x86 corroboration run shows

| lang | mean (ms) | σ |
|---|---|---|
| C | 447.5 ± 7.7 | 1.7% |
| **Kāra** | **458.8 ± 4.1** | 0.9% |
| C (`-march=x86-64-v3`) | 462.8 ± 6.9 | 1.5% |
| Go | 465.2 ± 7.5 | 1.6% |
| Rust | 749.1 ± 22.8 | 3.0% |
| Rust (checked + `target-cpu=v3`) | 785.8 ± 50.2 | 6.4% |
| Rust (checked, equal-safety) | 786.1 ± 34.6 | 4.4% |

**Kāra is second, 1.03× behind C** and inside noise of the two C builds and Go.

### Rust is 1.63× behind, and it is one `cmov`

Every other lane in this corpus has Rust within noise of C, so that gap was
probed before it was published. `rustc -O` if-converts the search loop:

```
cmp    %r10,(%rbx,%rdi,8)     ; citations[mid]  vs  n - mid
cmovge %rdi,%r9               ; hi = mid
cmovl  %rdi,%rdx              ; lo = mid + 1
```

`clang -O3` emits **zero** `cmov` in `main`, and Kāra's search loop is branchy
too. Forcing the branch back — changing only the codegen, same sink — takes Rust
from **758.0 to 480.6 ms**, level with Kāra and C. **The entire deficit is one
if-conversion decision.**

That makes three instances of the same mechanism in this corpus: #259 (`rustc -O`
if-converts a two-pointer loop, 65%), #270 (`clang -O3` if-converts BST child
selection, 23%), and now #275 at 58%. Binary search is the textbook case *for*
branchless code — the branch is maximally unpredictable, which is precisely the
argument for `cmov`. It loses anyway, because unpredictable-but-speculatable
still beats serialized. Full write-up in [`bench/probe/`](bench/probe/).

## Kāra features exercised

- **`Vec[Vec[i64]]` literals** as the test-case table, indexed and passed by
  `ref` to a function taking `ref Vec[i64]`.
- **Index-assign into a `Vec[i64]`** built by a `push` loop — the bucket
  histogram.
- **A `while` odometer over combinations with repetition** — the exhaustive
  enumerator, which mutates its own array in place and never allocates.
- **`seq` is a reserved keyword**, which the parser says plainly.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors. The bench kernel is checked
under the JIT and both AOT modes at full size, and across all four surfaces plus
Python at reduced size.

No compiler bugs found.

## Running

```bash
karac run h_index.kara
karac run h_index_scan.kara
karac run h_index_bucket.kara

diff <(karac run h_index.kara) <(python3 h_index.py) && echo OK

# 9,435 arrays — 6,435 of them exhaustive — three solvers plus the definition
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in h_index h_index_scan h_index_bucket differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done

# cross-language benchmark (needs hyperfine, rustc, clang, go)
bash bench/bench.sh
```
