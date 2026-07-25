# 387. First Unique Character in a String

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** String, Hash Map, Counting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/first-unique-character-in-a-string](https://leetcode.com/problems/first-unique-character-in-a-string/)

Given a string `s`, return the index of the first non-repeating character. If
there is none, return `-1`.

```
"leetcode"      →  0     ('l')
"loveleetcode"  →  2     ('v')
"aabb"          →  -1
```

**Constraints:** `1 ≤ s.length ≤ 10⁵`; `s` consists of lowercase English
letters only.

## Approaches

Two passes either way — tally, then scan for the first count of 1. The two
implementations differ in *where* the tally lives, and that difference is the
point: each is a distinct codegen surface.

| Approach | File | Shape |
|---|---|---|
| **Map tally** ★ | [`first_unique_char.kara`](first_unique_char.kara) | `Map[i64, i64]` keyed by byte; general, no alphabet assumption |
| Fixed-alphabet counts | [`first_unique_char_counts.kara`](first_unique_char_counts.kara) | 26-slot `Vec[i64]`; uses the lowercase-only constraint |
| Reference oracle | [`first_unique_char.py`](first_unique_char.py) | known-correct LeetCode answer |

Both also compute `unique_count` — the number of characters appearing exactly
once. In the Map version that drives a **`for k in counts.keys()` walk**, which
is deliberate: it is the surface the inline map bucket walk lowers (ledger
B-2026-07-24-2, `bef6bbc`), so this kata is live regression coverage for it. In
the counts version the same total comes from a plain indexed scan, giving a
same-answer cross-check across two very different lowerings.

## Why this kata

Chosen by **compiler surface, not sequence**. Small map-and-string programs have
been finding a disproportionate share of `karac` defects — this session, 13
sequential array/DP katas surfaced nothing while two collection/string katas
produced three ledger entries including a high-severity use-after-free. This one
adds coverage for scalar-keyed map iteration specifically.

It found no new bugs, which is itself the useful signal: the scalar map path is
in good shape after `bef6bbc`.

## Verification

| Surface | Result |
|---|---|
| `karac run --interp` | ✅ matches `first_unique_char.py` |
| `karac run` (LLJIT) | ✅ |
| `karac build` (auto-par default) | ✅ |
| `karac build` + `KARAC_AUTO_PAR=0` | ✅ |

Both implementations, all four surfaces, byte-identical to the oracle —
including the empty-string and single-character edge cases.

## Kāra features exercised

- **`Map[i64, i64]` insert / get / `keys()`** — the scalar-halved map path,
  which lowers to an inline bucket walk with no runtime iterator call.
- **`bytes()` byte view + `b'a'` byte literals** — index arithmetic on the
  zero-copy view rather than per-char decoding.
- **`match` on `Option` with a `0` fallback arm** — the counter-increment idiom.
- **Early `return` from inside a loop** in a `ref String`-taking function.
- **Indexed `Vec[i64]` accumulate** (`counts[idx] = counts[idx] + 1`) in the
  fixed-alphabet variant.
