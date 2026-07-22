# 165. Compare Version Numbers

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Two Pointers · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/compare-version-numbers](https://leetcode.com/problems/compare-version-numbers/)

Compare two dot-separated version strings. Each **revision** is compared as an **integer** (so leading zeros are insignificant: `"1.01" == "1.001"`), left to right. A version with fewer revisions is padded with implicit zeros (`"1.0" == "1"`). Return `-1`, `0`, or `1`.

```
"1.2",     "1.10"     ->  -1   (2 < 10)
"1.01",    "1.001"    ->   0
"1.0",     "1.0.0.0"  ->   0
"1.0.1",   "1"        ->   1
"7.5.2.4", "7.5.3"    ->  -1
```

**Constraints:** `1 ≤ |version| ≤ 500`; revisions are non-negative integers with no leading `+`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **digit-accumulation parse + lockstep compare** ★ | [`compare_version.kara`](compare_version.kara) ✓ | [`compare_version.py`](compare_version.py) ✓ |

`✓` runs end-to-end across interpreter, JIT, and codegen (default auto-par and `KARAC_AUTO_PAR=0`), byte-identical to the Python mirror. valgrind-clean (`KARAC_AUTO_PAR=0`).

## The mechanism

Parse each version into its list of integer revisions in a **single byte scan** — accumulate digits directly (`val = val*10 + (byte - '0')`) and split on `'.'`, with no substring allocation. Comparing as integers is what makes `"1.01"` and `"1.001"` equal. Then walk both revision lists to the longer length, treating a missing revision as `0`, and return on the first difference.

## Kāra features exercised

- **`s.bytes()` byte scan** with `u8` byte-literal delimiters (`b'.'`, `b'0'`) and `byte as i64` digit arithmetic — the O(1) raw-byte path (`s[i]` on a `String` is a compile error).
- **`Vec[i64]` per-version revision lists** returned by value from `revisions`.
- **`if`-expression zero-padding** for the shorter version (`let x = if i < na { a[i] } else { 0 }`).

## Running

```bash
karac run   compare_version.kara
karac build compare_version.kara && ./compare_version
python3 compare_version.py
diff <(karac run compare_version.kara) <(python3 compare_version.py) && echo OK
```

## Notes

Verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — agrees with the Python mirror, and is valgrind-clean. Oracle-only.
