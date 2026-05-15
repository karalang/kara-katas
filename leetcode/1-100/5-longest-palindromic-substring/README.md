# 5. Longest Palindromic Substring

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Two Pointers, Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-palindromic-substring](https://leetcode.com/problems/longest-palindromic-substring/)

Given a string `s`, return *a* longest palindromic substring of `s`.

**Constraints:** `1 ≤ s.length ≤ 1000`, `s` consists of digits and English letters. (The kata also exercises `s.length == 0` because the algorithm is well-defined there.)

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Expand around center | O(n²) time, O(n) space | [`expand_around_center.kara`](expand_around_center.kara) ✓ via `karac run` / `karac build` | [`expand_around_center.py`](expand_around_center.py) ✓ |

`✓` runs end-to-end today. The O(n) space is a one-shot `Vec[char]` snapshot used for O(1) indexed access (Pattern 3 from [`valid_palindrome.kara`](../../../../karac-rust/examples/leetcode/valid_palindrome.kara)); the algorithm itself uses O(1) auxiliary memory.

### Why expand-around-center

Every palindromic substring has a unique **center**: a single character for odd lengths, a gap between two characters for even lengths. There are exactly `2n − 1` centers in a string of length `n` (`n` odd centers + `n − 1` even centers). For each center, the maximal palindrome around it is found by walking two pointers outward in lockstep and stopping as soon as they go out of range or disagree. The overall answer is the longest palindrome found across all centers.

```
for each center (odd at i, even between i and i+1):
    lo, hi = seed
    while lo >= 0 and hi < n and chars[lo] == chars[hi]:
        lo -= 1
        hi += 1
    # palindrome is chars[lo+1 ..= hi-1]
    # start = lo + 1, length = hi - lo - 1
```

The inner loop runs at most `min(i, n−1−i)` iterations per odd center and `min(i, n−2−i)` per even, summing to O(n²) total. There is no faster *general* algorithm in this complexity class with constant auxiliary memory — Manacher's algorithm gets you to O(n), but at the cost of significantly more code and a transformed-string scratch array. For Kāra's current shape (no fancy string types, no `&str` slicing) expand-around-center is the most direct expression.

### Why the loop's exit-state arithmetic is `[lo + 1, hi - lo - 1]`

When the while loop exits, `lo` and `hi` are *one step past* the last matching pair. So the actual matched range is `chars[lo + 1 ..= hi − 1]`, giving:
- `start = lo + 1`
- `length = hi − (lo + 1) = hi − lo − 1`

For the even seed where `chars[i] != chars[i+1]`, the loop body never executes and this evaluates to `length = (i+1) − i − 1 = 0` — correctly rejected by the strict `> best_len` update on the caller side. The same arithmetic falls out cleanly for the empty-input case: `n = 0`, the outer `while i < n` never enters, and `(best_start, best_len) = (0, 0)` is returned.

## Kāra features exercised

- **`ref String` parameter + `for c in s.chars()`** — read-only string borrow, iterated per Unicode scalar value. Same character-iteration backbone as kata [#3](../3-longest-substring-without-repeating-characters/) — codegen lowers `chars()` to an inline byte-offset loop with a runtime UTF-8 decode helper (`karac_string_decode_char`).
- **`Vec[char]` built via `Vec.new()` + `push`** — explicit snapshot loop in place of `s.chars().collect()`, because `collect()` on a method-chain receiver currently hits a codegen dispatcher gap (the same shape that [`valid_palindrome.kara`](../../../../karac-rust/examples/leetcode/valid_palindrome.kara) trips on). Writing the snapshot as an explicit `for c in s.chars() { chars.push(c) }` works on both backends.
- **`ref Vec[char]` parameter on a helper** — the `expand` helper takes the snapshot by immutable borrow so it can run repeatedly per center without copying. The body-level ownership analysis sees the borrow used only for `.len()` and indexed reads, and the codegen lowers it as a plain pointer + length pair.
- **`Array[i64, 2]` return + tuple-style indexing on the caller** — the same `[start, length]` shape that kata [#1](../1-two-sum/) uses for `Two Sum`'s `[i, j]` result. Once `Option[(i64, i64)]` is solid in the interpreter, this can become a real tuple.
- **`while ... and ... and ...` short-circuit** — three-way conjunction in the loop guard, with the bounds check before the character compare so that out-of-range indexing never happens.
- **Mutable accumulator pattern** — `let mut best_start`, `let mut best_len` updated by guarded `if`. Strict `>` (not `>=`) preserves the left-to-right tiebreak: among equal-length palindromes, the leftmost wins.

No `Map`, no `Set`, no shared structs.

## API shape

Each Kāra solution exposes a pure `longest_palindrome(s: ref String) -> Array[i64, 2]` returning `[start, length]`, plus a thin `report` that prints. `main` calls `report` per test case. The Python file mirrors this with `longest_palindrome(s: str) -> tuple[int, int]` and the same `report` / `main` shape.

The case-driver in `main` binds each literal to a local before calling `report`:

```rust
let c1 = "babad"; report(c1);
```

rather than `report("babad")` inline — same `ref T` rvalue-coercion sugar gap as kata [#3](../3-longest-substring-without-repeating-characters/#api-shape).

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

### Runtime — close to native

Snapshot — M1, 2026-05-15, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Run | Mean ± σ |
|---|---|
| `kara expand_around_center` (codegen) | 45.8 ± 2.4 ms |
| `py   expand_around_center` | 2630 ± 17 ms |
| `rust expand_around_center` | 37.8 ± 2.8 ms |

This kata is **1.21× of Rust** — the tightest codegen-vs-Rust gap in the kata suite that has a meaningful inner loop. Compare with kata [#3](../3-longest-substring-without-repeating-characters/#runtime--and-what-the-gap-measures), where the codegen-vs-Rust ratio is **98×** because that workload is map-dominated and karac's `Map[K, V]` is still type-erased. Here, the inner loop is `chars[lo] == chars[hi]` plus the lo/hi pointer math — no map, no generic dispatch, no boxed values — and karac compiles it down to substantially the same LLVM IR shape as rustc's `Vec<char>` access.

**Where the remaining gap comes from.** Two effects, in rough order:

1. **Bounds checks on every `Vec[char]` read.** karac emits a runtime bounds check on every indexed read into a `Vec[T]`. The inner-loop measurement in the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md) attributes the bulk of the residual `1.2×–3×` codegen-vs-rust gap on tight indexing loops to this. Closes once bounds-check elision lands (planned P0).
2. **No autovectorization of the equality test.** rustc lifts the `chars[lo] == chars[hi]` compare into SIMD-friendly form in some cases; karac's IR doesn't carry the same alignment / no-aliasing hints. Closes incidentally as the LLVM-IR-hint surface grows.

The point of the comparison: when the workload is **not** map-dominated, the v1 codegen-vs-Rust gap is already small. Kata [#3](../3-longest-substring-without-repeating-characters/) shows the worst case (`Map[char, i64]` everywhere → 98×); this kata shows the best case (`Vec[char]` + tight inner loop → 1.21×). The user-facing model is "compiled-with-LLVM speed, modulo specific known gaps" — and kata #5 is the data point that holds up the "yes, on the right workload" half of that claim.

### Codegen vs Python and the wider picture

Same snapshot:

| Run | Mean ± σ | Gap vs Rust |
|---|---|---|
| `rust expand_around_center` | 37.8 ± 2.8 ms | 1.0× |
| `kara expand_around_center` (codegen) | 45.8 ± 2.4 ms | **1.21×** |
| `py   expand_around_center` | 2630 ± 17 ms | **69.6×** |

Python is **~57× slower than Kāra codegen** on this workload. CPython's per-iteration overhead dominates O(n²) algorithms with tight inner loops — there's no equivalent of the C-implemented `dict` to amortize away the interpreter cost, the way there was on kata #3. This is the regime where the codegen-vs-Python gap looks like the textbook "compiled vs interpreted" curve.

### Compile time and binary size

Snapshot — M1, 2026-05-15, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build expand_around_center.kara` | 62.7 ± 1.1 ms | 295.9 KiB |
| `rustc -O expand_around_center.rs` | 98.7 ± 0.6 ms | 455.4 KiB |

Kāra compiles this kata **1.57× faster** than `rustc -O` and produces a binary **~35% smaller**. Consistent with the other katas — the cross-archive LTO + DCE work landed 2026-05-12 keeps the runtime contribution to binary size tight when downstream features (HTTP, JSON, tokio subgraph) aren't reached.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara expand_around_center` (codegen) | 1.6 MiB |
| `rust expand_around_center` | 1.2 MiB |
| `py   expand_around_center` | 6.9 MiB |

The 5000-char String + the `Vec[char]` snapshot are both ~20–40 KB; neither dominates allocation. Kāra's small headroom over Rust is per-call buffer alignment for the runtime's `Vec` allocator (the snapshot is freshly built each call).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil. The **1.21× of Rust** gap here is the strongest single data point in the suite for "Kāra codegen is competitive with rustc on inner-loop algorithms" — and the natural counterpart to kata #3's "Kāra codegen is *not* competitive on map-dominated workloads, and we have a specific plan to fix that."
