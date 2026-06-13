# 722. Remove Comments

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-comments](https://leetcode.com/problems/remove-comments/)

Given a C++ source as a list of lines, strip `//` line comments and
`/* ... */` block comments and return the surviving lines (dropping any
line that becomes empty).

```
["/*Test program */", "int main()", "{ ",
 "  // variable declaration ", "int a, b, c;",
 "/* This is a test", "   multiline  ", "   comment for ",
 "   testing */", "a = b + c;", "}"]
  →  ["int main()", "{ ", "  ", "int a, b, c;", "a = b + c;", "}"]

["a/*comment", "line", "more_comment*/b"]  →  ["ab"]
```

A block comment can span lines, fusing code before its `/*` with code
after the matching `*/` into one output line; the implicit newline between
list entries is consumed inside the block. The first effective marker
wins: inside a block, a `//` is inert; inside a line comment, a `/*` is
inert. LeetCode guarantees the source has no quote characters, so there is
no string-literal state to track.

**Constraints:** `1 ≤ source.length ≤ 100`; `0 ≤ source[i].length ≤ 80`;
every opened block comment is eventually closed; no quote characters.

## Why this kata — the lexer's comment slice

This is the corpus's highest-fidelity stand-in for the self-hosted lexer's
**comment slice** (the `//` line and `/* */` block arms). It exercises the
same machinery the lexer's compiled binary stands on:

| Lexer surface | This kata |
|---|---|
| maximal-munch two-char lookahead (`/`+`/`, `/`+`*`, `*`+`/`) | the marker dispatch |
| in-comment **mode flag** carried across input | `in_block`, the only cross-line state |
| `String.push(char)` accumulation into a token/line buffer | the output buffer |
| **multi-line span advance** (L3 — newline / line boundary) | block comments that cross list entries; markers that may *not* span the implicit newline |

## Approaches

Three styles, each a different cut of the lexer's scan surface. All produce
byte-identical output to the Python oracle across all 16 cases, under `karac
run` **and** `karac build`.

| Approach | File | Shape | Lexer surface |
|---|---|---|---|
| **Byte-indexed segment-slicing** ★ | [`remove_comments_bytes.kara`](remove_comments_bytes.kara) | `bytes()` scan + zero-copy `s[a..b]` slice append of each surviving run | §1 byte scan + §3 `token_text` slicing |
| Index-heavy | [`remove_comments.kara`](remove_comments.kara) | `Vec[char]` snapshot per line + `cs[i+1]` lookahead | array-cursor form |
| Streaming | [`remove_comments_stream.kara`](remove_comments_stream.kara) | `for c in line.chars()`, carry the half-seen marker in a flag | forward-cursor form |
| Reference oracle | [`remove_comments.py`](remove_comments.py) | known-correct LeetCode answer | — |

The **byte-indexed** style (★) is the most lexer-faithful *and* the fastest:
it scans the line's zero-copy `bytes()` view with `b'/'`/`b'*'` byte
classification and appends each surviving run as one **zero-copy slice**
`source[li][a..b]` (Kāra's `&line[a..b]` analog) — O(segments) `push_str`
calls instead of O(chars) `push`, with no per-segment allocation. It is the
variant the [benchmarks](#benchmarks) below measure; it **beats Rust** on the
seq lane. The **index-heavy** form's per-line `Vec[char]` snapshot is pure
overhead the other two avoid — it benches **3.2× slower** than byte-indexed
(407 ms vs 127 ms), a teaching point on why the lexer indexes `bytes()`
directly. The
**streaming** form flushed no new defect once the bugs below were fixed — the
flat-curve signal.

## What this kata uncovered

Three karac bugs, fixed on the spot per the **no workarounds — fix the
compiler** discipline. The first surfaced writing the kata; the second and
third surfaced building and benching it.

**1 — `push_str(ref String)` rejected by `karac build`** ([`522bec1c`]).
Appending a **borrowed** String into a buffer (`buffer.push_str(name)`,
`name: ref String`) was rejected with `'push_str' expects a String argument,
found 'ref String'`, while `karac run` only *warned* (the interpreter's known
typecheck-bypass; `build` is the real gate). The same gate sat on `contains`
and `starts_with` — the lexer's keyword-membership and prefix ops. All three
read their argument's bytes; there is no ownership reason to demand a move.
Fix: an `is_str_like` helper (`src/typechecker/stdlib_seq.rs`) accepting
`String` or a `ref`/`mut ref` borrow. Test:
`test_string_methods_accept_borrowed_str_arg`.

**2 — chained `.bytes().len()` failed in codegen** ([`240389ff`]).
`out[k].bytes().len()` — the bench harness's char-count reduction — hit
`codegen: no handler for method 'len' on non-identifier receiver`, though the
interpreter handled it. The non-identifier `len`/`is_empty` handler only
matched the 3-field `{ptr,len,cap}` Vec struct; `bytes()` returns the 2-field
`{ptr, i64}` slice header. Fix: a slice-header branch extracting `len` from
field 1. Test: `test_e2e_chained_slice_len_on_nonident_receiver`.

**3 — `push_str(substring(…))` leaked the substring temp** ([`5ebdc96c`]).
The first byte-indexed draft appended via `buffer.push_str(source.substring(a,
b))` — *the lexer's token-text extraction* — which passes a freshly-malloc'd
String to `push_str`; `push_str` copied its bytes but never freed the temp. It
leaked ~48 bytes/call, **unbounded**: runtime peak RSS hit **52.7 MiB** where
Rust used 1.3 MiB. Fix: free the source buffer immediately after the copy,
gated on `expr_yields_fresh_owned_temp` (excludes literals / `ref String`
identifiers / `out[k]` place exprs) and `cap > 0` (a literal owns no heap),
dropping RSS to 1.2 MiB. Test:
`asan_push_str_substring_temp_no_double_free` (guards the new `free()` against
double-free / UAF). A follow-up ([`5bc5c2ec`]) factored the free into a shared
`free_fresh_owned_str_arg` helper and applied it to `contains` and
`starts_with` too — the same leak on the lexer's keyword-membership /
prefix-check surface (`keyword.contains(source.substring(a, b))`), closing the
whole borrowed-string-arg class fix #1 opened. *(The benched form then moved to
zero-copy slice append `s[a..b]`, which allocates no temp at all — see
§ Benchmarks — so the leak is moot there; the fix remains load-bearing for any
code that extracts an **owned** run, the lexer's stored-token path.)*

[`522bec1c`]: ../../../../kara/
[`240389ff`]: ../../../../kara/
[`5ebdc96c`]: ../../../../kara/
[`5bc5c2ec`]: ../../../../kara/

## Benchmarks

Workload: `REPS=60`-fold synthetic C++ source (600 lines), the stripper run
`ITERS=4000` times reducing to a surviving-char-count sink (30 960 000). Same
**byte-indexed segment-slicing** algorithm across all five implementations.
Apple M5 Pro; `bench/bench.sh` (`hyperfine`); see [`BENCH.md`](../../../BENCH.md)
for protocol. **Seq lane** = single-threaded, the per-core codegen-quality
comparison (the Kāra binary built `KARAC_AUTO_PAR=0`).

### Seq lane — runtime (single-threaded, apples-to-apples)

| | Go | C | **Kāra (seq)** | Rust |
|---|---|---|---|---|
| time | 70.6 ms | 77.9 ms | **81.4 ms** | 89.0 ms |
| vs Kāra | 1.15× faster | 1.05× faster | — | 1.09× slower |

Kāra **beats Rust** on identical code (~1.10×) and trails C by only 1.05×, on
a string-heavy workload. Getting here was the kata's most instructive perf
lesson:

| Kāra form | seq time | vs Rust |
|---|---|---|
| `Vec[char]` snapshot + per-char `push` (index-heavy) | 407 ms | 4.4× slower |
| `bytes()` scan + `substring(a,b)` append (allocating) | 134 ms | 1.45× slower |
| **`bytes()` scan + `s[a..b]` slice append (zero-copy)** ★ | **81 ms** | **1.10× faster** |

The whole gap to Rust was the **`substring()` allocation**: it returns an
*owned* `String` (malloc + copy + free per segment), so `push_str(substring())`
copies the run twice and heap-churns once per segment — measured at **+1.6B
instructions vs the slice form** (3.47B → 2.17B, −37%). Switching the append to
the zero-copy slice `source[li][a..b]` — Kāra's `&line[a..b]` — copies the run
*once*, no allocation, and the codegen-quality gap to Rust **vanishes** (Kāra
edges ahead). Reserve `.substring()` for when the run must outlive the source
(a stored token); for append, slice.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.2 MiB** | 1.3 MiB | 1.1 MiB | 8.4 MiB |
| binary size (seq) | 33 KiB | 456 KiB | 33 KiB | 2434 KiB |
| compile elapsed | 88 ms | 101 ms | 46 ms | — |
| compile peak RSS | 14.9 MiB | 31.6 MiB | 2.5 MiB | — |

Kāra's runtime memory is the **lowest tier** (1.2 MiB, between C's 1.1 and
Rust's 1.3) — the zero-copy slice form allocates nothing per segment, and the
earlier substring path's leak (fix #3) is moot here. The seq binary is 33 KiB
(14× smaller than Rust's 456 KiB, tied with C), and the cold compile (88 ms)
edges `rustc -O` (101 ms).

### Par lane — auto-par vs hand-tuned parallelism (multi-core)

The kata is **seq-only at the algorithm level** (the `in_block` flag carries
across lines → no per-line parallel lane), but the bench's outer reduction over
`ITERS` independent passes is embarrassingly parallel. All three parallelize that
same reduction; the difference is what the programmer had to write:

| | parallel code written | time |
|---|---|---|
| **Kāra (auto-par)** | **none** — the compiler emitted `karac_par_reduce` off the plain loop | **17.3 ms** |
| Rust + rayon | `rayon` crate + `.into_par_iter()` | 16.9 ms |
| Go goroutines | manual chunk + `sync.WaitGroup` + merge | 24.9 ms |

**Kāra's auto-par is dead-even with hand-tuned rayon** (16.9 vs 17.3 ms, within
the ±2 ms run-to-run noise) and **1.4× faster than hand-written goroutines** —
with no parallel source, a ~4.7× speedup over its own seq binary. Per
[`BENCH.md`]'s two-lane discipline this is multi-core, *not* comparable to the
single-thread seq rows above.

**Buyer reframe.** Colorless parallelism: the speedup that costs a Rust team a
crate + an API rewrite + data-race reasoning, and a Go team hand-rolled
chunk/merge, Kāra delivers from the same single-threaded source — matching rayon
and beating goroutines. Fewer lines, fewer concurrency incidents, equal throughput.

[`BENCH.md`]: ../../../BENCH.md

## Kāra features exercised

- **Zero-copy slice `s[a..b]` + `push_str`** — the byte-indexed style's
  surviving-run append; a borrowed view, no allocation (the lexer's fast path,
  the reason this kata beats Rust). `.substring(a, b)` is the *owned* sibling —
  the lexer's `token_text` surface (§3) when a run must outlive the source;
  closing its temp leak (fix #3) made it allocation-clean too.
- **`bytes()` byte classification** — `b'/'` / `b'*'` byte literals, zero-copy
  `Slice[u8]` indexing with `cs[i+1]` lookahead (§1 byte scan).
- **`String.push(char)` / `push_str`** — char-by-char (index-heavy/streaming)
  and slice-at-a-time (byte-indexed) accumulation; `push_str(ref String)` is
  the gap fix #1 closed.
- **`Vec[String]` literal + index** — `["a", "b"]` array literal coerced to
  `Vec[String]`, `source[li]` indexed.
- **Cross-line state machine** — `in_block` is the single piece of state that
  legitimately survives a line boundary; the streaming variant additionally
  carries per-line pending-marker flags that must reset at the newline.
