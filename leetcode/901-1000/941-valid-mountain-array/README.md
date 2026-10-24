# 941. Valid Mountain Array

Given an array of integers `arr`, return `true` if and only if it is a
valid mountain array.

Recall that `arr` is a mountain array if and only if:

- `arr.length >= 3`
- There exists some `i` with `0 < i < arr.length - 1` such that:
  - `arr[0] < arr[1] < ... < arr[i - 1] < arr[i]`
  - `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`

```
arr = [2,1]      ->  false
arr = [3,5,5]    ->  false
arr = [0,3,2,1]  ->  true
```

**Constraints:** `1 <= arr.length <= 10^4`; `0 <= arr[i] <= 10^4`.

## Approaches

| file | mechanism |
|---|---|
| `valid_mountain_array.kara` ★ | a walk up while each next value is higher, then down while each next is lower; a mountain when the climb stopped somewhere other than the first or last place and the way down reached the end. O(n) |
| `valid_mountain_array_ends.kara` | two climbers, one from the left while the values rise and one from the right while they rise going left; a mountain when both stop at the same place and neither stayed where it started. O(n) |
| `valid_mountain_array_signs.kara` | the sign of each step from one value to the next written down: a mountain has no flat step, a rise first, a fall last, and exactly one place where the sign changes. O(n) time and space |
| `valid_mountain_array_peak.kara` | the first place holding the largest value found first; it must be neither end, and every step to its left must rise and every step to its right fall. O(n) |
| `valid_mountain_array_states.kara` | a machine reading the steps in one of four states, an `enum` matched at each step: at the start, going up, going down, or failed; a rise starts or continues the climb, a fall turns or continues the way down, and anything else fails; a mountain when it ends going down. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines: LeetCode's three examples and seven
more (one value, the smallest mountain, a climb with no way down, a way
down with no climb, a flat step at the top, two peaks, and a mountain
ending in a flat step); for 300 random cases of 1 to 50 values, each a
climb to a random place and a way down by steps of 1 to 3, half of them
then with one value changed, the values, how many are mountains and a
checksum; and six of LeetCode's longest, 10,000 values: a mountain
peaking in the middle, the same with one flat step, a climb all the way,
a mountain peaking at the second value, all the same value, and random
values. `valid_mountain_array.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every `i` with `0 < i < n - 1` tried, the values checked to
rise strictly up to it and fall strictly after it. It checks 3,200
random cases made as the harness makes them: 3,000 of up to 8 values
with steps of 1 or 2, against the statement, and 200 of up to 2,000
values with steps of 1 to 3, against the other properties; 209,065
values, and 1,090 of the cases are mountains.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | a mountain has 3 values at least, a rise first and a fall last |
| P3 | the values reversed give the same answer |
| P4 | every value tripled and 7 added gives the same answer |
| P5 | a value written twice in a row never gives a mountain, and a mountain followed by a value one lower than its last is still one |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 209065 values, 1090 mountains, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (3 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first step never checked | P1 426, P2 426, P3 871, P5 345, P6 426 |
| M2 | ★: a rise of 1 ending the climb | P1 694, P3 421, P4 800, P6 800 |
| M3 | ★: the way down two steps at a time | P1 725, P2 95, P3 838, P5 799, P6 793 |
| M4 | ends: the right climber allowed to stay | P1 294, P2 294, P3 600, P6 294 |
| M5 | ends: the climbers allowed to stop apart | P1 190, P5 942, P6 281 |
| M6 | ends: fewer than 3 values a mountain | P1 778, P2 778, P5 631, P6 778 |
| M7 | signs: the first and last signs not checked | P1 46, P2 46, P5 46, P6 46 |
| M8 | signs: a turn at the first step not counted | P1 370, P3 505, P6 370 |
| M9 | signs: a turn at the last step not counted | P1 363, P3 505, P6 363 |
| M10 | peak: a flat step allowed on the left | P1 51, P2 30, P3 99, P5 498, P6 51 |
| M11 | peak: the step after the top never checked | P1 53, P2 28, P3 59, P5 325, P6 53 |
| M12 | peak: the first step never checked | P1 58, P2 58, P3 121, P5 186, P6 58 |
| M13 | states: a flat step on the way up | P1 48, P3 40, P5 503, P6 48 |
| M14 | states: a rise on the way down going up again | P1 123, P6 214 |
| M15 | states: a failure starting over | P1 67, P2 51, P3 227, P5 381, P6 112 |

P1 and P6 kill all fifteen, P3 eleven, P5 ten, P2 nine and P4 one.

P4 kills only M2, which ends the climb at a rise of exactly 1. Tripling
the values makes every rise at least 3, so M2 then answers rightly
where it did not; every other mistake depends only on the order of the
values, which tripling keeps.

P2 misses the six whose mistakes keep a rise first and a fall last in
every array they accept: M2, M8 and M9 only refuse mountains, and M5,
M13 and M14 accept arrays with two peaks or a flat step on the way up,
which still begin with a rise and end with a fall.

P3 misses the four whose mistakes are the same both ways round: M5 and
M14 accept two peaks, M7 accepts a valley, a rise last and a fall first
as well as a mountain, and M6 accepts arrays of one or two values,
whichever way they are read.

P5 misses M2, M4, M8, M9 and M14. None of them accepts a flat step, so a
value written twice in a row still gets `false`, and each of them goes
on accepting an array it accepted once a value one lower follows: M4
accepts a climb with no way down, which that value makes a mountain,
and M14's zigzags still end going down.

Twenty-two other edits were tried and set aside. Seventeen failed
exactly the same checks as each other, in seven groups, so none of them
was kept: ★ needing no climb and states going down after a fall at the
start; ★ allowing the top at the end and states accepting an end on the
way up; three that allow a flat step on the way up (★, ends climbing
one from the left, and signs taking it as a rise); four that allow one
on the way down (★, ends climbing one from the right, peak allowing one
on the right, and signs taking it as a fall); ends letting the left
climber stay and peak allowing the top at the start; ★ and ends never
checking the last step; and ★ stopping the way down one short of the
end and signs writing a fall as flat, both of which never answer
`true`. Two were sound but beyond three an arm (★ ending the way down
at a fall of exactly 1, and ★ never taking three values as a mountain).
Two were equivalent: ends stopping the left climber one short of the
end, which only matters for a climb all the way, refused anyway; and
signs allowing no turn as well as one, since a rise first and a fall
last make at least one. One crashed: signs skipping a flat step instead
of failing, on an array of equal values, whose list of signs is then
empty.

## Verification

Every arm prints the same output as `valid_mountain_array.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.2 s each and the differential
3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Legacy refuses all five arms and the bench program at a call with an
indexed `Vec` as its argument, `valid_mountain_array(examples[i])` and
`valid_mountain_array(arrays[c])`, a move out of an index ("cannot move
... out of an index"), which v2's borrowing parameters make a borrow. It
refuses the differential where `arm` passes its `ref` parameter on to
an arm ("expected 'Vec[i64]', found 'ref Vec[i64]'"), for the same
reason. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 100 arrays of 10,000 values once, LeetCode's
longest, each climbing by 1 to a random place and falling by 1 after
it, and every other one then with one value changed to a random value;
in each of 200 rounds it runs the ★ arm on every array, each round
starting from a different one, and folds which arrays are mountains
into a checksum. Every implementation prints `200 rounds over 100
arrays of 10000 values: 10000 mountains, checksum 674562253`: every
changed array is refused, and every other accepted. The walk reads the
whole of each mountain, and of each changed array up to its change.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.084 to 0.094 s | 0.087 s |
| Rust (`rustc -O`) | 0.114 to 0.145 s | 0.122 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.097 to 0.131 s | 0.111 s |
| Go | 0.117 to 0.159 s | 0.124 s |
| Python | 11.2 s | |
| Kāra (`karac build --mir`) | 0.100 to 0.118 s | 0.105 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). The compiled runs are short, since each step of the walk
is one comparison; Python's, which interprets every step, is about 130
times C's.

v2 takes 0.95 times Rust's median time under overflow checks and 1.20
times C's. Under valgrind's cachegrind v2 runs 1.21 billion instructions
and 0.32 billion branches with 52,000 mispredicted, Rust with overflow
checks 1.20 billion, 0.32 billion and 48,000, and C 0.83 billion, 0.24
billion and 47,000. v2 and Rust run nearly the same code; that the
quarter fewer branches in C are the bounds checks on `arr[i + 1]`,
which it does not make, is inferred, not profiled.
