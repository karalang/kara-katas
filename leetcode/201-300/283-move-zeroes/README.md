# 283. Move Zeroes

Move every `0` to the end while keeping the relative order of the non-zero
elements. In place.

```
[0,1,0,3,12]  ->  [1,3,12,0,0]
[4,0,5,0,0,6] ->  [4,5,6,0,0,0]
```

## Approaches

| file | mechanism | writes |
|---|---|---:|
| `move_zeroes.kara` ★ | write cursor, then zero-fill | always `n` |
| `move_zeroes_swap.kara` | swap when the cursor falls behind | 2 per displaced element |
| `move_zeroes_stable.kara` | collect non-zeros, pad, copy back | `n` (+ O(n) space) |
| `differential.kara` | every array of length 0–6, four checks | — |

## The answer is unique — so this kata measures something else

Unlike [#278](../278-alien-dictionary/), [#280](../280-wiggle-sort/) and
[#282](../282-expression-add-operators/), there's exactly one correct output, so
equality is the right oracle and the harness is simpler for it.

What it adds instead is **the follow-up's question**. The problem asks to
minimize operations, so the write count is measured per solver — the same
treatment [#277](../277-find-the-celebrity/) gave its API-call budget.

```kara
// ★: store every non-zero at the cursor, then fill the tail
for i in 0..n:  if a[i] != 0 { a[write] = a[i]; write += 1 }
for j in write..n:  a[j] = 0
```

The correctness argument is `write <= i` always, so a store never clobbers an
element the walk hasn't read. That inequality is also why the two loops can't be
fused: zeroing at `i` before the walk reaches it destroys data when `write == i`.

But it writes **every position** — `n` stores even for an array with no zeros,
where the right answer is zero writes.

## The swap version is cheaper, but not uniformly

```kara
if a[i] != 0 and i != write:  swap a[i], a[write]
```

When no zero has been seen, `write == i` and there's nothing to do. But a swap is
*two* writes, so once the cursor falls behind, every remaining non-zero costs
double. Measured over all 5461 arrays of length 0–6:

```
total writes: cursor 30948, swap 20280
cases where swap wrote less 3768, where the cursor wrote less 664
```

Swap is 34% cheaper overall and wins about 6:1 — but the cursor genuinely wins
664 times. The crossover is a property of the input: how early the first zero
appears and how many non-zeros follow it.

## Four checks, and each invariant has its own failure

Equality between solvers only says they agree. Three invariants hold of every
result on its own:

1. **The multiset is preserved** — a reorder must not invent or drop elements.
2. **The non-zeros keep their relative order.**
3. **Every zero is at the end.**

Check 2 is the one that gets forgotten, and it's exactly what a "sort by is-zero"
solution breaks: sorting puts all zeros at the end and scrambles everything else,
passing check 3 perfectly.

```
cases 5461
total writes: cursor 30948, swap 20280
cases where swap wrote less 3768, where the cursor wrote less 664
digest 170171595
multiset broken 0, non-zero order broken 0, zeros misplaced 0
cursor vs definition 0, swap vs definition 0
```

## What the injected bugs did

| injection | vs definition | multiset | order | zeros | writes |
|---|---:|---:|---:|---:|---|
| cursor: forget the zero-fill loop | 4692 | 4692 | 4692 | 2440 | 15474 |
| cursor: store at `i` instead of `write` | 4692 | 4692 | 4692 | 2440 | 30948 |
| **swap: drop the `i != write` guard** | **0** | **0** | **0** | **0** | **30948** |
| definition: collect non-zeros in reverse | 2758 | 0 | **2758** | 0 | — |
| definition: put the zeros first | 5208 | 0 | 0 | **5208** | — |

**The third row is why the write counter exists.** A self-swap is a no-op, so
dropping the guard leaves every result *perfectly correct* — equality clean, all
three invariants clean — while doing 53% more writes (20280 → 30948). No
result-based check can see it. That's [#277](../277-find-the-celebrity/)'s lesson
about API calls, in a problem where the operation being counted is a store.

Rows four and five give each remaining invariant its own demonstration: reversing
the non-zeros trips **only** check 2, and putting the zeros first trips **only**
check 3. Neither disturbs the multiset.

## Two reserved words this kata walked into

`writes` and `stable` are both reserved and cannot be identifiers — the first is
one of Kāra's eight effect verbs (`reads`, `writes`, `sends`, `receives`,
`allocates`, `panics`, `blocks`, `suspends`), the second a layout keyword. Both
produced clear diagnostics naming the collision; the counter here is `stores` and
the definitional solver is `by_definition`. Worth knowing before reaching for any
of those as a variable name.

## Kāra features exercised

- **`mut ref Vec[i64]`** for the in-place reorder, with a second `mut ref i64`
  threaded alongside as the operation counter.
- **Insertion sort over a copy** inside the multiset check, so the check never
  disturbs what it validates.

## Running

```bash
karac run move_zeroes.kara
karac run move_zeroes_swap.kara      # same answers, different write counts
karac run move_zeroes_stable.kara

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in move_zeroes move_zeroes_swap move_zeroes_stable differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

The differential's range was picked by measurement, as in
[#282](../282-expression-add-operators/): at length 6 every injection above is
still caught with each invariant firing alone, while the `--interp` leg goes
58 s → 4m35s → ~20 min for lengths 6, 7 and 8.
