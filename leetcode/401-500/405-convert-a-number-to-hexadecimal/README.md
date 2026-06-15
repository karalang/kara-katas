# 405. Convert a Number to Hexadecimal

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math, Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/convert-a-number-to-hexadecimal](https://leetcode.com/problems/convert-a-number-to-hexadecimal/)

Given a 32-bit integer `num`, return its hexadecimal representation as a
lowercase string. Negative numbers use the 32-bit **two's-complement** bit
pattern; no leading zeros except `"0"` itself. You may **not** use a library hex
conversion — pure nibble extraction.

```
26   →  "1a"
-1   →  "ffffffff"
0    →  "0"
```

**Constraints:** `-2³¹ ≤ num ≤ 2³¹ − 1`.

## Why this kata — the radix-16 *render* (inverse nibble map)

This is the **render** direction of the self-hosted lexer's number arm — the
exact inverse of `from_str_radix`. Where [#415 add-strings](../415-add-strings/)
established the digit-table slice at base 10, base 16 reuses it verbatim with a
16-symbol table and reaches each nibble by bit masking. Its slice-partner
[#171 excel-column](../../101-200/171-excel-sheet-column-number/) covers the
**parse** direction (char → value); together they are the lexer's radix arm in
both directions.

| Lexer surface | This kata |
|---|---|
| **value → digit glyph** (the inverse nibble map; §3 slice render) | `HEX[d..d+1]` one-byte zero-copy slice, `push_str` |
| **base-N decomposition** | `n & 0xf` / `n >> 4` (bitwise) or `n % 16` / `n / 16` (arithmetic) |
| **two's-complement read** | `num & 0xffffffff` folds a negative i64 to its unsigned 32-bit value for free |
| **no-library constraint** | digits emitted one nibble at a time, no `format`/`to_hex` |

## Approaches

Three styles, all byte-identical to the Python oracle across all 12 cases, under
`karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Bitwise mask-and-shift** ★ | [`to_hex.kara`](to_hex.kara) | `n & 0xf` nibble + `n >> 4`, buffer LSB-first, reverse and render through the hex table |
| Arithmetic mod/div | [`to_hex_divmod.kara`](to_hex_divmod.kara) | same render, nibble by `% 16` / `/ 16` — the literal base-16 sibling of #67/#415 carry arithmetic |
| Recursive descent | [`to_hex_recursive.kara`](to_hex_recursive.kara) | `hex_of(n)` recurses on `n >> 4` first, appends `HEX[n & 0xf]` on the way out — MSB-first, no reversal |
| Reference oracle | [`to_hex.py`](to_hex.py) | known-correct LeetCode answer |

The bitwise and arithmetic styles make one point together: the digit-table
render is one surface regardless of how the nibble is reached — `& 0xf`/`>> 4`
and `% 16`/`/ 16` produce the same stream over a non-negative value. Masking
`num & 0xffffffff` into a positive `i64` makes the two's-complement pattern of a
negative input fall out automatically (`-1 → 4294967295 → "ffffffff"`), after
which the value shifts right cleanly.

## What this kata uncovered

**Flat curve — no `karac` bug.** The whole radix-16 surface compiled and ran
first-try under both backends: i64 hex literals (`0xffffffffi64` / `0xfi64`),
the `&` / `>>` bitwise ops, the `% 16` / `/ 16` arithmetic, the `HEX[d..d+1]`
digit-table slice render via `push_str`, recursion with a scalar frame, and the
two's-complement extremes (INT_MIN `→ "80000000"`, `-26 → "ffffffe6"`). It sits
on the same zero-copy-slice + `push_str` path #722/#415 already hardened.

The auto-par output-ordering miscompile
([`B-2026-06-13-18`](../../../../kara/docs/bug-ledger.md)) that this slice's
partner [#171](../../101-200/171-excel-sheet-column-number/) flushed *also*
applies here in principle — `main` calls `report(...)` (which prints) several
times — but #405 was protected by the cost-model's `all_pure → trivial` gate
(`report` has no resource effect, so the group was marked trivial and never
emitted). #171's printing helper carries a real effect, which defeats that gate
and exposed the bug. The fix serializes all output here too.

## Benchmarks

Workload: render **4M distinct values** to hex, concatenated into one growing
buffer, then byte-checksummed (sink `2 231 199 964`). Persisting the output
defeats allocation-elision — a per-render byte-sum lets `rustc`/`clang`/`go`
elide the heap `String` and fold the work to arithmetic, but a buffer that is
built up and then observed cannot be elided. This is a **sequential
string-building** workload (the lexer's real shape) — the build carries a
loop-borne dependency on the buffer, so it does not auto-parallelize (seq-only by
construction). Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded string build)

| | C | Go | Rust (`-O`) | Rust (`overflow-checks=on`) | **Kāra** | Python |
|---|---|---|---|---|---|---|
| time | 17 ms | 50 ms | 208 ms | 214 ms | **271 ms** | 2058 ms |
| vs Kāra | 15.9× faster | 5.4× faster | 1.31× faster | 1.27× faster | — | 7.6× slower |

**This kata did its job twice over: it found two real codegen gaps and drove
both fixes.** The first run trailed Rust **2.7×** (596 ms) — allocation-bound, as
expected for a render-into-a-String loop. Profiling pinned the first cause:
`_xzm_free` topped the profile, and every `out.push_str(HEX[d..d+1])` called
`karac_string_slice`, which **allocated and freed a temp heap `String` for the
slice on every push** (~28M wasted allocations) — the digit-table slice this
README (and #415/#722) called "zero-copy" *wasn't*. Fix #1 (`karac 08ae0140`)
routed a string-slice `push_str` arg through the non-allocating borrow view
(`{ptr, len, cap: 0}`): **596 → 286 ms (2.08×)**.

A re-profile of the 286 ms binary then pinned the *second* gap:
`karac_realloc_or_panic` dominated, and a malloc-call census showed Kāra doing
**3× the reallocs of Rust** (12M vs 4M for the same algorithm). Cause: each
`to_hex` builds an 8-byte `String`, and Kāra floored every buffer's first
allocation at capacity 4 — so an 8-byte string grew `0→4→8`, one realloc too
many. Rust's `RawVec` floors 1-byte-element buffers at **8** (4 for wider), so
its 8-byte string lands in one allocation. Fix #2 (`karac 27adc6f9`) matches
Rust — String min-cap floor 4 → 8: reallocs **12M → 8M** (now at parity with
Rust's total alloc-ops), instructions **−16%**, **286 → 271 ms**, at **zero
memory cost** (macOS malloc's 16-byte quantum makes a 4- and 8-byte request the
same chunk).

Where Kāra now lands: **1.31× `rustc -O`** (1.27× at equal overflow safety) and
**16× the C floor**. The residual is the *other* per-render allocation — the
`String` that `to_hex` returns (Rust allocates it too) plus Rust's
decade-hardened `String`/allocator codegen — plus C being the bare-metal floor
that renders into a stack buffer and **never allocates per render at all** (so
the 16× is "Kāra builds a String; C doesn't," not the same task). The last
small-object lever is escape-analysis stack allocation of the non-escaping
nibble buffer — tracked, lower-yield now that the realloc count matches Rust.

### Compile, binary

| | Kāra | Rust | C |
|---|---|---|---|
| compile elapsed | **78 ms** | 106 ms | 52 ms |
| binary (seq) | **295 KiB** | 456 KiB | 33 KiB |

Kāra's cold compile (78 ms) beats `rustc -O` (106 ms), and emits a **295 KiB**
binary — 1.5× smaller than Rust, 8× smaller than Go (2.4 MiB). Runtime peak RSS
(**31.4 MiB**, *below* Rust's 33.5 MiB) is dominated by the ~30 MB concatenated
output buffer — the per-render churn no longer inflates it now that the realloc
count matches Rust.

**Where this lands.** This is the kata's whole value: it stressed the allocator
exactly the way a token-text-building lexer does, surfaced a genuine codegen
inefficiency (the `push_str(s[a..b])` temp-allocation — also the self-hosted
lexer's hot path), and **two** fixes that closed most of the gap (2.7× → 1.31×
Rust: the slice-borrow view, then the String min-cap-8 floor) ship from that
finding. The katas exist to find Kāra's gaps and fix them on the spot — not just
to win lanes.

## Kāra features exercised

- **i64 hex literals + bitwise ops** — `0xffffffffi64`, `0xfi64`, `n & 0xf`,
  `n >> 4`; the two's-complement mask read.
- **Radix-16 render** — `HEX[d..d+1]` one-byte zero-copy slice + `push_str`, the
  inverse nibble map of digit parsing (all three styles).
- **`Vec[i64]` accumulate + reverse** — buffer nibbles LSB-first, walk back to
  front (mask-shift + mod/div styles).
- **Recursion with a scalar frame** — `hex_of(n >> 4)` before the low nibble.

---

**Bug ledger:** the radix-render surface was a flat curve (no miscompile). The
auto-par output-ordering bug **`B-2026-06-13-18`** (surfaced by the slice partner
[#171](../../101-200/171-excel-sheet-column-number/)) covers this kata's
`report(...)` print sequence too — fixed (`48145ad4`). See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
