# 985. Sum of Even Numbers After Queries

You are given an integer array `nums` and an array `queries` where
`queries[i] = [val_i, index_i]`.

For each query `i`, first, apply `nums[index_i] = nums[index_i] + val_i`,
then print the sum of the even values of `nums`.

Return an integer array `answer` where `answer[i]` is the answer to the
`i`th query.

```
nums = [1,2,3,4], queries = [[1,0],[-3,1],[-4,0],[2,3]]  ->  [8,6,2,4]
nums = [1], queries = [[4,0]]                            ->  [0]
```

**Constraints:** `1 <= nums.length <= 10^4`;
`-10^4 <= nums[i] <= 10^4`; `1 <= queries.length <= 10^4`;
`-10^4 <= val_i <= 10^4`; `0 <= index_i < nums.length`.

## Approaches

The queries are `(val, index)` tuples, and every arm works on its own
copy of `nums`.

| file | mechanism |
|---|---|
| `sum_even_after_queries.kara` ★ | a running sum: the sum of the even values is kept as the queries change them; a query takes its value out of the sum if it was even, adds to it, and puts it back if it is even now. O(n + q) |
| `sum_even_after_queries_fenwick.kara` | a Fenwick tree: each place holds its value when even and 0 when odd, a query changes its place by the difference, and the answer is the sum over every place. O((n + q) log n) |
| `sum_even_after_queries_blocks.kara` | sums by block: the values are cut into blocks of about the square root of n, each keeping the sum of its even values; a query sums its block again from scratch and the answer adds up the block sums. O(q sqrt(n)) |
| `sum_even_after_queries_parity.kara` | four cases of parity: a `match` on whether the place was even before and is even after picks the change, the amount, the new value, minus the old one or nothing; the first sum is a `filter` and `sum` over the values. O(n + q) |
| `sum_even_after_queries_reverse.kara` | backwards from the end: every query is applied first, so the even sum of the final values is the last answer, and undoing the queries from the last to the first gives each answer before it. O(n + q) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's two
examples and eight more: a query that adds nothing; odd values turned
even one by one; negative values, among them a negative odd value
turned even; one value stepped back and forth between odd and even;
LeetCode's extreme values cancelling; zeros; and two cases of
LeetCode's largest size, 10,000 values and 10,000 queries, one of small
values and one of 10,000s that queries keep taking to 0 and back. Then
the answers' count, sum and checksum over random cases: 300 of up to 8
values and 8 queries between -10 and 10, 3,000 of up to 40 between
-1,000 and 1,000, and three of the largest size between -10,000 and
10,000. `sum_even_after_queries.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each query applied in turn, then every value added up that is
even. It checks 3,200 cases: 3,000 of up to 8 values and 8 queries
between -10 and 10 against the statement, and 200 of up to 300 values
and 300 queries up to LeetCode's 10,000 against the other properties.

| | property |
|---|---|
| P1 | the statement's answers, on the first 3,000 cases |
| P2 | a query that adds nothing, put in after a random query, repeats the answer before it |
| P3 | with every value and amount doubled, every value is even, so each answer is twice the sum of all the values after that query |
| P4 | the last query undone by one more query gives back the answer before it, or, with one query, the even sum of the values as given (the arm's own answer to a query adding nothing) |
| P5 | the queries in reverse order end at the same sum |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases of 43949 values and 43810 queries: sum
-5563176114, checksum 197965151, 95000 checks over 5 arms: 0 failures`
under `karac __mir-run` (7.7 s) and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the old value never taken out | P1 2558, P2 1523, P3 3185, P4 2224, P5 1996, P6 2757 |
| M2 | ★: the odd values summed at the start | P1 2903, P3 3102, P6 3103 |
| M3 | ★: an odd value put back | P1 2983, P2 3076, P3 3183, P4 3133, P5 2206, P6 3183 |
| M4 | fenwick: the update climbs by one place | P1 1432, P3 1687, P6 1625 |
| M5 | fenwick: the total misses the last place | P1 1940, P3 3148, P6 2085 |
| M6 | fenwick: every value counted | P1 2877, P6 3077 |
| M7 | blocks: a block summed one place short | P1 2146, P2 220, P3 3096, P4 209, P6 2344 |
| M8 | blocks: the block sum added to, not redone | P1 2798, P2 2341, P3 3185, P4 2662, P5 2429, P6 2998 |
| M9 | blocks: a place found in the wrong block | P1 1155, P2 131, P3 1666, P4 129, P5 548, P6 1350 |
| M10 | parity: even to even adds the new value | P1 1860, P2 1523, P3 3185, P4 948, P5 1734, P6 2058 |
| M11 | parity: odd to even adds the amount | P1 2028, P4 1500, P5 1430, P6 2227 |
| M12 | parity: even to odd takes nothing away | P1 1987, P4 1385, P5 1487, P6 2185 |
| M13 | reverse: the last answer left out | P1 2800, P2 962, P3 3189, P4 2361, P6 3000 |
| M14 | reverse: a query redone, not undone | P1 2222, P3 2810, P4 1345, P6 2420 |
| M15 | reverse: each answer taken after undoing | P1 2986, P2 3048, P3 3186, P4 3064, P5 2711, P6 3186 |

P1 and P6 kill all fifteen, P3 twelve (all but M6, M11 and M12), P4
eleven, and P2 and P5 eight each. M6 adds up every value, odd or even,
and every property but the statement's is blind to it: doubling makes
every value even, where every value is what M6 adds anyway; a query
adding nothing, a query undone and the queries reordered all keep a
plain total as they keep the even one. M11 and M12 go wrong only when a
query changes a value's parity, which doubling never does, so P3 passes
them. P5 compares only the last answer, which M2, M4, M5 and the others
that miscount the same way at every query get wrong by the same rule
in either order.

Ten other edits were tried and set aside. Two failed exactly the same
checks as a kept one: fenwick changing its place by the new part
alone, as M1; and parity summing the odd values at the start, as M2.
Seven were sound but beyond three an arm: ★ putting back the amount
rather than the value; ★ taking an odd negative value for even (`% 2
!= 1`, which a negative odd value's remainder of -1 passes); fenwick
reading the old part after the query; blocks summing the odd values at
the start; parity with before and after swapped; reverse summing the
odd values at the end; reverse never taking the old value out. One
survived and is equivalent: blocks one place smaller, which changes
only how the values are cut, and any cut gives the same sums.

## Verification

Every arm prints the same output as `sum_even_after_queries.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 0.6 s (★) to 7.7 s (blocks, which
at every query of the largest cases sums a block of 100 values and then
the 100 block sums), and the differential 7.7 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

The reverse arm first applied the queries with `for (val, index) in
queries.iter() { a[*index] += *val; }`. Every tool accepted it, and
accepts it without the stars too, although `karac check` refuses the
same `*` on `let (v, i) = queries.iter().next().unwrap()`; under the
spec the parts of a borrowed tuple are copied, so the arm writes no
`*`. The disagreement is kara's `B-2026-10-24-36`, first seen in kata
983.

The bench first took each case with `let (nums, queries) =
cases[(r + i) % 20]`. `karac check` refused the move out of the index
and offered a borrow, a copy or `swap`; `karac fix` would apply the
copy, `.clone()`, which would time a copy of 20,000 values a call, so
the bench borrows the case with `ref` instead.

## Benchmarks

The bench runs the ★ arm in all five languages. The program makes 20
cases of LeetCode's largest size, 10,000 values and 10,000 queries with
values and amounts between -10,000 and 10,000, once. In each of 300
rounds it runs the arm on every case, each round starting from a
different one, and folds each last answer into a sum and a checksum.
Every implementation prints `300 rounds over 20 cases of 10000 values
and 10000 queries: sum -85026192600, checksum 830759833`. Each call
copies the 10,000 values, sums the even ones, and answers the 10,000
queries into a fresh list.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.835 to 0.943 s | 0.856 s |
| Rust (`rustc -O`) | 0.987 to 1.137 s | 1.039 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.114 to 1.226 s | 1.176 s |
| Go | 1.320 to 1.583 s | 1.390 s |
| Python | 15.3 s | |
| Kāra (`karac build --mir`) | 1.126 to 1.262 s | 1.203 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 13 times
Kāra's.

v2 took 1.02 times Rust's median time under overflow checks and 1.41
times C's. Under valgrind's cachegrind v2 ran 2,908 million
instructions and 1,084 million branches with 0.19 million
mispredicted, Rust with overflow checks 2,501 million, 968 million and
0.15 million, and C 1,831 million, 676 million and 60.1 million. C
mispredicts about once per random value it tests for evenness, so it
branches on the test, while v2 and Rust hardly mispredict at all, which
fits their computing the even part without a branch (inferred, not
traced); C still runs fewer instructions and finishes first.
