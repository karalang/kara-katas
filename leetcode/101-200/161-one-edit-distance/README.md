# 161. One Edit Distance

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Two Pointers · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/one-edit-distance](https://leetcode.com/problems/one-edit-distance/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Given two strings `s` and `t`, return `true` iff they are **exactly one edit distance** apart. One edit is a single **insert**, **delete**, or **replace** of one character. Identical strings (zero edits) are `false`.

```
"ab",   "acb"   ->  true   (insert 'c')
"1203", "1213"  ->  true   (replace '0' -> '1')
"cab",  "ad"    ->  false
"abc",  "abc"   ->  false  (identical)
"abc",  "abcde" ->  false  (two inserts)
```

**Constraints:** `0 ≤ |s|, |t|`; consist of lowercase/uppercase letters and digits.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **single lockstep scan** ★ | [`one_edit.kara`](one_edit.kara) ✓ | [`one_edit.py`](one_edit.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Put the shorter string on the left (swap if needed). If the lengths differ by more than 1, no single edit can bridge them. Otherwise walk both in lockstep to the **first mismatch**:

- **No mismatch** across the shorter length → one edit iff the longer string has exactly one extra trailing char.
- **Mismatch at `i`, equal lengths** → a **replace**: the tails `s[i+1:]` and `t[i+1:]` must match.
- **Mismatch at `i`, lengths differ by one** → an **insert**: skip the extra char in the longer string, then `s[i:]` must equal `t[i+1:]`.

O(n) time, O(n) for the decoded `char` vectors.

## Kāra features exercised

- **`Vec[char]` reassign / three-way move** — the shorter-on-the-left normalization is `let tmp = a; a = b; b = tmp`, exercising heap-owning struct/`Vec` variable moves (the B-2026-07-16-18 class) — verified leak- and double-free-free.
- **`ref Vec[char]` tail comparison** — `tails_equal` borrows both vectors read-only and compares from independent offsets.
- **`s.chars().collect()`** to index chars in O(1).

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`7582220`). Workload: is_one_edit over 4000 string pairs (len 48, alphabet 26) x 3000 punched reps; data-dependent early-exit scan.

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 581.5 ms | 0.50× |
| Go | 736.5 ms | 0.64× |
| Rust `-O` | 764.2 ms | 0.66× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 799.1 ms | 0.69× |
| **Kāra (codegen)** | 1.16 s | 1.00× |
| Python (scale lane) | 41.62 s | 35.92× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run   one_edit.kara
karac build one_edit.kara && ./one_edit
python3 one_edit.py
diff <(karac run one_edit.kara) <(python3 one_edit.py) && echo OK
```

## Notes

A 🔒 **LeetCode-Premium** problem (locked; spec reconstructed from its widely-known description). Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
