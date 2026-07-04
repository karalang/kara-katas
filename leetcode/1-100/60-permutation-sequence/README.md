# 60. Permutation Sequence

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Math, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/permutation-sequence](https://leetcode.com/problems/permutation-sequence/)

The set `{1, 2, …, n}` has `n!` distinct permutations. Listed in lexicographic order and labelled `1 … n!`, return the **k-th** permutation sequence as a string.

```
n = 3  →  "123", "132", "213", "231", "312", "321"
                              ↑ k = 3  →  "213"

n = 4, k = 9   →  "2314"
n = 3, k = 1   →  "123"
```

**Constraints:** `1 ≤ n ≤ 9`, `1 ≤ k ≤ n!` (so `k ≤ 9! = 362880`, well inside i64).

This is the **closed-form dual of [kata #31](../31-next-permutation/)**: #31 steps *one* permutation forward in place; here we jump straight to the k-th without walking the `k-1` in between.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Factorial number system** — fix each digit by the block `(k-1) / (n-1-pos)!` it falls into, then recurse on the remainder | O(n²) time (pick-and-shift), O(n) space | [`permutation_sequence.kara`](permutation_sequence.kara) ✓ via `karac run` / `karac build` | [`permutation_sequence.py`](permutation_sequence.py) ✓ |
| **next_permutation iteration** — start from `1…n`, step forward `k-1` times (kata #31's four-move scan) | O(k·n) time, O(n) space | [`permutation_sequence_nextperm.kara`](permutation_sequence_nextperm.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output, the two solvers agree with each other, and the factorial solver agrees with the Python mirror across all seven cases (`n = 1…9`, including both extreme ranks `k = 1` and `k = n!`).

## Why two solvers?

**Factorial number system** ([`permutation_sequence.kara`](permutation_sequence.kara)) is the O(n²) closed form. The insight: sorted lexicographically, the `n!` permutations split into `n` contiguous blocks by their **first** element, each block holding exactly `(n-1)!` permutations. So the leading digit is fixed by which block the rank lands in — `idx = (k-1) / (n-1)!` — and the remainder `(k-1) % (n-1)!` re-poses the identical problem on the `n-1` digits left over. Working 0-indexed (`kk = k - 1`), at position `pos` the block size is `(n-1-pos)!`; `idx = kk / block` selects the digit to emit from the still-available pool and `kk = kk % block` descends into that block. The available digits live in a sorted `Vec[i64]` of `1…n`, and `digits.remove(idx)` pulls the chosen one out while shifting the tail down — the O(n) shift per step is the whole cost, giving O(n²).

**next_permutation iteration** ([`permutation_sequence_nextperm.kara`](permutation_sequence_nextperm.kara)) is the brute-but-honest dual: start from the first permutation `1,2,…,n` and step forward one lexicographic permutation at a time, `k-1` times, landing on the k-th. The step is [kata #31](../31-next-permutation/)'s four-move scan verbatim — pivot → successor → swap → reverse-suffix — here over a `mut ref Vec[i64]` so it mutates the caller's array in place. No wrap branch is needed: `k ≤ n!` guarantees we never step past the last permutation, so the pivot always exists. It is O(k·n) — up to `9! · 9 ≈ 3.3M` primitive ops at the bound, still instant, but asymptotically worse than the factorial form. It earns its place by exercising the exact #31 step and showing the incremental counterpart of the closed form.

## Kāra features exercised

- **`Vec[i64].remove(idx) -> i64` — index removal with tail-shift** (factorial) — `digits.remove(idx)` pulls the selected digit out of the pool and shifts the remainder down, returning the removed value. This is the delicate index-removal path on both surfaces (interpreter `method_call_seq.rs` and codegen `vec_method.rs` load + memmove + `len--`); the pool stays sorted for the next pick and both surfaces agree byte-for-byte.
- **`mut ref Vec[i64]` parameter mutated in place** (nextperm) — `fn next_permutation(a: mut ref Vec[i64], len)` swaps and reverses through the borrowed vector; the call site writes `mut a` (the `ref` is implied by the callee's signature), the same in-place-mutation shape as kata #37's `board: mut ref Vec[Vec[i64]]`.
- **Factorial table built by data-dependent `push`** — `fact[i] = fact[i-1] * i` folded into a growing `Vec[i64]`, then indexed as `fact[n - 1 - pos]` — a read whose index depends on the loop position, not a constant.
- **f-string accumulation into a `String`** — `result = f"{result}{digit}"` appends each emitted digit, the same accumulator pattern the corpus uses to build diffable output lines.
- **`for x in a.iter()` over `Vec[i64]`** (nextperm) — iterate the final array to render it, versus the factorial solver which builds the string as it picks.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   permutation_sequence.kara
karac build permutation_sequence.kara && ./permutation_sequence

# The next_permutation approach (identical output):
karac run permutation_sequence_nextperm.kara

# Python
python3 permutation_sequence.py

# Verify they all agree
diff <(karac run permutation_sequence.kara) <(python3 permutation_sequence.py)                    && echo OK
diff <(karac run permutation_sequence.kara) <(karac run permutation_sequence_nextperm.kara)       && echo OK
```
