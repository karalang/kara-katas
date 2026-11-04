# 394. Decode String

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Stack, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/decode-string](https://leetcode.com/problems/decode-string/)

Decode `k[encoded]` runs, where the bracketed string repeats `k` times. Runs
nest.

```
"3[a]2[bc]"      →  "aaabcbc"
"3[a2[c]]"       →  "accaccacc"
"2[abc]3[cd]ef"  →  "abcabccdcdcdef"
```

**Constraints:** `1 ≤ s.length ≤ 30`; `s` is lowercase letters, digits, and
brackets; `1 ≤ k ≤ 300`; the decoded output fits in `10⁵`. Every `[` has a
matching `]`; the input is always valid.

## Why this kata — the lexer's escape / repeat machinery

The closest corpus analog to the self-hosted lexer's escape and repeat-count
handling. A single left-to-right byte scan drives the same three moves the
lexer makes when it reads `\u{1F600}` or a counted construct:

| Lexer surface | This kata |
|---|---|
| **digit-run → integer** (`from_str_radix`, the count/codepoint folds) | `k = k*10 + (b - b'0')` over a digit run |
| **nesting stack** (bracket / group depth) | `Vec[String]` + `Vec[i64]` parallel stacks (iterative) or the call stack (recursive) |
| **push / concat output storm** | `cur = prev + cur*count`, plus literal-run appends |
| **byte classification + token-text slice** (§1 + §3) | `is_letter` byte test + zero-copy `s[i..j]` letter-run append |

## Approaches

Two styles, both byte-identical to the Python oracle across all 14 cases,
under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Iterative — explicit stacks** ★ | [`decode_string.kara`](decode_string.kara) | `Vec[String]`/`Vec[i64]` stacks; `]` pops + repeats |
| Recursive descent | [`decode_string_recursive.kara`](decode_string_recursive.kara) | `decode_at(s, start) -> (String, i64)`; `k[` recurses, returns segment + close position |
| Reference oracle | [`decode_string.py`](decode_string.py) | known-correct LeetCode answer |

Both follow the [lexer string-scan shape](../../../README.md): scan the line's
zero-copy `bytes()` view with `b'…'` byte literals, classify, and append each
letter run as **one zero-copy slice** `s[i..j]` — not char-by-char `push`. The
iterative style's repeat step (`cur = prev + cur*count`) uses **`String.repeat`**;
the recursive style appends by loop because its `cur` source is tuple-bound (see
below).

## What this kata uncovered

The byte-scan **correctness** surface stayed flat — byte classification,
`(b - b'0') as i64` digit folding, `Vec[String]` stack push/pop with `.unwrap()`,
zero-copy `s[i..j]` slice append, multi-value `(String, i64)` return + destructure,
and recursion all compiled and ran first-try under both backends. But adding the
**repeat** primitive and **benching** surfaced three karac gaps:

**1 — `String.repeat(n)` didn't exist** ([`bb10c5ce`]). The kata's core op
(`cur*count`) had no primitive — Rust/Go/Python all have one. Added across
typecheck + interp + codegen (single `malloc(n*len)` + an `n×` memcpy loop). The
iterative style now uses `cur.repeat(count)`. (`String * int`, the other spelling,
typecheck-warns then panics `unreachable!` in interp — tracked, B-2026-06-12-4.)

**2 — String methods don't dispatch on tuple-destructured bindings** (tracked,
B-2026-06-12-3). The recursive style's `inner` (from `let (inner, after) = …`)
can't call `inner.repeat(k)` *or* `inner.substring(…)` under codegen (`no handler …
on variable 'inner'`) — pre-existing, affects all String methods on tuple-bound
vars. So that style appends by `push_str` loop; the iterative style (whose `cur` is
a tracked `String` local) uses `repeat`.

**3 — `let s = <fn returning String>` leaks** (tracked, B-2026-06-12-5, **HIGH**).
The bench's runtime RSS was **86.9 MiB** vs Rust's 1.2 MiB — a function-returned
`String` bound to a `let` isn't freed at the caller's scope exit (general: any
`let s = f()` with `f -> String`; the self-hosted compiler returns `String`
everywhere). Isolated to 32.5 MiB at 2M iters; a `Vec[String]`-returning fn bound
the same way is clean, so the let-arm drop registration classifies Vec-returning
calls but misses String-returning ones. **Not yet fixed** — a delicate
drop-tracking change (double-free risk) in a file an active concurrent session is
editing; it warrants a focused ASAN-gated slice. The seq-lane *time* below is
unaffected; the memory column is dominated by this leak and is **not** a meaningful
Kāra-vs-Rust comparison until it's fixed.

[`bb10c5ce`]: ../../../../kara/

## Benchmarks
Workload: decode a fixed nested template (decodes to 52 chars, three repeat
levels) `ITERS=800k` times, reducing to total decoded length (sink 41 600 000).
Same iterative-stack algorithm across all five; each language's idiomatic repeat
(Kāra `String.repeat` / Rust `str::repeat` / Go `strings.Repeat` / C manual /
Python `*`). Apple M5 Pro; `bench/bench.sh` (`hyperfine`). **Seq lane** =
single-threaded (Kāra built `KARAC_AUTO_PAR=0`).

### Seq lane — runtime (single-threaded, apples-to-apples)

Snapshot — M5 Pro, **2026-11-04**, karac `0.8.0-dev.14370+gd33cb285d` (gd33cb285d, the v2/MIR backend).

| | Go | C | Rust (`overflow-checks=on`) | Rust | **Kāra (seq)** |
|---|---|---|---|---|---|
| time | 172.6 ± 6.8 ms | 241.7 ± 13.6 ms | 282.7 ± 8.2 ms | 289.1 ± 7.6 ms | **338.2 ± 6.5 ms** |
| vs Kāra | 1.96× faster | 1.40× faster | 1.20× faster | 1.17× faster | — |

**Kāra is the slowest of the four native mirrors here**: 1.17× `rustc -O`, 1.20×
equal-safety Rust, 1.40× `clang -O3` and 1.96× Go. The 2026-08-05 feed read 0.99×
`rustc -O`, 0.99× C and 1.64× Go, a three-way tie at the C/Rust floor, so this is a
real slip rather than comparator drift: exact counts against legacy dd86e3955
(`KARAC_AUTO_PAR=0`) are 1.27× instructions and 1.26× cycles, filed as
[`B-2026-11-04-30`](#bug-ledger). Go remains genuinely ahead: `strings.Repeat` plus GC
string handling suits this kernel unusually well, and Go's 106 % CPU shows it is
buying part of that with concurrent GC on a second core (see the Go-GC caveat in
[BENCHMARKS.md](../../../BENCHMARKS.md)).

### Compile, binary

| | Kāra | Rust | C |
|---|---|---|---|
| compile elapsed | 146.6 ms | 100.1 ms | 45.7 ms |
| compile peak RSS | 63.1 MiB | 29.9 MiB | 2.6 MiB |
| binary (seq) | 312.1 KiB | 455.7 KiB | 32.8 KiB |
| runtime peak RSS | 1.1 MiB | 1.1 MiB | 1.1 MiB |

Kāra's cold compile takes 1.46× `rustc -O`'s time. The 319,568 B seq binary is well
above the 52–69 KB most seq binaries in this re-bench reach
([`B-2026-11-04-31`](#bug-ledger)); the default auto-par binary is 402,848 B. Runtime
memory is level with Rust and C (Go 9.3 MiB): the 86.9 MiB that the B-2026-06-12-5 leak
once caused does not appear in this run.

### Par lane — auto-par vs hand-tuned parallelism (multi-core)

The decode is sequential within one pass, but the outer reduction over `ITERS`
independent decodes is embarrassingly parallel. All four implementations
parallelize that *same* reduction across the machine's cores — the difference is
what the programmer had to write:

Snapshot — M5 Pro, **2026-11-04**, karac `0.8.0-dev.14370+gd33cb285d` (gd33cb285d, the v2/MIR backend).

| | parallel code written | time | CPU | total CPU |
|---|---|---|---|---|
| C + pthreads *(metal floor)* | raw `pthread_create`/`join` + chunk + merge | **69.3 ± 8.2 ms** | 1560 % | 1082 ms |
| Go goroutines | manual chunking + `sync.WaitGroup` + partial-merge | 70.6 ± 3.5 ms | 573 % | 405 ms |
| Rust + rayon | `rayon` crate dependency + `.into_par_iter()` rewrite | 74.5 ± 12.4 ms | 1686 % | 1255 ms |
| **Kāra (auto-par)** | **none** — the compiler recognized the `sum += pass_len` reduction | **94.9 ± 10.4 ms** | 1431 % | 1357 ms |

**Kāra's auto-par is last in this lane: 1.27× rayon, 1.37× the raw-pthreads floor and
1.34× Go, with no parallel source at all.** The 2026-08-05 feed read 0.86× rayon and
1.02× C. The default `karac build` still parallelizes the plain sequential loop (one
`karac_mir_task_spawn` call in the emitted IR, none under `KARAC_AUTO_PAR=0`); the
Rust, Go, and C programmers each had to opt in and restructure (the C version is the
most boilerplate of all). Against its own seq lane that is a **3.56× self-speedup**
(338.2 → 94.9 ms) for free.

**Go is far ahead on efficiency.** Goroutines land at 70.6 ms, 1.34× ahead of Kāra,
while burning **405 ms of total CPU to Kāra's 1357 ms, a 3.4× gap**. Go extracts a
better wall-time from ~573 % CPU than Kāra does from ~1431 %. So on this kernel Kāra's
reduction split is *scaling wide rather than scaling well*: it recruits every core and
still finishes behind a scheduler using a third of them. That is the honest read and
the open efficiency question for auto-par on fine-grained, allocation-heavy,
bandwidth-bound work.

The C row is the floor here, raw OS threads with no runtime/work-stealing/GC, though
level with Go inside the error bars. (Multi-core within the par lane; per
[`BENCH.md`]'s two-lane discipline, *not* comparable to the single-thread seq
rows above. Kāra's wall time has higher run-to-run variance — worker-pool init
on a sub-100 ms run.)

**Buyer reframe.** The parallel speedup that costs a Rust team a crate, an API
rewrite, and a new class of data-race bugs to chase — and a Go team a hand-rolled
chunk/merge — Kāra delivers from the same single-threaded source. Colorless
parallelism: fewer lines, no `unsafe`/`Send`/`Sync` reasoning, no goroutine-leak
or partial-merge bugs. On this kata it currently costs throughput: **1.27× behind
rayon** and 1.34× behind goroutines, with goroutines also 3.4× cheaper in CPU. The
honest pitch here is less engineering at a measured wall-time price, not a win
against either hand-written version.

[`BENCH.md`]: ../../../BENCH.md

## Kāra features exercised

- **Zero-copy slice `s[i..j]` + `push_str`** — maximal letter-run append, no
  per-char `push`, no allocation (the lexer's token-text fast path).
- **`bytes()` byte classification** — `b'0'`/`b'9'`/`b'['`/`b']'` byte
  literals; `(b - b'0') as i64` digit-value widening cast.
- **Parallel `Vec[String]` / `Vec[i64]` stacks** — `push` / `pop().unwrap()`
  for the nesting levels (iterative style).
- **Multi-value return + destructure** — `decode_at` returns `(String, i64)`,
  `let (inner, after) = …` (recursive style).
- **`String.repeat(n)`** — the repeat primitive this kata motivated (iterative
  style's `cur.repeat(count)`); the recursive style falls back to a `push_str`
  loop because its source is tuple-bound.

---

**Bug ledger:** this kata surfaced `B-2026-06-12-3`, `B-2026-06-12-4`, `B-2026-06-12-5`, `B-2026-06-12-14` — see the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).

## Bug ledger

**Surfaced [`B-2026-11-04-30`](../../../../kara/docs/bugs-v2.md)** (perf, medium, open). On gd33cb285d (measured 2026-11-04) the seq lane moved 0.99× → 1.17× `rustc -O` and 0.99× → 1.40× C, and reads 1.20× equal-safety Rust; the par lane moved 0.86× → 1.27× rayon and 1.02× → 1.37× C-par, with auto-par still firing. Against legacy dd86e3955 the seq build runs 1.27× the instructions and 1.26× the cycles.

**Surfaced [`B-2026-11-04-31`](../../../../kara/docs/bugs-v2.md)** (perf, low, open). The seq binary is 319,568 B on gd33cb285d (measured 2026-11-04), where most seq binaries in this re-bench are 52–69 KB. The root keeping the larger runtime path alive here is not yet found.
