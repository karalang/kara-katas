# 857. Minimum Cost to Hire K Workers

There are `n` workers; worker `i` has a quality `quality[i]` and a
minimum wage `wage[i]`. Hire exactly `k` of them as a paid group, where
every worker is paid in proportion to their quality compared with the
others in the group, and every worker is paid at least their minimum
wage. Return the least amount of money that forms such a group; answers
within `10^-5` of the true one are accepted.

```
quality = [10,20,5], wage = [70,50,30], k = 2          ->  105.00000
quality = [3,1,10,10,1], wage = [4,8,2,2,7], k = 3     ->  30.66667
```

**Constraints:** `1 <= k <= n <= 10^4`, `1 <= quality[i], wage[i] <=
10^4`.

## Approaches

| file | mechanism |
|---|---|
| `mincost_to_hire_workers.kara` ★ | in a group paid fairly, every worker is paid one rate per unit of quality, which must reach the highest `wage / quality` in the group, so the group costs that rate times its total quality. Taking the workers in order of `wage / quality`, the worker just taken sets the rate for any group of the workers so far, and the cheapest such group has the k smallest qualities: a max-heap keeps them with their sum, dropping the largest whenever it holds more than k. O(n log n) |
| `mincost_to_hire_workers_brute.kara` | every worker in turn as the one who sets the rate: the others it can hire are those whose rate is no higher, and the cheapest group takes the k - 1 smallest of their qualities besides its own. O(n^2 log n) |
| `mincost_to_hire_workers_sorted.kara` | the ★ arm's walk, with the k smallest qualities so far in a sorted vector: a smaller quality is inserted where a binary search puts it and the largest is dropped, and a worker whose quality would not be kept is costed with it in place of the largest. O(n log n + n k) |
| `mincost_to_hire_workers_counts.kara` | the ★ arm's walk, with the k smallest qualities held as a count for each quality in a sorted map, the largest found as the map's `floor` of a bound above every quality. O(n log n) |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm compares rates and costs as exact fractions, by
cross-multiplying, and divides only the answer; the largest product, a
wage times a total quality times a quality, is below `10^16`. So every
arm returns the same correctly rounded `f64`, and the differential can
compare answers with `==`.

Every arm prints the same 11 lines: LeetCode's two examples; seven more
(one worker, three alike, three at one rate, the cheapest and the
dearest worker of a pair, three workers at the largest values, and a
group of 4 from 8); 1,000 random workers with values to `10^4` and `k =
300`; and 300 random groups of up to 30 workers with values to a random
top from 1 to 100, with the sum of their costs. Costs print to five
decimals. `mincost_to_hire_workers.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every group of exactly k workers, each paid the group's
highest wage per unit of quality times their own quality, which pays
everyone in proportion to quality and at least their wage, and the
cheapest group's cost. Its 1,600 cases of 1 to 10 workers come in four
kinds of 400: values from 1 to 5, so that many rates are equal, values
to 100, values to `10^4`, and workers at one of two rates, wage equal to
quality or twice it. Their costs sum to 45,399,029.83.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the workers in a random order give the same answer |
| P3 | every wage multiplied by the same factor, 1 to 5, multiplies the answer by it, to within `10^-9` of it |
| P4 | every quality multiplied by the same factor gives the same answer |
| P5 | hiring one more worker costs no less |
| P6 | one more worker to choose from costs no more |

It prints `1600 cases, costs sum to 45399029.82948, 38400 checks over 4
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the heap keeping the largest qualities | P1 427, P2 171, P6 107 |
| M2 | ★: one worker too many kept | P1 427, P2 171, P6 107 |
| M3 | ★: workers taken in order of wage alone | P1 877, P2 115 |
| M4 | brute: a worker at the same rate not hired | P1 316, P3 132, P5 59, P6 39 |
| M5 | brute: the rate setter's own quality left out | P1 1600 |
| M6 | brute: the k - 1 largest others taken | P1 371, P6 173 |
| M7 | sorted: the binary search reading the vector upside down | P1 427, P2 171, P6 107 |
| M8 | sorted: the sum not lowered when the largest is dropped | P1 427, P2 171, P6 107 |
| M9 | sorted: workers taken from the highest rate | P1 1070 |
| M10 | counts: the smallest quality dropped | P1 427, P2 171, P6 107 |
| M11 | counts: a dropped quality's count not lowered | P1 55, P2 1, P3 22, P5 9 |
| M12 | counts: a quality's count reset to 1 | P1 17, P6 3 |

P1 kills all twelve. M1, M2, M7, M8 and M10 fail the same cases: each
stops the walk from dropping the largest quality it holds (a heap or map
that drops the smallest, one worker too many, a sum that never falls, a
vector that is no longer sorted), and most likely each then answers with
the first k workers in order of rate (not traced). P4 kills nothing,
since every arm compares rates by cross-multiplying and a common factor
in the qualities cancels. M12, which forgets how many workers share a
quality, fails only 20 cases, most likely those where the walk drops a
quality that two of the workers it holds share (not traced).

## Verification

Every arm prints the same output as `mincost_to_hire_workers.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `ccbab82462`, and the runtime archives were
rebuilt there, after the day's runtime change. Under `karac __mir-run`
the ★, sorted and counts arms take 0.2 to 0.3 s, the brute arm 1.1 s and
the differential 3.2 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the brute arm through `karac run
--interp`, `karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build
with the same output. They refuse the other three arms, the differential
and the bench program at `let i = *i` over `order.iter()`, saying an
`i64` is copied, where v2 yields a reference to each element. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 16 sets
once, each of LeetCode's most workers, `10^4`, with quality and wage
from 1 to `10^4`; set `g` hires `k = 1 + 600 g`. Each of 600 rounds
costs the next set. C has no heap, so its twin writes one out, and it
sorts with `qsort`, whose comparator reads the set through two
file-level pointers. Every implementation prints `600 rounds of 16 sets:
costs sum to 31781247916.25857`, the Kāra program under `karac
__mir-run` included, in 214 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.06 to 1.28 s |
| Rust (`rustc -O`) | 0.42 to 0.53 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.41 to 0.54 s |
| Go | 2.61 to 2.75 s |
| Python | 15.5 to 16.6 s |
| Kāra (`karac build --mir`) | 0.86 to 1.20 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.00 s, against Rust's
0.47 (0.43 under overflow checks), C's 1.07 and Go's 2.66: 2.33 times
Rust's time under overflow checks, 0.93 times C's and 0.38 times Go's.
Under valgrind's cachegrind Rust runs 3.27 billion instructions and 0.50
billion branches, with 18 million mispredicted; v2 runs 5.15 billion,
1.22 billion and 33 million, and C 4.44 billion, 0.69 billion and 67
million. 81 million of C's branches are indirect, one call of the
`qsort` comparator per comparison, where Rust and v2 sort with the
comparison inlined; that most likely explains why C trails Rust here
(not traced). Go sorts with `sort.SliceStable`, whose closure is also
called per comparison. Built for `x86-64-v3`, the target `karac build`
uses, C takes 1.01 to 1.15 s and Rust with overflow checks 0.40 to 0.46
s, against v2's 0.90 to 1.05 s in the same five interleaved runs. Python
takes 15.5 s, about 15 times C's time. The comparison with C and Rust
waits until after M4.
