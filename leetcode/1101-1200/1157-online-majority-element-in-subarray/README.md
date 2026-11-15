# 1157. Online Majority Element In Subarray

Design a data structure that efficiently finds the majority element of a
given subarray. The majority element of a subarray is an element that
occurs `threshold` times or more in the subarray.

- `MajorityChecker(int[] arr)` initializes the instance of the class with
  the given array `arr`.
- `int query(int left, int right, int threshold)` returns the element in
  the subarray `arr[left...right]` that occurs at least `threshold` times,
  or `-1` if no such element exists.

```
["MajorityChecker","query","query","query"]
[[[1,1,2,2,1,1]],[0,5,4],[0,3,3],[2,3,2]]   ->  [null,1,-1,2]
```

**Constraints:** `1 <= arr.length <= 2 * 10^4`; `1 <= arr[i] <= 2 * 10^4`;
`0 <= left <= right < arr.length`; `threshold <= right - left + 1`;
`2 * threshold > right - left + 1`; at most `10^4` calls will be made to
`query`.

The arms are `struct MajorityChecker` with `new(arr: Vec[i32])` and
`query(self, left, right, threshold)`. The harness passes LeetCode's
`int`s as `i32`, which the Kāra arms take as `i64` and the Rust arm as
`i32`.

## Approaches

Since `2 * threshold` exceeds the range's length, an answer holds more
than half the range, so there is at most one, and every arm finds a
single candidate and then counts it.

| file | mechanism |
|---|---|
| `majority_checker.kara` ★ | a segment tree of Boyer-Moore votes, each node the value its range votes for and the votes left to it; two ranges merge as one vote, the same value adding and different values cancelling. A query merges the O(log n) nodes covering its range, bottom up, and counts the survivor among its sorted places with two `partition_point`s. O(n) to build, O(log n) a query |
| `majority_checker_bits.kara` | prefix counts of each of the 15 bits: a value holding `threshold` places decides every bit, so the bits set at `threshold` places or more spell the only candidate, counted from its sorted places. O(15 n) to build, O(15 + log n) a query |
| `majority_checker_sample.kara` | 40 random places of the range, from a seed made of the query, each place's value counted from its sorted places; a value holding more than half the range escapes all 40 with odds below 10^-12. O(40 log n) a query |
| `majority_checker_heavy.kara` | values held at `cut` places or more, `cut` the least whose square reaches n, get prefix counts; a query whose `threshold` reaches `cut` tries each of them, and one whose `threshold` falls short has a range shorter than 2 `cut`, walked by a Boyer-Moore vote. O(n sqrt n) to build, O(sqrt n) a query |
| `majority_checker_solution.kara` | a Rust solution as LeetCode's Rust users write it (a recursive segment tree over `4 * n` nodes, `usize` indices, a `HashMap` of each value's places filled with `entry().or_insert_with`, `Self::` calls, `if let Some`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's example (1, -1, 2); one
value (`[7]`, 7); `[1, 2]` asked whole at 2 (-1) and at its second
place (2); a run of five 5s asked in part and whole (5, 5); values in
turn, `[1, 2, 1, 2, 1]`, where only an odd range has a majority (1, 2,
-1); and the largest value, `[20000, 1, 20000]` (20000 at 2, -1 at 3).
Then 300 random arrays of 1 to 60 values, over the first 1 to 4 values
or one value planted at about two places in three, 20 queries each with
a threshold from the least the range allows to all of it (`300 random
arrays: total 4633647, checksum 53556414`), and three arrays of 20,000
values with 10,000 queries each, the most the constraints allow: over
two values, a planted value, and all one value. `majority_checker.py`
mirrors the ★ arm and its output is byte-identical; a Python count of
every range agrees on all of it.

The Mend loop: the four Kāra arms check clean as written. The Rust arm
takes four `karac fix` rounds (34, 3, 18 and 5 edits): the `HashMap`
import dropped and `HashMap` to `Map`, `usize` to `i64`, `&self` to
`self`, `&mut Vec<_>` to `mut ref Vec[_]` and `&Vec<_>` to a plain
borrow, `&x` patterns and `&` arguments dropped, `||` and `&&` to `or` and `and`, `vec![(0, 0); 4 *
n]` to `Vec.filled`, `Vec::new` and `Self::` to `.` paths, and the
`as usize` casts dropped. Its output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the range sorted and a value held `threshold` times found
among its runs. It checks 300 arrays in four kinds of 75, 8 queries
each: 1 to 12 values over the first 1 to 3; 10 to 80 values over 1 to 5
values, low or just under 20000 (so the bits arm reads its top bits),
or one value planted at about two places in three; a range of 1 to 120
values holding one value at about half its places, either shuffled or
all at the range's end, after 0 to 10 or 100 to 400 random values and
before 0 to 10, asked at the least threshold and the two above it; and
50 to 400 values over 1 to 8, one value at about 55% of places, asked
with ranges of about twice the heavy arm's cut and thresholds from one
below the cut to one above. The rest of each case's 8 queries are
random. Every random choice the properties make is drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the same checker asked every query again, in reverse order, answers alike |
| P3 | a threshold one lower keeps an answer, and one higher keeps -1 or the answer |
| P4 | the array reversed, the range with it, gives the same answer |
| P5 | the values renamed by a bijection of 1 to 20000 give the answer renamed |
| P6 | 0 to 20 random values added before and after, the range shifted, give the same answer |
| P7 | a value holding more than half a range holds more than half of one of its two parts, split at a random place |

All 84,000 checks pass on every arm: `300 arrays, 2400 queries (1148
answered): checksum 38617790, 84000 checks over 5 arms: 0 failures`, in
25 s under `karac __mir-run`. A Python reading of the same draws, with
the mirror's answers against a count of each range, gives the same
line.

## Mutation testing

Twenty-six edits to the differential, four to seven to each arm, each
run under `karac __mir-run` and `karac __mir-llvm-run` with
`KARAC_HASH_SEED=1`, each failing the same way under both. Twenty-two
are caught and four are equivalent. In the ★ arm, a tie between two
values' votes going to the second range (T2): either value is left with
no votes, and a value with no votes cannot outlast a majority. In the
heavy arm, the cut halved (H1), and a threshold equal to the cut sent
down the walk (H3): the walk answers every short range correctly, and
the heavy values still include every value a long threshold could
need, so the cut decides only the cost. In the Rust arm, every leaf
given two votes (X5): doubling every count leaves every vote's winner.

| # | mutation | failures by property |
|---|---|---|
| T1 | ★: one value's votes over two ranges not added | P1 51, P4 57, P6 56, P7 12 |
| T3 | ★: the range's last place left out of the vote | P1 200, P4 48, P6 7, P7 164 |
| T4 | ★: the wrong left nodes taken | P1 136, P4 141, P6 97, P7 18 |
| T5 | ★: a value at exactly the threshold refused | P1 550, P7 112 |
| T6 | ★: the range's first place not counted | P1 475, P4 116, P7 128 |
| T7 | ★: the root never built | P1 13, P6 13 |
| B1 | bits: the top bit never read | P1 60, P5 199 |
| B2 | bits: a bit at exactly the threshold dropped | P1 468, P5 32, P7 132 |
| B3 | bits: each bit counted as the next | P1 1148 |
| B4 | bits: the range's last place not counted | P1 439, P4 64, P5 15, P7 154 |
| S1 | sample: one place tried | P1 180, P3 121, P4 245, P6 203, P7 92 |
| S2 | sample: only the first half of the range tried | P1 6, P3 4, P4 6, P6 6 |
| S3 | sample: a value at exactly the threshold refused | P1 550, P7 112 |
| S4 | sample: places tried from the array's start | P1 2, P4 5, P6 3 |
| H2 | heavy: a value at exactly the cut not heavy | P1 68, P6 70 |
| H4 | heavy: a threshold one below the cut tries only heavy values | P1 17, P6 21 |
| H5 | heavy: a different value ends the vote | P1 13, P3 9, P4 25, P6 13, P7 20 |
| H6 | heavy: the range's last place left out | P1 262, P4 46, P6 142, P7 198 |
| X1 | solution: a node starting at the range's left end left out | P1 188, P4 20, P6 11, P7 169 |
| X2 | solution: a value at exactly the threshold refused | P1 550, P7 112 |
| X3 | solution: the query splits nodes unlike the build | integer overflow (the recursion never narrows) |
| X4 | solution: a node's votes counted as one | P1 57, P4 66, P6 58, P7 16 |

Of the twenty-one caught edits that do not stop the program, P1 catches
all twenty-one, P7 fourteen, P6 thirteen, P4 twelve, and P3 and P5 three
each. The
root never built (T7) shows only when a range is the whole of an array
whose length is a power of two. A first run found the sampling edits on
almost nothing (S2 on 4 checks, S4 on 5), since a value holding more
than half a range is in its first half and near its start more often
than not; the border ranges were then lengthened to 120 values, given
the arranged form with the value at the end, and put after up to 400
other values, which raised S2 to 22 checks and S4 to 10. They stay low
because 40 tries miss only when the value is rare where they look.

## Benchmarks

`bench/` times the ★ arm against the same vote tree and sorted places in
C, Rust, Go and Python. Four arrays of 20,000 values, the most the
constraints allow, are built once in four kinds: over 2 values, one
value at about two places in three, over all 20,000 values, and one
value at about half the places. Each gets a checker and 10,000 random
queries, drawn once; each of 100 passes answers all 40,000. Every
program prints `100 passes over 4 arrays of 20000 values, 10000 queries
each: checksum 156927228`. The C program keeps each value's places in
one array cut by offsets, and searches them as `partition_point` does:
the span halved by a select marked unpredictable, as Rust's library and
Kāra's mark it. Without the mark clang compiles the select as a branch
that mispredicts about half the time, and the C program took 0.95 s.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `77ed9881fc`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Rust (`rustc -O -C overflow-checks=on`) | 0.533 to 0.648 s | 0.565 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.534 to 0.637 s | 0.576 s |
| Rust (`rustc -O`) | 0.546 to 0.645 s | 0.585 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.568 to 0.665 s | 0.591 s |
| C (`clang -O3`) | 0.568 to 0.679 s | 0.604 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.581 to 0.734 s | 0.644 s |
| Kāra (`karac build`) | 0.581 to 0.746 s | 0.661 s |
| Go | 0.996 to 1.171 s | 1.074 s |
| Python | 13.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte, so the two Kāra rows are one program timed twice. Kāra takes
about 1.14x overflow-checked Rust's time, the equal-safety comparison,
and C about 0.94x Kāra's; the spread of the runs overlaps all three.
Go takes about 1.7x and Python about 21x. Go searches with
`sort.Search`, the library's binary search, which halves the span with
a branch and calls a closure at each step; that is likely most of its
gap, inferred from its source, not measured.
