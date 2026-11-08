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

> ✅ **M5 re-bench (2026-11-01).** Measured on the corpus's **Apple M5 Pro reference machine** (arm64, 6P+12E; clang 21 / rustc 1.95 / go 1.26) with **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23). The first M5 snapshot (2026-07-10/11, legacy backend) replaced an earlier x86-64 cloud-container one. **This kata is an honest loss for kāra:** unlike the sibling compute-bound katas ([#74](../74-search-a-2d-matrix/)/[#75](../75-sort-colors/), where kāra sits *ahead* on the M5), here kāra stays **last of five** — a small, diffuse codegen gap tracked as `B-2026-07-10-5`. The M5 narrowed the gap (container 1.55× → 1.24× vs C in July), and the MIR backend has widened it again to 1.34× (see below). `bench/results.json` records the M5 host.

**Workload.** The sliding-window need/have algorithm (the ★) over a fixed `n = 50,000`-symbol sequence (4-symbol alphabet) **built once**, then **K = 5,000** iterations each run `min_window` against a `k`-cycled 3-symbol target (6 patterns, so the result varies with `k` and nothing hoists), folding `(start, length)` into a rolling hash. The O(n) window scan is what's measured (the alphabet is small integers so the count tables index by value; the kata itself exercises the `String.bytes()` `u8`-index path). All five compiled mirrors must agree on `487341820` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99.9 % CPU — the loop-carried hash is not a reduction the auto-par pass splits: the default `karac build` emits no call of `karac_mir_task_spawn` (verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin), so both run the same single-threaded loop. **M5 Pro numbers, karac g6697158fa, 2026-11-01.**

| Implementation | Wall time |
|---|---|
| go   minimum_window_substring                        | **296.8 ± 10.1 ms** |
| rust minimum_window_substring (rustc -O)             | 320.9 ± 4.4 ms |
| c    minimum_window_substring (clang -O3)            | 323.2 ± 4.4 ms |
| rust minimum_window_substring (rustc -O, overflow-checks=on) | 358.0 ± 17.7 ms |
| **kāra minimum_window_substring**                   | **432.5 ± 11.0 ms** |

**Kāra is last here** — 1.46× behind Go, 1.34× behind the C floor, 1.35× behind `rustc -O`, and 1.21× behind **equal-safety** `rustc -O -C overflow-checks=on` (358.0 ms). Since that peer is *also* overflow-checked, the gap is a **pure codegen gap**, not a safety tax. In the July snapshot (legacy backend) the gap was 1.12× to rust_ovf, 1.23× to `rustc -O` and 1.24× to C, and kāra retired **12.46 G** instructions to C's 7.58 G (1.64×) and rust_ovf's 11.14 G (1.12×) at the *highest* IPC of the three (8.00) — more, cheap instructions, not slower ones. The cause is **diffuse** (~4-5 extra instructions per outer iteration), and an IR-level investigation (`B-2026-07-10-5`) has already *ruled out* the two tempting explanations: the surviving `s[l]` bounds check is **soundly required** (its `l < n` bound holds only through the algorithm's `formed == required` invariant, which the compiler — and Rust, which checks `s[l]` identically — cannot prove), and the `Vec[i64]`-vs-`[i64;4]` count-table difference is **erased by the optimizer** (rebuilding kāra's tables as fixed arrays moved instructions 0.03%). It is a genuine, small, not-yet-localized codegen gap — tracked honestly rather than hand-waved.

**Movement since July (ratios, not ms — every comparator ran 7–18 % slower this session).** Kāra/Rust went 1.23× → 1.35×, Kāra/C 1.24× → 1.34×, Kāra/Go 1.32× → 1.46× — about 10 % relative, borderline against this session's noise. The MIR binary runs 1.15× the instructions of the October legacy build at 1.09× its cycles, so part of the move is the backend's: kāra lost ground on this kata in the MIR switch, and the gap is wider than in July. Python was last measured 2026-07-11 and not re-run: at 1/10 the iteration count it took ~1.78 s (~50× kāra projected, at July's kāra time).

Compile-cold: clang 47.8 ms < rustc 92.1 ms < **karac 126.2 ms** (2.6× clang, 1.37× rustc). Binary size: c 32.9 KiB / **kāra 295.8 KiB** / rust 455.7 KiB / go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Peak RSS: c 1.39 / **kāra 1.45** / rust 1.52 / go 3.11 MiB. See [`bench/results.json`](bench/results.json) for exact records.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline seq ratio is the codegen-vs-Rust gap — and here it is an honest **loss**: kāra trails equal-safety `rustc -C overflow-checks=on` by 1.21× on the M5 (2026-11-01; 1.12× in July), a small, diffuse, not-yet-localized codegen gap (`B-2026-07-10-5`; the two obvious explanations were investigated at the IR level and disproven). That is exactly the value of keeping Rust in the harness — it turns a soft "kāra is fast" into a precise, tracked gap. C calibrates the metal floor (kāra 1.34× behind it), Go is the other native data point (fastest here), Python (run at 1/10 the iteration count, timed separately; last measured 2026-07-11) the ergonomic foil.

### Fixed-size tables are arrays (2026-11-08)

Until 2026-11-08 the bench built its 4-slot `need` and `have` counts as
`Vec.new()` and pushes, heap vectors per call where the C and Rust
mirrors use stack arrays (`[0i64; 4]`); the bench now writes `[0; 4]`.
`karac fix` also took the allow-level lints the changed files had picked
up since. Every arm's output and the bench's sink line are
byte-identical before and after, under `__mir-run`, `__mir-llvm-run` and
`build`, checked against a clean checkout; the bench's time did not move
measurably, the allocation being small next to the work. Any M5 row
above predates the change.
