# 4. Median of Two Sorted Arrays

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array, Binary Search, Divide and Conquer &nbsp;·&nbsp; **Source:** [leetcode.com/problems/median-of-two-sorted-arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/)

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays. The required runtime complexity is `O(log(m + n))`.

**Constraints:** `0 ≤ m, n ≤ 1000`, `1 ≤ m + n ≤ 2000`, `-10⁶ ≤ nums1[i], nums2[i] ≤ 10⁶`, both inputs sorted non-decreasing.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Binary-search partition | O(log(min(m, n))) time, O(1) extra space | [`binary_search_partition.kara`](binary_search_partition.kara) ✓ via `karac run` / `karac build` | [`binary_search_partition.py`](binary_search_partition.py) ✓ |

`✓` runs end-to-end today.

### Why binary-search partition

The naive "merge then index" answer is O(m + n) and misses the problem's stated bound. The trick is that *we don't need the merged sequence* — only the value(s) at the middle index. Choosing a partition point `i` in `nums1` and the matching `j = (m + n + 1) / 2 − i` in `nums2` carves the two inputs into a "left half" of size `(m + n + 1) / 2` and a "right half" of size `(m + n) / 2`. The partition is **correct** when every value on the left is `≤` every value on the right — checked with two cross-comparisons, `nums1[i − 1] ≤ nums2[j]` and `nums2[j − 1] ≤ nums1[i]`.

```
half = (m + n + 1) / 2          // size of left partition (ceiling for odd T)
lo, hi = 0, m
while lo <= hi:
    i = (lo + hi) / 2
    j = half - i
    left_a, right_a  = a[i-1] or -∞,  a[i] or +∞
    left_b, right_b  = b[j-1] or -∞,  b[j] or +∞
    if   left_a > right_b: hi = i - 1         // too many a's on the left
    elif left_b > right_a: lo = i + 1         // too few  a's on the left
    else: lower = max(left_a, left_b); upper = min(right_a, right_b); done
```

Only `i` is searched — `j` is derived from the invariant — so the loop bounds are `[0, m]` and the runtime is `O(log m)`. Ensuring `m ≤ n` (by swapping inputs at the entry) makes it `O(log min(m, n))`, which also keeps `j` non-negative for every `i`.

### Why ±∞ sentinels

Treating `a[-1] = b[-1] = −∞` and `a[m] = b[n] = +∞` collapses the four boundary cases (`i = 0`, `i = m`, `j = 0`, `j = n`) into the same cross-check shape as the interior. Without sentinels the loop body would need a four-way branch on `(i ∈ {0, m}, j ∈ {0, n})` and a separate "one array fully consumed" path. With them, the cross-checks never spuriously fail at a boundary because `−∞ ≤ x ≤ +∞` is always true. `i64.MIN` / `i64.MAX` are wide enough (≈ ±9.2e18) to serve as sentinels for any value in the problem's `±10⁶` range.

### Why the ceiling on `half`

`half = (m + n + 1) / 2` (integer division) sizes the left partition so that for odd totals the *extra* element falls on the left side. That makes `max(left_a, left_b)` directly equal to the median when `m + n` is odd. For even totals the left and right halves are equal-sized, and the median is `(max(left_a, left_b) + min(right_a, right_b)) / 2` — the arithmetic mean of the two middle elements. The same `half` works for both parities, no branching on `m + n` during the search.

## Kāra features exercised

- **`Slice[i64]` parameter** — `middle_pair` takes both inputs by immutable slice. The LeetCode case-driver passes fresh `Array[i64, N]` literals, which coerce to `Slice[i64]` at the call site (same coercion exercised by kata [#88](../88-merge-sorted-array/)).
- **Recursion across the `Slice[i64]` boundary** — the `m > n` swap is implemented as a one-deep self-call with the arguments reversed (`middle_pair(b, a)`). The second invocation has `m ≤ n` and skips the branch, so the recursion is bounded.
- **`i64.MIN` / `i64.MAX` as ±∞ sentinels** — primitive-type associated constants resolved by the typechecker and lowered to the corresponding LLVM constants. Lets the partition cross-checks treat boundary cases uniformly without branching.
- **`if cond { x } else { y }` as expression** — used to materialise the four sentinel-guarded values (`left_a`, `right_a`, `left_b`, `right_b`) into local `i64` bindings in one line each, same shape as kata [#322 (`coin_change.kara`)](../../../../karac-rust/examples/leetcode/coin_change.kara).
- **`else if` chain** — three-way branch on the cross-check outcome (`left_a > right_b`, `left_b > right_a`, else). Parser desugars to nested `if`/`else` blocks.
- **`Array[i64, 2]` return** — the same `[lower, upper]` pair-shape used by kata [#1](../1-two-sum/) for `[i, j]` and kata [#5](../5-longest-palindromic-substring/) for `[start, length]`. Once `Option[(i64, i64)]` is solid in the interpreter, this can become a real tuple.

No `Map`, no `Vec`, no strings, no shared structs. The hot loop is six `i64` comparisons plus three or four `Slice[i64]` reads per iteration.

## API shape

Each Kāra solution exposes `middle_pair(a: Slice[i64], b: Slice[i64]) -> Array[i64, 2]` returning `[lower_median, upper_median]`, plus a thin `report` that prints. `main` calls `report` per test case. The Python file mirrors this with `middle_pair(a, b) -> tuple[int, int]` and the same `report` / `main` shape.

The case-driver in `main` binds each pair of array literals to locals before calling `report`:

```rust
let a1: Array[i64, 2] = [1, 3];  let b1: Array[i64, 1] = [2];  report(a1, b1);
```

rather than `report([1, 3], [2])` inline — same `ref T` rvalue-coercion sugar gap as kata [#5](../5-longest-palindromic-substring/#api-shape) and kata [#3](../3-longest-substring-without-repeating-characters/#api-shape). The `let` for each fresh `Array[i64, N]` binds the rvalue so the slice coercion has a stable place to point at.

## Output format

**Two lines per test case** — the *lower median* and the *upper median*, where the median is `(lower + upper) / 2`. For odd-total cases the two values are equal (the median is a single element); for even-total cases they are the two middle elements. Concretely:

- `(T + 1) / 2`-th smallest element of the merged sequence → `lower`
- `(T + 2) / 2`-th smallest element of the merged sequence → `upper`
- `median = (lower + upper) / 2`

The integer-pair shape rather than a printed float:

1. Diffs line-for-line between Kāra and Python without depending on float-formatting choices (`2.0` vs `2.00000` vs `2`).
2. Sidesteps any `f64` printing convention differences across the two runtimes.
3. Mirrors kata [#1](../1-two-sum/)'s and kata [#5](../5-longest-palindromic-substring/)'s `Array[i64, 2]` → "two lines per case" shape, so the output convention across the suite is consistent.

Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
2
2
2
3
1
1
2
2
1
2
2
3
4
4
1
1
5
6
-2
-2
```

## Running

```bash
# Kāra (compiled or interpreted — both work)
karac run   binary_search_partition.kara
karac build binary_search_partition.kara && ./binary_search_partition

# Python
python3 binary_search_partition.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs three passes:

1. **Runtime** — `hyperfine --warmup 3 --runs 10` across the three binaries. Inputs are `M = N = 1_000_000` perfectly-alternating sorted prefixes; each outer iter picks `off = k % R` with `R = 1000` and runs `middle_pair_off(base_a, off, M, base_b, off, N)`. `K = 10_000_000` outer iterations. The rotation makes each iter's inputs unique, defeating the cross-iteration CSE that would otherwise hoist the pure `middle_pair_off` call out of the loop and reduce the bench to a multiply-by-`K`.
2. **Compile (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` invocation.
3. **Binary size** — bytes / KiB of the produced artifact.

| File | What it does |
|---|---|
| [`bench/binary_search_partition.kara`](bench/binary_search_partition.kara) | M = N = 1_000_000, R = 1000, K = 10_000_000, rotated alternating-evens / alternating-odds inputs |
| [`bench/binary_search_partition.py`](bench/binary_search_partition.py) | Algorithmic mirror — same M, N, R, K, same offset+length API |
| [`bench/binary_search_partition.rs`](bench/binary_search_partition.rs) | Algorithmic mirror; compiled with `rustc -O` |

All three print the same sum-of-results sink (`Σ_{k<K} (lower + upper) = 20_019_970_000_000`) so the algorithm's output participates in I/O and can't be elided.

Note the bench's `middle_pair_off(a, a_off, a_len, b, b_off, b_len)` signature differs from the kata file's `middle_pair(a, b)`. The offset+length form lets the bench rotate inputs without sub-slicing on the inner loop, which would be zero-cost in Kāra/Rust (slices are pointer + length) but `O(len)` per iter in Python (`list[a:b]` copies). All three languages here use the same offset form so the per-iter work stays comparable.

### Runtime — parity with Rust

Snapshot — M5 Pro, 2026-05-17, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build` and `rustc -O`. Requires karac at commit [`bdac0d8`](../../../../karac-rust/) (internal-linkage fix) or later.

| Run | Mean ± σ |
|---|---|
| `kara binary_search_partition` (codegen) | 16.2 ± 0.2 ms |
| `py   binary_search_partition` | 2.021 ± 0.028 s |
| `rust binary_search_partition` | 15.8 ± 0.3 ms |

This kata is **1.03× of Rust** — inside measurement noise of parity — on a hot inner-loop algorithm with no map, no strings, no shared structs. Just six `i64` comparisons and three or four `Slice[i64]` reads per binary-search step. Same family as kata [#88](../88-merge-sorted-array/#codegen-vs-rust-the-headline) (kara 1.11× faster than Rust on M5 Pro) and kata [#5](../5-longest-palindromic-substring/#runtime--close-to-native) (kara 1.10× faster).

### How we got here

The first measurement on this bench landed at **1.83× of Rust** (kara 28.4 ms vs rust 15.5 ms). The README at that revision pre-baked a "bounds checks dominate" hypothesis to explain it. Empirical investigation killed that hypothesis:

1. **`objdump --syms` on both binaries.** Rust had `middle_pair_off` fully inlined into `main` — the symbol was gone. Kara had `_middle_pair_off` as a `g F __TEXT,__text` global symbol and `main` called it via `bl` 10M times.
2. **`objdump -d` on the inner loop.** Both implementations emit bounds checks (`cmp + b.hs <panic>`) on every indexed slice read; the instruction counts roughly match. Bounds checks were *not* the differentiator.
3. **Manual-inline experiment.** Pasted the binary-search body directly into kara's `main` (no callsite), measured: 17.0 ms — within noise of Rust. The inner loop itself was fine; the call was the problem.

Root cause: `src/codegen/functions.rs:117` was passing `None` to `module.add_function`, which inkwell maps to `ExternalLinkage`. External linkage forces LLVM to keep the function symbol live in the object file even after every call site has been inlined, and the inliner's cost model is more conservative with external callees. Rust by default emits non-`pub` items with internal/hidden linkage, so its inliner has free rein.

Fix shipped in karac [`bdac0d8`](../../../../karac-rust/): non-`pub`, non-FFI-marked user functions now emit `Linkage::Internal`. `pub` keeps External for future multi-crate compatibility; `#[no_mangle]` / `#[used]` keep External so FFI symbols / link-section anchors survive. With the patched karac, `objdump --syms` on this bench's binary shows `middle_pair_off`, `min_i64`, `max_i64` all elided — LLVM inlined them all and dropped the standalone definitions. Cross-kata regression check on the suite is in the [karac commit message](../../../../karac-rust/); the headline: no regressions; kata [#88](../88-merge-sorted-array/) also picked up a 13% speedup from the same change (its `merge` function was hit by the same external-linkage issue).

The lesson worth keeping: **don't pre-bake explanations for perf gaps.** The first three suspects ("bounds checks", "no autovectorization", "branch prediction") were all plausible — and all wrong. The actual cause was visible in five minutes of `objdump --syms` once we looked, but the rhetorical framing on the README would have buried it indefinitely.

### Codegen vs Python

Same snapshot:

| Run | Mean ± σ | Gap vs Rust |
|---|---|---|
| `rust binary_search_partition` | 15.8 ± 0.3 ms | 1.0× |
| `kara binary_search_partition` (codegen) | 16.2 ± 0.2 ms | **1.03×** |
| `py   binary_search_partition` | 2021 ± 28 ms | **128×** |

Python is **~125× slower than Kāra codegen** on this workload. The per-iter CPython bytecode dispatch (function call + `if/elif` chain + four conditional indexed reads + min/max) dominates the algorithm's actual work, and the rotation prevents Python from caching anything across iterations. This is the regime where the codegen-vs-Python gap looks like the textbook "compiled vs interpreted" curve.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-17, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build binary_search_partition.kara` | 53.6 ± 0.8 ms | 32.9 KiB |
| `rustc -O binary_search_partition.rs` | 80.5 ± 0.7 ms | 455.4 KiB |

Kāra compiles this kata **1.50× faster** than `rustc -O` and produces a binary **~93% smaller** (14× the size disparity, vs the ~35% disparity on the other katas in the suite). The much smaller binary tracks the much narrower runtime surface this workload reaches — `Vec.filled` + indexed read/write, `Slice[i64]` indexing, `println(i64)` — and nothing else. The cross-archive LTO + DCE work landed 2026-05-12 elides the rest of the runtime (HTTP, JSON, tokio subgraph, `Map`, `String`, shared structs) cleanly when downstream features aren't reached.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara binary_search_partition` (codegen) | 16.4 MiB |
| `rust binary_search_partition` | 16.4 MiB |
| `py   binary_search_partition` | 85.7 MiB |

**Parity with Rust on memory.** Both implementations hold two `Vec[i64]` / `Vec<i64>` of `M + R = 1_001_000` elements (~8 MiB each, ~16 MiB total), and that dominates the steady state. Kāra's `Vec.filled(n, 0)` short-circuits the doubling-grow that hurt kata [#88](../88-merge-sorted-array/#runtime-memory-peak)'s `Vec.new() + push` baseline — closing that 16 MiB headroom is exactly the fix the kata-88 README points to, and this kata shows it landed.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil. The **1.03× of Rust** result here — together with **memory parity** at the same 16.4 MiB peak RSS — is the strongest single data point in the suite for "Kāra codegen is competitive with rustc on inner-loop algorithms once LLVM's inliner is unblocked." The path to that result was empirical (see *How we got here* above), and the karac change that produced it is the kind of cross-cutting perf win the v1 budget is designed to capture.
