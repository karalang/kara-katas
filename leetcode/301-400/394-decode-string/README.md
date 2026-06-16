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

| | Go | C | Rust | **Kāra (seq)** |
|---|---|---|---|---|
| time | 166.5 ms | 198.0 ms | 239.6 ms | **240.2 ms** |
| vs Kāra | 1.44× faster | 1.21× faster | 1.00× (parity) | — |

Kāra is **at parity with Rust** and 1.21× behind C on identical code — a healthy
per-core codegen-quality result on an allocation-heavy string workload. (Go's
`strings.Repeat` + GC string handling is unusually fast here, 1.44×.)

### Compile, binary

| | Kāra | Rust | C |
|---|---|---|---|
| compile elapsed | **86 ms** | 113 ms | 49 ms |
| compile peak RSS | 14.0 MiB | 30.0 MiB | 2.5 MiB |
| binary (seq) | 295 KiB | 456 KiB | 33 KiB |

Kāra's cold compile (86 ms) edges `rustc -O` (113 ms). **Runtime memory is omitted
as a comparison** — Kāra's 86.9 MiB is the B-2026-06-12-5 leak, not representative;
Rust/C sit at ~1.2 MiB.

### Par lane — auto-par vs hand-tuned parallelism (multi-core)

The decode is sequential within one pass, but the outer reduction over `ITERS`
independent decodes is embarrassingly parallel. All three implementations
parallelize that *same* reduction across the machine's cores — the difference is
what the programmer had to write:

| | parallel code written | time | total CPU |
|---|---|---|---|
| Go goroutines | manual chunking + `sync.WaitGroup` + partial-merge | 68.4 ms | 288 ms |
| **Kāra (auto-par)** | **none** — the compiler recognized the `sum += pass_len` reduction | **23.5 ms** | 322 ms |
| C + pthreads *(metal floor)* | raw `pthread_create`/`join` + chunk + merge | 26.5 ms | 345 ms |
| Rust + rayon | `rayon` crate dependency + `.into_par_iter()` rewrite | 22.0 ms | 347 ms |

**Kāra's auto-par beats the raw-pthreads "metal floor" *and* hand-written
goroutines, and lands within 1.07× of hand-tuned rayon — with no parallel source
at all.** The default `karac build` emits a `karac_par_reduce` dispatch off the
plain sequential loop; the Rust, Go, and C programmers each had to opt in and
restructure (the C version is the most boilerplate of all).

The C row was *meant* to be the floor — raw OS threads with no
runtime/work-stealing/GC — but on this fine-grained, allocation-heavy,
memory-bandwidth-bound workload it isn't: per-process `pthread` spawn plus
bandwidth contention mean the **pooled lightweight schedulers (Go's goroutines,
Kāra's `karac_par_reduce` runtime) win over hand-rolled threads.** An honest
finding, not spin — raw threads aren't automatically fastest for this shape, and
Kāra's runtime is well-tuned for it. (Multi-core within the par lane; per
[`BENCH.md`]'s two-lane discipline, *not* comparable to the single-thread seq
rows above. Kāra's wall time has higher run-to-run variance — worker-pool init
on a sub-100 ms run — but the mean sits below C and Go.)

**Buyer reframe.** The parallel speedup that costs a Rust team a crate, an API
rewrite, and a new class of data-race bugs to chase — and a Go team a hand-rolled
chunk/merge — Kāra delivers from the same single-threaded source. Colorless
parallelism: fewer lines, no `unsafe`/`Send`/`Sync` reasoning, no goroutine-leak
or partial-merge bugs, *and* it runs within 1.07× of rayon here. Less engineering and fewer
concurrency incidents for equal-or-better throughput.

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
