# 316. Remove Duplicate Letters

Given a string of lowercase letters, remove duplicates so that every letter
appears **once**, and among all such results return the **lexicographically
smallest**. The result must be a subsequence of the input — letters keep
their relative order.

```
"bcabc"     ->  "abc"
"cbacdcbc"  ->  "acdb"
"bcac"      ->  "bac"    the first c cannot go: nothing bigger is behind it
```

Equivalently: the answer is the smallest **permutation of the distinct
letters** that is a **subsequence** of the input. Both halves of that sentence
are checked independently below.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `remove_duplicate_letters.kara` ★ | monotone stack with a last-occurrence table | `O(n)` |
| `remove_duplicate_letters_greedy.kara` | prove the first letter, delete it, recurse | `O(26 n)` |
| `remove_duplicate_letters_mask.kara` | suffix-availability bitmasks, one scan per placed letter | `O(26² n)` worst |
| `remove_duplicate_letters_brute.kara` | every subsequence, keep the letter-unique ones, take the min | `O(2ⁿ n)` |
| `differential.kara` | four arms, eleven properties, 5,832 + 1,056 cases | — |
| `bench/remove_duplicate_letters.kara` | 4,000,000 letters × 100 passes | — |

## Three ways to decide a letter's fate

**★ The stack.** Walk left to right, keeping the answer so far on a stack. A
letter already on the stack is skipped — it is placed, and it was placed as
early as it could be. Otherwise pop every top that is **bigger** than the new
letter **and still has a later copy**: popping it now and re-adding it later
gives a smaller string. Then push. Both halves of the pop condition are a way
to be wrong: pop a letter with no later copy and it is gone from the answer;
keep a bigger letter that could be deferred and the answer is not the
smallest. `last[c]` — the index of each letter's final occurrence — is one
pass before the walk. Each position is pushed at most once and each push is
popped at most once, so the whole thing is linear.

**The recursive greedy.** The first letter of the answer is the smallest
letter that can go first. Scan left keeping `pos` at the smallest letter so
far, decrementing a remaining count per letter; the moment some letter's count
hits zero, stop — everything after that point is missing that letter, so the
answer must start at or before it, and `s[pos]` is the smallest candidate.
Emit it, delete every later copy of it from the suffix after `pos`, recurse.
Each level places one distinct letter, so there are at most 26 levels.

**Suffix masks.** `suf[i]` is the 26-bit set of letters occurring in
`s[i..]`. With `need` the letters still to place and `start` the first usable
index, the next letter is the **smallest** `c` in `need` for which some
`p >= start` holds `c` and `suf[p]` covers `need` — every needed letter is
still available at or after `p`. Take the **leftmost** such `p`. No stack, no
deletion, no recursion: one table and a scan per placed letter.

The brute force is the definition: enumerate the `2ⁿ` position masks, keep
the subsequences in which each distinct letter appears exactly once, take the
minimum under `String`'s `<`. It knows nothing about greediness, which is what
makes it the oracle.

## The differential

Two tiers. The brute is a **complete oracle**, so for `n <= 11` it settles
every case (P1, 1,056 cases over six alphabets with their own seed band). For
`n` up to 40 the three fast arms are cross-checked (P2, P3) and then held to
properties that do not know the algorithm — 5,832 random and patterned
strings over alphabets of 2, 3, 4, 5, 8 and 26 letters, a quarter of the
random ones generated with a downward drift so long pop chains appear:

| property | what it checks | who it binds |
|---|---|---|
| P4 | the answer is a permutation of the distinct letters | ★ |
| P5 | the answer is a subsequence of the input | ★ |
| P6 | **relabel commutes**: `solve(map(s)) == map(solve(s))` for two strictly increasing letter maps (a shift to the top of the alphabet, and stride-2) | each arm |
| P7 | **idempotence**: `solve(solve(s)) == solve(s)` | each arm |
| P8 | appending the sorted alphabet yields the sorted alphabet | each arm |
| P9 | an all-distinct string (the reversed answer) is a fixed point | each arm |
| P10 | **local optimality**: no adjacent swap of the answer is both a subsequence of `s` and smaller (9,600 swaps were subsequences) | ★ |
| P11 | first-letter closed form: the smallest letter at or before the earliest last-occurrence | ★ |

P6–P9 relate **two invocations** of the same arm, so they carry weight the
oracle cannot: a mutant wrong the same way on both inputs still has to be
wrong *consistently under relabelling* to slip P6. P10 is the one property
with teeth against "not the smallest" beyond the brute's reach — it has no
oracle, only the answer and the input.

Green on `karac run`, `karac build`, the auto-par build and `--interp`,
byte-identical.

## Mutation testing

Content-anchored edits inside named function bodies, each run through the
full differential under the JIT. Two controls (a local rename in the stack
arm; the mask arm's letter loop respelled as `while`) must stay silent.

| mutant | edit | outcome | fired |
|---|---|---|---|
| M1 | stack: pop ignores `last` (loses letters) | killed | P1 597, P2/P3/P4 2,641, P9 5,340, P11 1,532 |
| M2 | stack: no `on_stack` skip (duplicates) | killed | P1 667, P2/P3/P4 5,160, P8 5,832, P9 1,079, P10 26,797 |
| M3 | stack: `last` records the *first* occurrence | killed | P1 407, P2/P3 4,149, P8 4,734, P10 5,816, P11 3,120 |
| E4 | stack: pop test `top > c` → `top >= c` | **equivalent** — silent, as predicted | — |
| M5 | greedy: no early break (global minimum) | killed | P2 2,641, P9 5,340 |
| M6 | greedy: keeps later copies of `first` | killed | P2 5,160, P8 5,832, P9 1,079 |
| M7 | greedy: rightmost minimum (`<` → `<=`) | killed — **predicted equivalent, wrong** | P2 1,416 |
| M8 | mask: no suffix-cover check | killed — **hangs** | 120 s budget |
| M9 | mask: rightmost valid position, not leftmost | killed | P3 1,416 |
| M10 | brute: accepts any letter-unique subsequence | killed | P1 1,056 |
| M11 | brute: takes the largest | killed | P1 616 |
| X12 | all three fast arms return the sorted alphabet | killed | P1 597, P5 2,641, P9 5,642 ×3, P11 1,532 |
| C1 | stack: rename a local | control — silent | — |
| C2 | mask: letter loop respelled as `while` | control — silent | — |

M7 and M9 fire on exactly the same 1,416 cases: they are the same mistake —
taking the rightmost of several equally-small candidates — made in two arms
whose mechanisms look nothing alike. X12 is the consistent-mirror probe: with
every fast arm wrong the same way, P2 and P3 are blind by construction, and
it is P5 (the answer is not a subsequence) and P11 (the first letter is
wrong) that carry it, plus the brute where it reaches. That is what the
oracle-free properties are for.

**Two predictions of "equivalent", one right and one wrong.** E4 changes the
stack's pop test from `top > c` to `top >= c` and is genuinely equivalent:
`top == c` cannot happen, because a letter on the stack is skipped before the
pop loop runs. M7 changes the greedy's minimum from leftmost (`<`) to
rightmost (`<=`), and I argued it equivalent too — every letter seen before
the later copy still has an occurrence after it, so nothing is lost. The
harness fired on 1,416 cases. On `abacb` the rightmost `a` sits at index 2;
the `b` before it is indeed still available afterwards, but only **after the
`c`** — so the recursion on the suffix `cb` yields `acb`, not `abc`. Nothing
is lost; the order is. The proof had a hole exactly one letter wide and the
first alphabet-of-three sweep found it.

**A mutant that hangs is a mutant that is killed, and the harness must know
that.** M8 removes the mask arm's suffix-cover check. On any input where the
smallest needed letter has no valid position after `start`, `placed` never
becomes true and `while need != 0` spins forever. The first run of the
harness sat on it for the subprocess timeout; a 120-second budget that
reports `HANG` as a kill is now part of the harness, and it should be part
of every harness whose arm contains a loop the mutation can un-terminate.

## Benchmark

`build-once + punch`: 4,000,000 letters generated once with a downward drift
(three steps in four go to the next-smaller letter, the fourth jumps
anywhere), so the text is long descending runs — the shape that makes the
stack push and pop rather than skip. 100 passes; each overwrites one position
chosen from the running checksum with a letter chosen the same way, runs the
★ arm, folds the answer bytes into the checksum, and restores the letter. All
five mirrors work on the byte buffer (bytes in, bytes out) and agree on
`checksum 993478848`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each, box otherwise idle. σ is 7–10% on every lane, so read the
Rust/Go/Kāra lanes as one band — canonical Apple-silicon numbers await an
idle run on the owner's machine ([#313's methodology note](../313-super-ugly-number/#a-methodology-note-because-the-first-version-of-this-table-was-wrong)).

| | mean | vs kara |
|---|---:|---:|
| c (`-O3`) | 251 ms ± 21 | 0.50× |
| c (`-O3 -march=x86-64-v3`) | 252 ms ± 18 | 0.50× |
| rust (`-O`) | 434 ms ± 35 | 0.86× |
| rust (equal safety + matched ISA) | 446 ms ± 43 | 0.88× |
| rust (`-O -C overflow-checks=on`, equal safety) | 450 ms ± 36 | 0.89× |
| go | 483 ms ± 40 | 0.95× |
| **kara** (codegen, seq) | **507 ms ± 49** | **1.00×** |

**The hot loop is four instructions per byte in C and roughly twice that
everywhere else.** For each of the 400 million positions the stack arm loads a
byte, subtracts `'a'`, loads a flag, and branches — and on this drifting text
the branch is almost always "already placed, skip". C does exactly that. Rust,
Go and Kāra each also bounds-check the byte load and the 26-slot flag lookup
(the index is a `u8` minus `'a'`, which the compiler cannot prove below 26),
and Kāra additionally overflow-checks the subtraction. That is the whole 2×:
the checked lanes sit within 17% of each other, and C is the only unchecked
one. Rust's equal-safety build turns on the overflow check but keeps the same
bounds checks it already had, which is why it moves only 4%.

**Kāra is at the back of the checked band, 13% behind equal-safety Rust,
inside 1.5σ.** The per-pass allocations are the same in every mirror (two
26-slot tables and the answer). Peak memory is 5.3–6.2 MiB in all four
compiled lanes — the 4 MB text and little else.

## Compiler findings: nothing to file

Four arms, the differential and the bench mirror compiled and agreed on all
four backends first time. The one diagnostic on the way was the call-site
`mut` marker on the LCG seed passed to `grow(…, seed: mut ref i64, …)`; `karac
fix` applied both occurrences and the file checked clean — the Mend loop
working as intended. Nothing in `u8` arithmetic (`(c - b'a') as i64`,
`(c as u8) + b'a'`, `u8 as char`), the 26-bit masks (`1 << c`, `& ~(1 << c)`),
`String`'s `<`, `Vec[u8]` as a stack, or the recursion returning `String`
gave the compiler any trouble.
