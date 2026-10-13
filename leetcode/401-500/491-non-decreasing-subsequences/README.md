# 491. Non-decreasing Subsequences

Given an integer array `nums`, return all the different possible
non-decreasing subsequences of the given array with at least two
elements. You may return the answer in any order.

```
nums = [4,6,7,7]   ->  [[4,6],[4,6,7],[4,6,7,7],[4,7],[4,7,7],[6,7],[6,7,7],[7,7]]
nums = [4,4,3,2,1] ->  [[4,4]]
```

**Constraints:** `1 <= nums.length <= 15`; `-100 <= nums[i] <= 100`.

## Approaches

Every arm is `fn find_subsequences(nums: Vec[i64]) -> Vec[Vec[i64]]`,
in whatever order the arm finds them; the harness sorts the answer
before printing it.

| file | mechanism |
|---|---|
| `non_decreasing_subsequences.kara` ★ | backtracking: grow a subsequence one later, no smaller number at a time and record it from two numbers on; at each depth a value is tried at most once (a `Set` of the values tried there), which is what keeps equal subsequences from being found twice |
| `non_decreasing_subsequences_masks.kara` | every subset of indices: the 2^n subsets each pick a subsequence; keep those of two or more numbers that never decrease, in a `Set[Vec[i64]]`, then move them out with `found.into_iter()` |
| `non_decreasing_subsequences_grow.kara` | growing them all at once: keep every distinct subsequence so far, one number long included; each number extends those ending no higher and starts one of its own, and a `Set[Vec[i64]]` drops repeats |
| `non_decreasing_subsequences_since.kara` | the same growth with no set of subsequences: a number seen before only extends the subsequences made since its last turn (the older ones it extended then) and does not start another; a map from value to where its last turn began is the only bookkeeping |
| `differential.kara` | the four arms on 1,500 random arrays, five properties |

Every arm prints the same 8 lines: the two LeetCode examples, one
number, all equal, falling, negatives, rising, and for 300 random
arrays (1 to 12 numbers from -3 to 3) how many subsequences there were
and a checksum over them in sorted order. `non_decreasing_subsequences.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random arrays of 1 to 10 numbers, from -1 to 1, -3 to 3 or -20
to 20 in turn. The reference takes or leaves each number in turn,
taking it only when it is no smaller than the last one taken, then
sorts what it finds and keeps each subsequence once.

| | property |
|---|---|
| P1 | the answers, sorted, are the reference's |
| P2 | each answer has two or more numbers, never decreases and is a subsequence of the array |
| P3 | no answer is given twice |
| P4 | a number above all the others, appended, gives twice as many answers plus one for each distinct value |
| P5 | the array reversed and negated has as many answers |

P4 holds because the new number ends a copy of every old answer and
also follows each distinct value on its own. P5 holds because reversing
a non-decreasing subsequence and negating it gives a non-decreasing
subsequence of the turned array, one for one.

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run` in 7 s, and a count for each property when anything
fails. Until kara B-2026-10-13-14 was fixed the v2 backends refused
the whole program as written, at the masks arm's `found.into_iter()`
(see Compiler findings); the mutants below were run then, on a copy
whose masks arm takes `for s in found` and pushes `s.clone()`.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run` on the copy described under Differential. All eight
are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value tried at one depth is not recorded | P1 778, P3 778, P4 904 |
| M2 | ★: equal numbers do not follow each other | P1 904 |
| M3 | masks: equal neighbours count as a fall | P1 904 |
| M4 | masks: one number is enough | P1 1500, P2 1500, P4 1301 |
| M5 | grow: a number only extends ones ending below it | P1 904 |
| M6 | grow: a longer one is kept even when seen before | P1 664, P3 664, P5 674 |
| M7 | since: a value's turn is marked from its end, not its start | P1 904 |
| M8 | since: a value seen before starts another of its own | P1 679, P3 679, P4 904, P5 676 |

M2, M3, M5 and M7 each lose exactly the subsequences that repeat a
value, and every property but P1 is blind to that: they still give
well-formed answers, once each, and P4 and P5 hold among the answers
that remain. Only the comparison with the reference sees them, in the
904 arrays that hold a repeated value.

## Verification

The ★, grow and since arms print the same output as
`non_decreasing_subsequences.py` under `karac __mir-run` (the v2 MIR
interpreter) and `karac __mir-llvm-run`, and run clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output
identical, no error, no leak. `karac check` passes on every file, the
bench program included.

The masks arm and the differential were rechecked as written at kara
`df61cbfff6`, after the fix for B-2026-10-13-14 (see Compiler
findings): the masks arm matches the mirror on `__mir-run`,
`__mir-llvm-run` and `__mir-llvm-asan`, and the differential prints
`30000 checks, 0 failures` on the first two and runs clean under the
third. Before the fix both were refused at build, at `for s in
found.into_iter()`, and were verified on a copy that wrote the loop
as `for s in found { out.push(s.clone()); }`.

The frozen legacy backends agree on the ★, grow and since arms: `karac
run --interp`, LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1`
build print the same output. Legacy `karac build` warns that `nums` is
"moved here, used again here", where `show` lends it twice and legacy
reads the first as a move; the output is right all the same. On the
masks arm `karac run --interp` is right, but LLJIT and legacy `karac
build` abort with `free(): double free detected in tcache 2`. The
differential does not type-check on legacy, which reads the items of
`nums.iter()` as `i64` and refuses `*x`. Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 3,000 arrays of 15
numbers (the problem's most), the k-th from k / 2 to k / 2 + 3 so that
they mostly rise and give many answers, once, then solves each once.
Every implementation prints `3000 arrays of 15: 3526131 subsequences,
checksum 442914400`, the Kāra program under `karac __mir-run` included
(in 26 s). The checksum runs over the answers in the order the search
finds them, so every mirror searches in the same order.

Rust keeps the values tried at each depth in a `HashSet`, Go in a
`map[int64]bool` and Python in a `set`; C has no hash set, so it keeps
them (at most 15) in an array and scans it, and puts every answer into
one growing buffer of numbers with the lengths alongside. Spot timings
on a shared 4-core container, three runs each (two for Python;
`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.21 to 0.23 s |
| Rust (`rustc -O`) | 0.59 to 0.69 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.50 to 0.59 s |
| Go | 0.57 to 0.62 s |
| Python | 3.8 to 5.5 s |
| Kāra (`karac build`) | 0.64 to 0.73 s |
| Kāra (`karac build --mir`) | 0.73 to 0.85 s |

The legacy `karac build` builds and runs this program correctly, so
`bench.sh` is the `scripts/new-bench.sh` output unchanged and times
that build. The `--mir` row is the v2 compiled backend, timed for
comparison. Both Kāra rows are timed at kara `d9a7136c58`. Under
`karac __mir-llvm-run` the program prints the same line in 4.9 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

- **B-2026-10-13-14** (fixed in kara `4e8c04ce62`): the MIR builder
  refused `for x in c.into_iter()` over a `Set`, `VecDeque`, `Map` or
  `SortedMap` whose elements are not `Copy`, at "a `for` loop over a
  collection is not lowered yet", though `karac check` accepted it and
  the diagnostic for moving out of a bare `for` recommended that very
  spelling. Found here in the masks arm, which moves its
  `Set[Vec[i64]]` out at the end.

`karac fix` answers the bare `for s in found { out.push(s); }` with
`out.push(s.clone())`, a copy per answer, rather than `.into_iter()`;
it prefers `.clone()` whenever the type has one. Not filed: the copy is
correct, and which fix to prefer is a design choice.
