# 575. Distribute Candies

Alice has `n` candies, where the `i`-th candy is of type `candyType[i]`.
Alice noticed that she started to gain weight, so she visited a doctor.
The doctor advised Alice to only eat `n / 2` of the candies she has (`n`
is always even). Alice likes her candies very much, and she wants to eat
the maximum number of different types of candies while still following
the doctor's advice. Given the integer array `candyType` of length `n`,
return the maximum number of different types of candies she can eat if
she only eats `n / 2` of them.

```
candyType = [1,1,2,2,3,3]  ->  3   (one of each type)
candyType = [1,1,2,3]      ->  2   (two types of the three)
candyType = [6,6,6,6]      ->  1
```

**Constraints:** `n == candyType.length`; `2 <= n <= 10^4`; `n` is even;
`-10^5 <= candyType[i] <= 10^5`.

## Approaches

Every arm is `fn distribute_candies(candy_type: Vec[i64]) -> i64`. Alice
can eat no more types than there are and no more than `n / 2`, and she
can always eat the smaller of the two, one candy of each type she picks
and the rest of her `n / 2` from any type.

| file | mechanism |
|---|---|
| `distribute_candies.kara` ★ | the types gathered in a `Set[i64]`, its size against `n / 2`; O(n) |
| `distribute_candies_sorted.kara` | a sorted copy, the types counted as the places where a value differs from the one before it, plus one; O(n log n) |
| `distribute_candies_seen.kara` | a table of 200,001 flags, one for each possible type, the walk stopping as soon as `n / 2` types have turned up; O(n) |
| `distribute_candies_chain.kara` | the types collected into a set by `candy_type.iter().cloned().collect()`; O(n) |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 14 lines: ten lists at the edges (the three
examples, two candies alike and not, every candy its own type, the two
ends of the range, one stray candy, and as many types as `n / 2` and one
more), a total and checksum over 300 random lists of 2 to 40 candies
over 1 to 30 types spread over the whole range, and the problem's
largest, 10,000 candies all different, of 4,999 types, and of two.
`distribute_candies.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: every choice of `n / 2` of the candies,
the types in each counted, the most taken. Each arm is held to the
properties below on 1,000 random lists of 2 to 10 candies over 1 to
6 types between -10 and 10, with the ends of the range among them now
and then.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | at least 1, at most `n / 2`, at most the number of types |
| P3 | the candies in another order change nothing |
| P4 | renaming the types, each to a type of its own, changes nothing |
| P5 | two candies of a new type add exactly one |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `n / 2` left out | P1 253, P2 253 |
| M2 | ★: each type halved, so neighbours merge | P1 43, P4 10 |
| M3 | sorted: the copy not sorted | P1 296, P2 296, P3 25, P5 163 |
| M4 | sorted: the count started at 0 | P1 747, P2 227 |
| M5 | seen: the walk stopped one type late | P1 253, P2 253 |
| M6 | seen: a type and its negative share a flag | P1 85 |
| M7 | chain: the larger of the two taken | P1 706, P2 706 |
| M8 | chain: the first candy left out | P1 50, P3 77, P5 12 |
| E1 | ★: `n / 2` rounded up | 0 |
| E2 | sorted: neighbours compared with `>` | 0 |
| E3 | seen: the stop tested with `>=` | 0 |
| E4 | chain: the copy made by `map` | 0 |

M1 and M5 fail on the same 253 cases, those with more types than `n /
2`: M1 answers every type there, and M5 one more than `n / 2`. P5 sees
neither, since two candies of a new type raise their wrong answers by
one as well. M3 counts the runs of the unsorted list, more than the
types whenever a type comes back after another, so its answer also moves
when the order does or the two new candies split a run. M4 is one short
everywhere; P2 sees it only on lists of one type, where it answers zero.
M6 merges a type with its negative, so P4, which renames each type to
its negative, is blind to it, and only P1 sees it. M2's halving merges a
type with its neighbour, which P4's renaming of 0 to 99,999 pulls apart
ten times. M8 drops a candy, so the answer depends on which candy comes
first, and P3 and P5 see that. E1 is safe because `n` is even,
E2 because the copy is sorted, and E3 because the count rises by one
from 0 and `n / 2` is at least 1, so it meets `n / 2` before passing it.

## Verification

The four arms print the same output as `distribute_candies.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends: the sorted arm prints the right output under
`karac run --interp`, `karac run` and `karac build`, and under
`KARAC_AUTO_PAR=1 karac build`. The ★ and seen arms, the differential
and the bench program stop at type checking on `*c`: legacy gives the
elements of `iter()` as `i64` where v2 gives references ("unary '*'
requires 'ref T' ... found 'i64'"). The chain arm fails at run time
under `karac run --interp` ("method 'cloned' not found on type
'unknown'") and in code generation under `karac run` and `karac build`
("no handler for method 'collect' on non-identifier receiver"). Legacy
is frozen, so these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 100 cases once, each of
10,000 candies (the problem's most) drawn from a pool of 1 to
10,000 types spread over the whole range; then 200 times over every case
is answered. Every implementation prints `100 cases of 10000 candies,
200 rounds: 68130400 types eaten, checksum 386012632`, the Kāra program
under `karac __mir-run` included (343 s).

Each call makes a fresh hash set, as the Kāra arm makes a fresh
`Set[i64]`: a `HashSet<i64>` with the default hasher in Rust, a map with
no size hint in Go, and a `set` in Python. C has no hash set, so each
call `malloc`s an open-addressing table of 16,384 slots, hashes by a
64-bit multiply and frees the table. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.42 to 1.50 s |
| Rust (`rustc -O`) | 4.84 to 4.95 s |
| Rust (`rustc -O -C overflow-checks=on`) | 4.58 to 4.98 s |
| Go | 6.76 to 7.40 s |
| Python | 11.2 to 11.5 s |
| Kāra (`karac build --mir`) | 6.90 to 7.18 s |

The legacy `karac build` refuses this program on the same `*c`. So
`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`680733538b`. Under `karac __mir-llvm-run` the program prints the same
line in 59 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 1.45 times Rust's, level with Go's, and about five
times C's, whose table is sized once and hashed by one multiply. Where
the gap to Rust comes from is not measured.

## Compiler findings

None. The chain arm first called `.copied()`, which `karac check`
refused ("no method 'copied' on type 'Iterator'"); the standard library
defines `cloned` on iterators and not `copied`, and the spec does not
name `copied`, so that is not a bug, and the arm uses `cloned`. The
legacy failures above are not filed because legacy is frozen.
