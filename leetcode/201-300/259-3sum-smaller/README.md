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
