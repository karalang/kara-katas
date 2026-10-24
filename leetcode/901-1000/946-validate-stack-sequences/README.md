# 946. Validate Stack Sequences

Given two integer arrays `pushed` and `popped` each with distinct values,
return `true` *if this could have been the result of a sequence of push
and pop operations on an initially empty stack, or* `false` *otherwise.*

```
pushed = [1,2,3,4,5], popped = [4,5,3,2,1]  ->  true
pushed = [1,2,3,4,5], popped = [4,3,5,1,2]  ->  false
```

**Constraints:** `1 <= pushed.length <= 1000`; `0 <= pushed[i] <= 1000`;
all the elements of `pushed` are unique; `popped.length ==
pushed.length`; `popped` is a permutation of `pushed`.

## Approaches

| file | mechanism |
|---|---|
| `validate_stack_sequences.kara` ★ | the stack replayed: the values pushed in order, and after each push popped for as long as the top is the next value to pop. Popping whenever it can is never wrong, since a value on top that is due now would be buried by the next push. The sequences fit when every value has been popped. O(n) |
| `validate_stack_sequences_drive.kara` | driven by the pops: each value to pop is either on top of the stack now, or not yet pushed, and then the values before it are pushed and it is pushed and popped at once; a value already pushed but not on top is buried, and the answer is no. O(n) |
| `validate_stack_sequences_inplace.kara` | the replay with the stack written over a copy of the pushed values: the stack never holds more values than have been read, so its top stays at or below the read position. O(n), no second array but the copy |
| `validate_stack_sequences_links.kara` | each value numbered by the place it was pushed, the highest place pushed so far kept, and the places still on the stack linked each to the one below it. A pop above the highest pushes every place up to it; a pop at or below it must be the top. A popped place is unlinked by pointing past it. O(n) |
| `validate_stack_sequences_pattern.kara` | a forbidden pattern: with each pop written as its place, everything pushed before a popped place and still on the stack lies under it, so the later pops of earlier places must fall, in the reverse of their pushing order. The sequences fit exactly when no place is followed by a lower place and then a place between the two. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and six more
(one value, two values popped in either order, three values with the
first popped last, three with the last popped first and then the first,
and two pairs each popped in reverse); for 300 random cases of 1 to 12
values, 1,906 values in all, half popped by a random run of pushes and
pops and half in a random order, how many fit and a checksum; and five
cases of LeetCode's longest sequences, 1,000 values: popped by a random
run, the same with two pops swapped, popped in reverse, popped as pushed,
and popped in a random order. `validate_stack_sequences.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every sequence of push and pop operations on an initially
empty stack, a push taking the next value of `pushed` and a pop the top
of the stack, run until every value has been pushed and popped, and how
many of them pop the values in the order of `popped`. It checks 3,200
random cases, 3,000 of 1 to 7 values against the statement and 200 of up
to 999 values against the other properties, 118,752 values in all; a
third of the cases are popped by a random run of pushes and pops, a
third by the same with two neighbouring pops swapped, and a third in a
random order. 2,417 fit.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the operations run backwards, every push a pop and every pop a push: `popped` reversed pushed and `pushed` reversed popped give the same answer |
| P3 | every value renamed gives the same answer |
| P4 | followed by a second case of other values, the answer is yes exactly when it is yes for both |
| P5 | when the answer is yes, still yes with one value taken out of both |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 118752 values, 2417 fit, checksum 826249805,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (33 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pops read from the end | P1 893, P2 805, P4 673, P6 992 |
| M2 | ★: pops only after an even value is pushed | P1 1707, P3 741, P5 49, P6 1807 |
| M3 | ★: a value of 900 or more never popped | P1 689, P3 915, P6 788 |
| M4 | drive: the bottom of the stack compared | P1 652, P6 752 |
| M5 | drive: values matched by their remainder mod 500 | P1 2, P2 30, P3 28, P6 20 |
| M6 | drive: the value after the one popped passed over | P1 1669, P2 583, P4 438, P5 150, P6 1769 |
| M7 | in place: the first value never pushed | P1 1232, P4 336, P5 60, P6 1329 |
| M8 | in place: the last value never pushed | P1 1173, P2 650, P4 432, P5 45, P6 1270 |
| M9 | in place: values written mod 500 | P1 1930, P3 520, P6 2030 |
| M10 | links: a run of one never linked | P1 1073, P2 195, P5 196, P6 1172 |
| M11 | links: each place linked two down | P1 567, P2 128, P5 11, P6 667 |
| M12 | links: an even value popped from under the top | P1 124, P3 198, P5 4, P6 131 |
| M13 | pattern: the next pop passed over | P1 343, P2 83, P6 364 |
| M14 | pattern: the values taken as places | P1 1008, P2 724, P3 702, P4 452, P6 1108 |
| M15 | pattern: the first pop never checked | P1 244, P2 201, P4 184, P6 244 |

P1 and P6 kill all fifteen, P2 nine, P5 seven, P3 and P4 six each.

P3 kills exactly the six that look at the values as numbers (M2's
parity, M3's 900, M5 and M9's remainders, M12's parity, and M14 using
the values as places); the other nine use them only to compare them for
equality, which renaming keeps.

P2 misses M2, M3, M4, M7, M9 and M12, P4 the nine other than M1, M6,
M7, M8, M14 and M15, and P5 the eight other than M2, M6, M7, M8, M10, M11
and M12. P5 looks only at cases whose answer is yes.

Thirty-five other edits were tried and set aside. Twenty-five failed
exactly the same checks as others, in seven groups, so none of them was
kept. Ten answer yes only when the values are popped in the order they
were pushed, which a count over the 3,000 small cases confirms (823 such
cases, 1,494 other cases that fit): ★ comparing the bottom of the stack,
in place comparing the value just read, ★ popping at most once after
each push, drive never popping the top, never pushing the values it
passes or leaving the value to pop on the stack, drive checking the top
only over another value, links leaving the popped place on top, and
pattern requiring the later pops to rise or measuring their fall from
before the first place. Four answer yes for every case: ★ answering yes
once anything is popped, drive passing over a buried value or answering
yes for one, and pattern never moving its last pop on. Two answer no for
every case (★ and in place never popping the last value on the stack),
two write the stack wrongly in place, two (links never linking a new run
to the top, or taking the next place down as under the top) unlink the
same places wrongly, and two compare values by their remainder mod 500 (★
and in place). Three are the same mistake in three arms: ★ pushing the
values in reverse, and links and pattern numbering the places from the
end. Four were sound but beyond three an arm: in place answering yes
when the bottom is the last pop, links setting the highest place one
short, and pattern allowing a rise of one or not counting a place just
below as below. Two crashed with an index out of bounds: ★ starting the
pops from the second, and in place counting a pop twice. Four were
equivalent. ★ answering yes with one value left, and in place with at
most one on the stack: when every value but one is popped, the one left
is the last to pop, and it was popped as soon as it was on top. ★
answering yes when nothing was popped: a value is on top as soon as it
is pushed, so the first value to pop is popped then, and something is
always popped. Links popping any place under the top: the places above
it stay linked, and must be popped later from below the new top, which
answers no then.

## Verification

Every arm prints the same output as `validate_stack_sequences.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `4540c92380`, the runtime
archives at `086f304909`, with no change to the runtime's sources between
the two. Under `karac __mir-run` the arms take 0.2 to 0.3 s each, the
pattern arm 0.8 s, and the differential 33 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The pattern arm first stored the address of each place rather than the
place: `p.push(place.get(*v).unwrap())` into a `Vec[i64]` kept the
reference that `get` returns, so the compiled lanes compared
addresses and `karac __mir-run` refused the first `<` between two places.
That is kara `B-2026-10-24-3`, filed for this kata and fixed in
`bd015b5c7c`; the arm keeps the natural way to write it.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds 20 pairs of sequences of 1,000 values once,
LeetCode's longest: each pushes 1,000 of the values 0 to 1000 in a
random order, and pops them by a random run of pushes and pops, every
second one with two neighbouring pops then swapped. In each of 2,500
rounds it runs the ★ arm on every pair, each round starting from a
different one, and folds the answers into a checksum. Every
implementation prints `2500 rounds over 20 pairs of sequences of 1000
values: 37500 fit, checksum 763009056`: half of the swapped pairs still
fit. Each call grows a new stack: a `Vec` in Kāra and Rust, a slice in
Go, a list in Python, and in C an array allocated for the call.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.44 to 0.50 s | 0.48 s |
| Rust (`rustc -O`) | 0.46 to 0.54 s | 0.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.48 to 0.52 s | 0.51 s |
| Go | 0.62 to 0.74 s | 0.68 s |
| Python | 7.80 s | |
| Kāra (`karac build --mir`) | 0.54 to 0.63 s | 0.57 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 16 times
C's.

v2 takes 1.13 times Rust's median time under overflow checks and 1.19
times C's. Under valgrind's cachegrind v2 runs 2.14 billion
instructions and 0.54 billion branches with 46 million mispredicted,
Rust with overflow checks 1.58 billion, 0.35 billion and 45 million,
and C 1.52 billion, 0.24 billion and 44 million. The mispredictions are
the same in all three: whether the top is the next value to pop is
decided by the random runs.
