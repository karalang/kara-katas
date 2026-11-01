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

**The bench then surfaced a second, deeper gap.** The 2026-05-25 bench (see § Benchmarks § Pre-fix snapshot) made the cost of the only available String-builder shape — f-string self-append `out = f"{out}{c}"` — visible as a wall-clock number: 17.58× behind C, 1.87× behind Rust on the seq lane, with auto-par recovering only half of the gap. The shape itself is **O(n²)**: each `f"{...}"` allocates a fresh String and copies all of the previous `out` into it. C escapes the cost by writing into a stack `char[64]`; Rust and Go via amortized-O(1) builder methods (`String::push` / `strings.Builder`); Kāra had no equivalent in the stdlib.

Per the same `no workarounds — fix the compiler` discipline, karac was extended (commit [`7ef42b9`](../../../../karac-rust/), 2026-05-25) with `String.push(char)` end-to-end (typechecker / interpreter / codegen, reusing the existing `karac_string_encode_char` runtime helper for 1–4 UTF-8 byte encoding) plus a `push_str` interpreter dispatch arm that closed a side gap (push_str typechecked + codegened cleanly but `karac run` panicked). The kata source was rewritten to the natural shape `out.push_str("/")` + `out.push(cs[p])`; the post-fix bench is recorded in § Benchmarks above.

## Kāra features exercised

- **`ref String` + `for c in s.chars()`** — read-only string borrow iterated per Unicode scalar; ASCII input means `chars` and `bytes` would both work, `chars` chosen so f-string append in the output loop avoids a `u8 as char` round-trip.
- **`Vec[char]` snapshot for random access** — `s.chars()` has no `len()` and no random access, but the algorithm needs both (`cs[i + 1]` for the second dot, post-scan position-indexed reads).
- **Parallel `Vec[i64]` start/end stacks with safe-on-empty `pop`** — `Vec.pop` returns `None` on an empty Vec, so the saturate-at-root rule needs no explicit guard; the two stacks stay in lockstep because pushes always go to both together.
- **`and` short-circuit inside `while` and `let` conditions** — `while i < n and cs[i] == slash` is the boundary-safe slash-skip; `is_dotdot` shortcuts the second `cs[]` read when the length doesn't match.
- **`String.push_str(&str)` + `String.push(char)` as the String-builder** — `out.push_str("/")` for the separator and `out.push(c)` for each component byte; both mutate `out` in place with amortized O(1) per call. Kāra's first version of this kata used f-string self-append (`out = f"{out}{c}"`) because `String.push(char)` wasn't on the stdlib surface; the bench made the O(n²) cost visible (see § Benchmarks § Pre-fix snapshot) and the surface was added in karac commit [`7ef42b9`](../../../../karac-rust/) (2026-05-25). `String + String` is still tracked in [`phase-8-stdlib-floor.md`](../../../../karac-rust/docs/implementation_checklist/phase-8-stdlib-floor.md) but is no longer load-bearing for this kata.

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

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go file with `go build`, and the Kāra file twice — default `karac build` (auto-par regime) plus a second `KARAC_AUTO_PAR=0 karac build` (seq lane, apples-to-apples with `rustc -O` / `clang -O3` / `go build`). All cached in `bench/target/`, gitignored. Hyperfine runs the two lanes as separate sub-runs; straight `wc` / `time -l` reads cover binary size + memory. The par sub-run also times three hand-parallelised comparators of the same K = 1M reduction: Rust `rayon` `par_iter` ([`bench/rayon/`](bench/rayon/)), Go goroutines + `WaitGroup` ([`bench/go-par/`](bench/go-par/main.go)), and C pthreads ([`bench/simplify_par.c`](bench/simplify_par.c), the bare-metal floor). Python is timed in a long-workload pass at the same K = 1M (only with `KARA_BENCH_INCLUDE_PY=1`).

| File | What it does |
|---|---|
| [`bench/simplify.kara`](bench/simplify.kara) | N = 8 distinct inputs cycled by `k % N` (every component class exercised), K = 1,000,000 outer iters, sink = sum of simplified-output i64 lengths |
| [`bench/simplify.py`](bench/simplify.py) | Algorithmic mirror — same N, K, same input set, same sink formula |
| [`bench/simplify.rs`](bench/simplify.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/simplify.c`](bench/simplify.c) | Algorithmic mirror, hand-rolled scalar baseline with a stack-allocated `char[64]` output buffer — no malloc on the hot path; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror using `strings.Builder`; compiled with `go build` |

The N = 8 inputs are picked to exercise every disposition the inner state machine can take — short trailing-slash (`"/home/"`), single-`..` backtrack (`"/home/user/Documents/../Pictures"`), multi-dot-name + interleaved pops (`"/.../a/../b/c/../d/./"`), heavy tail backtrack (`"/a/b/c/../.."`), heavy slash + dot churn (`"/a//b////c/d//././/.."`), simple alphabet with underscores (`"/abc_123"`), pop-past-root + new push (`"/a/b/../c/../../d"`), and multi-dot file name (`"/...hidden"`). Per-cycle the simplified outputs have total length 5+19+8+2+6+8+2+10 = 60, so K = 1M / 8 cycles × 60 = **7,500,000** at the default parameters. All five compiled impls print the same sink before timing.

### Runtime — seq lane (apples-to-apples, single-threaded)

M5 Pro, 2026-11-01, hyperfine `--warmup 5 --runs 30 --shell=none`, Kāra built by karac `g6697158fa` (v2/MIR backend). Per BENCH.md's two-lane discipline, the kara binary here is built with `KARAC_AUTO_PAR=0` so the comparison is per-core codegen-quality only — directly stackable against `rustc -O`, `clang -O3`, and `go build`. Requires karac at commit [`7ef42b9`](../../../../karac-rust/) (the `String.push(char)` + `push_str` interpreter dispatch slice) or later.

| Run | Mean ± σ | User |
|---|---|---|
| `kara simplify` (seq, KARAC_AUTO_PAR=0) | 153.4 ± 10.2 ms | 152 ms |
| `rust simplify` | 171.4 ± 10.1 ms | 170 ms |
| `rust simplify` (`-C overflow-checks=on`, equal-safety) | 167.9 ± 11.3 ms | 167 ms |
| `c    simplify` | 14.1 ± 0.4 ms | 13 ms |
| `go   simplify` | 60.3 ± 1.5 ms | 59 ms |

Single-thread kara is now **ahead of Rust** — 0.90× `rustc -O` and 0.91× equal-safety Rust (both gaps about one σ) — 2.5× behind Go, and 10.9× behind C. Against the July feed (karac 0.1.0, 2026-07-28: 1.05× Rust, 3.3× Go, 14.2× C) kāra gained on every comparator by more than 10 % relative; the comparators themselves ran 0–13 % slower in this session, so read the move in ratios, not milliseconds. (Older snapshots: 2026-06-05 read kara 144.8 / rust 134.5 / c 13.1 / go 53.3 ms, 1.08× Rust; 2026-05-25 read kara 122.2 / rust 120.8 / c 13.0 / go 55.1. An earlier revision of this paragraph mis-stated the Go relationship as "2.22× ahead"; Go's `strings.Builder` + GC-arena allocator beats both heap-`String` mirrors on this shape, and kara has trailed it in every snapshot.) C's ~11× lead is the stack-allocated `char[64]` output buffer shape (no allocation per byte vs the kara/rust heap-`String::push`); on a workload where the algorithm doesn't need a heap-owned output, C will always win this lane. The kara seq picture reads as **codegen quality at or slightly ahead of Rust on a heap-String workload** — the gap to C is the cost of the algorithmic shape, not the compiler.

### Runtime — auto-par regime (kara default, multi-core)

Default `karac build` output: karac's auto-par-on-reduction recognizes the `sum = sum + simplify(inputs[idx]).len()` reduction in main's K=1M loop and parallelises it — the default build's emitted IR (`KARAC_MIR_LL`) carries a call of `karac_mir_task_spawn` and the `KARAC_AUTO_PAR=0` twin's does not (re-verified with karac `g6697158fa`). Hyperfine `--warmup 10 --runs 50` to absorb worker-pool init noise. Same hardware + date as the seq lane; the three comparators parallelise the same reduction by hand.

| Run | Mean ± σ | User | User / wall |
|---|---|---|---|
| `c    simplify` (pthreads — metal floor) | 3.0 ± 1.7 ms | 13 ms | 4.3× |
| `go   simplify` (goroutines + WaitGroup) | 6.3 ± 0.3 ms | 41 ms | 6.5× |
| `kara simplify` (auto-par default) | 42.5 ± 5.0 ms | 536 ms | 12.6× |
| `rust simplify` (rayon `par_iter`) | 46.7 ± 3.8 ms | 753 ms | 16.1× |

Auto-par runs **0.91× rayon** — ahead of hand-written Rust parallelism with no annotation — and 6.8× behind Go's goroutines and 14× behind the C pthreads floor; the July feed read 1.04× rayon, 10.8× Go, 21.8× C, so kāra gained on every par comparator too. The ranking inside the par lane mirrors the seq lane: the heap-`String` mirrors (kāra, Rust) sit together, Go's builder and C's stack buffer far ahead. Auto-par is **3.6× faster than kara's own seq baseline** (153.4 → 42.5 ms). The User / wall ratio of 12.6× says ~12–13 cores are busy on the M5 Pro (6 P-cores + ~6 E-cores), but per-core efficiency = (152 ms seq User) / (536 ms auto-par User) = **28%** — each worker still hits the system malloc on every `simplify` call (Vec[char] snapshot + the two Vec[i64] stacks), so this lane is allocator-contention-bound, not dispatch-bound. (History: the 2026-06-05 snapshot read 21.5 ms auto-par, 6.7× over seq at 55 % per-core efficiency; the July feed already read 51.4 ms, 3.4×.) NOT directly comparable to the single-thread rows above per BENCH.md's two-lane discipline — reported separately so the production-default Kara behavior stays visible.

The outer loop body that lights this up:

```kara
let r: String = simplify(inputs[idx]);
sum = sum + r.len();
```

The seq Rust, C, and Go mirrors stay single-threaded — none of `rustc -O`, `clang -O3`, or `go build` auto-parallelizes the analogous for-loop; their par-lane rows above needed explicit rayon / pthreads / goroutine code.

### Pre-fix snapshot — how the O(n²) String hole surfaced

**Pre-2026-05-25 snapshot** (same hardware, same K, karac before commit [`7ef42b9`](../../../../karac-rust/)): kara seq 225.9 ± 5.4 ms / kara auto-par 28.5 ± 2.0 ms. The kata's per-output-char shape

```kara
out = f"{out}/";
out = f"{out}{c}";
```

was the only available String-builder pattern in the stdlib — f-string interpolation builds a fresh String per call (cost proportional to current `out` length), giving **O(L²)** total work per `simplify` call for an output of length L. C escapes the cost by writing into a stack-allocated `char[64]` (no allocation per byte); Rust's `String::push(char)` writes into a heap buffer with amortized power-of-two growth (O(L)); Go's `strings.Builder` does the same. The 17.58× seq slowdown vs C and the 1.87× seq slowdown vs Rust pre-fix were **not** a karac codegen gap — they were a stdlib feature gap that the codegen was faithfully lowering.

Per the project's `no workarounds — fix the compiler` discipline (same posture as the [Vec.pop dispatch fix](#what-this-kata-uncovered) above), karac was extended (commit [`7ef42b9`](../../../../karac-rust/), 2026-05-25) with `String.push(char)` on the full pipeline (typechecker / interpreter / codegen), reusing the existing `karac_string_encode_char` runtime helper for the 1–4 UTF-8 byte encoding and sharing `push_str`'s power-of-two growth + heap-free geometry. The kata source was then rewritten to use the natural shape

```kara
out.push_str("/");
out.push(cs[p]);
```

which is amortized O(1) per call. Closing the gap dropped this kata's seq wall from **225.9 ms → 122.2 ms (1.85× speedup)** and the auto-par wall from **28.5 ms → 20.7 ms (1.38× speedup)**, moving kara from 1.87× behind Rust to **parity with Rust on the seq lane** and from 4.23× ahead on auto-par to **5.83× ahead on auto-par**. The gap to C narrowed from 2.23× slower to 1.58× slower on the auto-par lane — what's left is the algorithmic shape (heap-owned String vs stack buffer), not a karac limitation.

### Codegen vs Python

Python was last measured 2026-06-05 and not re-run (the 2026-11-01 re-bench did not set `KARA_BENCH_INCLUDE_PY`). In that snapshot Python was **34.5× slower than Kāra auto-par** at the same K (742.5 ms vs 21.5 ms) and **5.13× slower than Kāra seq** (742.5 ms vs 144.8 ms). The post-fix serial-vs-serial Kāra/Python ratio widened from 3.30× (pre-fix) to ~5.1× because closing the stdlib hole halved Kāra's seq cost while CPython's per-iter cost was unchanged. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was ~2,220× because the inner body there is a few integer ops — interpreter overhead dominates a much larger fraction of CPython's cost when the per-iter work is light.

### Runtime memory — seq slightly above C, auto-par +~3 MiB

2026-11-01 feed:

| Run | Peak RSS |
|---|---|
| `kara simplify` (seq) | 1.11 MiB |
| `kara simplify` (auto-par) | 2.58 MiB |
| `rust simplify` | 1.22 MiB |
| `rust simplify` (rayon) | 4.69 MiB |
| `c    simplify` | 1.02 MiB |
| `c    simplify` (pthreads) | 1.33 MiB |
| `go   simplify` | 8.22 MiB |
| `go   simplify` (goroutines) | 4.23 MiB |
| `py   simplify` (last measured 2026-06-05, not re-run) | 7.0 MiB |

Kara seq at 1.11 MiB stays slightly **below** Rust's 1.22 MiB — both ~0.1–0.2 MiB above C's stack-buffer baseline, the cost of the heap String/Vec churn. Auto-par adds ~1.5 MiB on top and stays under rayon's 4.69 MiB (the 06-05 snapshot read 1.2 → 3.1 MiB, +1.9; the 05-25 sample read +2.5) because each worker thread holds its own per-thread allocator state (libmalloc tcache) for the per-call allocation rate; pre-fix this delta was ~2.7 MiB so closing the O(n²) hole pulled it down marginally (the per-iter alloc count dropped from ~L+5 to ~5). Acceptable cost for the 3.6× wall-clock win, and the seq lane stays available for embedded / constrained-memory targets where the worker pool isn't worth paying for. Go's 8.2 MiB reflects GC heap reservation overhead independent of the actual working set.

The +2.5 MiB delta is **steady-state**, not a leak — verified by running at K=100K, 1M, 10M (RSS 3.5 / 3.6 / 4.1 MiB; only 0.7 MiB of growth across a 100× K-increase, which is steady-state allocator metadata + minor heap fragmentation). Users who need to trade parallelism for memory can dial the worker count down via `KARAC_PAR_WORKERS=N` (karac commit [`d33b389`](../../../../karac-rust/), 2026-05-25 — same ergonomic shape as `RAYON_NUM_THREADS` / `OMP_NUM_THREADS` / `GOMAXPROCS`):

| Setting | Auto-par RSS | Wall (relative) |
|---|---|---|
| (default, ~13 workers) | 3.8 MiB | 1.0× |
| `KARAC_PAR_WORKERS=4` | 1.8 MiB | ~2.5× slower |
| `KARAC_PAR_WORKERS=2` | 1.5 MiB | ~5× slower |
| `KARAC_PAR_WORKERS=1` | 1.3 MiB | matches seq lane (single-worker fast path) |

`KARAC_PAR_WORKERS=1` engages `karac_par_reduce`'s single-worker fast path, so the worker pool's per-thread tcache disappears entirely and RSS lands at the seq lane's level (these probe rows are 2026-05-25 single-shot readings; the 06-05 seq sample reads 1.2 MiB — page-level noise) — useful for container CPU quotas, multi-tenant servers, or M-series battery-aware runs (`KARAC_PAR_WORKERS=6` keeps work off the E-cores). Invalid or `0` values fall back to the auto-detect default. *(Note 2026-11-01: v2/MIR-built binaries no longer read `KARAC_PAR_WORKERS` — the probe above is legacy-backend history; the worker-count knob is now `KARAC_THREADS`, and `KARAC_THREADS=1` runs this kata at seq-lane speed.)*

The deeper fix — per-worker scratch buffers in `karac_par_reduce` so the worker pool stops paying the per-iter allocation cost in the first place — is queued under [phase-7-codegen.md § Auto-par runtime: per-worker scratch buffers](../../../../karac-rust/docs/implementation_checklist/phase-7-codegen.md). That one addresses the root cause (closing the alloc-rate-driven tcache scaling) rather than masking it via reduced parallelism.

### Compile time and binary size

M5 Pro, 2026-11-01, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build simplify.kara` (auto-par default) | 180.0 ± 4.9 ms | 377.1 KiB |
| `rustc -O simplify.rs` | 126.2 ± 2.7 ms | 455.7 KiB |
| `clang -O3 simplify.c` | 46.9 ± 0.6 ms | 32.8 KiB |

karac now compiles this kata **1.43× slower** than `rustc -O` (it was 1.46× faster in the 2026-05-25 / 06-05 snapshots) and produces an auto-par binary **1.21× smaller** than `rustc -O`'s (466,632 / 386,168 B). Clang is **3.8× faster** than karac with a **13.9× smaller binary than Rust's** — the same lower-floor C reference shape as kata [#65](../65-valid-number/#compile-time-and-binary-size). The seq-build kara binary is **295.8 KiB** (302,888 B), 1.54× smaller than Rust's; the +81 KiB delta between seq and auto-par kara binaries is the task-spawn runtime + thread-pool helpers, the cost of the 3.6× wall-clock win. Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (this kata's seq build was 33.5 KiB on legacy); that growth is tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).

Compile memory: karac peaks at **61.8 MiB** vs rustc's **32.2 MiB** vs clang's **2.6 MiB** — ~1.9× rustc's compile-time RAM and ~24× clang's (the 06-05 snapshot had karac at 14.6 MiB, ~2.2× *under* rustc).

### Why Rust, C, and Go are in the harness

Same rationale as kata [#65](../65-valid-number/#why-rust-c-and-go-are-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware) and the headline ratio for v1 is the codegen-vs-Rust gap; C is the **lower-floor reference** for "what a hand-rolled scalar baseline looks like" with no heap String type; Go is the **GC + builder-tuned-stdlib peer** anchoring the seq lane on the high end. The current result (2026-11-01) — **seq lane ahead of Rust (0.90× `rustc -O`, 0.91× equal-safety), 2.5× behind Go's builder-tuned stdlib, 10.9× behind C on algorithmic shape; auto-par 0.91× hand-written rayon, with a 3.6× intra-Kāra seq→par speedup; 1.21× smaller binary than Rust on auto-par (1.54× smaller on seq); 1.43× slower compile than Rust at ~1.9× its compile RAM; 1.11 MiB seq RSS (below Rust's 1.22), 2.58 MiB auto-par RSS for the worker thread pool (below rayon's 4.69)** — comes from the kata that surfaced the **O(n²) String-builder hole**, drove the `String.push(char)` + `push_str` stdlib fix in karac commit [`7ef42b9`](../../../../karac-rust/), and validated the fix end-to-end via the pre/post snapshots above. The auto-par User/wall reading (~12.6×) shows the parallel reduction spreading across the cores on a workload heavier than the DFA / arithmetic shapes of katas 7/8/65 — heap allocation per iter narrows the per-core efficiency to ~28%, but the multi-core win (3.6× over seq, ahead of rayon) is still substantial.

---

**Bug ledger:** this kata surfaced `B-2026-05-20-1`, `B-2026-05-25-1` — see the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).

## Bug ledger

**Surfaced [`B-2026-11-01-17`](../../../../kara/docs/bugs-v2.md)** (perf, open). With exactly two workers (`KARAC_THREADS=2`) the auto-par binary runs 1.6–2.6× slower than with one (0.24–0.39 s against 0.15 s), on 5× the cycles for 7% more instructions; three or more workers run 0.04–0.06 s. The published par row uses the default worker count and is unaffected. Measured 1 Nov 2026 with karac g6697158fa.
