# 2231. Largest Number After Digit Swaps by Parity

You are given a positive integer `num`. You may swap any two digits of
`num` that have the same **parity** (i.e. both odd digits or both even
digits).

Return *the **largest** possible value of* `num` *after **any** number
of swaps.*

```
num = 1234   ->  3412
num = 65875  ->  87655
```

**Constraints:** `1 <= num <= 10^9`.

Swaps within a parity reach every order of that parity's digits among
its own places, and touch nothing else. So the odd digits are sorted
from largest down into the odd digits' places, and the even ones into
theirs. O(d log d) for d digits.

## Approaches

| file | mechanism |
|---|---|
| `parity.kara` ★ | the digits split by parity into two `Vec`s and sorted, each place then `pop`ping the largest left of its own parity |
| `parity_counts.kara` | a count of each digit 0 to 9, no sort: the digits read off by division, and each place from the left taking the largest digit of its parity still counted, stepping down by 2 |
| `parity_swaps.kara` | the swaps themselves: a selection sort over the digits as `char`s, each place taking the largest digit of its parity to its right by one `swap`; parsed back with `i64.parse` |
| `parity_struct.kara` | a `struct Piles` of two `PriorityQueue.max_first()`s, filled by `add` and drawn by `take` (`mut ref self`) |
| `parity_iter.kara` | the parities split by `filter` and sorted, each drawn largest first through its own `rev()` iterator's `next`, and the number `fold`ed back together |
| `parity_solution.kara` | LeetCode's Rust template: `i32` in and out, the digits as bytes through `num.to_string().into_bytes()`, each parity `filter(\|&&c\| (c - b'0') % 2 == 1)` `cloned` and sorted largest first by `sort_unstable_by(\|a, b\| b.cmp(a))`, written back over the bytes through `iter_mut()` and `*c = ...`, and parsed by `String::from_utf8(d).unwrap().parse().unwrap()`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples and six
more (one digit, the largest num, evens around an odd, a 0 that must
stay low, all of one parity, and every digit once), each with its
answer; then a checksum of 3000 random nums of 1 to 10^9, as many with
up to 4, 7 and 10 digits; then the total the swaps add over every num
from 1 to 10^5. `parity.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 18 edits: `Vec<u8>` to
`Vec[u8]`, `into_bytes()` to `bytes().to_vec()`, the `|&&c|` patterns to
`|c|`, `sort_unstable_by` to `sort_by`, `let (mut i, mut j)` to `let mut
(i, j)`, `String::from_utf8(d).unwrap().parse().unwrap()` to
`i32.parse(String.from_utf8(d).unwrap()).unwrap()`, `struct Solution;`
to `struct Solution {}`, and the adapter's `as i64` dropped, since the
`i32` widens where it is returned. `iter_mut()` with `*c = ...`, the
byte literal `b'0'` and `b.cmp(a)` are Kāra's too.

The struct arm was first written with Rust's `f"{num}".bytes().map(...)`;
`karac check` reported that a `Slice` has no `map` and `karac fix` put
`.iter()` before it, and in the same pass made the `u8` difference an
`i64` for the `Vec[i64]` it is collected into.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every number reachable from num by swapping two digits of
one parity, again and again, found by a breadth-first search from num,
and the largest of them; no sorting. It checks 300 random nums of 1 to
6 digits; then 30 of odd digits only; then 30 whose digits alternate odd
and even. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | it is at least num, has num's digits, and each place keeps its digit's parity |
| P3 | the answer's own answer: itself |
| P4 | num * 10: the answer * 10, the 0 staying last |
| P5 | a 9 written before num: the answer with the 9 still before it |
| P6 | each arm agrees with at least three of the other five |

P4 holds because 0 is the smallest even digit and the last place is
even, and P5 because 9 is the largest odd digit and the first place is
odd.

The differential prints `360 cases: checksum 242903525, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that takes
the largest of the `itertools.permutations` keeping each place's parity.
On a failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
of the others, each run under `karac __mir-llvm-run`, and the kept ones
under `karac __mir-run` too. Seventeen are kept, three to each Kāra arm
and two to the Rust-template arm. Each kept one is killed, fails the
same way under both backends and not by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the digits written back as they were | P1 203, P6 203 |
| M4 | ★: every digit read one less | P1 360, P2 360, P3 360, P4 360, P5 360, P6 360 |
| M6 | ★: the places read from the right | P1 184, P2 184, P3 182, P4 306, P5 282, P6 184 |
| M7 | counts: a digit used again | P1 259, P2 259, P4 276, P5 207, P6 259 |
| M9 | counts: each digit counted twice | P1 259, P2 259, P3 133, P4 239, P5 246, P6 259 |
| M10 | counts: the parity ignored stepping down | P1 170, P2 170, P3 16, P6 170 |
| M12 | swaps: the parity ignored | P1 182, P2 182, P6 182 |
| M14 | swaps: the next place never looked at | P1 113, P6 113 |
| M15 | swaps: the smallest brought forward | P1 259, P2 203, P4 276, P5 286, P6 259 |
| M17 | struct: the odd queue smallest first | P1 186, P2 107, P5 286, P6 186 |
| M18 | struct: a 9 written as 8 | P1 99, P2 99, P3 27, P5 360, P6 99 |
| M21 | struct: the even queue smallest first | P1 159, P2 91, P4 276, P6 159 |
| M24 | iter: a 9 written as 0 | P1 99, P2 99, P3 18, P5 360, P6 99 |
| M25 | iter: the odd digits unsorted | P1 126, P2 67, P3 176, P5 286, P6 126 |
| M26 | iter: a 1 written before the number | P1 360, P2 360, P3 360, P5 360, P6 360 |
| M28 | solution: every even place given the first even digit | P1 159, P2 159, P4 276, P6 159 |
| M30 | solution: every odd place given the largest odd digit | P1 186, P2 186, P5 207, P6 186 |

P1 and P6 kill all seventeen, P2 fifteen, P5 eleven, P3 eight, and P4
seven. P2 misses the two edits whose answer is still a reordering within
each parity, only not the largest (M3, M14). P4 adds a 0 at the end, so
it catches the edits that spoil the even digits or the order of the
places, and P5 a 9 at the front, the odd ones. P3 catches the edits
whose answer is not a fixed point: one that writes a digit wrong keeps
changing it when asked again.

Of the thirty-one, fourteen were not kept. One survives and is
equivalent: the swaps arm also swapping a digit with an equal one
(M13), which changes nothing. None crashes, and none differs between
the backends. Ten fail as a kept one does: the ★ arm's odd digits
unsorted (M1) as the iter arm's (M25); the ★, iter and template arms'
odd digits smallest first (M2, M22, M27) as the struct arm's queue
(M17); the counts arm's digits written back as they were (M11) as the ★
arm's (M3); the struct arm's digits one more (M20) as the ★ arm's one
less (M4); the ★ and iter arms' even digits smallest first (M5, M23) as
the struct arm's queue (M21); the counts arm's places from the right
(M8) as the ★ arm's (M6); and the struct arm's digits added twice (M19)
as the counts arm's counted twice (M9). Three fail their own way and are
left out for the count of three (two for the template): the swaps arm's
opposite parity (M16), and the template's evens unsorted and 8 written
as 6 (M29, M31).

## Verification

Every arm prints the same output as `parity.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.1 s to 2.6 s, the iter arm 3.7
s and the struct arm, with its two priority queues, 4.4 s. The
differential takes 0.8 s.

## Benchmarks

The bench draws 10^5 nums of 1 to 10^9 once, then makes 20 passes over
all of them, one num drawn again before each pass, with the ★ arm in all
five languages; C writes the number out with `snprintf` and sorts with
`qsort`. Every implementation prints `20 passes over 10^5 nums:
checksum 79230271`.

BENCHTAB
