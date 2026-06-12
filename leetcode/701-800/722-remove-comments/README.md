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
| **Byte-indexed segment-slicing** ★ | [`remove_comments_bytes.kara`](remove_comments_bytes.kara) | `bytes()` scan + `substring` slice of each surviving run | §1 byte scan + §3 `token_text` slicing |
| Index-heavy | [`remove_comments.kara`](remove_comments.kara) | `Vec[char]` snapshot per line + `cs[i+1]` lookahead | array-cursor form |
| Streaming | [`remove_comments_stream.kara`](remove_comments_stream.kara) | `for c in line.chars()`, carry the half-seen marker in a flag | forward-cursor form |
| Reference oracle | [`remove_comments.py`](remove_comments.py) | known-correct LeetCode answer | — |

The **byte-indexed** style (★) is the most lexer-faithful *and* the fastest:
it scans the line's zero-copy `bytes()` view with `b'/'`/`b'*'` byte
classification and emits each surviving run as one `substring` slice —
exactly the lexer's `token_text = source.substring(start, current)` shape,
O(segments) `push_str` calls instead of O(chars) `push`. It is the variant
the [benchmarks](#benchmarks) below measure. The **index-heavy** form's
per-line `Vec[char]` snapshot is pure overhead the other two avoid — it
benches **3.2× slower** than byte-indexed (407 ms vs 127 ms on the bench
workload), a teaching point on why the lexer indexes `bytes()` directly. The
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
The byte-indexed style's core shape `buffer.push_str(source.substring(a, b))`
— *the lexer's token-text extraction* — passes a freshly-malloc'd String to
`push_str`, which copied its bytes but never freed the temp. It leaked ~48
bytes/call, **unbounded**: the bench's runtime peak RSS was **52.7 MiB** where
Rust used 1.3 MiB. Fix: free the source buffer immediately after the copy,
gated on `expr_yields_fresh_owned_temp` (excludes literals / `ref String`
identifiers / `out[k]` place exprs) and `cap > 0` (a literal owns no heap).
Post-fix RSS is **1.2 MiB** — lower than Rust, tied with C. Test:
`asan_push_str_substring_temp_no_double_free` (guards the new `free()` against
double-free / UAF). A follow-up ([`5bc5c2ec`]) factored the free into a shared
`free_fresh_owned_str_arg` helper and applied it to `contains` and
`starts_with` too — the same leak on the lexer's keyword-membership /
prefix-check surface (`keyword.contains(source.substring(a, b))`), closing the
whole borrowed-string-arg class fix #1 opened.

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

| | Kāra (seq) | Rust | C | Go |
|---|---|---|---|---|
| time | 134.6 ms | 92.6 ms | 82.5 ms | 73.5 ms |
| vs Kāra | — | 1.45× | 1.63× | 1.83× |

Kāra is **1.45× behind Rust** on identical code — in line with the corpus norm
(simplify-path is 1.85×), and a 2.9×→1.45× improvement over the index-heavy
snapshot form this kata started from.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.2 MiB** | 1.3 MiB | 1.2 MiB | 8.4 MiB |
| binary size (seq) | 33 KiB | 456 KiB | 33 KiB | 2434 KiB |
| compile elapsed | 100 ms | 108 ms | 51 ms | — |
| compile peak RSS | 14.7 MiB | 31.5 MiB | 2.5 MiB | — |

Kāra's runtime memory is the **lowest of all** (tied with C, below Rust) —
after fix #3; pre-fix it was 52.7 MiB. The seq binary is 33 KiB (14× smaller
than Rust's 456 KiB, tied with C), and the cold compile (100 ms) edges
`rustc -O` (108 ms).

### Auto-par regime (Kāra default, multi-core — reported separately)

The kata is **seq-only at the algorithm level** (the `in_block` flag carries
across lines → cross-line data dependency, no per-line parallel lane). But the
bench's outer reduction over `ITERS` independent passes is recognized by
karac's auto-par-on-reduction pass, which emits a `karac_par_reduce` dispatch:
**27.3 ms** wall (User-CPU 291 ms confirms multi-core), a ~5× speedup over the
seq binary, at a +263 KiB binary footprint. Per [`BENCH.md`]'s two-lane
discipline this is **not** comparable to the single-thread rows above — it is
the production-default Kāra behavior, reported so it stays visible.

[`BENCH.md`]: ../../../BENCH.md

## Kāra features exercised

- **`String.substring(start, end)` byte-slicing** — the byte-indexed style's
  surviving-run extraction; the lexer's `token_text` surface (§3). Closing
  the temp leak (fix #3) made it allocation-clean.
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
