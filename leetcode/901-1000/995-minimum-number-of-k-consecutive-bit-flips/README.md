# 995. Minimum Number of K Consecutive Bit Flips

You are given a binary array `nums` and an integer `k`.

A **k-bit flip** is choosing a **subarray** of length `k` from `nums`
and simultaneously changing every `0` in the subarray to `1`, and every
`1` in the subarray to `0`.

Return *the minimum number of **k-bit flips** required so that there
is no* `0` *in the array*. If it is not possible, return `-1`.

A **subarray** is a **contiguous** part of an array.

```
nums = [0,1,0], k = 1            ->  2
nums = [1,1,0], k = 2            ->  -1
nums = [0,0,0,1,0,1,1,0], k = 3  ->  3
```

**Constraints:** `1 <= nums.length <= 10^5`;
`1 <= k <= nums.length`.

## Approaches

Flips commute, and flipping a window twice undoes it, so an answer is
a set of windows. The leftmost 0 can only be cleared by the window
that starts on it, which settles that window, and so on to the right:
the greedy that flips wherever a bit, seen through the flips covering
it, is still 0 is forced, and fails only when that window would run
off the end. Every arm runs that greedy; they differ in how they know
how many flips cover the current bit.

| file | mechanism |
|---|---|
| `min_k_bit_flips.kara` ★ | a running parity: a list of booleans marks where each flip stops covering, and the parity of the flips covering a bit changes at each start and each mark. O(n) |
| `min_k_bit_flips_diff.kara` | a count as a difference array: a flip adds 1 where it starts and takes 1 off where it stops, and a bit reads as 0 when it and the running count add up to an even number. O(n) |
| `min_k_bit_flips_deque.kara` | a queue of where the covering flips began: those that began k or more places back leave the front, and the queue's length is the count. O(n) |
| `min_k_bit_flips_marks.kara` | marks in a copy of the array: a flip adds 2 to the bit it starts at, which leaves the bit's parity as it was, and a value above 1 k places back says that flip has stopped. O(n) |
| `min_k_bit_flips_fenwick.kara` | a Fenwick tree: a flip adds 1 at its start and takes 1 off at its end, and the sum up to a place is the count. O(n log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 20 lines. The first ten are LeetCode's three
examples and seven more: a single 1 and a single 0; two zeros cleared
by one flip of both; two flips that overlap, and a window of the
whole array that cannot help; an array already all ones; and two
pairs of zeros. Then six arrays of LeetCode's largest size, 100,000
bits: all zeros with k = 1, k = 100,000, k = 3, which leaves one bit
over, and k = 4; and 0 and 1 in turn with k = 2 and k = 50,000. Then
totals over random arrays: 300 of up to 8 bits, 3,000 of up to 60,
300 of up to 1,000, and three of 100,000, each with a random k up to
20; half of them random bits and half all ones put through random
flips of k, so that they can be made all ones again.
`min_k_bit_flips.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: a breadth-first search over every array of n bits,
each held as a number, one flip of k bits a step, gives the fewest
flips from `nums` to all ones, or -1 if the search never meets it. It
checks 3,200 random arrays, made as the arms' random arrays are:
3,000 of up to 10 bits with any k against the statement, and 200 of up
to 300 bits with k up to 30 against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 arrays |
| P2 | the array reversed gives the same answer |
| P3 | with k = 1 the answer is the number of zeros |
| P4 | one random window of k flipped moves a possible answer up or down by exactly one, and leaves an impossible one impossible |
| P5 | 1 to k ones put in front give the same answer |
| P6 | each arm agrees with at least two of the other four |

P4 holds because the forced greedy makes the set of windows unique:
flipping one more window either adds it to the set or takes it out.

It prints `3200 arrays of 46321 bits: 939 impossible, 5802 flips,
checksum 159970302, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (2.3 s) and `karac __mir-llvm-run`, and the same
under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-seven edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last window refused | P1 722, P2 670, P3 1234, P4 522, P6 755 |
| M2 | ★: a flip never stops | P1 963, P2 771, P3 1748, P4 846, P6 1059 |
| M3 | ★: a new flip not seen at its own start | P1 1197, P2 619, P3 1748, P4 1182, P6 1295 |
| M4 | diff: the parity test turned round | P1 2114, P3 2832, P5 1910, P6 2216 |
| M5 | diff: a flip stops a place early | P1 1193, P2 607, P3 1748, P4 1107, P6 1291 |
| M6 | diff: the count set, not added to | P1 1133, P2 412, P3 1773, P4 1433, P6 1230 |
| M7 | deque: a flip covers one place too many | P1 963, P2 613, P3 1773, P4 773, P6 1058 |
| M8 | deque: a flip may run off the end | P1 254, P2 309, P6 258 |
| M9 | deque: the newest flip leaves, not the oldest | P1 352, P2 209, P4 452, P6 441 |
| M10 | marks: any bit above 0 read as a mark | P1 1220, P2 783, P3 2290, P4 623, P5 1620, P6 1319 |
| M11 | marks: the mark k places back missed at place k | P1 548, P2 695, P3 953, P4 382, P5 574, P6 574 |
| M12 | marks: a mark adds 1 | P1 975, P2 881, P3 1792, P4 652, P6 1072 |
| M13 | fenwick: an add steps one place at a time | P1 939, P2 495, P3 1481, P4 856, P5 773, P6 1031 |
| M14 | fenwick: a flip taken off a place early | P1 878, P2 358, P4 709, P6 971 |
| M15 | fenwick: a sum steps one place at a time | P1 1029, P2 853, P3 1441, P4 964, P5 843, P6 1126 |

P1 and P6 kill all fifteen, P2 fourteen, P4 thirteen, P3 twelve and
P5 five. M4 clears the ones instead of the zeros, which answers the
question for the array with every bit turned over; reversing it, or
flipping one more window, treats that array as it treats the real
one, so P2 and P4 cannot see it. With k = 1 no flip can run off the
end, no two flips are ever covering at once, and a flip taken off at
its own place has done its work, so P3 misses M8, M9 and M14. Ones put
in front move every bit along, which only an arm that reads a place
by its number can notice: marks reading a bit k places back (M10,
M11), and the Fenwick tree, whose sums gather different nodes for a
different place (M13, M15); P5 kills those four, and M4, which flips
the ones put in front.

Twelve other edits were tried and set aside. Six failed exactly the
same checks as a kept one: diff and marks not seeing a new flip at its
own start, as M3; marks flipping at the bits seen as 1, as M4; deque
queueing a flip a place late, and fenwick summing to the place before,
which both keep a flip a place too long, as M7; and fenwick never
taking a flip off, as M2. Two were sound but beyond three an arm: ★
flipping at the bits seen as 1, which fails M4's checks, and answering
an overrun with the flips so far. Four survived and are equivalent.
Diff adding 1 where a flip stops rather than taking 1 off changes the
count by 2 there, which keeps its parity. Deque letting at most one
flip leave in a step is enough, since flips begin at different places
and so at most one ends at each. Fenwick's sums leaving out place 0
miss only the sum up to place 0, which is read before any flip is
added; and adding a flip at the place after its start changes no sum
read later, since the start's own sum is read before the add. None
crashed.

## Verification

Every arm prints the same output as `min_k_bit_flips.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 1.4 s (★) to 7.0 s (fenwick,
which walks its tree for every bit), and the differential 2.3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
arrays of LeetCode's largest size, 100,000 bits, once: ten of random
bits, each with a random k up to 100, which all turn out impossible,
and ten of ones put through random flips of a random k up to 100, with
that k. In each of 50 rounds it runs the arm on every array, each
round starting from a different one, and folds every answer into a
checksum. Every implementation prints `50 rounds over 20 arrays of
100000 bits: 500 impossible, 12498000 flips, checksum 638905717`. Each
call walks all 100,000 bits with a fresh list of 100,001 booleans; a
random array fails only near its end. Drawing the arrays, millions of
steps of the random generator and of flips, is part of every timing.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.605 to 0.657 s | 0.629 s |
| Rust (`rustc -O`) | 0.504 to 0.586 s | 0.543 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.535 to 0.586 s | 0.564 s |
| Go | 0.857 to 0.937 s | 0.905 s |
| Python | 13.2 s | |
| Kāra (`karac build --mir`) | 0.601 to 0.637 s | 0.626 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 21 times
Kāra's.

v2 took 1.11 times Rust's median time under overflow checks and the
same as C's. Under valgrind's cachegrind v2 ran 2,265 million
instructions and 701 million branches with 40.5 million mispredicted,
Rust with overflow checks 1,600 million, 446 million and 40.5 million,
and C 2,128 million, 345 million and 40.5 million. The three mispredict
alike: whether to flip at a bit is as random as the bits, and that
branch is missed about two times in five over the 100 million bits the
calls walk.
