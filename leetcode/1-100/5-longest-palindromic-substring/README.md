# 5. Longest Palindromic Substring

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Two Pointers, Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-palindromic-substring](https://leetcode.com/problems/longest-palindromic-substring/)

Given a string `s`, return *a* longest palindromic substring of `s`.

**Constraints:** `1 ≤ s.length ≤ 1000`, `s` consists of digits and English letters. (The kata also exercises `s.length == 0` because the algorithm is well-defined there.)

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Expand around center | O(n²) time, O(1) extra space | [`expand_around_center.kara`](expand_around_center.kara) ✓ via `karac run` / `karac build` | [`expand_around_center.py`](expand_around_center.py) ✓ |

`✓` runs end-to-end today. The algorithm uses O(1) auxiliary memory; positional access into `s` goes through a zero-copy `s.bytes()` view (`Slice[u8]`), so no snapshot Vec is allocated. The LeetCode input alphabet is ASCII (digits + English letters), so byte-equality is character-equality.

### Why expand-around-center

Every palindromic substring has a unique **center**: a single character for odd lengths, a gap between two characters for even lengths. There are exactly `2n − 1` centers in a string of length `n` (`n` odd centers + `n − 1` even centers). For each center, the maximal palindrome around it is found by walking two pointers outward in lockstep and stopping as soon as they go out of range or disagree. The overall answer is the longest palindrome found across all centers.

```
for each center (odd at i, even between i and i+1):
    lo, hi = seed
    while lo >= 0 and hi < n and bytes[lo] == bytes[hi]:
        lo -= 1
        hi += 1
    # palindrome is bytes[lo+1 ..= hi-1]
    # start = lo + 1, length = hi - lo - 1
```

The inner loop runs at most `min(i, n−1−i)` iterations per odd center and `min(i, n−2−i)` per even, summing to O(n²) total. There is no faster *general* algorithm in this complexity class with constant auxiliary memory — Manacher's algorithm gets you to O(n), but at the cost of significantly more code and a transformed-string scratch array. For Kāra's current shape (no fancy string types, no `&str` slicing) expand-around-center is the most direct expression.

### Why the loop's exit-state arithmetic is `[lo + 1, hi - lo - 1]`

When the while loop exits, `lo` and `hi` are *one step past* the last matching pair. So the actual matched range is `bytes[lo + 1 ..= hi − 1]`, giving:
- `start = lo + 1`
- `length = hi − (lo + 1) = hi − lo − 1`

For the even seed where `bytes[i] != bytes[i+1]`, the loop body never executes and this evaluates to `length = (i+1) − i − 1 = 0` — correctly rejected by the strict `> best_len` update on the caller side. The same arithmetic falls out cleanly for the empty-input case: `n = 0`, the outer `while i < n` never enters, and `(best_start, best_len) = (0, 0)` is returned.

## Kāra features exercised

- **`ref String` parameter + `s.bytes()`** — read-only string borrow plus a zero-copy `Slice[u8]` view (design.md § Character type pins `s.bytes()[i]` as the O(1) byte-positional primitive). The codegen lowers `bytes()` to a `{ptr, len}` slice header against the String's existing storage — no allocation, no copy, no element-by-element walk. Replaced the explicit `Vec[char]` snapshot pattern earlier versions used in place of `s.chars().collect()`.
- **`Slice[u8]` parameter on a helper** — the `expand` helper takes the byte view by value (Slice is a borrow form, no `ref` prefix needed). The body uses only `.len()` and indexed reads, both O(1) over the slice header.
- **`Array[i64, 2]` return + tuple-style indexing on the caller** — the same `[start, length]` shape that kata [#1](../1-two-sum/) uses for `Two Sum`'s `[i, j]` result. Once `Option[(i64, i64)]` is solid in the interpreter, this can become a real tuple.
- **`while ... and ... and ...` short-circuit** — three-way conjunction in the loop guard, with the bounds check before the byte compare so that out-of-range indexing never happens.
- **Mutable accumulator pattern** — `let mut best_start`, `let mut best_len` updated by guarded `if`. Strict `>` (not `>=`) preserves the left-to-right tiebreak: among equal-length palindromes, the leftmost wins.

No `Map`, no `Set`, no shared structs.

## API shape

Each Kāra solution exposes a pure `longest_palindrome(s: ref String) -> Array[i64, 2]` returning `[start, length]`, plus a thin `report` that prints. `main` calls `report` per test case. The Python file mirrors this with `longest_palindrome(s: str) -> tuple[int, int]` and the same `report` / `main` shape.

The case-driver in `main` passes each literal directly to `report`:

```rust
report("babad");
```

per design.md § Part 1½ Rule 4 — `ref String` accepts any source unmarked, and the codegen materializes the literal into a stack temp at the call site automatically.

## Output format

**Two lines per test case** — start index, then length — rather than the substring itself. The substring is fully identified by `(start, length)` over the input, and the integer shape:

1. Diffs line-for-line between Kāra and Python without depending on encoding choices.
2. Doesn't hit the codegen path's char-printing gap (`println(c)` for a `char` currently prints the integer codepoint instead of the glyph; tracked separately, doesn't matter for this kata because we never print chars).
3. Mirrors kata [#1](../1-two-sum/)'s `Array[i64, 2]` → "two lines per case" shape, so the output convention across the suite is consistent.

Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
0
3
1
2
0
1
0
1
0
0
0
7
0
3
0
9
3
10
0
3
```

**LeetCode admits multiple valid answers** when palindromes tie for the maximum length. For `"babad"`, both `"bab"` (start=0) and `"aba"` (start=1) are accepted; this kata's strict `>` tiebreak picks the leftmost (`(0, 3)`). The Python and Kāra implementations make the same choice, so the diff stays clean across all cases.

## Running

```bash
# Kāra (compiled or interpreted — both work)
karac run   expand_around_center.kara
karac build expand_around_center.kara && ./expand_around_center

# Python
python3 expand_around_center.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

The bench binaries use the earlier `Vec[char]` snapshot shape (matching Rust's `Vec<char>`) for apples-to-apples comparison; the shipped `expand_around_center.kara` uses `s.bytes()` instead. A future bench refresh can switch both languages to byte-array equivalents — the headline numbers below would shift downward correspondingly.

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs three passes:

1. **Runtime** — `hyperfine --warmup 3 --runs 10` across the three binaries. Input is N = 5000 copies of `'a'` (the worst-case shape for expand-around-center: every center expands all the way to the boundary, no character compare ever short-circuits). K = 10 outer iterations.
2. **Compile (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` invocation.
3. **Binary size** — bytes / KiB of the produced artifact.

| File | What it does |
|---|---|
| [`bench/expand_around_center.kara`](bench/expand_around_center.kara) | N=5000 single-char `'a'` input, K=10 outer iterations, `Vec[char]` snapshot + indexed access |
| [`bench/expand_around_center.py`](bench/expand_around_center.py) | Algorithmic mirror — same input, same K, `list[str]` |
| [`bench/expand_around_center.rs`](bench/expand_around_center.rs) | Algorithmic mirror; `Vec<char>`; compiled with `rustc -O` |

All three print the same sum-of-results sink (`K × (best_start + best_length) = 10 × (0 + 5000) = 50_000`) so the algorithm's output participates in I/O and can't be elided.

### Runtime — kara 1.10× faster than Rust

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build` and `rustc -O`. Requires karac at any commit on the post-`60ad643` (auto-par cost-model gate) trunk.

| Run | Mean ± σ |
|---|---|
| `kara expand_around_center` (codegen) | 35.7 ± 1.8 ms |
| `py   expand_around_center` | 2645 ± 5 ms |
| `rust expand_around_center` | 39.3 ± 3.4 ms |

This kata is **1.10× faster than Rust** — the same shape as kata [#88](../88-merge-sorted-array/#codegen-vs-rust-the-headline) (kara 1.14× faster) and kata [#121](../121-best-time-to-buy-and-sell-stock/#codegen-vs-rust-the-headline) (kara 1.02× faster). The inner loop is `chars[lo] == chars[hi]` plus the lo/hi pointer math — no map, no generic dispatch, no boxed values — and karac compiles it down to substantially the same LLVM IR shape as rustc's `Vec<char>` access.

The May-15 snapshot read **1.21× of Rust** (kara 45.8 ± 2.4 ms vs rust 37.8 ± 2.8 ms). Two karac changes between then and now flipped the sign:

1. **Cross-archive LTO + DCE work** (landed 2026-05-12) — strips unreachable runtime surface (HTTP, JSON, tokio subgraph, `Map`, shared structs) from binaries that don't need it. Binary 295.9 → 49.1 KiB.
2. **Vec drop / allocator pathway fix** — the same drop pathway that closed kata [#88](../88-merge-sorted-array/#runtime-memory-peak)'s 16 MiB headroom tightened this kata's inner-loop µs cost by removing per-iter free overhead on the `Vec[char]` snapshot.

Bounds-check elision on indexed `Vec[char]` reads (the residual the v62 archive flagged at the May-15 snapshot) is still tracked as a P0 follow-up but is no longer the headline story — kara is already past Rust parity without it. SIMD autovectorization of the equality test similarly stays a forward-looking item, not a current gap explanation.

The point of the comparison: kara codegen now beats `rustc -O` on inner-loop-heavy workloads in the kata suite. This kata, kata [#88](../88-merge-sorted-array/), kata [#121](../121-best-time-to-buy-and-sell-stock/), and kata [#6](../6-zigzag-conversion/) collectively make the "yes, on the right workload" half of that claim.

### Codegen vs Python and the wider picture

Same snapshot:

| Run | Mean ± σ | Gap vs Rust |
|---|---|---|
| `kara expand_around_center` (codegen) | 35.7 ± 1.8 ms | **0.91× (kara 1.10× faster)** |
| `rust expand_around_center` | 39.3 ± 3.4 ms | 1.0× |
| `py   expand_around_center` | 2645 ± 5 ms | **67×** |

Python is **~74× slower than Kāra codegen** on this workload. CPython's per-iteration overhead dominates O(n²) algorithms with tight inner loops — there's no equivalent of the C-implemented `dict` to amortize away the interpreter cost, the way there was on kata #3. This is the regime where the codegen-vs-Python gap looks like the textbook "compiled vs interpreted" curve.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build expand_around_center.kara` | 60.1 ± 0.5 ms | 49.1 KiB |
| `rustc -O expand_around_center.rs` | 98.1 ± 0.7 ms | 455.4 KiB |

Kāra compiles this kata **1.63× faster** than `rustc -O` and produces a binary **~89% smaller** (9.3× the size disparity, vs the ~35% disparity measured against the same source on 2026-05-15). The much smaller binary tracks the cross-archive LTO + DCE work landed 2026-05-12 — runtime surface this workload doesn't reach (HTTP, JSON, tokio subgraph, `Map`, shared structs) gets stripped cleanly. The kata-5 binary is slightly larger than the kata 4 / 88 / 121 / 6 cohort (32-33 KiB) because palindrome processing reaches more of the `Vec[char]` + String + char-printing surface; still a fraction of rustc's output. Same shape as kata [#4](../4-median-of-two-sorted-arrays/#compile-time-and-binary-size), [#88](../88-merge-sorted-array/#compile-time-and-binary-size), [#121](../121-best-time-to-buy-and-sell-stock/#compile-time-and-binary-size).

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara expand_around_center` (codegen) | 1.3 MiB |
| `rust expand_around_center` | 1.2 MiB |
| `py   expand_around_center` | 7.0 MiB |

**At parity with Rust** (1.3 vs 1.2 MiB, ~1×). The May-15 snapshot read 1.6 MiB for kara — the small headroom that the v62 archive attributed to per-call buffer alignment closed with the same drop-pathway fix that affected kata [#88](../88-merge-sorted-array/#runtime-memory-peak) and kata [#121](../121-best-time-to-buy-and-sell-stock/#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil. The **1.10× faster than Rust** result here joins kata [#88](../88-merge-sorted-array/) (1.14× faster), kata [#121](../121-best-time-to-buy-and-sell-stock/) (1.02× faster), and kata [#6](../6-zigzag-conversion/) (1.03× faster) in making the case "Kāra codegen is competitive with — or faster than — rustc on inner-loop algorithms once the stdlib surface is in shape".
