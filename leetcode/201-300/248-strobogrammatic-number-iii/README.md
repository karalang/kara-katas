# 248. Strobogrammatic Number III

Given two strings `low` and `high` representing decimal integers with no
leading zeros, return **how many** strobogrammatic numbers lie in the inclusive
range `[low, high]`.

A strobogrammatic number reads the same after a 180° rotation: `0↔0`, `1↔1`,
`8↔8`, `6↔9`, `9↔6`. Every other digit is destroyed by the rotation.

```
low = "50", high = "100"   ->  3        (69, 88, 96)
low = "0",  high = "0"     ->  1        (0 itself counts)
```

Closes the family started by [#246](../246-strobogrammatic-number/) (is one
number strobogrammatic?) and [#247](../247-strobogrammatic-number-ii/)
(list them all of a given length).

## Approaches

| file | shape |
|---|---|
| `strobogrammatic_iii.kara` | generate every candidate of each length in range, keep those inside the bounds |
| `strobogrammatic_count.kara` | closed-form count for interior lengths; generate only at the two boundary lengths |
| `differential.kara` | 3,000 randomized ranges, generate-and-filter vs brute force |

## The mechanism

**The range test is a string compare, not a numeric one.** This is the whole
design of the kata, and it is not an optimisation — it is what keeps the
algorithm correct at the problem's stated size.

Every candidate enumerated for a given length *has* that length, and so does
the bound it is compared against. For equal-length decimal strings with no
leading zeros, lexicographic order **is** numeric order. So `s < low` is a byte
walk and never a parse. LeetCode allows bounds up to 15 digits; a solution that
reaches for `parse::<i64>()` inherits that ceiling for free and then silently
loses it the moment the bounds grow. Comparing digits makes the algorithm
indifferent to how long the bounds are.

**Only the two boundary lengths need testing at all.** A candidate whose length
sits strictly between `len(low)` and `len(high)` has more digits than `low` and
fewer than `high`, so it is in range by construction. `strobogrammatic_iii`
still walks them (the straightforward reading of the problem);
`strobogrammatic_count` exploits it, replacing every interior length with a
closed form:

```
L == 1         ->  3                        "0", "1", "8"
L even         ->  4 * 5^(L/2 - 1)
L odd, L >= 3  ->  4 * 5^((L-1)/2 - 1) * 3
```

The `4` is the outermost pair (five pairs minus the barred `0/0`), each further
pair is a free `5`, and an odd length adds a centre worth `3`. That reproduces
3, 4, 12, 20, 60, 100, 300 for L = 1..7 — exactly the counts #247 enumerates.
On a 15-digit bound this is the difference between materialising ~250k strings
and materialising only the boundary lengths.

The generator itself is #247's, unchanged: build middle-outward, wrapping a
legal pair around the strobogrammatic numbers of length `k-2`, with only the
**outermost** layer barring a leading zero — which is why `n` rides along
beside `k` through the recursion. `n == 1` is exempt, because `"0"` alone is a
valid answer, and that falls out of the `k == 1` base case never consulting `n`.

## Verification

`differential.kara` runs 3,000 randomized ranges through two answers that share
no code path: the kata algorithm (which never parses a number) and brute force
over every integer in the range using #246's two-pointer predicate (which never
generates one). Ranges are held narrow (width ≤ 500) so brute force stays cheap
while the generator still has to get lengths, boundaries and the leading-zero
rule right.

```
cases=3000 mismatch=0 hash=568337804
```

Kāra and Python agree on that hash, and all three programs are byte-identical
across the four surfaces — `run --interp`, `run` (JIT), `build` (auto-par
default), and `KARAC_AUTO_PAR=0 build`. `strobogrammatic_iii.py --verify`
independently cross-checks the oracle's own generate-and-filter against brute
force on the 15 fixed cases before any of that.

## Kāra features exercised

- `bytes()` → `Slice[u8]` as an O(1)-indexable view, driving a three-way
  compare (`cmp_digits`) rather than #247's pure string building
- recursion returning `Vec[String]`, with per-level allocation
- `String` `push_str` accumulation, f-string interpolation of an `i64`
- integer `/` and `%` for the closed-form counts

## Benchmark

`bench/` times the **closed-form counting** variant — 1,000 LCG-drawn
`[low, high]` pairs of up to 8 digits. Sink `2183700`, reproduced exactly by the
C, Rust, Go and Python mirrors.

The counting variant, not the generate-and-filter twin, and not by accident:
[#247](../247-strobogrammatic-number-ii/)'s lane now measures recursive string
generation, so benching the twin here would re-measure it. This file exists to
make the interior-lengths point, and the bench is sized so that point is what
gets measured.

**The 8-digit cap was measured, not guessed**, and the first attempt was wrong.
Sized at 60,000 queries up to 15 digits it ran past two minutes, because the
closed form skips only INTERIOR lengths — both boundary lengths are still
enumerated, so per-query cost is set by the longer bound: ~13 ms at 15 digits
(4·5⁶·3 = 187,500 strings) against ~0.4 ms at 8 (4·5³ = 500). Sizing to 15
digits would have measured boundary enumeration — #247's job — and left ~35
queries, too few for a stable mean. At 8 digits the closed-form path dominates,
which is the thing worth timing.

This section previously read "no benchmark", arguing the runtime would be
allocator-dominated. That is true of the generate-and-filter twin and is
precisely what the sizing above avoids; [#246](../246-strobogrammatic-number/)
still carries the family's two-pointer-scan lane.

Published numbers await the Apple-silicon host — `bench/results.container-x86.json`
is corroboration only (BENCHMARKS.md § Hosts).

## Running

```bash
karac run strobogrammatic_iii.kara
karac run strobogrammatic_count.kara      # must print the same 15 lines
karac run differential.kara               # cases=3000 mismatch=0 hash=568337804
python3 strobogrammatic_iii.py --verify   # oracle vs brute force
```

## Notes

This is the third kata over the same family, and it surfaced **no new compiler
gaps** — the string, slice and recursion surfaces it leans on were all already
exercised by #246 and #247. That is a reasonable outcome for a third pass and
is recorded here rather than left implied: the corpus's bug-finding yield comes
from new shapes, and a family's third member is mostly confirmation.
