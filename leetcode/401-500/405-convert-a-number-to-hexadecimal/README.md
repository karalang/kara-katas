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
| time | 17 ms | 51 ms | 212 ms | 218 ms | **596 ms** | 2094 ms |

**Honest read: Kāra trails here — ~2.7× Rust, ~34× the C floor — and it is *not*
the overflow-safety tax.** Unlike the compute-bound parse in
[#171](../../101-200/171-excel-sheet-column-number/), turning on Rust's overflow
checks barely moves it (212 → 218 ms): this workload is **allocation-bound**. The
kata's `to_hex` allocates a `Vec[i64]` nibble buffer **and** a `String` per
render — ~8M small heap allocations over 4M renders — and Kāra's small-object
allocation throughput currently trails Rust's allocator + `Vec`/`String` by that
factor. The render *logic* (mask/shift, digit-table slice) is cheap; the cost is
allocation churn. **This is a real optimization target** — surfaced exactly
because the kata stresses the allocator the way a token-text-building lexer does.

### Compile, binary

| | Kāra | Rust | C |
|---|---|---|---|
| compile elapsed | **78 ms** | 107 ms | 52 ms |
| binary (seq) | **279 KiB** | 456 KiB | 33 KiB |

Kāra's cold compile (78 ms) still beats `rustc -O` (107 ms), and emits a
**279 KiB** binary — 1.6× smaller than Rust, 9× smaller than Go (2.4 MiB).
Runtime peak RSS (67.6 MiB) is dominated by the ~30 MB concatenated output buffer
plus allocation churn — about 2× Rust's 33.5 MiB, tracking the same small-alloc
overhead.

**Where this lands.** Unlike #722/#125 (where Kāra's seq codegen beats or ties
Rust) and #171 (parity at equal safety), #405 is the workload that finds a
genuine gap: per-render small-object allocation. It is reported here straight, as
an optimization target rather than a headline — the kata earned its place by
surfacing the gap, not by winning the lane.

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
