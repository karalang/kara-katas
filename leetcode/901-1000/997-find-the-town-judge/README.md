# 997. Find the Town Judge

In a town, there are `n` people labeled from `1` to `n`. There is a
rumor that one of these people is secretly the town judge.

If the town judge exists, then:

1. The town judge trusts nobody.
2. Everybody (except for the town judge) trusts the town judge.
3. There is exactly one person that satisfies properties **1** and
   **2**.

You are given an array `trust` where `trust[i] = [ai, bi]` representing
that the person labeled `ai` trusts the person labeled `bi`. If a trust
relationship does not exist in `trust` array, then such a trust
relationship does not exist.

Return *the label of the town judge if the town judge exists and can be
identified, or return* `-1` *otherwise*.

```
n = 2, trust = [[1,2]]              ->  2
n = 3, trust = [[1,3],[2,3]]        ->  3
n = 3, trust = [[1,3],[2,3],[3,1]]  ->  -1
```

**Constraints:** `1 <= n <= 1000`; `0 <= trust.length <= 10^4`;
`trust[i].length == 2`; all the pairs of `trust` are unique;
`ai != bi`; `1 <= ai, bi <= n`.

## Approaches

The judge is trusted by all `n - 1` others and trusts nobody, and two
people cannot both be: each would have to trust the other. Three arms
count, for every person, how often they trust and are trusted; two ask
the trusts themselves, one in a table and one in a set.

| file | mechanism |
|---|---|
| `find_judge.kara` ★ | one score per person: each trust adds 1 to the person trusted and takes 1 off the person trusting, and only the judge can reach `n - 1`. O(n + m) |
| `find_judge_degrees.kara` | two counts per person, how many they trust and how many trust them; the judge trusts 0 and is trusted by `n - 1`. O(n + m) |
| `find_judge_matrix.kara` | an `n` by `n` table of booleans holds every trust; a person is the judge when, against every other person, their own row says no and the other's says yes. O(n² + m) |
| `find_judge_celebrity.kara` | one candidate, then a check: the trusts go into a `Set` keyed `a(n + 1) + b`, a walk over the people passes the candidacy to whoever the candidate trusts, and a pass over everyone else confirms or refuses the one left. O(n + m) |
| `find_judge_sorted.kara` | runs in sorted lists: with the trusted sorted, each person's trusters form a run, a run of `n - 1` names the only possible judge, and a binary search in the sorted trusting makes sure they trust nobody. O(m log m) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 18 lines. The first ten are LeetCode's three
examples and seven more: one person and no trust, whose answer is 1;
two people and no trust; two who trust each other; a judge among four
who are also trusted by someone else; a chain of trust; a person
trusted by two of three others; and a judge whose trusters also trust
each other. Then five towns of LeetCode's largest size, 1,000 people:
all trusting person 500; the same with 500 trusting person 1; no trust
at all; all but person 1,000 trusting 500; and a ring of trust. Then
totals over random towns: 300 of up to 4 people, 3,000 of up to 30 and
300 of up to 1,000; half of them with a judge whom everyone else
trusts, a third of those spoiled by one trust taken away or one trust
from the judge, other trusts at random, all in random order.
`find_judge.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: a person is the judge when they trust nobody and
everybody else trusts them, each asked of the list of trusts in turn,
and the answer is that person when exactly one person is, -1
otherwise. It checks 3,200 random towns, made as the arms' random
towns are: 3,000 of up to 8 people against the statement, and 200 of
up to 100 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 towns |
| P2 | the trusts in another order give the same answer |
| P3 | everyone relabelled by a random permutation gives the judge's new label, or -1 again |
| P4 | a judge given one trust of their own is no judge |
| P5 | a trust taken away whose trusted person is not the judge leaves the judge as they were |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 towns of 23632 people: 1500 judges, checksum
842312323, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (6.7 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-seven edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: trusting someone not scored | P1 371, P3 97, P4 1455, P6 400 |
| M2 | ★: a score of `n - 2` enough | P1 671, P3 116, P4 1393, P5 4, P6 700 |
| M3 | ★: person `n` never looked at | P1 659, P3 364, P6 660 |
| M4 | degrees: the truster counted as trusted | P1 1039, P6 1100 |
| M5 | degrees: trusting one person allowed | P1 359, P3 71, P4 1066, P5 5, P6 382 |
| M6 | degrees: person 0 looked at | P1 377, P3 378, P6 378 |
| M7 | matrix: each person tested against themselves | P1 1421, P6 1482 |
| M8 | matrix: every trust stored the wrong way round | P1 1066, P4 314, P5 165, P6 1148 |
| M9 | matrix: person `n` never asked about | P1 459, P3 402, P4 599, P5 7, P6 461 |
| M10 | celebrity: the candidate's own trust not checked | P1 253, P3 209, P4 852, P6 270 |
| M11 | celebrity: being trusted by all not checked | P1 1042, P3 705, P4 553, P5 15, P6 1088 |
| M12 | celebrity: the walk starts at person 3 | P1 244, P3 355, P6 247 |
| M13 | sorted: one person alone not the judge | P1 377, P6 378 |
| M14 | sorted: a run of `n - 2` enough | P1 331, P3 108, P4 14, P6 356 |
| M15 | sorted: the search finds the first after | P1 371, P3 100, P4 1455, P6 400 |

P1 and P6 kill all fifteen, P3 eleven, P4 nine, P5 five and P2 none.
Every arm reads the trusts as a collection, a count, a table, a set or
a sorted list, so their order never shows; the one edit P2 saw was
sorted's binary search on a list left unsorted, beyond three. P3, P4
and P5 hold an arm to its own answers, and P4 and P5 only where it
names a judge, so they cannot see the mutants that answer -1 where
there is a judge: M4, whose counts of the trusted are the counts of
trusting and so never reach `n - 1` for a person who trusts nobody,
unless `n` is 1; M7, which refuses everyone; and M13, which refuses
the only person of a town of one. M6 refuses that person too but
answers 0, which P3 does not take for -1. P4 sees the nine mutants
that still name a judge given a trust of their own. P5 sees M2, M5, M9
and M11, which can name someone short of the rule, and then someone
else once a trust between two others goes; and M8, whose judge is the
one who trusts everybody, unseated when one of those trusts goes. The
checks draw random
numbers only where an arm names a judge, so a mutant's later towns are
not the right arms' towns, and counts from two mutants do not add up.

Twelve other edits were tried and set aside. Six failed exactly the
same checks as a kept one: degrees not asking what a person trusts,
and matrix not asking the judge's own row, as M1; degrees counting the
trusted as trusting, matrix reading the other's trust the wrong way
round and celebrity passing the candidacy on to whoever trusts the
candidate, which all refuse every town of two or more, as M4; and
sorted not checking the judge's own trust, as M15. Five were sound but
beyond three an arm: ★ never naming person 1, and answering 0 for no
judge; matrix never naming person 1; celebrity keying its pairs
`an + b`, where two pairs can share a key; and sorted not sorting the
trusting. One survived and is equivalent: matrix without its early
stop, which only goes on asking once the person is refused. None
crashed.

## Verification

Every arm prints the same output as `find_judge.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 12.3 s (degrees) to 21.5 s
(sorted, which copies and sorts two lists for every town), and the
differential 6.7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
towns of LeetCode's largest size, 1,000 people and 10,000 different
trusts, once: in the even ones 999 of the trusts are everyone else
trusting a judge, and the rest are at random. In each of 1,000 rounds
it runs the arm on every town, each round starting from a different
one, and folds every answer into a checksum. Every implementation
prints `1000 rounds over 20 towns of 1000 people: 10000 judges,
checksum 561483662`. Each call fills a fresh list of 1,001 scores from
the 10,000 trusts and walks it; the trusts are a list of two-element
lists, as LeetCode gives them, and C's are `int64_t` rows.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.363 to 0.485 s | 0.389 s |
| Rust (`rustc -O`) | 0.521 to 0.601 s | 0.559 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.527 to 0.616 s | 0.563 s |
| Go | 0.520 to 0.599 s | 0.554 s |
| Python | 21.9 s | |
| Kāra (`karac build --mir`) | 0.469 to 0.665 s | 0.552 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 40 times
Kāra's.

v2 took 0.98 times Rust's median time under overflow checks and 1.42
times C's. Under valgrind's cachegrind v2 ran 5,739 million
instructions and 1,637 million branches with 0.15 million
mispredicted, Rust with overflow checks 5,149 million, 1,638 million
and 0.23 million, and C 1,589 million, 319 million and 0.09 million.
In `main`, where the calls are inlined, v2 and Rust both take 1,418
million branches for the 200 million trusts the calls read, about
seven a trust, which fits a loop test, a bounds check on each of the
four reads and an overflow check on each of the two sums (inferred);
C's `main` takes 118 million.
