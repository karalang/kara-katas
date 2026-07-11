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

> ⚠️ **Machine caveat.** Measured on a **shared x86-64 Linux cloud container** (Intel Xeon @ 2.80 GHz, 4 vCPU, Linux 6.18.5; karac from current `main`). These are container numbers only — this kata has **no M5 `results.json` yet**; it will be re-benched on the corpus's Apple M5 Pro and the canonical table added then. Don't compare absolute times/sizes/RSS against sibling katas' M5 tables; [`bench/results.container-x86.json`](bench/results.container-x86.json) records the real host.

**Workload.** The sliding-window need/have algorithm (the ★) over a fixed `n = 50,000`-symbol sequence (4-symbol alphabet) **built once**, then **K = 5,000** iterations each run `min_window` against a `k`-cycled 3-symbol target (6 patterns, so the result varies with `k` and nothing hoists), folding `(start, length)` into a rolling hash. The O(n) window scan is what's measured (the alphabet is small integers so the count tables index by value; the kata itself exercises the `String.bytes()` `u8`-index path). All five compiled mirrors must agree on `487341820` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded (the loop-carried hash is not a reduction the auto-par pass can split; the default build is verified equal to `KARAC_AUTO_PAR=0`). **Cloud-container numbers.**

| Implementation | Wall time |
|---|---|
| c    minimum_window_substring (clang -O3)              | **510.6 ± 14.0 ms** |
| rust minimum_window_substring (rustc -O)              | 555.5 ± 25.4 ms |
| go   minimum_window_substring                         | 667.6 ± 6.6 ms |
| rust minimum_window_substring (rustc -O, overflow-checks=on) | 706.9 ± 15.0 ms |
| **kāra minimum_window_substring**                    | **789.6 ± 8.8 ms** |

On this branch-heavy sliding-window scan the container puts **kāra last, ~1.55× the C floor** — and behind even overflow-checked Rust (706.9 ms), so the gap is more than the ~28% overflow-check cost `rustc` pays going `-O` → `-O -C overflow-checks=on` (555 → 707 ms) here. This is a **container data point flagged for the M5 re-bench**, not a tracked regression: the container/M5 ordering has already diverged for sibling katas ([#73](../73-set-matrix-zeroes/) went kāra-4th→1st, [#74](../74-search-a-2d-matrix/) mid-pack→2nd on the M5). Python at 1/10 the iteration count is ~4.3 s.

Compile-cold (clang 79 ms < rustc 117 ms < karac 213 ms) and binary size (c 15.8 KiB, **kāra 324.5 KiB**, go 2.12 MiB, rust 3.77 MiB — kāra links the runtime floor but stays far under Rust/Go); peak RSS c 1.79 / go 2.14 / rust 2.49 / kāra 2.60 MiB. See [`bench/results.container-x86.json`](bench/results.container-x86.json) for exact records.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline seq ratio is the codegen-vs-Rust gap. C calibrates the metal floor, Go is the other native data point, Python (run at 1/10 the iteration count, timed separately) the ergonomic foil. On this branch-heavy window scan the container puts kāra behind the natives — a container data point flagged for the M5 re-bench (the container/M5 ordering has already diverged for sibling katas: see [#73](../73-set-matrix-zeroes/)/[#74](../74-search-a-2d-matrix/)).
