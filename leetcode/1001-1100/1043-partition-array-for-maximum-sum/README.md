# 1043. Partition Array for Maximum Sum

Given an integer array `arr`, partition the array into (contiguous)
subarrays of length **at most** `k`. After partitioning, each subarray
has its values changed to become the maximum value of that subarray.

Return the largest sum of the given array after partitioning. Test
cases are generated so that the answer fits in a **32-bit** integer.

```
arr = [1,15,7,9,2,5,10], k = 3              ->  84   ([15,15,15,9,10,10,10])
arr = [1,4,1,5,7,3,6,1,9,9,3], k = 4        ->  83
arr = [1], k = 1                            ->  1
```

**Constraints:** `1 <= arr.length <= 500`; `0 <= arr[i] <= 10^9`;
`1 <= k <= arr.length`.

The harness and the bench go past the 32-bit promise: their values run
to `10^9` on arrays of up to 500, so an answer can reach `5 * 10^11`,
which every implementation holds in a 64-bit integer.

## Approaches

Every arm rests on one recurrence. The last part of the first `i`
values is some `j` of them, 1 to `k`, and becomes `j` copies of their
largest, so the best for the first `i` values is the largest, over `j`,
of the best for the first `i - j` plus `j` times that largest value.

| file | mechanism |
|---|---|
| `partition_max.kara` ★ | the table bottom-up: `best[i]` for each prefix, the part's largest value kept as a running maximum while `j` grows. O(n k) |
| `partition_max_memo.kara` | top-down over the suffixes: a recursive `most(i)` for the values from `i` on, each kept in a `Vec[Option[i64]]` memo. O(n k) |
| `partition_max_ring.kara` | the table kept to its last `k + 1` entries, a ring indexed by `i` modulo `k + 1`. O(n k) time, O(k) space |
| `partition_max_forward.kara` | the table filled the other way: each finished `best[i]` offers `best[i] + j * largest` to `best[i + j]`. O(n k) |
| `partition_max_iter.kara` | each entry one expression: `(1..k.min(i) + 1).map(..).max()`, each part's largest taken afresh as `arr[i - j..i].iter().max()`. O(n k^2) |
| `differential.kara` | the five arms against every partition tried in turn, five properties |

Every arm prints the same 19 lines: the answers for ten arrays,
LeetCode's three examples among them, with the first example at `k = 1`
(the plain sum) and `k = 7` (the whole array as one part), a falling and
a rising run, five equal values, one `10^9` among zeros and an
alternating run; for every array of 1 to 6 values from 0 to 3, with
every `k`, the number of cases, the sum of the answers and a checksum;
the same for 300 random arrays of 1 to 100 values up to `10^9`; and the
two largest, 500 values of `10^9` at `k = 1` and the values 0 to 499 at
`k = 500`. `partition_max.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each of the `n - 1` gaps between values is a cut or
not, a set of cuts whose parts are all at most `k` long is a partition,
and the answer is the largest worth over every partition. It checks
7572 cases: every array of 1 to 5 values from 0 to 3 with every `k`
(6372), 1000 random arrays of 6 to 10 values and 200 of 11 to 60, half
of them with values up to 9 and half up to `10^9`, each with a random
`k`. The 7372 of at most 10 values have every partition tried.

| | property |
|---|---|
| P1 | the answer is the best over every partition, on at most 10 values |
| P2 | the answer lies between the sum of the values and `n` times the largest, is the sum at `k = 1` and is `n` times the largest at `k = n` |
| P3 | a longer limit, `k + 1`, never gives less |
| P4 | the array reversed changes nothing |
| P5 | a second array put after this one gives at least the two answers added |
| P6 | each arm agrees with at least two of the other four |

The differential prints `7572 cases (7372 with every partition tried):
checksum 19037199, 218720 checks over 5 arms: 0 failures` under `karac
__mir-run` (15 s), `karac __mir-llvm-run` and `karac __mir-llvm-asan`
with no error, and the same line under `karac run` and from a `karac
build` binary. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with a 120 s limit.
Fifteen are kept, three to each arm. All fifteen are killed, each fails
the same way under both backends, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: parts of at most `k - 1` | P1 5689, P2 2296, P6 5814 |
| M2 | ★: parts of up to `k + 1` | P1 4194, P2 1492, P6 4310 |
| M3 | ★: `best[n - 1]` returned, one value short | P1 6745, P2 3108, P4 3867, P6 6944 |
| M4 | memo: the empty suffix worth 1 | P1 7372, P2 4485, P5 2804, P6 7572 |
| M5 | memo: the longest part taken, not the best | P1 1942, P3 697, P4 3125, P5 757, P6 2076 |
| M6 | memo: the rest always starts one value on | P1 5824, P2 5845, P4 5120, P6 6020 |
| M7 | ring: parts of at most `k - 1` | P1 7357, P2 4481, P4 3523, P6 7557 |
| M8 | ring: the entry one too late read | P1 7194, P2 7114, P4 5068, P5 435, P6 7394 |
| M9 | ring: the last value taken for the largest | P1 3807, P2 962, P4 5014, P6 3993 |
| M10 | forward: no offer from the prefix one value short of the end | P1 2229, P2 1507, P4 1248, P5 11, P6 2241 |
| M11 | forward: `+` for `*` | P1 6432, P2 3718, P6 6632 |
| M12 | forward: each offer compared with `best[i]` | P1 6291, P2 2442, P4 4269, P5 392, P6 6489 |
| M13 | iter: the worst length, `min` for `max` | P1 5824, P2 1468, P6 6020 |
| M14 | iter: always the entry one back | P1 5824, P2 5844, P4 5120, P6 6020 |
| M15 | iter: parts counted `i` long | P1 7234, P2 7236, P4 6798, P6 7434 |

P1 and P6 kill all fifteen, P2 fourteen, P4 ten, P5 five and P3 one.
P2 misses only M5, which takes the longest part allowed: at `k = 1`
that is the sum and at `k = n` the whole array, the two ends P2 pins.
M5 is also the one edit P3 sees, since a longer limit changes which
part is longest. P4 misses five: the ★ arm's limits off by one (M1,
M2), which are as wrong read from either end, M4's extra 1, and the
arithmetic slips M11 and M13. It catches the ring arm's limit off by
one (M7), because there `k.min(i)` caps the short prefixes too, so the
array's start loses parts its end keeps. P5 sees five, among them M4,
whose extra 1 is counted once for the joined array and twice for the
two apart.

Fifteen other edits were set aside. Three are equivalent. The ring arm
works with `k` slots as well as `k + 1`: `best[i]` reads the entries
`i - 1` down to `i - k`, which fall in `k` different slots, and the
slot it shares with `best[i - k]` is written only after that last read.
Starting the ring arm's maximum at the entry before is harmless, since
the best never shrinks as the prefix grows, and the forward arm's `>=`
for `>` only rewrites an entry with its own value. Six fail exactly as
a kept one does: the memo arm's limit of `k - 1` (as M1), the forward
arm's limit of `k + 1` (as M2), the memo arm's last part never reaching
the end and the ring arm's last entry one short (both as M3), the
iterator arm's empty prefix worth 1 (as M4) and its slice of the last
value alone (as M9). Six fail in ways of their own: the ★, memo and
forward arms taking a part's last or first value for its largest
(three that fail exactly alike), the ★ arm keeping the longest part and
counting every part `k` long, and the iterator arm skipping parts of
one value, which panics on an `unwrap` of `None` under both backends.

## Verification

Every arm prints the same output as `partition_max.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error. `karac run` and a `karac build` binary print the same output
for every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara
`c2a612b69c`, which has the fix below. Under `karac __mir-run` the arms
take 0.8 s (forward) to 1.7 s (memo), and 26 s for the iterator arm,
which takes each part's largest afresh: its last case, 500 values at
`k = 500`, reads about 21 million slice elements. Taking a slice's
maximum with `.iter().max()` costs 2.6 times a hand loop over the same
elements there (23 s against 8.8 s on that case alone, measured on an
earlier build).

The arms went through the Mend loop clean. Probing a Rust-shaped arm
turned up one gap, fixed in kara at `c2a612b69c` (B-2026-11-04-5): Rust's
`::` paths had no fix. `std::cmp::max(a, b)`, `Vec::new()`, `i64::MAX`,
`String::from(..)` and a match arm's `Dir::Up =>` each drew only
"Expected `;` (or `=>`), found `::`". Worse, after `std::cmp::max` the
recovery misread the block and offered a `;` after the function's tail
`dp[n]`, which `karac fix` applied, turning the return value into a
statement; and `std::mem::swap(..)` at the start of a statement drew a
`;` after `std`. Each path is now one diagnostic whose fix writes the
Kāra spelling, `max(a, b)`, `Vec.new()`, `i64.MAX`, `Dir.Up`. An import
path, `import std::collections::HashMap;`, still has no fix, and the
row stays open for it.

## Benchmarks

The bench builds 400 random arrays of 500 values up to `10^9` once in
all five languages, each with a random `k` of 1 to 50, then runs the ★
arm over every array 40 times, adding up the answers and folding each
into a checksum. Every implementation prints `400 arrays of 500 values,
40 rounds: total 7547687588636080, checksum 998124652`. Doubling the
rounds doubles C's time (0.82 to 0.96 s against 0.41 to 0.43 s), so no
compiler hoists the table out of the round loop. Each implementation
keeps the ★ arm's table, one growable array of `n + 1` entries built
afresh on every call, and its inner loop of a running maximum and one
multiply-add a step, about 5 million steps a round.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.379 to 0.434 s | 0.412 s |
| Kāra (`karac build`) | 0.464 to 0.487 s | 0.479 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.472 to 0.492 s | 0.485 s |
| Rust (`rustc -O`) | 0.467 to 0.533 s | 0.503 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.445 to 0.529 s | 0.513 s |
| Go | 0.676 to 0.741 s | 0.720 s |
| Python | 31 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(its user time, 0.47 s, matches its real time) and runs as fast as the
sequential one.

Kāra took 0.95 times Rust's median time under overflow checks, and 1.18
times C's.
