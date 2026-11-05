# 1054. Distant Barcodes

In a warehouse, there is a row of barcodes, where the `i`th barcode is
`barcodes[i]`.

Rearrange the barcodes so that no two adjacent barcodes are equal. You may
return any answer, and it is guaranteed an answer exists.

```
barcodes = [1,1,1,2,2,2]      ->  [2,1,2,1,2,1]
barcodes = [1,1,1,1,2,2,3,3]  ->  [1,3,1,3,1,2,1,2]
```

**Constraints:** `1 <= barcodes.length <= 10000`; `1 <= barcodes[i] <= 10000`.

## Approaches

A rearrangement exists exactly when no barcode fills more than every other
place, `(n + 1) / 2` of them. Laying the most common barcode on places 0,
2, 4, ... and every other value after it, each value's copies together, on
the even places left and then the odd ones, never puts two equal barcodes
side by side: a value can meet itself only by wrapping from the last even
place round to place 1 and running on, which takes more copies than the
most common barcode has.

| file | mechanism |
|---|---|
| `barcodes.kara` ★ | counts in a `Vec` up to the largest barcode, the most common first on the even places, then the others in value order, wrapping to place 1. O(n + V) for barcodes up to V |
| `barcodes_heap.kara` | a `PriorityQueue.max_first()` of `(count, value)`: each place takes the top unless it was just placed, then the next, and the first goes back. O(n log k) for k distinct barcodes |
| `barcodes_sort.kara` | the barcodes sorted by `(-count, value)` with `sort_by_key`, dealt to the even places and then the odd ones. O(n log n) |
| `barcodes_iter.kara` | counts by `fold` into a `SortedMap`, a stable `sort_by` on the count, `flat_map` of `repeat(v).take(c)`, and the result `zip`ped with `(0..n).step_by(2).chain((1..n).step_by(2))`. O(n + k log k) |
| `barcodes_greedy.kara` | the smallest answer in dictionary order, place by place: with an odd `m` places left, a barcode holding `(m + 1) / 2` of them must go now, and otherwise the smallest barcode but the one just placed keeps the rest possible. O(n k) |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 14 lines: whether its answers are valid for
LeetCode's two examples and eight more; how many of 3000 random arrays of 1
to 8 barcodes of 1 to 3, and of 300 arrays of 1 to 2000 barcodes of 1 to
50, can be rearranged and how many answers were valid; and two arrays of
10000, the limit: 5000 of one barcode and the rest of six others, and 5000
of one barcode followed by 5000 of another. An answer is valid when it
holds the same barcodes and no two next to each other are equal. The arms
may answer differently, so the lines report validity, not the answers;
the differential compares the answers themselves. `barcodes.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: arrangements are tried in dictionary order, each place taking
the smallest barcode left that differs from the one before and the search
backing up when none does, and the first one it completes is the smallest
valid arrangement. It checks 3000 random arrays that can be rearranged:
2000 of 1 to 8 barcodes of 1 to 3, where barcodes repeat, and 1000 of 1 to
30 of 1 to 100.

| | property |
|---|---|
| P1 | the answer holds the same barcodes, and no two next to each other are equal |
| P2 | the greedy arm's answer is the first arrangement the search in dictionary order finds, and no arm's answer is smaller |
| P3 | the barcodes reversed, or sorted, give the same answer |
| P4 | every barcode 3 larger, or doubled, moves the answer the same way |
| P5 | n + 1 copies of a new barcode, added to n barcodes, take every even place, and the answer is valid |

P3 holds because every arm reads only how many of each barcode there are,
and breaks ties by value. P4 holds because every arm compares barcodes and
counts them, and adding 3 or doubling keeps their order. P5's new barcode
fills `(m + 1) / 2` of the `m = 2n + 1` places, so it can sit only on the
even ones.

The differential prints `3000 arrays: checksum 361596854, 75000 checks
over 5 arms: 0 failures` under `karac __mir-run` (12 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-seven edits to the differential, six to each arm and seven more to
the heap and greedy arms, each run under `karac __mir-run` and `karac
__mir-llvm-run`. Fifteen are kept, three to each arm. All fifteen are
killed, each fails the same way under both backends, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the largest barcode never the most common | P1 212, P2 212, P5 3000 |
| M2 | ★: one step past a used-up barcode | P1 2299, P2 1531, P4 2633, P5 1679 |
| M3 | ★: the wrap back to place 0 | P1 2633, P2 638, P4 2633, P5 3000 |
| M4 | heap: a barcode put back only with two left | P1 1973, P2 316, P5 3000 |
| M5 | heap: each barcode placed twice | P1 3000, P2 397, P5 3000 |
| M6 | heap: a copy of the first lost when the second takes its place | P1 468, P2 57, P5 2633 |
| M7 | sort: least common first | P1 485, P2 259, P5 3000 |
| M8 | sort: ties left in the order given | P1 345, P2 62, P3 1990 |
| M9 | sort: the wrap back to place 0 | P1 2633, P2 526, P4 2633, P5 3000 |
| M10 | iter: in value order, not by count | P1 419, P2 419, P5 3000 |
| M11 | iter: the odd places every place | P1 2091, P2 117, P4 2091, P5 2633 |
| M12 | iter: one copy short | P1 3000, P2 1661, P5 3000 |
| M13 | greedy: the barcode just placed allowed | P1 1426, P2 1426 |
| M14 | greedy: the largest, not the smallest | P2 2317 |
| M15 | greedy: a used-up barcode kept | P1 1576, P2 1576, P5 2633 |

P2 kills all fifteen, P1 fourteen, P5 twelve, P4 four and P3 one. M14 is
seen only by P2: any barcode but the one just placed keeps the rest
possible, so taking the largest still gives a valid answer, only not the
smallest. P5 sees the edits that can lose the most common barcode's hold
on the even places; it holds for M8, whose ties sit inside one count, and
for M13 and M14, whose forced barcode still goes on every even place. P4 sees the edits whose
answer depends on where the array happens to end (M2, M3, M9, M11): adding
3 or doubling keeps every comparison, but the wrap and the step past a
used-up barcode follow the values' gaps and the array's length. P3 sees
only M8, the one edit that reads the order the barcodes came in.

Twenty-two other edits were set aside. Five fail exactly as a kept one
does: the ★ arm starting from the smallest barcode, or never finding the
most common, and the sort arm sorting by value alone, as M10; the iter arm
taking the least common first, as M7; and the greedy arm reading its
answer backwards, as M14. Two fail as a pair with no kept twin: the ★ and
sort arms filling every place in turn. Three fail in ways of their own:
the heap arm never checking the barcode just placed, or putting the second
back with none left, and the greedy arm avoiding the first barcode placed
rather than the last. Two are equivalent: the sort and iter arms breaking
ties by the larger value, which is as valid and moves the same way. Nine
crash, each the same way on both backends: six heap edits (fewest copies
first, the heap ordered by value, the first barcode dropped or the second
put back late, the barcode just placed placed again, the first barcode
compared rather than the last) empty the heap at a second pop ("called
unwrap() on None"), and three greedy edits to the forced barcode leave
only the barcode just placed. One does not compile: taking the even places
from the back with `(0..n).step_by(2).rev()` is "no method 'rev' on type
'IterStepBy'", filed as kara B-2026-11-05-35.

## Verification

Every arm prints the same output as `barcodes.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. The runs used a release build of kara with the fixes below. Under
`karac __mir-run` the arms take 2.1 s (★, sort) to 9.8 s (greedy).

The ★ arm and the harness drew one fix, `copied` to `cloned`. The other
four arms, written the way Rust writes them, reached a clean check through
`karac fix` and two compiler changes in kara `6808f01a9c`:

- `std::iter::repeat(*v).take(*c as usize)` was fixed to `repeat(*v)`,
  which named nothing ("undefined name 'repeat'"). Kāra had no `repeat`
  or `once`; the library now has both (library/iterators.md, Sources), and
  a program's own function of either name keeps it.
- `*counts.entry(b).or_default() += 1` was "no method 'or_default' on type
  'Entry'" with no fix. It now draws one that writes the default out:
  `or_insert(0)` for a number, `or_insert(Vec.new())` for a container.

The rest were existing fixes: `&&` to `and`, `&b` patterns and arguments
dropped, `Some(&b)` to `Some(ref b)`, `|mut m, b|` rebound in the body,
`*c as usize` to `*c`, `vec![0; n]` to `Vec.filled(n, 0)` and `.copied()`
to `.cloned()`.

## Benchmarks

The bench builds 200 arrays of 20000 barcodes once in all five languages:
1 to 9000 copies of one random barcode, then random barcodes of 1 to 10000.
It then runs the ★ arm on every array 25 times, folding every 97th place of each answer
into a checksum. Every implementation prints `200 arrays of 20000
barcodes, 25 rounds: total 14669100, checksum 683075750`.

Each implementation allocates the counts up to the largest barcode and the
answer afresh for every call, and reads and writes with bounds checks where
the language checks them.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with the karac that became kara
`6808f01a9c`, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.881 to 0.925 s | 0.899 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.905 to 0.960 s | 0.910 s |
| C (`clang -O3`) | 0.950 to 1.011 s | 0.974 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.049 to 1.125 s | 1.069 s |
| Rust (`rustc -O`) | 1.040 to 1.105 s | 1.074 s |
| Go | 1.174 to 1.211 s | 1.188 s |
| Python | 17.6 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.870 s) is below its real time.

Kāra took 0.85 times Rust's median time under overflow checks, and 0.93
times C's. Rust's user time (0.89 s) is close to Kāra's (0.89 s); the
rest of its real time is outside the program's own code, and was not
broken down. Go took 1.22 times C's.
