# 393. UTF-8 Validation

Given a buffer of bytes, decide whether it is a valid UTF-8 encoding — i.e.
whether it splits cleanly into a sequence of well-formed 1–4 byte UTF-8
characters.

A UTF-8 character is discriminated entirely by its **leading byte's high
bits**, then followed by the right number of `10xxxxxx` continuation bytes:

| Leading byte | Length | Followed by            |
|--------------|--------|------------------------|
| `0xxxxxxx`   | 1      | —                      |
| `110xxxxx`   | 2      | one `10xxxxxx`         |
| `1110xxxx`   | 3      | two `10xxxxxx`         |
| `11110xxx`   | 4      | three `10xxxxxx`       |

Anything else as a leading byte (a bare `10xxxxxx` continuation, or
`11111xxx`) is invalid, and a declared character whose continuation bytes
are missing or malformed makes the whole buffer invalid.

(LeetCode states the input as an integer array where only the low 8 bits of
each entry are data; here the buffer is a `Vec[u8]` directly.)

## Approach

One forward pass with an index `i`. At each step, classify `data[i]` with
`lead_len` (a few bit-mask comparisons) to learn the character width `need`;
bail if it isn't a valid leading byte or if `need` bytes don't fit in the
remaining buffer; then verify the next `need - 1` bytes are all
`10xxxxxx` continuations and advance `i` by `need`. O(n) time, O(1) extra
space.

## Kāra features exercised

This is a deliberately **byte-level** kata — it dogfoods the `u8` surface
end to end:

- **hex `u8` literals** — `0x80u8`, `0xE0u8`, `0xC0u8`, `0xF0u8`, `0xF8u8`.
- **bitwise `&` masking** on `u8` — the leading-byte and continuation-byte
  classifiers.
- **`Vec[u8]` building + indexing** — `data[i]`, `data[i + k]`, `.len()`.
- **`for b in s.bytes()`** — the byte iterator, used by the property check
  below. (This kata is what surfaced — and now guards against — a codegen
  bug where `for b in s.bytes()` iterated zero times in compiled mode.)
- **named-array range slicing** — `let a = [...]; validate_lit("…", a[0..n])`
  (codegen range-slicing requires a named source variable).

### Property check via `s.bytes()`

Every well-formed Kāra `String` is valid UTF-8 by construction, so feeding
`s.bytes()` through the validator must always return `true`. The
`report_str` cases (`"héllo"`, `"café ☕"`, `"日本語"`) are a cross-check
that the hand-written validator and the runtime's UTF-8 invariant agree —
and that the byte iterator yields the right bytes in both the interpreter
and compiled binary.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`506796`). Workload: validate 40k x 32-byte records (mostly-valid whole-char fills + ~8% corruption) x 60 passes; data-dependent lead-byte dispatch.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 222.8 ms | 0.90× |
| Rust `-O` | 241.5 ms | 0.98× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 243.9 ms | 0.99× |
| **Kāra (codegen)** | 247.6 ms | 1.00× |
| Go | 249.3 ms | 1.01× |
| Python (scale lane) | 6.65 s | 26.85× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
# Kāra (compiled or interpreted — both produce identical output)
karac run validate_utf8.kara
karac build validate_utf8.kara && ./validate_utf8

# Python reference (output matches line-for-line; diffable)
python3 validate_utf8.py
```

All three agree line-for-line. No benchmark harness ships with this kata —
it is a correctness / dogfooding kata for the byte surface, not a
performance comparison.
