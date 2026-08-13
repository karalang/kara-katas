# 259. 3Sum Smaller

Count index triplets `i < j < k` with `nums[i] + nums[j] + nums[k] < target`.

```
[-2,0,1,3], target 2  ->  2      ([-2,0,1] and [-2,0,3])
[0,0,0],    target 1  ->  1
[0,0,0],    target 0  ->  0      strictly less than
```

**Constraints:** `0 ≤ n ≤ 3500`; `-100 ≤ nums[i], target ≤ 100`.

## Approaches

| file | shape | cost |
|---|---|---|
| `three_sum_smaller.kara` ★ | sort + converging two pointers | O(n²) |
| `three_sum_smaller_brute.kara` | three nested loops, the definition | O(n³) |
| `three_sum_smaller_bsearch.kara` | sort + upper-bound bisection per pair | O(n² log n) |
| `differential.kara` | 4,000 randomized arrays, all three agree | — |

## The mechanism

**`count += hi - lo`, not `+ 1`.** That single line is the whole problem. Because
the array is sorted, if the pair `(lo, hi)` qualifies then so does `(lo, k)` for
*every* `k` strictly between them — each such `nums[k] ≤ nums[hi]`, so each sum
is no larger. Counting the run in one step is what turns an O(n³) enumeration
into an O(n²) scan. Writing `+ 1` gives a smaller and entirely plausible answer.

**Sorting is legitimate here and would not always be.** The answer counts *sets*
of indices: `i < j < k` ranges over each unordered triple exactly once, and
permuting the array changes which indices name a triple but not which triples
exist. A variant asking for the triples themselves could not sort.

## Why three, and why the third is not redundant

The two fast forms both work by **counting a whole run at once**, and that is
precisely where each can be wrong. But they locate the run by opposite means: the
two-pointer form converges a scan and adds `hi - lo`; the bisection form finds a
boundary index and adds `bound - j - 1`. An off-by-one in one does not mirror an
off-by-one in the other.

Neither can adjudicate its own error, though — both failure modes produce
smaller, plausible counts. That is what the O(n³) file is for: it rests on no
sort and no run-length argument, so when the three disagree it is the one to
believe.

**Both failure modes were tested, not assumed:**

| injected bug | mismatches / 4,000 |
|---|---|
| two-pointer counting `+ 1` instead of `+ (hi - lo)` | **2,412** |
| bisection using `<=` (lower bound) instead of `<` | **1,956** |

## Generator design

**The target has to land inside the band of achievable sums.** Drawn uniformly,
it sits far above or far below every triple sum almost always, so the answer
saturates at `0` or at `C(n,3)` and the run-length arithmetic is never exercised.
Each case therefore computes its array's actual minimum and maximum triple sums
and draws the target from within that range.

Values come from a **small range** (`-10..10`) on **short arrays**, so ties are
common — which matters because the comparison is strict, and sums landing exactly
*on* the target are where a `<`-versus-`<=` slip or a lower/upper-bound mix-up
shows.

Over 4,000 cases: **112,190 triples counted**, with 1,182 answering 0 (most of
them the `n < 3` cases, which cannot produce a triple) and 249 saturating at
`C(n,3)`.

## Benchmark

`bench/` builds **one 4,000-element array once**, then punches the ★ sorted
two-pointer count through it **26 times** — 208M inner iterations against 26
sorts. Sink `540236372`, reproduced by all four mirrors.

The target is chosen **at the median of the achievable triple sums**, not below
or above the band. That is load-bearing: with a target under every sum the inner
loop only ever decrements `hi`, and with one over every sum it only ever
advances `lo` — either extreme is a monotone sweep with a perfectly predicted
branch. A mid-band target makes the choice data-dependent at every step. The
trip count is identical either way (`hi - lo`, since every iteration moves one
pointer by one), so the target changes *predictability* and nothing else.

That turns out to be the whole story of this lane.

### What the x86 corroboration run shows

| lang | mean (ms) | σ | inner loop |
|---|---|---|---|
| Rust (checked, equal-safety) | 447.7 ± 5.9 | 1.3% | branchy |
| Rust (checked + `target-cpu=v3`) | 453.5 ± 11.3 | 2.5% | branchy |
| **Kāra** | **459.7 ± 11.2** | 2.4% | branchy |
| Go | 497.2 ± 11.8 | 2.4% | branchy |
| C (`-march=x86-64-v3`) | 703.0 ± 6.8 | 1.0% | **branchless** |
| C | 709.8 ± 5.8 | 0.8% | **branchless** |
| Rust | 739.7 ± 3.4 | 0.5% | **branchless** |

**Overflow-checked Rust appears to beat unchecked Rust by 65%.** It does not.
`rustc -O` and `clang -O3` both **if-convert** the two-pointer body into
`setge`/`setl`/`cmovge`, which turns the loop into a serial dependency chain —
the next load's address waits on the `cmov`, so every iteration pays full
load-to-use latency with nothing else in flight. `-C overflow-checks=on` emits
`jo` edges that LLVM will not fold into a select, so that build stays branchy and
the predictor runs several iterations ahead.

Re-running every build with `target = max_sum + 1` — identical trip count,
identical instructions, perfectly predicted branch — settles it:

| build | mid-band | `max_sum + 1` |
|---|---:|---:|
| Kāra | 460.7 ms | **208.9 ms** |
| Rust (checked) | 448.6 ms | **233.7 ms** |
| Rust | 740.0 ms | 746.8 ms |
| C | 729.3 ms | 722.2 ms |

The branchy builds more than halve. The branchless builds do not move — which is
what "immune to branch prediction" predicts, and is what confirms the mechanism
instead of merely fitting it. Full disassembly and method in
[`bench/probe/README.md`](bench/probe/README.md).

**So the plain `rust` and `c` rows measure an if-conversion pessimisation, not
the cost of unchecked arithmetic**, and should not be read as "C is 1.5× slower
than Kāra at counting triples." The honest comparator is the equal-safety twin,
and it lands **within 3% of Kāra**.

Worth stating plainly because the direction is the reverse of the usual framing:
Kāra's **default overflow checking** — normally the thing that costs it against
`rustc -O` — is what keeps this loop branchy, and therefore what makes it fast
here.

**It is not `qsort`.** The function-pointer comparator that explained C's
position in [#252](../252-meeting-rooms/) and [#253](../253-meeting-rooms-ii/)
does not explain it here: with the counting loop disabled, the 26 `qsort` calls
cost **10.4 ms of 729** — 1.4% of the lane.

Published numbers await the Apple-silicon host —
`bench/results.container-x86.json` is corroboration only (BENCHMARKS.md § Hosts).

## Kāra features exercised

- **`Vec.from_slice` + `sort()`** — the comparator-free sort on `Vec[i64]`.
- **Converging two-pointer scan** with a data-dependent branch on each step.
- **Upper-bound bisection** written out (`lo + (hi - lo) / 2`, `hi = mid`), the
  form that counts a half-open span correctly when the comparison is strict.
- **Triple-nested loops** over an index space, the O(n³) reference.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the two with
mirrors match Python.

No compiler bugs found — sorting, bisection and nested index loops are all
well-trodden ground in this corpus.

## Running

```bash
karac run three_sum_smaller.kara
karac run three_sum_smaller_brute.kara
karac run three_sum_smaller_bsearch.kara

diff <(karac run three_sum_smaller.kara) <(python3 three_sum_smaller.py) && echo OK
diff <(karac run three_sum_smaller.kara) <(karac run three_sum_smaller_brute.kara) && echo OK
diff <(karac run three_sum_smaller.kara) <(karac run three_sum_smaller_bsearch.kara) && echo OK

# 4,000 randomized arrays with in-band targets, three counters cross-checked
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in three_sum_smaller three_sum_smaller_brute three_sum_smaller_bsearch differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

```bash
# cross-language benchmark (needs hyperfine, rustc, clang, go)
BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
