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

## Benchmark

`bench/` fixes one multiset of **8 character pairs** and punches the ★
half-backtracking generator through it **44 times**. Each round adds one extra
copy of a *different* character, making that character the lone middle: the
search tree is identical round to round (half length 8, all distinct, so
8! = 40,320 arrangements) while the bytes produced differ, so no round repeats
the last. Sink `120871863`, reproduced by all four compiled mirrors and Python.

**What it measures is the recursive search** — 40,320 leaves reached through a
tree whose every node scans 128 counter slots to find the few that are non-zero,
with a decrement/push descending and a pop/restore returning. A sparse scan
inside a recursion is a shape the corpus does not otherwise have. The 128-slot
scan is kept rather than compacted into a list of live characters, because it is
what the ★ file does and what makes the deduplication free.

**Every mirror writes its 17 bytes into one hoisted buffer**, not a fresh string.
That is a parity decision, not an optimisation, and the first version of this
lane got it wrong — see below.

### What the x86 corroboration run shows

| lang | mean (ms) | σ |
|---|---|---|
| C (`-march=x86-64-v3`) | 308.8 ± 14.6 | 4.7% |
| Rust (checked, equal-safety) | 327.3 ± 9.5 | 2.9% |
| Rust (checked + `target-cpu=v3`) | 331.4 ± 12.9 | 3.9% |
| Go | 397.7 ± 9.4 | 2.4% |
| C | 405.6 ± 16.5 | 4.1% |
| Rust | 406.7 ± 15.5 | 3.8% |
| **Kāra** | **445.5 ± 10.5** | 2.4% |

**This lane cannot rank the languages, and the table should not be read as
doing so.** Two rows in it are impossible: `-march=x86-64-v3` beats plain
`clang -O3` by 31%, and *overflow-checked* Rust beats plain `rustc -O` by 24%.
Checks cannot make a program faster.

Both are **code alignment**. The two C builds emit the same hash-loop instruction
sequence; forcing alignment collapses the gap:

| build | default | `-falign-loops=32 -falign-functions=32` |
|---|---:|---:|
| `clang -O3` | 397.4 ms | **319.1 ms** |
| `clang -O3 -march=x86-64-v3` | 306.6 ms | **312.0 ms** |

Aligned, they land 2% apart instead of 30%, same sink. The baseline's 397 ms was
a misaligned hot loop, not an ISA deficit.

The obvious response — add the alignment flags everywhere — is refused on
purpose. `clang -O3` and `rustc -O` are the corpus's methodology; tuning them for
the one lane where they embarrass a build makes it incomparable with the other
250 and invites picking flags that flatter whoever is losing. So the table stands
as measured and claims only what it supports: **the intra-language twin spread
(31%, 24%) exceeds the inter-language spread, so the ordering is not resolvable
here.** What it does support is the range — every mirror between 309 and 446 ms,
a 1.44× band, with Kāra inside it rather than an outlier.

### The first version was wrong by 3×, for a parity reason

Before the hoisted buffer, each leaf built a string, and Kāra came out at
**476.5 ms against C's 156.0** — 3.05×, which would have read as a language
result. It was four different allocation strategies: C used a stack array and
allocated nothing, Rust and Go appended in place, and Kāra's `s = s + f"{…}"`
allocated a *new string per character* — 17 per leaf, since `+` is an immutable
concatenation. Giving every mirror one reusable buffer took Kāra from 476.5 to
227 ms on the identical sink.

That is the same defect as [#266](../266-palindrome-permutation/)'s stack-array
counters: the mirror written differently from the other three is the one
producing the false number. Full method for both artifacts in
[`bench/probe/README.md`](bench/probe/README.md).

Kāra's binary is 332.9 KiB against C's 15.8 KiB, Go's 2.17 MB and Rust's 3.86 MB;
peak RSS is 2.2 MiB, level with Rust's.

Published numbers await the Apple-silicon host —
`bench/results.container-x86.json` is corroboration only (BENCHMARKS.md § Hosts).

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

```bash
# cross-language benchmark (needs hyperfine, rustc, clang, go)
BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
