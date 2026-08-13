# 266. Palindrome Permutation

Given a string, decide whether **any permutation of it** is a palindrome.

```
"code"     ->  false
"aab"      ->  true      aba
"carerac"  ->  true      racecar
""         ->  true      the empty palindrome
"aabb"     ->  true      abba — even length, zero odd counts
```

**Constraints:** `1 ≤ s.length ≤ 5000`; `s` consists of lowercase English letters.

## Approaches

| file | state | mechanism |
|---|---|---|
| `palindrome_permutation.kara` ★ | 256 counters | histogram, then count the odd entries |
| `palindrome_permutation_toggle.kara` | a `Set` | toggle membership; the set *is* the odd characters |
| `palindrome_permutation_bits.kara` | one `i64` | XOR a bit per character; test for ≤ 1 bit set |
| `differential.kara` | — | 4,000 cases, three deciders + a brute-force reference |

## The mechanism

A palindrome pairs off: position `i` must match position `n-1-i`. So every
character needs an even count — with one exception, the lone middle character of
an odd-length palindrome. Hence:

> permutable ⟺ **at most one** character occurs an odd number of times.

## At most one, not exactly one

That distinction is the whole problem. `odd == 1` is the natural slip — a
palindrome *does* have a middle character — but only an odd-**length** one does.
`"aabb"` has zero odd counts and permutes to `"abba"`; `odd == 1` rejects it.

The two readings agree on every odd-length string and disagree on every
even-length one. That is a clean 50/50 split of any random test set, so the bug
does not hide *statistically* — it hides only if the examples on hand happen to
be odd-length, and the harness below counts how many even-length permutable
cases it generated so that the claim is a number.

## Why three, and why they cannot check each other

The three files are the same theorem in three currencies: counts, set
membership, and bits. That makes them good at catching each other's *clerical*
errors — a missed removal, a wrong bit index — and useless against an error in
the theorem itself.

If `at most one` is misread as `exactly one`, all three can be written wrong in
the same way, and then they agree with each other perfectly:

| injected bug | deciders disagreeing | brute force disagreeing |
|---|---|---|
| `odd == 1` in the histogram only | 1,224 | 987 |
| toggle never removes | 1,310 | 0 |
| bitmask demands `mask == 0` | 1,400 | 0 |
| ★ **`exactly one` in all three at once** | **0** | **987** |

The last row is why the differential carries a reference that knows nothing about
counts, parity or middles: for lengths up to 7 it enumerates **every**
permutation — next-permutation over the sorted bytes, which visits each distinct
arrangement of a multiset exactly once — and asks whether any of them reads the
same both ways. That is the problem statement executed literally. Three
implementations of one idea cannot adjudicate the idea.

(The 1,224 in the first row is exactly the count of generated cases that are both
even-length and permutable, which is precisely the set where `<= 1` and `== 1`
differ. The generator and the harness agree on their own arithmetic.)

## Generator design

Uniformly random strings are almost never permutable once the alphabet grows, so
the accept path would go untested. Of the eight families, three **construct**
permutable strings — pairs plus an optional lone middle, then shuffled — and one
perturbs such a string by a single character, giving negatives that share every
structural property with a true case except the answer. Alphabets stay small
(1..4 for the brute-forced families) so ties, and therefore even counts, are
common.

Over 4,000 cases: **2,624 permutable** (66%), **1,224 of them even-length**, and
**3,065 verified against the brute-force reference** with zero disagreements.
Lengths above 7 are cross-checked between the three deciders only — the factorial
reference cannot follow them there, and that limit is stated rather than papered
over.

## The bug this kata found

The toggle solver's natural spelling is

```kara
for b in s.bytes() {
    if odd.contains(b) { odd.remove(b); } else { odd.insert(b); }
}
```

and it **miscompiled**. `bytes()` yields `u8`, the set holds `i64`, and under
both compiled backends `Set.contains` returned false for an element that was
present — so the remove branch was dead and the set silently became the
*distinct* characters rather than the *odd-parity* ones. `"aab"` and `"aabb"`
answered false. The interpreter was correct, so it was a run-vs-build divergence
with a silent wrong answer.

Note how well it hid: `"aa"`, `"zzzzzzzz"`, `"code"` and `"aaabbb"` all give the
**right** answer under the wrong set. A small example set passes entirely; the
kata's four-surface A/B matrix is what caught it.

Filed as **`B-2026-08-13-15`** (class `miscompile`, high) and **fixed the same
day** by `675494c`. The code above is what the file now contains — no cast, no
workaround — and it is byte-identical across all four surfaces.

### Two things this kata got wrong, kept here because they are the lesson

**The design call was not open.** The filed row offered two fixes — reject the
width mismatch at typecheck, or coerce in codegen — and framed accepting a `u8`
at a container argument as *inconsistent* with Kāra refusing `b - 97i64`. It is
not inconsistent; the two rules are deliberately different. Kāra's
`check_int_widening_coercion` rejects only **narrowing**, and its own diagnostic
says so out loud: *"widening coercions such as i32 → i64 remain implicit."* So a
`u8` argument to a `Set[i64]` method was always legal, and the bug was simply
that codegen did not implement what the typechecker had promised. Rejecting it
would have deleted a documented feature.

That is why the file above carries no cast, and why the bitmask solver's
`b as i64` is a different situation entirely: that one is *arithmetic*, where
mixed widths are refused outright.

**The scope table was wrong, and wrong for an avoidable reason.** This kata
reported `Set[i64].insert(u8)`, `remove(u8)`, `Vec[i64].contains(u8)` and
`Map[i64,i64].contains_key(u8)` as *correct*. They were not. Every one of those
probes used the byte `97`, and **97 is the one value at which the bug cannot
appear** — sign- and zero-extension agree below 128, and the undefined high bytes
happened to be zero. Re-probed with the high bit set (`200u8`, `60000u16`,
`4000000000u32`), 14 of 15 shapes were wrong.

A probe value has to be chosen to *expose* the boundary it is testing, exactly
the way this kata's own generator picks small alphabets to force ties and
[#265](../265-paint-house-ii/)'s picks a narrow cost range for the same reason.
Applying that discipline to the harness and not to the bug report is how a
scope table ends up asserting the opposite of the truth.

## Kāra features exercised

- **`String.bytes()`** in a `for`, and Kāra's asymmetric width rules on the
  result: implicit **widening** at a container argument (`Set[i64].contains(u8)`
  needs no cast) but no mixing at all in **arithmetic** (`b - 97i64` is refused).
- **`Set[i64]`** with `insert` / `remove` / `contains` / `len`.
- **XOR and shift on `i64`** (`mask ^ (1 << (b as i64 - 97))`), plus the
  clear-lowest-bit test `mask & (mask - 1) == 0`.
- **Short-circuit `and` as an index guard** — `while i >= 0i64 and a[i] >= a[i+1]`
  in next-permutation, where the left operand is what keeps the right one legal
  (the same shape as [#251](../251-flatten-2d-vector/)).
- **In-place `Vec` reverse and swap**, for the permutation walk.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

## Running

```bash
karac run palindrome_permutation.kara
karac run palindrome_permutation_toggle.kara
karac run palindrome_permutation_bits.kara

diff <(karac run palindrome_permutation.kara) <(python3 palindrome_permutation.py) && echo OK
diff <(karac run palindrome_permutation.kara) <(karac run palindrome_permutation_toggle.kara) && echo OK
diff <(karac run palindrome_permutation.kara) <(karac run palindrome_permutation_bits.kara) && echo OK

# 4,000 cases, three deciders plus an exhaustive-permutation reference
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in palindrome_permutation palindrome_permutation_toggle palindrome_permutation_bits differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
