# 151. Reverse Words in a String

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String · Two Pointers · Parsing &nbsp;·&nbsp; **Source:** [leetcode.com/problems/reverse-words-in-a-string](https://leetcode.com/problems/reverse-words-in-a-string/)

Reverse the **order of the words** in a string. A word is a maximal run of non-space characters; the result joins the words back-to-front with a **single** space, with **no** leading, trailing, or repeated spaces — regardless of how the input was spaced.

```
"the sky is blue"            ->  "blue is sky the"
"  hello world  "            ->  "world hello"
"a good   example"           ->  "example good a"
"single"                     ->  "single"
"   "                        ->  ""            (all spaces)
"  leading and trailing  "   ->  "trailing and leading"
```

**Constraints:** `1 ≤ s.length ≤ 10⁴`; `s` contains English letters, digits, and spaces; there is at least one word.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **byte scan → word slices → emit back-to-front** ★ | [`reverse_words.kara`](reverse_words.kara) ✓ | [`reverse_words.py`](reverse_words.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

One left-to-right pass over `s.bytes()`. Skip any run of spaces, then take the maximal non-space run `[start, i)` as a word and push the **slice** `s[start..i]` (an owned `String`) into a `Vec[String]`. After the scan, emit the words **back to front**, joining with a single space — which drops all the incidental spacing (leading, trailing, and runs between words) for free.

## Kāra features exercised

- **String slicing into owned words** — `words.push(s[start..i].to_string())`: a ranged index `s[start..i]` produces a fresh owned `String`, collected into `Vec[String]`.
- **Byte-level scanning** — `s.bytes()` → `Slice[u8]`, the `b' '` space literal, no `Vec[char]` snapshot.
- **Reverse-order emit** — a descending `while k >= 0` over the word vector, `out.push_str(words[k])` with a leading-space guard.

## Compiler friction surfaced & fixed by this kata

The natural word-collection line `words.push(s[start..i].to_string())` surfaced a **run-vs-build divergence** ([kara `B-2026-07-22-6`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)): calling `.to_string()` (or `.clone()`) directly on a **string slice** `s[a..b]` compiled fine under the interpreter but failed under codegen with *"indexed-receiver method 'to_string' — element TypeExpr unknown"*. The codegen path for `obj[i].method()` assumed the indexed receiver was a `Vec`/`Slice`/`Array` element, but a String with a range index is a substring, not an element. Since a string slice is already an owned `String`, `.to_string()`/`.clone()` on it is the slice itself — **fixed in the compiler** by returning the sliced `String` directly, not worked around here. Regression test: `codegen::e2e_string_slice_to_string_method`.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`445176123`). Workload: reverse-words over a large multi-word byte buffer x passes, rolling-hash checksum sink.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-11-01, karac g6697158fa (v2/MIR backend) (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 261.3 ms | 0.96× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 265.2 ms | 0.98× |
| Go | 269.7 ms | 0.99× |
| **Kāra (codegen)** | 271.3 ms | 1.00× |
| Rust `-O` | 275.9 ms | 1.02× |

Kāra is now 1.02× ahead of `rustc -O` and 1.02× behind the equal-safety Rust row, 1.04× behind C. Against the previous measurement (karac 0.1.0, legacy backend, 2026-07-27) the ratios are flat: Kāra/Rust 1.01× → 0.98×, Kāra/C 1.06× → 1.04×, Kāra/Go 1.03× → 1.01× (every comparator also ran ~11% slower in absolute terms this session, so compare ratios, not milliseconds).

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   reverse_words.kara
karac build reverse_words.kara && ./reverse_words
python3 reverse_words.py
diff <(karac run reverse_words.kara) <(python3 reverse_words.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean.

**Benchmarked since this note was written** (see § Benchmarks; it was first kept oracle-only). The work is string parsing and per-word allocation, so the benchmark measures each language's stdlib string/`Vec` allocator as much as codegen; read its ratios with that in mind.
