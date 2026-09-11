# 320. Generalized Abbreviation

A **generalized abbreviation** of a word replaces any set of disjoint,
non-adjacent substrings with their lengths. `"word"` has sixteen:

```
word  1ord  w1rd  2rd  wo1d  1o1d  w2d  3d
wor1  1or1  w1r1  2r1  wo2   1o2   w3   4
```

Return all of them, in any order.

The statement is written in terms of substrings, which makes it sound like a
constraint-satisfaction problem. It is not. An abbreviation is a choice made
independently for each of the `n` letters — **keep it, or count it** — and
every one of the `2^n` choices is legal, so the answer has exactly `2^n`
entries and is indexed by an `n`-bit mask.

The "disjoint and non-adjacent" clause is not a rule to enforce; it is a
description of what the mask already gives you. Two counted runs that touched
would be one longer run — and the notation could not express them as two even
if you wanted it to, because a run of 1 followed by a run of 2 has to be
written `"12"`, which reads back as a single run of *twelve*. So the real rule
is *numbers are maximal runs of counted letters*, which is exactly what
run-length encoding a mask produces for free.

## Approaches

| file | mechanism | n=20 |
|---|---|---|
| `generalized_abbreviation.kara` ★ | walk `0..2^n`, run-length encode each mask | 399.0 ms |
| `generalized_abbreviation_backtrack.kara` | recurse per letter carrying a pending run | 251.0 ms |
| `generalized_abbreviation_grow.kara` | hold level `k`, build level `k+1` by editing strings | 348.4 ms |
| `generalized_abbreviation_runs.kara` | enumerate the maximal-run decompositions directly | 251.5 ms |
| `differential.kara` | four arms, thirteen properties | — |
| `bench/generalized_abbreviation.kara` | 8 passes × all `2^20` masks of a 20-letter word | — |

All four arms are `Θ(2^n · n)` — the output alone is that big, so none of them
can be better — and what separates them is the per-entry constant. The times
are AOT, `KARAC_AUTO_PAR=0`, 10 runs each, on a 20-letter word; the ratios hold
flat at `n = 16` and `n = 18` too.

## Four ways to enumerate 2^n things

**★ Count in binary.** Bit `i` set means "letter `i` is counted". Sweep the
letters left to right accumulating a run of counted positions, and flush the
run as a decimal number the moment a kept letter interrupts it. One pass per
mask, no recursion, no state between masks. Under this convention mask 0 is
the word itself and mask `2^n - 1` is the bare length, so the enumeration
reads `"word"` first and `"4"` last.

`n == 0` is not a special case anywhere in this arm: `1 << 0` is 1, the single
mask sweeps zero letters, and the output is one empty abbreviation — which is
right, since the empty word has exactly one.

**Recurse instead.** Same two-way choice per letter, made in a different
order: at each letter, branch on *count it* (the pending run grows, the string
does not) and *keep it* (flush the run as a number, then append the letter).
The recursion tree has `2^n` leaves and one abbreviation comes out of each.

The state that carries the work is `run` — counted letters since the last kept
one. It is the structural reason two numbers can never end up adjacent: a
second number cannot start until a kept letter has flushed the first. The ★
arm gets that same guarantee from run-length encoding; here it is a property
of the recursion rather than of the encoder. Both ends need care — a pending
run still has to be flushed at `i == n`, and `path` must be cloned for the
first branch because the second consumes it.

This arm emits `"4"` before `"word"`, exactly reversing the ★ arm's order.
Nothing about the problem fixes an order, and the differential compares the
arms as sorted multisets, which makes the disagreement useful: two arms that
agreed on order would probably be the same algorithm twice.

**Grow the answer.** The only inductive arm. It holds the complete answer for
`word[0..k]` and turns it into the answer for `word[0..k+1]` by extending every
entry both ways: append the letter, or bump the entry's trailing number (or
append a `"1"` if it does not end in one). Level 0 is the single empty
abbreviation, so the doubling is visible in the data structure instead of
argued about.

The second rule is why this arm is here. The other three carry the pending run
as an **integer** and format it once; this one has already committed the run to
text and has to go back into the string to change it — scan back over the
trailing digits, re-parse, increment, re-emit. That is a decimal carry
performed on a string: `"9"` becomes `"10"` and the entry gets one byte longer.
It is a completely different way to be wrong from the other arms, which is the
point. An off-by-one in a run length surfaces here as a parse or carry bug
rather than as a miscounted loop. (`"abcdefghijk"` is in the arm's demo set
precisely because 3 of its 2048 abbreviations reach a two-digit run.)

**Enumerate the runs.** This arm never asks the per-letter question at all. It
reads the statement literally and enumerates the replaced substrings: pick
where the next one starts, how long it is, then jump past the letter that has
to survive after it. "Non-adjacent" is enforced structurally rather than
checked — after a run covering `[a, a+len)` the arm recurses at `a + len + 1`,
having emitted the letter at `a + len` as kept, so the next run cannot begin
where this one ended.

Each abbreviation comes out exactly once because every abbreviation has a
unique decomposition into maximal runs. Getting `2^n` out of a recursion that
never mentions 2 is the interesting part: the count obeys
`f(m) = 1 + Σ f(m - a - len - 1)`, and none of the ★ arm's reasoning appears
anywhere in it. That independence is what makes this the arm worth disagreeing
with.

**It is also the one measurement in this kata I got backwards.** The arm
re-copies the kept prefix `word[p..a]` for every (start, length) pair it
considers, which reads like wasted work on top of an already redundant
enumeration, and I wrote it down as the slowest of the four before timing it.
It is the fastest — 251.5 ms against the ★ arm's 399.0 ms at `n = 20`, and the
same 1.6× at 16 and 18, so it is a constant and not a crossover waiting to
happen. The copying is done **once per node and inherited by that node's whole
subtree**, whereas the ★ arm rebuilds every entry from the empty string.
Sharing prefix work down a recursion tree beats not doing it, by more than the
copying costs. The backtracking arm, which shares in the same way, lands at the
same 251.0 ms — which is the confirmation that this is what the two of them
have in common and not a property of enumerating runs.

## Differential

There is no external oracle for this problem — the answer *is* the enumeration
— so the harness leans on properties that do not know how any arm works. Two of
them are complete on their own: **P4** pins the size of the answer and **P9**
pins its content, because "the recovered masks are a permutation of `0..2^n`"
says the set is exactly right without reference to how it was produced.

`karac run differential.kara` sweeps every word length 0–11 (three patterned
words — all one letter, strictly ascending, two-letter alternating — plus three
random ones per length), enumerating all four arms on each, and then pushes the
run census out to length 14 where full checking would be too slow.

```
cases 72 relabel-cases 54 entries 24570 census-cells 510
DIFFERENTIAL OK
```

| # | property |
|---|---|
| P1 | the backtracking arm agrees with the mask arm (as sorted multisets) |
| P2 | the growing arm agrees |
| P3 | the runs arm agrees |
| P4 | the answer has exactly `2^n` entries |
| P5 | every entry expands back to `word` |
| P6 | the entries are pairwise distinct |
| P7 | every number is `>= 1`, carries no leading zero, and fits the letters left |
| P8 | length identity: `\|entry\| == kept letters + Σ digits(run)` |
| P9 | the masks recovered from the entries are a permutation of `0..2^n` |
| P10 | prefix induction: dropping each entry's last unit maps `A(word[0..k])` onto `A(word[0..k-1])` exactly two-to-one |
| P11 | reversal symmetry: reversing every entry's *token* order in `A(reverse(word))` gives `A(word)` |
| P12 | relabelling the letters commutes with abbreviating — per arm |
| P13 | run census: entries with exactly `r` numbers match `Σ_s C(s-1, r-1) · C(n-s+1, r)` |

P9 and P13 are the two that watch the machine rather than the answer. P9
inverts every entry back to the choice that produced it, so an arm that emits
`2^n` strings which are not the *right* `2^n` is caught even though the count
is right. P13 counts the answer a second way — by run structure rather than by
letter choice: choose the total counted length `s`, split it into `r` runs
(`C(s-1, r-1)` compositions), and drop those runs into the `n-s+1` slots
between kept letters so no two touch (`C(n-s+1, r)`). For `n = 4` that reads
`1 + 10 + 5 = 16`, and an arm that loses one particular *shape* of
abbreviation while gaining another is caught by the census even when the total
still comes out at `2^n`.

P10 and P11 are the two that relate *different* invocations, which is weight no
single-run property can carry: a mutant that is wrong the same way on every
input still has to be wrong consistently under prefix-shortening and under
reversal to slip them.

**The sizing is set by the tree-walk interpreter, not by the JIT.** The repo's
A/B rule wants this harness byte-identical under `karac run`, `karac run
--interp` and both `karac build` modes, and the interpreter is roughly three
orders of magnitude slower. The first cut of this file swept to length 13 with
P12 on every case and ran for over ten minutes of interpreter CPU without
finishing; trimming to 11, capping P12 at 8 (it re-runs all four arms twice
more per case, and it is a property about a per-letter map, so short words
exercise it fully) and the census at 14 brings it to 0.9 s on the JIT and
2 m 08.6 s under `--interp`.

## Mutation testing

Seventeen content-anchored edits to `differential.kara`, each run through the
full sweep. HANG, PANIC and BUILD-FAIL count as kills alongside
`DIFFERENTIAL FAILED`.

| # | mutation | predicted | outcome | properties that fired |
|---|---|---|---|---|
| M1 | the ★ arm drops the trailing run flush | kill | **killed** | P1, P2, P3, P5, P9, P10, P11, P13 |
| M2 | the ★ arm's bit convention is inverted | *silent* | silent | — |
| M3 | the mask loop runs `mask <= limit` | kill | **killed** | P1, P2, P3, P4, P6, P9, P10, P13 |
| M4 | the backtracking arm drops the flush at the leaf | kill | **killed** | P1 |
| M5 | the "keep" branch forwards `run` instead of resetting it | kill | **killed** | P1 |
| M6 | `bump_tail` starts a fresh run at `"0"` | kill | **killed** | P2 |
| M7 | `bump_tail` re-emits the run without incrementing | kill | **killed** | P2 |
| M8 | the runs arm recurses at `a + len`, allowing adjacent runs | kill | **killed** | P3 |
| M9 | the runs arm's length loop stops at `a + len < n` | kill | **killed** | P3 |
| M10 | the runs arm stops emitting the separator letter | kill | **killed** | P3 |
| M11 | `to_mask`'s zero-value guard weakened to `value < 0` | *silent* | silent | — |
| M12 | the census closed form uses `C(n-s, r)` | kill | **killed** | P13 |
| M13 | `drop_last_unit` leaves a `"0"` behind | kill | **killed** | P10 |
| M14 | `reverse_tokens` reverses characters, not units | kill | **killed** | P11 |
| M15 | `canon` stops sorting | kill | **killed** | P1, P2, P3, P10, P11 |
| M16 | the ★ **and** backtracking arms both drop the flush | kill | **killed** | P5, P9 |
| M17 | every kept letter becomes the word's first letter | kill | **killed** | P1, P5, P9 |

**15 killed, 2 silent, both silents predicted.** The two that survive are
genuine equivalents rather than gaps. M2 inverts the ★ arm's bit convention so
that a *clear* bit means "counted"; complementation is a bijection on masks, so
the arm emits the same `2^n` strings in a different order, and the harness
compares sorted multisets. M11 weakens a guard in the harness's own decoder
that rejects a `"0"` in an abbreviation — no correct arm can produce one, so
nothing reaches it. Removing it would be wrong for the same reason it is
unkillable: it is there to stop a *future* mutant from decoding as valid.

**M16 is the mutant worth the table.** Breaking the ★ arm and the backtracking
arm in exactly the same way leaves P1 at zero, P4 at zero and P6 at zero — the
cross-arm agreement check sees two arms that agree, and the count is still
`2^n` with no duplicates. Only P5 and P9 fire. Cross-checking arms against each
other is not a substitute for pinning what the answer *is*, and M16 is the
demonstration rather than the assertion.

M4–M10 each fire only the one arm-comparison property, which reads like thin
coverage and is not: P5–P9 pin the ★ arm's output completely (P9 alone proves
the set is exactly right), and P1–P3 assert the other three arms equal that
output. The chain is complete — an arm-specific bug necessarily surfaces as a
disagreement with an output that is itself proven correct — and M16 is what
happens when a mutation attacks both links at once.

## Verification

All four arms plus the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build` — the full A/B set the repo requires.
`generalized_abbreviation.py` is byte-identical to the ★ arm's output.

The benchmark mirror is verified on JIT, AOT-sequential and AOT-auto-par and
against all four language twins — all seven print
`sink 650225651 chars 127975424`. It is not run under `--interp`: it is 8.4
million abbreviations, which the tree-walk backend would take hours to finish.
The kata's semantics are covered by the arms and the differential, which do run
on every backend.

## Benchmarks

`bench/generalized_abbreviation.kara` and its four mirrors run 8 passes, each
walking all `2^20` masks of a different 20-letter word and run-length encoding
every one of them into a reusable byte buffer — 8.4 million abbreviations,
128 million emitted characters — then folding those bytes into a rolling hash.

Two deliberate departures from the ★ arm keep the five mirrors measuring the
same thing. The abbreviations go into a fixed buffer rather than freshly
allocated strings, and the run length is emitted digit by digit rather than
through each language's integer formatter. Without those, the benchmark would
be comparing five allocator and stdlib policies instead of one mask walk. The
fold reads every emitted byte back, so no mirror can skip the encoding, and the
word changes each pass so the answer moves rather than being one constant. A
run can be at most 20 letters long here, so two digits always suffice.

30 runs each, 5 warmups, on a 4-core x86-64 Linux container. Python is its own
lane at 3 runs.

| implementation | mean | vs fastest |
|---|---|---|
| c `clang -O3` | 928.3 ms ± 11.2 | 1.00× |
| c `-march=x86-64-v3` (matched-ISA) | 931.6 ms ± 10.3 | 1.00× |
| go `go build` | 1025 ms ± 9 | 1.10× |
| rust `-O` | 1033 ms ± 8 | 1.11× |
| rust `-O -C overflow-checks=on` (equal-safety) | 1065 ms ± 12 | 1.15× |
| rust `-C target-cpu=x86-64-v3` + overflow-checks (matched) | 1071 ms ± 19 | 1.15× |
| **kāra `karac build`** | **1086 ms ± 15** | **1.17×** |
| python 3.11 | 35472 ms ± 238 | 38.2× |

Kāra is last among the compiled legs, by 1.7% over the nearest Rust leg and
17% over clang — a real gap, but one where the whole compiled field is inside
17% of itself, so it separates the backends less than kata 319's cache-bound
simulation did. Two comparisons that usually carry weight are non-events here,
and saying so is more useful than quoting them:

- **Equal-safety costs Rust about 3%.** `rustc -O -C overflow-checks=on` came
  in at 1065 ms against plain `-O`'s 1033 ms, which is 2.7σ and therefore
  real, if small. That is the closest thing this kata has to a measurement of
  what Kāra's default-checked arithmetic buys: the inner loop's arithmetic is
  a handful of increments and one `acc * 131 + byte` per emitted character, so
  there is something to check but not much.
- **`-march=x86-64-v3` does nothing.** 931.6 ms against 928.3 ms for C, well
  inside 1σ. A mask walk with a data-dependent branch per letter and a
  variable-length inner fold has nothing to vectorise, and the Rust matched
  leg says the same (1071 vs 1065 ms).

Python is 38× the compiled field rather than the 66× kata 319 measured, which
is the same story from the other side: this workload's inner loop is short
integer arithmetic over small values, which is the case CPython handles least
badly.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 108.8 ms ± 1.9 | 15.7 KiB | 1.5 MiB |
| rust | 149.8 ms ± 3.4 | 3865.2 KiB | 2.0 MiB |
| kāra | 390.0 ms ± 15.7 | 341.6 KiB | 2.4 MiB |
| go | — | 2178.6 KiB | 1.8 MiB |
| python | — | — | 7.7 MiB |

`karac build` is 3.6× clang's cold compile and 2.6× rustc's; its binary is 22×
clang's and 11× smaller than rustc's. Every leg's resident set is small — the
workload allocates one 28-byte buffer and holds no output — so the RSS column
is measuring runtime overhead rather than the program. Raw numbers in
`bench/results.container-x86.json`; methodology and caveats in
[`BENCHMARKS.md`](../../../BENCHMARKS.md).

## Compiler findings

**None filed.** Across five `.kara` files the only diagnostics were six
`E0219`s and `karac fix` applied all six. They are the *converse* of the
call-site `mut` marker Kāra normally asks new authors for: inside the three
recursive helpers the accumulator parameter is already `mut ref`, so forwarding
it to the recursive call needs no marker, and writing one is an error rather
than harmless noise. Every one was in a self-recursive call — which is exactly
where the habit of marking every mutable argument survives longest, because the
callee and the caller are the same signature. No workarounds, no contorted
phrasing, no `KARAC_AUTO_PAR=0`-only pass.

One near-miss is worth recording because it looked like a gap and was not:
naming a local `distinct` produced five parse errors, because `distinct` is a
Kāra keyword (distinct types / newtypes, design.md § Distinct Types). The
diagnostic named the keyword, pointed at each use, and offered `r#distinct` —
correct and actionable. The local is now called `sorted_entries`.
