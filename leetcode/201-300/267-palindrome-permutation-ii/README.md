# 267. Palindrome Permutation II

Return **all distinct palindromic permutations** of a string, or an empty list
if none exist.

```
"aabb"     ->  abba, baab
"abc"      ->  (none)
"aabbc"    ->  abcba, bacab
"carerac"  ->  acrerca, arcecra, carerac, craearc, racecar, rcaeacr
""         ->  the empty palindrome
```

**Constraints:** `1 ≤ s.length ≤ 16`; `s` consists of lowercase English letters.

## Approaches

| file | search space | shape |
|---|---|---|
| `palindrome_permutation_ii.kara` ★ | `(n/2)!` | halve the counts, backtrack over distinct characters, mirror |
| `palindrome_permutation_ii_iter.kara` | `(n/2)!` | same halving, walked by next-permutation instead of recursion |
| `palindrome_permutation_ii_brute.kara` | `n!` | permute the whole string, keep the palindromes |
| `differential.kara` | — | 2,500 cases against **two** independent oracles |

## The mechanism

[#266](../266-palindrome-permutation/) asked *whether* a palindromic permutation
exists — at most one character may occur an odd number of times. This asks for
the set of them, and the whole design follows from one observation:

> a palindrome is determined by its **first half**.

So don't permute the string. Halve every count, permute the multiset of halves,
and mirror each arrangement around the optional lone middle character. For a
10-character input that turns 3,628,800 arrangements into 120.

**It also disposes of deduplication for free**, which is the part that bites.
Permuting `"aabb"` directly yields `"abba"` twice — once per ordering of the two
`a`s — so a permute-then-filter solution needs a `seen` set or a sort-and-unique
pass afterwards. Permuting the half `"ab"` yields each arrangement once, because
the backtracking loop iterates over **distinct characters** and consumes from
their counts: two identical characters are never two choices.

## Why three, and how each one breaks

The two halving forms share the insight and fail in different places:

- **Backtracking** can get *deduplication* wrong. Iterate over positions rather
  than over distinct characters and the duplicates come straight back.
- **Next-permutation over the sorted half** cannot duplicate — it visits each
  arrangement of a multiset exactly once by construction — but it can get the
  *mirror* wrong: an off-by-one in the reversed tail, or forgetting that the
  middle character is not part of the half. Its loop is
  `while true { emit; if not next_perm { break } }` rather than
  `while next_perm { emit }`, because the sorted half is itself the first answer
  and a pre-test loop would skip it.

The brute force asserts nothing at all — no halving, no claim about the middle,
no deduplication argument — which is what makes it the reference for *content*.
It uses next-permutation for the same reason the iterative form does: walked from
the sorted string it visits each distinct arrangement once, so a reference that
would otherwise need its own `seen` set doesn't have one.

## The fourth oracle, which generates nothing

Three generators of the same idea can all be wrong in the same way. The count of
distinct palindromic permutations has a **closed form** — the number of distinct
arrangements of the half multiset:

```
(n/2)! / Π (count_c / 2)!
```

That is a formula, not an enumeration: it shares no loop, no recursion and no
deduplication argument with any generator. It also keeps working past the point
where the `O(n!)` reference has to drop out.

**Both properties were tested, not assumed:**

| injected bug | half-forms disagree | brute force | multinomial |
|---|---|---|---|
| `odd > 1` guard dropped from the ★ form | 551 | 551 | 551 |
| iterative form drops the middle character | 904 | 0 | 0 |
| ★ **both halving forms double-count, but only at `n ≥ 10`** | **0** | **0** | **75** |

The last row is the argument for having the closed form at all. Both generators
are wrong identically, so cross-checking them is silent; the bug fires only above
`n = 8`, where the factorial reference cannot follow; and the count oracle catches
it anyway. The middle row is the mirror image — there the two generators catch
what the oracles cannot, because the oracles agree with whichever one is right.

## Generator design

Random strings over a wide alphabet are essentially never permutable, so the
answer would be the empty list almost always. Half the families therefore
**construct** permutable inputs — pairs plus an optional lone middle — one
deliberately breaks a constructed input so the empty answer arrives for a
structural reason rather than by luck, and one emits a single repeated character,
where the answer is always exactly one palindrome.

Over 2,500 cases: **1,949 non-empty answers** (78%), **5,998 palindromes
generated**, **2,390 verified against the brute force** with zero disagreements,
and zero multinomial disagreements at every size.

## Kāra features exercised

- **Recursion with `mut ref` parameters** threaded through — and the call-site
  marker rule in both directions: `build(counts, half, …)` forwards without
  `mut` because those are already `mut ref` in scope, while `next_perm(mut a)`
  needs the marker because `a` is a fresh owned binding.
- **`Vec.pop()`** as the backtracking undo, paired with the count restore.
- **`b as u8 as char` inside an f-string** to turn a code point back into text.
- **`while true` with a mid-body `break`**, where the first value must be emitted
  before the first step.
- **Short-circuit `and` as an index guard** in next-permutation
  (`i >= 0i64 and a[i] >= a[i+1]`).

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

No compiler bugs found. The two call-site `mut`-marker diagnostics encountered
while writing this were both correct and both said exactly what to do.

## Running

```bash
karac run palindrome_permutation_ii.kara
karac run palindrome_permutation_ii_iter.kara
karac run palindrome_permutation_ii_brute.kara

diff <(karac run palindrome_permutation_ii.kara) <(python3 palindrome_permutation_ii.py) && echo OK
diff <(karac run palindrome_permutation_ii.kara) <(karac run palindrome_permutation_ii_iter.kara) && echo OK
diff <(karac run palindrome_permutation_ii.kara) <(karac run palindrome_permutation_ii_brute.kara) && echo OK

# 2,500 cases, three generators plus an exhaustive reference and a closed form
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in palindrome_permutation_ii palindrome_permutation_ii_iter palindrome_permutation_ii_brute differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
