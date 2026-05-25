# 71. Simplify Path

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Stack &nbsp;·&nbsp; **Source:** [leetcode.com/problems/simplify-path](https://leetcode.com/problems/simplify-path/)

Given an absolute Unix-style path, return its canonical form.

A canonical path:

- starts with `/`,
- has each adjacent pair of directories separated by exactly one `/`,
- contains no `.` or `..` navigation tokens,
- does not end with a trailing `/` unless the result is the root itself.

```
"/home/"                            →  "/home"
"/home//foo/"                       →  "/home/foo"
"/home/user/Documents/../Pictures"  →  "/home/user/Pictures"
"/../"                              →  "/"
"/.../a/../b/c/../d/./"             →  "/.../b/d"   ("..." is a name, not a navigation token)
```

**Constraints:** `1 ≤ path.length ≤ 3000`; `path` consists of English letters, digits, `'.'`, `'/'`, `'_'`; `path` is an absolute path starting with `/`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust | C | Go |
|---|---|---|---|---|---|---|
| One-pass scan + (start, end) index stack | O(n) time, O(n) space | [`simplify.kara`](simplify.kara) ✓ via `karac run` / `karac build` | [`simplify.py`](simplify.py) ✓ | [`bench/simplify.rs`](bench/simplify.rs) ✓ (bench quint) | [`bench/simplify.c`](bench/simplify.c) ✓ (bench quint) | [`bench/go-seq/main.go`](bench/go-seq/main.go) ✓ (bench quint) |

Interpreter and codegen produce identical output to the Python mirror across all 24 test cases in `main`.

## Why a stack — and why index pairs, not strings

The canonical form is determined by what's left on the stack after walking the input. Components fall into three classes:

| Component | Action |
|---|---|
| `'.'` | skip — same directory |
| `'..'` | pop one entry (or stay at root if empty) |
| anything else | push |

A naïve implementation would split the input on `/` into a `Vec[String]`, then push/pop those strings. That works, but allocates a fresh `String` per component and keeps both the input *and* the parts buffer live for the whole walk. The stack here instead holds **`(start, end)` index pairs into the snapshotted input chars** — 16 bytes per entry regardless of how long the component is, and no per-component allocation. The output walk reads characters back out of the input buffer at the recorded positions.

The length is part of the discriminator on purpose. `"..."` is a three-character file name and must be pushed, not interpreted as "parent of parent" — the `/.../a/../b/c/../d/./` LeetCode example exists to catch implementations that look only at the leading byte.

## What this kata uncovered

The first version of this kata couldn't call `Vec.pop` at all — the typechecker accepted it and codegen lowered it, but `karac run` panicked with "method 'pop' not found on type 'unknown'": the interpreter's Vec-method dispatch arm covered `pop_back` / `pop_front` but not the bare `pop` synonym. The kata was the first thing in the corpus to want stack-style push/pop on a `Vec[i64]`, so it surfaced the gap on its first probe.

Per the project's `no workarounds — fix the compiler` discipline, the interpreter dispatch was extended (commit [`7ebb8dd`](../../../../karac-rust/) — `pop` aliased to `pop_back` in `src/interpreter/method_call_seq.rs:207` plus a matching arm in `eval_vec_deque_method`) rather than the kata staying on a `top`-counter simulation of pop. This kata is now the natural integration test for that arm — drop the dispatch and the `'..'` cases (`/../`, `/a/../../b`, `/a/b/c/../..`) immediately panic.

## Kāra features exercised

- **`ref String` + `for c in s.chars()`** — read-only string borrow iterated per Unicode scalar; ASCII input means `chars` and `bytes` would both work, `chars` chosen so f-string append in the output loop avoids a `u8 as char` round-trip.
- **`Vec[char]` snapshot for random access** — `s.chars()` has no `len()` and no random access, but the algorithm needs both (`cs[i + 1]` for the second dot, post-scan position-indexed reads).
- **Parallel `Vec[i64]` start/end stacks with safe-on-empty `pop`** — `Vec.pop` returns `None` on an empty Vec, so the saturate-at-root rule needs no explicit guard; the two stacks stay in lockstep because pushes always go to both together.
- **`and` short-circuit inside `while` and `let` conditions** — `while i < n and cs[i] == slash` is the boundary-safe slash-skip; `is_dotdot` shortcuts the second `cs[]` read when the length doesn't match.
- **f-string interpolation as the String-builder** — `out = f"{out}/"` and `out = f"{out}{c}"` are the available append shape; kara doesn't have `String + String` or `substring` today (both tracked in [`phase-8-stdlib-floor.md`](../../../../karac-rust/docs/implementation_checklist/phase-8-stdlib-floor.md), surfaced from this kata).

No `Map`, no shared structs, no `Vec[String]`.

## Running

```bash
# Kāra — interpreter and codegen both produce the same output today.
karac run   simplify.kara
karac build simplify.kara && ./simplify

# Python
python3 simplify.py

# Verify they agree
diff <(./simplify) <(python3 simplify.py) && echo OK
diff <(karac run simplify.kara) <(python3 simplify.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go file with `go build`, and the Kāra file twice — default `karac build` (auto-par regime) plus a second `KARAC_AUTO_PAR=0 karac build` (seq lane, apples-to-apples with `rustc -O` / `clang -O3` / `go build`). All cached in `bench/target/`, gitignored. Hyperfine runs the two lanes as separate sub-runs; straight `wc` / `time -l` reads cover binary size + memory. Python is timed in a long-workload pass at the same K = 1M.

| File | What it does |
|---|---|
| [`bench/simplify.kara`](bench/simplify.kara) | N = 8 distinct inputs cycled by `k % N` (every component class exercised), K = 1,000,000 outer iters, sink = sum of simplified-output i64 lengths |
| [`bench/simplify.py`](bench/simplify.py) | Algorithmic mirror — same N, K, same input set, same sink formula |
| [`bench/simplify.rs`](bench/simplify.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/simplify.c`](bench/simplify.c) | Algorithmic mirror, hand-rolled scalar baseline with a stack-allocated `char[64]` output buffer — no malloc on the hot path; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror using `strings.Builder`; compiled with `go build` |

The N = 8 inputs are picked to exercise every disposition the inner state machine can take — short trailing-slash (`"/home/"`), single-`..` backtrack (`"/home/user/Documents/../Pictures"`), multi-dot-name + interleaved pops (`"/.../a/../b/c/../d/./"`), heavy tail backtrack (`"/a/b/c/../.."`), heavy slash + dot churn (`"/a//b////c/d//././/.."`), simple alphabet with underscores (`"/abc_123"`), pop-past-root + new push (`"/a/b/../c/../../d"`), and multi-dot file name (`"/...hidden"`). Per-cycle the simplified outputs have total length 5+19+8+2+6+8+2+10 = 60, so K = 1M / 8 cycles × 60 = **7,500,000** at the default parameters. All five compiled impls print the same sink before timing.

### Runtime — seq lane (apples-to-apples, single-threaded)

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 5 --runs 30 --shell=none`. Per BENCH.md's two-lane discipline, the kara binary here is built with `KARAC_AUTO_PAR=0` so the comparison is per-core codegen-quality only — directly stackable against `rustc -O`, `clang -O3`, and `go build`.

| Run | Mean ± σ | User |
|---|---|---|
| `kara simplify` (seq, KARAC_AUTO_PAR=0) | 225.9 ± 5.4 ms | 222.3 ms |
| `rust simplify` | 120.5 ± 3.9 ms | 118.6 ms |
| `c    simplify` | 12.8 ± 0.5 ms | 11.7 ms |
| `go   simplify` | 54.9 ± 1.1 ms | 52.9 ms |

This is the kata that **surfaces the kara stdlib's O(n²) string-builder hole as a bench number**. The per-output-character append shape

```kara
out = f"{out}{c}";
```

builds a fresh String each iteration (no `String.push(char)` / `String.push_str` / `String + String` in the stdlib today, tracked in [`phase-8-stdlib-floor.md`](../../../../karac-rust/docs/implementation_checklist/phase-8-stdlib-floor.md)). For an output of length L this gives O(L²) total work per `simplify` call instead of the O(L) the algorithm should cost. C escapes the cost by writing into a stack-allocated `char[64]` (no allocation per byte), Rust's `String::new()` + `push(char)` writes into a heap buffer with amortized growth (O(L)), and Go's `strings.Builder` does the same. The 17.58× seq gap to C and 1.87× seq gap to Rust here is **not** a karac codegen gap — it's a stdlib feature gap that the codegen is faithfully lowering. Per the project's `no workarounds — fix the compiler` discipline (same posture as the [Vec.pop dispatch fix](#what-this-kata-uncovered) above), the right next step is closing the stdlib hole rather than rewriting this kata to avoid the natural shape; that work is queued under phase 8.

### Runtime — auto-par regime (kara default, multi-core)

Default `karac build` output: karac's auto-par-on-reduction recognizes the `sum = sum + simplify(inputs[idx]).len()` reduction in main's K=1M loop and emits a `karac_par_reduce` dispatch. Hyperfine `--warmup 10 --runs 50` to absorb worker-pool init noise. Same hardware + date as the seq lane.

| Run | Mean ± σ | User | User / wall |
|---|---|---|---|
| `kara simplify` (auto-par default) | 28.5 ± 2.0 ms | 380.4 ms | 13.3× |

Auto-par is **7.92× faster than kara's own seq baseline**, **4.23× faster than rust**, **1.93× faster than go**, **2.23× slower than c**, and **26.1× faster than python**. The User / wall ratio of 13.3× says ~13 cores are doing useful work on the M5 Pro (6 P-cores + ~7 E-cores) — strong scaling despite the allocation-heavy per-iter shape. Per-core efficiency = (222.3 ms seq User) / (380.4 ms auto-par User) = **58%** — lower than kata 65's 94% because each worker hits the system malloc on every `simplify` call (Vec[char] snapshot, two Vec[i64] stacks, the O(L²) String build), and the M5 Pro's allocator serializes some of that. The remaining gap to C is **the same O(n²) stdlib hole as in the seq lane, partially hidden by multi-core dispatch** — closing the phase-8 stdlib floor work should narrow it further. NOT directly comparable to the single-thread rows above per BENCH.md's two-lane discipline — reported separately so the production-default Kara behavior stays visible.

The outer loop body that lights this up:

```kara
let r: String = simplify(inputs[idx]);
sum = sum + r.len();
```

Rust, C, and Go stay single-threaded — none of `rustc -O`, `clang -O3`, or `go build` auto-parallelizes the analogous for-loop without explicit rayon / OpenMP / goroutine annotation.

### Codegen vs Python

Python is **26.1× slower than Kāra auto-par** at the same K (745.1 ms vs 28.5 ms) and **3.30× slower than Kāra seq** (745.1 ms vs 225.9 ms). The serial-vs-serial Kāra/Python comparison is the closest of any kata in the corpus so far — CPython's C-implemented `str` builder + `list.append` / `list.pop` happen to be well-tuned for exactly the per-iter shape this workload exercises, while kara seq pays the O(n²) f-string append cost. The auto-par lowering pulls the gap back to a wider 26.1× by fanning across cores. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was ~2,220× because the inner body there is a few integer ops — interpreter overhead dominates a much larger fraction of CPython's cost when the per-iter work is light.

### Runtime memory — seq slightly above C, auto-par +2.7 MiB

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara simplify` (seq) | 1.4 MiB |
| `kara simplify` (auto-par) | 4.1 MiB |
| `rust simplify` | 1.4 MiB |
| `c    simplify` | 1.1 MiB |
| `go   simplify` | 8.7 MiB |
| `py   simplify` | 7.0 MiB |

Kara seq matches Rust at 1.4 MiB — both 0.3 MiB above C's stack-buffer baseline, both paying the allocator's heap-arena cost on per-iter String/Vec churn. Auto-par adds another ~2.7 MiB on top because each worker thread holds its own per-thread allocator state for the high allocation rate; this is heavier than kata 65's +0.4 MiB delta (which is a compute-bound workload with negligible per-iter allocation). Acceptable cost for the 7.92× wall-clock win, and the seq lane stays available for embedded / constrained-memory targets where the worker pool isn't worth paying for. Go's 8.7 MiB reflects GC heap reservation overhead independent of the actual working set.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-25, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build simplify.kara` (auto-par default) | 70.8 ± 3.9 ms | 312.0 KiB |
| `rustc -O simplify.rs` | 114.9 ± 1.2 ms | 455.7 KiB |
| `clang -O3 simplify.c` | 42.4 ± 0.3 ms | 32.8 KiB |

Kāra compiles this kata **1.62× faster** than `rustc -O` and produces an auto-par binary **1.46× smaller** than `rustc -O`'s. Clang is **1.67× faster** and produces a binary **9.5× smaller** — the same lower-floor C reference shape as kata [#65](../65-valid-number/#compile-time-and-binary-size). The seq-build kara binary is **49.3 KiB** (auto-par dispatch dead-code-eliminated when `KARAC_AUTO_PAR=0`), bringing the kara/rust binary-size ratio to **9.2× smaller** when the runtime weight isn't paid for. The +263 KiB delta between seq and auto-par kara binaries is the `karac_par_reduce` runtime + thread-pool helpers — identical in shape to kata [#65](../65-valid-number/), [#7](../7-reverse-integer/), and [#8](../8-string-to-integer-atoi/), and the cost of the 7.92× wall-clock win.

Compile memory: karac peaks at **10.5 MiB** vs rustc's **32.4 MiB** vs clang's **2.6 MiB** — ~3.1× lower compile-time RAM than rustc, ~4.0× higher than clang. Same ordering as the rest of the suite.

### Why Rust, C, and Go are in the harness

Same rationale as kata [#65](../65-valid-number/#why-rust-c-and-go-are-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware) and the headline ratio for v1 is the codegen-vs-Rust gap; C is the **lower-floor reference** for "what a hand-rolled scalar baseline looks like" with no heap String type; Go is the **GC + builder-tuned-stdlib peer** anchoring the seq lane on the high end. The current result — **seq lane 17.58× behind C, 1.87× behind Rust, 4.11× behind Go (all the same stdlib hole, faithfully lowered); auto-par 4.23× faster than Rust on wall, 1.93× faster than Go, but 2.23× slower than C; 1.46× smaller binary than Rust on auto-par (9.2× smaller on seq); 1.62× faster compile than Rust; ~3.1× lower compile RAM than Rust; +0.3 MiB seq RSS over C, +2.7 MiB auto-par RSS over seq for the worker thread pool** — is **the first kata in the suite where the headline number is a stdlib gap, not a codegen win**. It's also the first kata that gets a clear `User / wall ≈ 13×` reading on auto-par despite an allocation-bound per-iter — concrete evidence that `karac_par_reduce` scales on workloads heavier than the DFA / arithmetic shapes of katas 7/8/65, and the bench will be re-run after the phase-8 stdlib floor work lands to capture the post-fix delta.
