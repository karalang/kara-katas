# 280. Wiggle Sort

Reorder the array so that `nums[0] <= nums[1] >= nums[2] <= nums[3] >= ...`.

Any valid arrangement is accepted, and one always exists — the comparisons are
non-strict, so even an all-equal array already wiggles.

```
[3,5,2,1,6,4]  ->  [3,5,1,6,2,4]   (the greedy's answer)
               ->  [1,3,2,5,4,6]   (sort-then-pair's answer — also correct)
[6,6,5,6,3,8]  ->  already wiggles, unchanged
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `wiggle_sort.kara` ★ | one pass, fix each position locally | **O(n)** |
| `wiggle_sort_sorted.kara` | sort, then swap adjacent pairs | O(n log n) |
| `wiggle_sort_brute.kara` | permutations, first that wiggles | O(n!·n) |
| `differential.kara` | 1680 arrays, validated not compared | — |

## Why a local fix can't break the constraint behind it

```kara
for i in 1..n:
    if i is odd  and nums[i] < nums[i-1]:  swap
    if i is even and nums[i] > nums[i-1]:  swap
```

This is the part that makes the greedy more than a plausible-looking trick. Say
`i` is odd and we swap because `nums[i] < nums[i-1]`. The worry is that moving
the larger value into `i-1` violates the already-satisfied
`nums[i-2] >= nums[i-1]`.

It can't. At that point `nums[i-2] >= nums[i-1]` held, and the value arriving at
`i-1` is the *old* `nums[i]`, which was strictly smaller than the old `nums[i-1]`
— hence smaller than `nums[i-2]` too. **The constraint behind gets more
satisfied, never less.** The even case is the mirror image.

So no lookahead and no second pass. The usual bug is fixing position `i` by
swapping with `i+1`, which *does* break the pair behind it — 473 invalid results
in the table below.

## Validity is two conditions, and the second gets forgotten

The answer isn't unique, so output can't be compared as strings — that would fail
correct solvers. Validity is checked instead:

1. **The wiggle property** — `v[i] >= v[i-1]` at odd `i`, `<=` at even `i`.
2. **The same multiset as the input.**

Forgetting the second makes the first nearly worthless: `[0]` wiggles, `[1,2]`
wiggles, and a solver that dropped half the array would sail through a
property-only check. **A validator for a reordering problem has to verify that a
reordering is what happened.** Measured, by truncating the greedy to two
elements:

| | invalid detected |
|---|---:|
| multiset check **on** | **1200** |
| multiset check **removed** | **0** |

The lex bound below independently catches 87 of those 1200 — so the two checks
overlap, but nowhere near enough to substitute for each other.

## A bound that survives non-uniqueness

The brute force returns the lexicographically **smallest** valid arrangement, so
every other correct solver's output must be lex ≥ it. That's sharper than "all
three are valid": it's a single ordering fact each solver must respect.

```
cases 1680, of which contain a duplicate 1204
greedy answers differing from the lex-smallest 794
sort-then-pair answers EQUAL to the lex-smallest 1680
answers lexicographically BELOW the brute-force minimum: greedy 0, sorted 0
digest 677552294
invalid (wiggle or multiset): greedy 0, sorted 0, brute 0
```

**794 greedy answers differ from the lex-smallest** — the non-uniqueness is
heavily exercised, and a string-comparison harness would have reported 794 false
failures.

**Sort-then-pair equalled the lex-smallest in all 1680 cases.** That is a
*measurement over this range*, not a theorem — I haven't proved that sorting and
swapping pairs always yields the lexicographically minimal wiggle, and it is
stated here as an observation precisely because it looks like one you'd be
tempted to assume.

The alphabet is deliberately tiny (2–5 distinct values), so **1204 of 1680 arrays
contain a duplicate**. Ties are where the non-strict comparisons matter: a solver
using `<` where it needs `<=` is correct on distinct values and wrong the moment
two entries match.

## What the injected bugs did

| injection | invalid (greedy / sorted / brute) | below lex-min |
|---|---|---|
| greedy: swap with `i+1` instead of `i-1` | **473** / 0 / 0 | 0 / 0 |
| greedy: invert the odd/even test | 1295 / 0 / 0 | 65 / 0 |
| greedy: truncate to 2 elements | **1200** / 0 / 0 | 87 / 0 |
| sorted: swap pairs from index 0, not 1 | 0 / **1295** / 0 | 0 / 480 |
| sorted: skip the sort entirely | 0 / **884** / 0 | 0 / 70 |
| shared `wiggles()`: strict `<` | 573 / 579 / **352** | 206 / 434 |

The last row is a **validator** bug rather than a solver bug, and it reads
differently from the others: it implicates all three solvers at once, including
the brute force. That signature — everything failing together, the oracle
included — is what a broken check looks like, and it's worth being able to tell
apart from a broken solver.

## Kāra features exercised

- **`mut ref Vec[i64]`** as an in-place reorder — the whole problem is mutation
  through a borrow, and every solver shares that signature.
- **Insertion sort and next-permutation**, both written in place with explicit
  swaps.
- **`Vec[Vec[i64]]` literals** copied per case, so each solver sees a pristine
  input.

## Running

```bash
karac run wiggle_sort.kara
karac run wiggle_sort_sorted.kara      # a different, equally valid arrangement
karac run wiggle_sort_brute.kara

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in wiggle_sort wiggle_sort_sorted wiggle_sort_brute differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
