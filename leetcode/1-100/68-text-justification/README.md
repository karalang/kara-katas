# 68. Text Justification

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · String · Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/text-justification](https://leetcode.com/problems/text-justification/)

Format an array of `words` into lines of **exactly** `max_width` characters, **fully justified**: pack as many words per line as fit (at least one space between words), then pad each line to the width by spreading the leftover spaces as evenly as possible between the words — and when they do not divide evenly, the **left** gaps take one extra each. Two lines break the rule: the **last** line and any line holding a **single word** are *left*-justified (single spaces, padded on the right).

```
words = ["This","is","an","example","of","text","justification."], max_width = 16

"This    is    an"      full-justified: 6 spare spaces over 2 gaps → 3 and 3
"example  of text"      6 spare over 2 gaps unevenly → 2 (left) and 1
"justification.  "      last line: left-justified, right-padded
```

**Constraints:** `1 ≤ words.length ≤ 300`; `1 ≤ word.length ≤ max_width ≤ 100`; each word is non-empty, no word exceeds `max_width`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Greedy pack + spread** ★ — one pass: fit the widest run, build the line inline | O(total chars) time, O(line) extra | [`text_justification.kara`](text_justification.kara) ✓ via `karac run` / `karac build` | [`text_justification.py`](text_justification.py) ✓ |
| **Two-phase** — pack every line's word indices into groups, then format each group | O(total chars) time, O(lines) extra | [`text_justification_twophase.kara`](text_justification_twophase.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all eight test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## Two decisions per line

Text Justification is a **simulation**, not a search: the words appear in order and never split, so there is no choice about *which* words go where beyond "take as many as fit." Each line is two mechanical decisions.

**1. Greedy pack.** Starting at word `i`, keep adding words while the minimal layout still fits: with `count` words chosen totalling `line_chars` characters, the tightest width is `line_chars + (count - 1)` — one space per gap. The next word fits iff `line_chars + word_len + count ≤ max_width` (the `count` counting the single-space gaps that would precede it). This greedy choice is *forced* to be optimal here — fewer words on a line can only push work to later lines — so unlike the grid DP of katas [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/) there is no table to fill; the "min over choices" that needed a DP there is absent because order + no-split removes the choice.

**2. Distribute the slack.** `total = max_width - line_chars` spaces fill `gaps = count - 1` slots. Each slot gets `base = total / gaps`; the leftmost `extra = total % gaps` slots get one more. That "extra spaces go left" rule is the whole spacing subtlety, and it is pure integer division — `base` and `extra` from one `/` and one `%`, no floats. The two exceptions collapse to a simpler rule: a **single-word** line (`gaps == 0`, no slot to divide by) and the **last** line are left-justified with single spaces and right-padded to the width.

**Greedy pack + spread** ([`text_justification.kara`](text_justification.kara)) is the ★: one loop per line finds the run and builds the string in place. **Two-phase** ([`text_justification_twophase.kara`](text_justification_twophase.kara)) splits the two concerns — Phase 1 collects every line's word indices into a `Vec[Vec[i64]]` of groups; Phase 2 formats each, where "is this the last line?" is a plain `gi == groups.len() - 1` against the materialised list rather than the ★'s inline `j == n`. It costs the extra index groups the ★ folds away, buying a cleaner separation of *which words* from *how spaced* — the clarity-vs-allocation contrast and an independent cross-check of the identical spacing arithmetic.

## Kāra features exercised

- **`Vec[String]` input + `String` building** — words are a `Vec[String]` (`words[j].len()`, `words[i + g]`); each line is built with `let mut line: String = ""` then `push_str(words[…])` and `push(' ')`, the string-assembly idiom of katas [#67](../67-add-binary/) and [#14](../14-longest-common-prefix/).
- **`Vec[String]` result + re-scan for the checksum** — `full_justify` returns a fresh `Vec[String]`; the harness borrows each line, `line.bytes()` gives a `Slice[u8]` for the positional checksum `Σ (k+1)·byte[k]` (the same byte-scan shape as kata [#58](../58-length-of-last-word/)).
- **`Vec[Vec[i64]]` index groups** (two-phase) — nested `Vec.new()`/`push` of word-index runs, the same nested-Vec shape as katas [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/)'s DP tables, here holding indices rather than counts.
- **Integer `/` and `%` for even spacing** — `base = total / gaps`, `extra = total % gaps`; the leftmost `extra` gaps get `base + 1`. No floats, exactly as the width arithmetic demands.
- **Quoted-line + `sums:` harness** — each output line is printed wrapped in `"…"` so trailing spaces are visible in a diff, plus the folded `sums:` checksum, the byte-for-byte anchor shared with katas [#54](../54-spiral-matrix/) and [#62](../62-unique-paths/)–[#66](../66-plus-one/). A one-space spacing error changes a checksum even when the line width does not.

**v1 note — `group` is a reserved keyword.** The natural name for a line's collected words is `group`, but Kāra reserves `group` (task-group concurrency), so `let mut group: Vec[i64] = …` fails to parse (`Expected pattern, found Group`) — identically under `karac run` and `karac build` (a consistent parse rejection, not a divergence). The two-phase solver uses `grp` instead; the plural `groups` is fine (only the bare keyword collides). Inputs are ASCII, so `String.len()` / `String.bytes()` measure the character width the problem counts, and every width and checksum fits i64 (`max_width ≤ 100`, `words.length ≤ 300`).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   text_justification.kara
karac build text_justification.kara && ./text_justification

# The two-phase approach (identical output):
karac run text_justification_twophase.kara

# Python
python3 text_justification.py

# Verify they all agree
diff <(karac run text_justification.kara) <(python3 text_justification.py)                  && echo OK
diff <(karac run text_justification.kara) <(karac run text_justification_twophase.kara)     && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`text_justification.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** The numbers below were measured on the corpus's **Apple M5 Pro reference machine** (arm64, clang 21 / rustc 1.95 / go 1.26), with Kāra built by karac `g6697158fa` (v2/MIR backend). **Kāra still sits in a tight C/Rust-parity cluster** — 1.03× Rust, 1.02× C, 1.01× overflow-checked Rust, and level with Go (0.99×); all five rows are within 3.2 % end to end. The July feed (karac 0.1.0, 2026-07-28) had 1.01× Rust / 1.00× C / 0.97× Go, so the ratios are flat. Every comparator also ran ~12–13 % slower in this session than in July (machine state), so compare ratios, not milliseconds, across sessions.

**Workload.** A single `full_justify` is cheap, and materialising its `Vec[String]` output every call would make the benchmark measure the **allocator**, not the algorithm (the alloc-domination pitfall BENCHMARKS.md warns against). So the bench runs the *identical* greedy-pack + even-spread logic but **streams the emitted bytes** — word characters and gap spaces — straight into a rolling hash instead of building line strings. No per-call allocation (the fixed 40-word list is built once); what's measured is the algorithm's core: the greedy pack decision, the `total / gaps` + `total % gaps` spacing arithmetic, the extra-spaces-to-the-left placement, and the word-byte reads. The list is justified K = 300,000 times at a **swept** width `max_width = 10 + k % 40` (widths 10–49), so the lines re-break and the spaces re-spread every iteration — nothing is hoistable. The sink is a rolling polynomial hash `h = (h*131 + byte) % 1_000_000_007` over every emitted byte, which captures the exact justified byte stream (a one-space error changes it); all four compiled mirrors must agree on `335237798` before timing.

**Seq-only kata**: the hash is a **loop-carried dependency**, so the loop is not a reduction karac's auto-par pass can split — the default `karac build` stays single-threaded (its emitted IR, `KARAC_MIR_LL`, carries no call of `karac_mir_task_spawn` — re-verified with karac `g6697158fa`), directly comparable to `rustc -O` / `clang -O3` / `go build` on a per-core basis.

### Runtime — seq lane

`--warmup 5 --runs 30 --shell=none`. All single-threaded (`KARAC_AUTO_PAR=0`). **M5 Pro numbers, 2026-11-01.**

| Implementation | Wall time | vs Kāra |
|---|---|---|
| rust text_justification (rustc -O)   | 270.9 ± 3.9 ms | 0.97× |
| c    text_justification (clang -O3)  | 272.1 ± 2.8 ms | 0.98× |
| rust text_justification (`-C overflow-checks=on`) | 275.0 ± 3.1 ms | 0.99× |
| **kāra text_justification**          | **278.0 ± 4.1 ms** | **1.00×** |
| go   text_justification              | 279.6 ± 2.8 ms | 1.01× |

**Kāra sits in a tight parity cluster with C and Rust** — 1.03× `rustc -O`, 1.02× C and 1.01× equal-safety Rust (`-C overflow-checks=on`), and level with Go (0.99×, inside the σ); all five rows are within ~3.2 % end to end. This is the clean C/Rust-parity result the scan-family katas (#62/#63/#66) established, reproduced on the string-heavy justifier, with no #64-style asterisk. Kāra pays for its default overflow checks on the `h*131 + byte` hash arithmetic that `rustc -O`/`clang -O3` skip, so the equal-safety row is the honest Rust baseline; against it the gap is ~1 %.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py text_justification` (K=30k) — last measured 2026-07-08, not re-run | 401.4 ± 1.5 ms |

Python at K=30k was ~0.40 s; projecting to the compiled mirrors' K=300k (~4.0 s) put it **~16× slower than that snapshot's kāra seq** (245.4 ms) — the per-iteration body is the whole pack+spread over 40 words, which CPython runs statement-by-statement. The 2026-11-01 re-bench did not set `KARA_BENCH_INCLUDE_PY`, so this row is not re-measured.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 text_justification.c          | **49.8 ms** |
| rustc -O text_justification.rs          | 85.7 ms |
| **karac build text_justification.kara** | **140.6 ms** |

On the M5 karac compiles at ~2.8× clang and ~1.64× rustc — slower than both. Small-single-file compile time is dominated by process/LLVM-init overhead that differs across the toolchain sets.

### Binary size

| Implementation | Size |
|---|---|
| c    text_justification                | 32.7 KiB |
| **kāra text_justification**            | **295.8 KiB** |
| rust text_justification                | 455.6 KiB |
| go   text_justification                | 2.38 MiB |

Kāra's seq binary is **295.8 KiB** — between C's 32.7 KiB and Rust's 455.6 KiB, and well below Go's 2.4 MiB. Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (this kata's was 33.1 KiB in July); that growth is tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    text_justification                | 1.02 MiB |
| **kāra text_justification**            | **1.05 MiB** |
| rust text_justification                | 1.06 MiB |
| go   text_justification                | 2.59 MiB |

Kāra's peak RSS (**1.05 MiB**) sits within ~32 KiB of C's and a hair under Rust's — the working set (a 40-word list + a scalar hash) is tiny, so peak is the process/runtime base; Go's 2.59 MiB carries its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 text_justification.c          | **2.6 MiB** |
| rustc -O text_justification.rs          | 26.6 MiB |
| **karac build text_justification.kara** | **59.6 MiB** |

On the M5 karac's compile-memory footprint is now the highest of the three — ~2.2× rustc's (it was 22.3 MiB, under rustc's, with the July legacy-backend build).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, Python is the ergonomic foil. On this greedy-pack + even-spread simulation (M5) kāra matches C and Rust to within ~3 % (~1 % against equal-safety Rust) and ties Go — the clean C/Rust-parity result the scan-family katas established, holding on a control-flow-heavy string workload (greedy fit + integer space arithmetic + byte reads) rather than a numeric scan. The load-bearing claim is the five-language sink agreement and that kāra reaches C's/Rust's time at its stricter (overflow-checked) safety posture, with a near-C peak RSS.
