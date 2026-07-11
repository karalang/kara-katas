# 76. Minimum Window Substring

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Hash Table · String · Sliding Window &nbsp;·&nbsp; **Source:** [leetcode.com/problems/minimum-window-substring](https://leetcode.com/problems/minimum-window-substring/)

Given strings `s` and `t`, return the **shortest substring of `s`** that contains **every character of `t`, including multiplicity**. If no such window exists, return `""`.

```
s = "ADOBECODEBANC", t = "ABC"  ->  "BANC"
s = "a",           t = "a"      ->  "a"
s = "a",           t = "aa"     ->  ""     (only one 'a' available)
```

**Constraints:** `1 ≤ |s|, |t| ≤ 10⁵`; English letters. **Follow-up:** can you do it in **O(|s| + |t|)**?

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Sliding window (need/have counts)** ★ | O(\|s\| + \|t\|) | [`minimum_window_substring.kara`](minimum_window_substring.kara) ✓ via `karac run` / `karac build` | [`minimum_window_substring.py`](minimum_window_substring.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output across all twelve test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and the solver agrees with the Python mirror.

> 🐛 **This kata found — and got fixed — a real compiler bug.** The natural solution indexes count tables directly by a byte value: `need[c]` / `have[c]` where `c = s.bytes()[i]` is a **`u8`**. On the first run this **passed under `karac run` but failed `karac build`** with an LLVM module-verification error (`icmp uge i8 %idx, i64 %len` — the bounds check compared the narrow index against the `i64` length without widening it) — a **run/build divergence**, which the corpus treats as a compiler bug, not a kata quirk. Rather than route around it (an un-idiomatic `need[c as i64]`), the bug was filed as **`B-2026-07-11-2`** and **fixed in `karac`**: every `Vec`/`Slice`/`Array` index now routes through the existing `coerce_to_i64` widening helper before the bounds check and GEP (the `Column` index path already did). The kata below is the natural code that now compiles and runs identically across all engines. See `kara/tests/codegen.rs::u8_byte_index_into_vec_widens_to_i64`.

## The sliding window — grow right, shrink left

Two pointers bound a window `[l, r]` over `s`; four running quantities decide when it's "complete" and how tight it can get:

```
need[c]  = how many of char c the window still owes t
required = number of DISTINCT chars t needs
have[c]  = how many of char c the window currently holds
formed   = number of distinct chars whose have[c] has reached need[c]

expand right, adding s[r]:  have[s[r]]++; if have==need for that char, formed++
while formed == required:   record the window if it's the shortest so far,
                            then drop s[l] and l++ (if that breaks a quota, formed--)
```

Each index enters the window once (`r++`) and leaves once (`l++`), so despite the nested loop it is **O(|s| + |t|)** — the linear follow-up. Character counts live in fixed length-128 `Vec[i64]` tables indexed by the byte value (ASCII English letters), the same `s.bytes()` zero-copy view katas [#3](../3-longest-substring-without-repeating-characters/) and [#5](../5-longest-palindromic-substring/) use. Like kata [#5](../5-longest-palindromic-substring/), the harness reports the window's `(start, length)` rather than materialising the substring — and additionally folds a **hash of the window's bytes** into the sink, so the window's *content* is cross-checked against the Python oracle, not just its position.

## Kāra features exercised

- **`u8`-value-as-index count tables** — `need[c]` / `have[c]` where `c = s.bytes()[i]` is a `u8`; the counting idiom that surfaced and drove the fix for `B-2026-07-11-2` (narrow-index widening in codegen).
- **`s.bytes()` zero-copy `Slice[u8]`** — `sb[r]` / `sb[l]` positional byte reads over the `String`'s storage, no `Vec[char]` snapshot; the string-scan idiom of katas [#3](../3-longest-substring-without-repeating-characters/)/[#28](../28-find-the-index-of-the-first-occurrence-in-a-string/).
- **Nested `while formed == required` shrink loop** — the two-pointer window contraction, a three-quantity generalisation of the two-pointer scans in katas [#3](../3-longest-substring-without-repeating-characters/)/[#11](../11-container-with-most-water/).
- **`Array[i64, 2]` multi-return** — `min_window` returns `[best_start, best_len]`, the fixed-size pair-return shared with kata [#48](../48-rotate-image/).
- **`u8` → `i64` cast in a fold** — `sb[start + i] as i64` widens a byte into the rolling window hash (the explicit cast the typechecker requires between `u8` and `i64`).

**v1 note.** Counts and indices are bounded well under i64; the `(start, length)` pair plus the window-bytes hash make the sink both position- and content-sensitive. Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   minimum_window_substring.kara
karac build minimum_window_substring.kara && ./minimum_window_substring

# Python
python3 minimum_window_substring.py

# Verify they agree
diff <(karac run minimum_window_substring.kara) <(python3 minimum_window_substring.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`minimum_window_substring.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5-confirmed (2026-07-10).** Re-measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26; karac from current `main`), replacing the earlier x86-64 cloud-container snapshot. **This kata is an honest loss for kāra:** unlike the sibling compute-bound katas ([#74](../74-search-a-2d-matrix/)/[#75](../75-sort-colors/), where kāra pulled *ahead* on the M5), here kāra stays **last of five** — a two-pointer sliding-window bounds-check-elision gap, root-caused and tracked as `B-2026-07-10-5`. The M5 narrowed the gap (container 1.55× → 1.24× vs C) but did not close or reorder it. `bench/results.json` records the M5 host.

**Workload.** The sliding-window need/have algorithm (the ★) over a fixed `n = 50,000`-symbol sequence (4-symbol alphabet) **built once**, then **K = 5,000** iterations each run `min_window` against a `k`-cycled 3-symbol target (6 patterns, so the result varies with `k` and nothing hoists), folding `(start, length)` into a rolling hash. The O(n) window scan is what's measured (the alphabet is small integers so the count tables index by value; the kata itself exercises the `String.bytes()` `u8`-index path). All five compiled mirrors must agree on `487341820` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99.7 % CPU — the loop-carried hash is not a reduction the auto-par pass splits *at runtime*: current karac emits a `parallel_group` for the batch but the cost model suppresses fan-out, so the default `karac build` and `KARAC_AUTO_PAR=0` are byte-identical and equal-time (350 vs 353 ms). **M5 Pro numbers.**

| Implementation | Wall time |
|---|---|
| go   minimum_window_substring                        | **265.3 ± 2.6 ms** |
| c    minimum_window_substring (clang -O3)            | 282.7 ± 0.5 ms |
| rust minimum_window_substring (rustc -O)             | 285.7 ± 2.2 ms |
| rust minimum_window_substring (rustc -O, overflow-checks=on) | 312.3 ± 7.2 ms |
| **kāra minimum_window_substring**                   | **351.0 ± 7.7 ms** |

**Kāra is last here** — 1.32× behind Go, 1.24× behind the C floor, and 1.12× behind **equal-safety** `rustc -O -C overflow-checks=on` (312.3 ms). Since that peer is *also* overflow-checked, the 1.12× is a **pure codegen gap**, not a safety tax. Instruction counts pin it as a *bounds-check-elision* miss, not slow instructions: kāra retires **12.46 G** instructions to C's 7.58 G (1.64×) and rust_ovf's 11.14 G (1.12×) at the *highest* IPC of the three (8.00) — many cheap surviving bounds checks. The specific miss is the window-left pointer `s[l]`: `l` is incremented only inside the conditional `while formed == required` shrink loop, so LLVM can't prove the relational invariant `l ≤ r < n` — the same conditionally-monotone class kāra folds for binary-search midpoints (kata [#34](../34-find-first-and-last-position-of-element-in-sorted-array/)) but **not yet** for two-pointer windows. Root-caused and tracked as **`B-2026-07-10-5`** (the sliding-window sibling of the midpoint BCE fix). The M5 narrowed the gap from the container's 1.55× vs C to 1.24×, but — unlike [#73](../73-set-matrix-zeroes/)/[#74](../74-search-a-2d-matrix/) — did not reorder it. Python at 1/10 the iteration count is ~1.78 s (~50× kāra projected).

Every *static* metric is at C parity — the gap is isolated entirely to the runtime hot loop. Compile-cold: clang 42.5 ms < rustc 85.2 ms < **karac 89.4 ms** (~2.1× clang, ≈ rustc). Binary size: c 32.9 KiB / **kāra 33.4 KiB** / rust 455.7 KiB / go 2.38 MiB. Peak RSS: c 1.41 / **kāra 1.42** / rust 1.50 / go 3.14 MiB. See [`bench/results.json`](bench/results.json) for exact records.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline seq ratio is the codegen-vs-Rust gap — and here it is an honest **loss**: kāra trails equal-safety `rustc -C overflow-checks=on` by 1.12× on the M5, a pure-codegen bounds-check-elision miss on the two-pointer window (`B-2026-07-10-5`). That is exactly the value of keeping Rust in the harness — it turns a soft "kāra is fast" into a precise, tracked gap with a known fix direction. C calibrates the metal floor (kāra 1.24× behind it), Go is the other native data point (fastest here), Python (run at 1/10 the iteration count, timed separately) the ergonomic foil.
