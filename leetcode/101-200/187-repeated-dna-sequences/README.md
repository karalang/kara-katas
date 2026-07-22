# 187. Repeated DNA Sequences

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Table · String · Sliding Window · Hash Function · Bit Manipulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/repeated-dna-sequences](https://leetcode.com/problems/repeated-dna-sequences/)

Return every length-10 substring (over the DNA alphabet `A/C/G/T`) that appears **more than once** in the string.

```
"AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"  ->  ["AAAAACCCCC","CCCCCAAAAA"]
```

**Constraints:** `1 ≤ |s| ≤ 10⁵`; `s` consists of `A`, `C`, `G`, `T`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **sliding window + count map** ★ | [`repeated_dna.kara`](repeated_dna.kara) | [`repeated_dna.py`](repeated_dna.py) |

Runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Slide a width-10 window across the string and count each 10-mer in a `Map[String, i64]`. A sequence is recorded exactly once — the first time its count crosses **1 → 2** — so the output is each repeated sequence in first-repeat order (deterministic across backends; LeetCode accepts any order). O(n) windows, each an O(10) substring hash.

## Kāra features exercised

- **`Map[String, i64]` counter with `String` keys** — the canonical grouping/counting idiom. Each iteration `get`s (borrows the key), and on a duplicate `insert`s over an existing key. This is the exact `String`-keyed overwrite surface the [#49 map-of-lists](../../1-100/49-group-anagrams/) work drove into the compiler's leak-fix (B-2026-07-22-12 / the older duplicate-key B-2026-06-20-9); here the value is a scalar `i64`, and it is verified valgrind-clean.
- **`s[i..i+10].to_string()`** — an owned `String` key minted per window from a slice.
- **`Option` match + `.clone()`** — record on the count transition, then reinsert.

## Running

```bash
karac run   repeated_dna.kara
karac build repeated_dna.kara && ./repeated_dna
python3 repeated_dna.py
diff <(karac run repeated_dna.kara) <(python3 repeated_dna.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
