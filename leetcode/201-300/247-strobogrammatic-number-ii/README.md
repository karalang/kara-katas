# 247. Strobogrammatic Number II

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Recursion · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/strobogrammatic-number-ii](https://leetcode.com/problems/strobogrammatic-number-ii/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

Return **every** strobogrammatic number of length `n` — the generation problem behind [#246](../246-strobogrammatic-number/)'s recognition problem.

```
n = 1  ->  0 1 8
n = 2  ->  11 69 88 96
n = 3  ->  101 609 808 906 111 619 818 916 181 689 888 986
```

**Constraints:** `1 ≤ n ≤ 14`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| recursive build from the middle outward ★ | O(output) | [`strobogrammatic_ii.kara`](strobogrammatic_ii.kara) ✓ | [`strobogrammatic_ii.py`](strobogrammatic_ii.py) ✓ |

`✓` marks agreement under **interpreter**, **JIT**, and **codegen** — default auto-par build and `KARAC_AUTO_PAR=0` alike.

## The mechanism

**Build from the middle outward, not left to right.** A strobogrammatic number of length `k` is a legal outer pair wrapped around a strobogrammatic number of length `k-2`, so the recursion bottoms out **twice**:

```
k == 0  ->  [""]            even lengths
k == 1  ->  ["0","1","8"]   odd lengths — the digits that survive rotating IN PLACE
```

That second base case is the same fact #246 leans on from the other side: an odd-length number's centre pairs with *itself*, so only `0`, `1` and `8` may sit there. Recognition and generation are two views of one constraint.

Every other level wraps each inner result in each of the five pairs `0/0 1/1 6/9 8/8 9/6`.

**The leading zero is the whole wrinkle.** `"0"` wrapped in a `0/0` pair gives `"000"`, which is not a number of length 3. So the **outermost** layer — and only that one — refuses the `0/0` pair, which is why `n` is threaded through the recursion beside `k`: the recursion has to know whether it is at the outside. `n == 1` is exempt, because `"0"` alone *is* a valid answer, and that falls out for free since the `k == 1` base case never consults `n`.

Counts run **3, 4, 12, 20, 60, 100, 300** for n=1..7 — each added pair multiplies by 5 at inner layers, by 4 at the outermost where `0/0` is barred.

## What it found

**No compiler bugs.** Two independent checks, not one:

- **`valid == count` at every n**, in both mirrors. Every generated number is re-tested with #246's two-pointer predicate, which re-derives the property from the string instead of trusting how it was built. A generator that emitted something illegal would show `valid < count`.
- **Generator == brute force** for n≤5 — `python3 strobogrammatic_ii.py --verify` enumerates all n-digit candidates, filters them through the same predicate, and compares as sets. Construction versus enumerate-and-filter are genuinely different algorithms, and this catches the errors the first check cannot: a generator that *omits* valid numbers, or admits a leading zero. It is Python-only because brute force needs zero-padded integer formatting; the `valid` check is the half both languages run.

This is the third clean kata in a row, which is the honest headline. The shapes here — recursion returning `Vec[String]`, `String` concatenation via `push_str`, nested `while` over a `Vec[String]` — are well covered by the corpus.

## Kāra features exercised

- **Recursion returning `Vec[String]`** — each level allocates a fresh vector and consumes the level below, the main new surface relative to #246.
- **Two base cases in one function**, dispatching on `k == 0` and `k == 1`, with early `return` of a locally built `Vec`.
- **A parameter threaded purely for context** (`n` alongside `k`) to make the outermost layer distinguishable — no accumulator, no mutable state.
- **`String` building by `push_str`** of a borrowed `Vec[String]` element, plus `push(char)` for the separator in `join_all`.
- **`num.bytes()[i]` byte indexing** in the validity re-check, carried over from #246, where Kāra refuses `s[i]` outright.

## Running

```bash
karac run   strobogrammatic_ii.kara
karac build strobogrammatic_ii.kara && ./strobogrammatic_ii
python3 strobogrammatic_ii.py

diff <(karac run strobogrammatic_ii.kara) <(python3 strobogrammatic_ii.py) && echo OK
python3 strobogrammatic_ii.py --verify     # generator vs brute force, n<=5
```

## Notes

Verified byte-identical under `karac run --interp`, `karac run`, and `karac build` — including the default auto-parallelising build and `KARAC_AUTO_PAR=0`.

**Benchmark: `bench/`.** Generates every strobogrammatic number of length 16 (312,500 strings), re-verifies each by the two-pointer rotation check, 12 rounds. Sink `404314354`, reproduced exactly by the C, Rust, Go and Python mirrors.

This lane previously read "no benchmark", on the grounds that the runtime is dominated by allocating and concatenating output and so would measure each language's string allocator rather than the algorithm. **That objection is correct and the lane is kept anyway**, because string building *is* what this algorithm does — the middle-outward recursion has no other cost — and measuring it on identical work across five languages is a legitimate comparison, not a confound. What the section must not do is imply the number says something about the strobogrammatic construction specifically; it says something about string throughput under that construction.

Which turned out to be the point. On the x86 corroboration host Kāra runs **793 ms against `rustc -O`'s 681 and equal-safety Rust's 716** — 1.17× and 1.11×. That independently reproduces the residual the compiler README already tracks ("a few string-building loops, ~1.2×"), on a workload chosen for a different reason. A lane that surfaces a known gap earns its place; recognition ([#246](../246-strobogrammatic-number/)) still carries the two-pointer-scan measurement for the pair.

Published numbers await the Apple-silicon host — `bench/results.container-x86.json` is corroboration only (BENCHMARKS.md § Hosts).
