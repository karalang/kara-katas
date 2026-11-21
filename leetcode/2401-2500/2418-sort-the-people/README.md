# 2418. Sort the People

You are given an array of strings `names`, and an array `heights` that
consists of **distinct** positive integers. Both arrays are of length
`n`.

For each index `i`, `names[i]` and `heights[i]` denote the name and
height of the `i`th person.

Return `names` *sorted in **descending** order by the people's
heights*.

```
names = ["Mary","John","Emma"], heights = [180,165,170]   ->  ["Mary","Emma","John"]
names = ["Alice","Bob","Bob"],  heights = [155,185,150]   ->  ["Bob","Alice","Bob"]
```

**Constraints:** `n == names.length == heights.length`;
`1 <= n <= 10^3`; `1 <= names[i].length <= 20`;
`1 <= heights[i] <= 10^5`; `names[i]` consists of lower and upper case
English letters; all the values of `heights` are distinct.

The heights are distinct, so the order is fixed by them alone: two
people never tie, and a name that repeats, as Bob does, is placed by
its own height each time.

## Approaches

| file | mechanism |
|---|---|
| `people.kara` ★ | an index sort: the indexes `0..n` sorted by `sort_by` on the heights, tallest first, and each index's name read out in that order. O(n log n) |
| `people_count.kara` | counting: a table over every height up to the tallest holds the index of the person of that height, or -1, and is walked down from the tallest. O(n + the tallest height) |
| `people_map.kara` | a `SortedMap` from height to name, walked in ascending order and the names collected reversed. O(n log n) |
| `people_pairs.kara` | pairs: each person a `(height, name)` tuple, the tuples sorted, which orders them by height since the heights are distinct, and read backwards. O(n log n) |
| `people_iter.kara` | iterators: the heights and names paired by `zip`, `collect`ed and sorted by `sort_by_key` on the negated height, the names read out by `map`. O(n log n) |
| `people_solution.kara` | LeetCode's Rust template: `Vec<usize>` indexes sorted by `sort_unstable_by(\|&a, &b\| heights[b].cmp(&heights[a]))` and the names cloned out by `into_iter().map(..).collect()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one person;
heights already falling, and rising; a random group of the constraints'
largest, 1000 people with names of up to 20 letters and heights up to
`10^5`, by a digest of the answer; then 2000 random groups of 1 to 10
people, names of up to 3 letters drawn from `a`, `b`, `A` and `B`,
heights up to 1 to 30, with a checksum of the digests. `people.py`
mirrors the ★ arm and its output is byte-identical, and the mirror was
checked on 20000 random groups of up to 7 people against the one
ordering, among all of theirs, whose heights fall at every step.

`check` first reports 8 errors on the template, and `karac fix` carries
it in one call, reporting 14 edits: each `Vec<..>` given brackets; the
`&` of both closure patterns and of `&heights[a]` dropped; `usize`
written `i64`; `sort_unstable_by` written `sort_by`, Kāra's one
comparator sort; and `struct Solution;` given its braces. The template
takes LeetCode's `Vec<i32>` heights, so its harness entry converts the
shared `i64` ones.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the tallest person not yet placed is found by a scan of
everyone, placed next and marked, until everyone is placed. No sort. It
checks 300 random groups of 1 to 10 people, heights up to 30; then 30
of up to 1000 people, heights up to `10^5`; then 30 of up to 1000
people whose heights are 1 to n. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer holds the same names, sorted, as the input |
| P3 | the people given in reverse order: the same answer |
| P4 | every height doubled: the same answer |
| P5 | the tallest person left out: the answer without its first name |
| P6 | each arm agrees with at least three of the other five |

P2 holds because the answer only reorders the names, P3 because the
order depends on the heights alone, which are distinct, P4 because
doubling keeps every comparison, and P5 because the tallest comes first
and leaving them out moves no one else.

The differential prints `360 cases: checksum 358715131, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and places the people by the same scan. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: heights compared halved | P1 160, P3 226, P4 160, P5 38, P6 160 |
| M5 | ★: the first and last swapped after | P1 323, P5 332, P6 323 |
| M6 | ★: at most five names | P1 215, P2 215, P6 215 |
| M7 | pairs: the pairs never sorted | P1 312, P3 332, P5 268, P6 312 |
| M10 | pairs: sorted by the last digit | P1 238, P4 288, P5 218, P6 238 |
| M11 | pairs: every other pair read | P1 332, P2 332, P6 332 |
| M12 | map: heights keyed halved | P1 227, P2 227, P3 226, P4 227, P6 227 |
| M15 | map: every name read twice | P1 360, P2 360, P6 360 |
| M16 | map: every height given the first name | P1 332, P2 332, P3 324, P5 58, P6 332 |
| M17 | count: a height of 1 never read | P1 158, P2 158, P4 158, P6 158 |
| M20 | count: the first person taken for none | P1 360, P2 360, P3 331, P6 360 |
| M21 | count: an empty height holding the first person | P1 302, P2 302, P3 273, P4 360, P6 302 |
| M22 | iter: sorted by the height modulo 7 | P1 280, P3 227, P4 280, P5 253, P6 280 |
| M23 | iter: each height raised by its name length | P1 205, P3 203, P4 178, P5 56, P6 205 |
| M24 | iter: the shortest third left out | P1 299, P2 299, P6 299 |
| M29 | solution: heights compared modulo 50 | P1 59, P3 59, P4 79, P5 57, P6 59 |
| M30 | solution: heights handed over modulo 100 | P1 58, P3 58, P4 59, P5 58, P6 58 |

P1 and P6 kill all seventeen, P3 ten, and P2, P4 and P5 nine each. P2
asks only that the answer hold the input's names, so it misses every
mutant that keeps the names and orders them wrongly; P4 doubles the
heights, which a mutant that compares them wrongly in a way doubling
keeps (the first and last swapped, the pairs never sorted) passes; P3
and P5 miss the mutants whose error does not depend on the input's
order or on its tallest person.

Of the thirty-one, fourteen were not kept. Seven fail the same checks
as a kept one: the tallest left out in the ★ and pairs arms, the
shortest left out, and the count arm's walk starting below the tallest
(M2, M8, M9, M19) as every name read twice (M15), since each answer
then holds the wrong number of names; the first person left out (M14)
as the first person taken for none (M20); every height holding the
first person (M18) as every height given the first name (M16); and the
template's only the shorter half read (M31) as every other pair read
(M11). Seven fail apart from every kept one and were left out because
those arms keep their share already: the ★ arm's shortest first (M1)
and name read from the mirror index (M3); the map arm's at most eight
names (M13); the iter arm's names paired backwards (M25), which fails
as M3 does, and shortest names first (M26); and the template's only
the first half sorted (M27) and name read one along (M28).

## Verification

Every arm prints the same output as `people.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.4 to 0.8 s. The differential
takes 22 s there, 4.5 s under `karac __mir-llvm-asan` and 1.1 s under
`karac run`.

## Benchmarks

The bench builds 10 groups of 1000 people, names of 1 to 20 lower case
letters and distinct heights up to `10^5`, once from its own generator,
then makes 500 passes, sorting every group and folding the first letter
of every name in the answer, plus the pass, into the checksum, with the
★ arm in all five languages. Every implementation prints `500 passes
over 10 groups of 1000 people: checksum 649655561`. Each sorts the
indexes by a stable sort and copies the names out: Kāra's and Rust's
`sort_by`, Go's `sort.SliceStable` and a merge sort in C, each name
cloned (`strdup` in C, `strings.Clone` in Go).

BENCHTAB
