# 1601. Maximum Number of Achievable Transfer Requests

We have `n` buildings numbered from `0` to `n - 1`. Each building has a
number of employees. It's transfer season, and some employees want to
change the building they reside in.

You are given an array `requests` where `requests[i] = [fromi, toi]`
represents an employee's request to transfer from building `fromi` to
building `toi`.

All buildings are full, so a list of requests is achievable only if for
each building, the net change in employee transfers is zero. This means
the number of employees leaving is equal to the number of employees
moving in.

Return the maximum number of achievable requests.

```
n = 5, requests = [[0,1],[1,0],[0,1],[1,2],[2,0],[3,4]]  ->  5
n = 3, requests = [[0,0],[1,2],[2,1]]                    ->  3
n = 4, requests = [[0,3],[3,1],[1,2],[2,0]]              ->  4
```

**Constraints:** `1 <= n <= 20`; `1 <= requests.length <= 16`;
`requests[i].length == 2`; `0 <= fromi, toi < n`.

## Approaches

| file | mechanism |
|---|---|
| `transfers.kara` ★ | every subset of the requests as a bit mask, a mask no larger than the best skipped by `count_ones`; the rest checked by the net change of each building in a `Vec.filled(n, 0)`. O(2^r (r + n)) |
| `transfers_backtrack.kara` | each request granted or not in turn, one `Vec[i32]` of net changes updated and undone on the way down a recursion with `mut ref` parameters, a branch stopped when granting every request left cannot beat the best. O(2^r n) |
| `transfers_largest.kara` | every mask collected and sorted by `count_ones`, most first, with `sort_by`; `find` takes the first whose requests balance. O(2^r (r + n)) |
| `transfers_solution.kara` | LeetCode's Rust template (an associated `fn dfs` over `&Vec<Vec<i32>>`, a `&mut Vec<i32>` of net changes and a `&mut i32` best, `usize` indices), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one request from a building to itself, one request with no
return, sixteen requests in a ring), then the total and a checksum for
3000 random problems of up to 4 buildings and 5 requests, 300 of up to 8
and 10, and 10 of up to 20 and 16. `transfers.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every list of the requests kept in order, built by taking or
leaving each in turn, and a list achievable when, sorted, the buildings
its employees leave are the buildings they move to, so each building
loses as many as it gains. It checks 3000 problems of 1 to 4 buildings
and 1 to 7 requests, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the requests in reverse order leave the answer |
| P3 | every request turned round leaves the answer |
| P4 | a request from a building to itself added raises the answer by one |
| P5 | the buildings renumbered back to front leave the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 720661437, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M1, a subset taken as balanced when no building gains, was
equivalent: the net changes always add up to zero, so none above zero
means all at zero.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an employee counted back at the building they leave | P1 1854, P6 1854 |
| M2 | ★: the last request never granted | P1 1891, P2 1051, P4 1389, P6 1891 |
| M3 | ★: leaving counted as arriving | P1 2581, P4 3000, P6 2581 |
| M4 | backtrack: a branch that can only tie or win by one stopped | P1 596, P2 50, P4 992, P6 596 |
| M5 | backtrack: an arrival not undone | P1 1435, P4 1854, P6 1435 |
| M6 | largest: the masks sorted fewest first | P1 2581, P4 3000, P6 2581 |
| M7 | largest: a mask's requests read from its zero bits | P1 1854, P6 1854 |
| M8 | template: the last balanced subset kept, not the largest | P1 2581, P4 3000, P6 2581 |
| M9 | template: a granted request counted twice | P1 2581, P4 3000, P6 2581 |
| M10 | largest: the answer capped at 4 | P1 678, P4 1020, P6 678 |

## Benchmarks

The bench draws 100 problems of 16 requests among 6 buildings first,
then answers each by the ★ arm, in all five languages. Every
implementation prints `100 problems of 16 requests among 6 buildings:
total 957, checksum 726103134`. The C mirror allocates a fresh array of
net changes for each mask, as the Kāra `Vec.filled` does.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.173 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.252 s |
| Rust (`rustc -O`) | 0.257 s |
| Kāra (`karac build`) | 0.258 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.269 s |
| Go | 0.377 s |
| Python | 4.9 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.236 s and 0.239 s on one run).

## Verification

All four arms print the same output as `transfers.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★ arm was written in Kāra and checked as written. The backtracking
arm wrote Rust's `let mut best = 0; choose(.., mut best); best` with
`best: mut ref i32`, and it is refused as an `i64`, though design.md §8
has an argument fix a literal's type (B-2026-11-17-130); `karac fix`
typed it `best: i32`. The largest arm wrote
`sort_by_key(|m| Reverse(m.count_ones()))`; `karac check` said Kāra has
no `Reverse` and a descending sort compares the keys the other way
round, and it was rewritten by hand as `sort_by(|a, b|
b.count_ones().cmp(a.count_ones()))`. Its `find(|m| .. **m)` became
`*m` by `karac fix`, as `find` hands the closure a `ref i64`.

The Rust template took one `karac fix`, of 35 edits: `struct Solution;`
to `struct Solution {}`, the `Vec<..>` types to `[..]`,
`vec![0; n as usize]` to `Vec.filled(n, 0)`, `let mut ans = 0` typed
`i32` (B-2026-11-17-130 again), `&Vec<Vec<i32>>` to `Vec[Vec[i32]]`,
`&mut` parameters to `mut ref` and the calls' `&mut` to `mut`, `usize`
to `i64`, the `|&x|` pattern to `|x|`, and `Self::` to `Solution.`. It
then checks and agrees with no hand edit.
