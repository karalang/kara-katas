# 362. Design Hit Counter

Design a hit counter that counts the hits received in the past five minutes.
`hit(timestamp)` records a hit at that second, and `getHits(timestamp)`
returns the number of hits in the past 300 seconds, that is at times `t'`
with `timestamp - 300 < t' <= timestamp`. Calls arrive in non-decreasing
timestamp order, and several hits may share a second.

```
hit(1); hit(2); hit(3)
getHits(4)     -> 3
hit(300)
getHits(300)   -> 4
getHits(301)   -> 3     (the hit at 1 is now 300 seconds old)
```

**Constraints:** `1 <= timestamp <= 2 * 10^9`; at most 300 calls.
**Follow-up:** what if the number of hits per second could be huge?

## Approaches

| file | mechanism | memory |
|---|---|---|
| `hit_counter.kara` ★ | a `VecDeque` of hit times, oldest at the front; a query drops the front while it is 300 or more seconds old, and the queue's length is the answer | the hits of one window |
| `hit_counter_buckets.kara` | 300 one-second buckets in a ring, each holding its second and a count; a hit into a bucket holding an older second resets it, and a query adds the buckets whose second is in the window | 300 buckets, whatever the hit rate (the follow-up) |
| `hit_counter_search.kara` | every hit kept in a sorted `Vec`; a query binary-searches for the first hit later than `t - 300` | every hit ever made |
| `differential.kara` | the three arms against an oracle that scans the whole hit history, 30,000 checks, five properties | — |

The search arm writes its own lower-bound loop. The library's
`binary_search` returns `Option[i64]`, the index of an equal element, and
there is no `partition_point` or `lower_bound` to find the first element
greater than a bound.

Every arm prints the same 11 lines: the LeetCode example, nine edge cases
(no hits, a hit counted at its own second, 299 and 300 seconds later, many
hits in one second, a long gap, a sliding window, queries between hits,
timestamps near `2 * 10^9`), and a checksum over 20,000 random calls. A line
shows the answer to each query. `hit_counter.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the three arms, plus an oracle that
keeps every hit and counts the ones in `(t - 300, t]` at each query. The
test draws 2,000 random sequences of 0 to 40 calls, half hits and half
queries. Each sequence picks small, medium or large steps between calls, so
some stay inside one window and others cross many. Every sequence ends with
two queries at its last time and one at least 300 seconds after its last
hit.

| | property |
|---|---|
| P1 | each arm gives the oracle's answer to every query |
| P2 | shifting every timestamp by the same amount changes no answer |
| P3 | no answer exceeds the number of hits made |
| P4 | two queries at the same second give the same answer |
| P5 | a query 300 or more seconds after the last hit returns 0 |

It prints `2000 cases, 30000 checks, 0 failures` under `karac __mir-run`.

## Mutation testing

Nine edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All nine are killed.

| # | mutation | how |
|---|---|---|
| M1 | queue: keeps a hit exactly 300 seconds old | P1 and P5, 568 failures |
| M2 | queue: drops a hit 299 seconds old | P1, 83 failures |
| M3 | queue: counts without evicting | P1 and P5, 3830 failures |
| M4 | buckets: a reused bucket keeps its old count | P1, 174 failures |
| M5 | buckets: ignores which second a bucket belongs to | P1 and P5, 3830 failures |
| M6 | buckets: 299 buckets | P1 and P2, 116 failures |
| M7 | search: the bound includes hits exactly 300 seconds old | P1 and P5, 568 failures |
| M8 | search: off by one at the end of the range | P1 and P5, 4000 failures |
| M9 | oracle: a 301-second window | P1, 966 failures |

## Verification

All three arms print the same output as `hit_counter.py` under
`karac __mir-run` (the v2 MIR interpreter), and all three pass
`karac check`. The bucket and search arms also match under
`karac run --interp`. They are byte-identical under
LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build` too. The ★ arm
is not: the frozen legacy backends do not implement `VecDeque.front`
(below).

The bench program prints `checksum 402009242` under `karac __mir-run`
(28.7 s), as do its C, Rust, Go and Python mirrors.

## Benchmarks

The bench program makes 2,000,000 calls with the ★ arm's queue of hit
times, each timestamp advancing by 0 to 2 seconds and one call in four a
query. The legacy native build refuses the ★ arm (below); the v2/MIR backend
builds it. The C, Rust, Go and Python mirrors agree on the checksum.

### Apple M5 Pro, 2026-11-06

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14606+g162ee7a0e`
(g162ee7a0e, the v2/MIR backend), measured 2026-11-06, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| **kāra `karac build`, seq** | **11.0 ms ± 0.3** | **—** |
| rust `-O -C overflow-checks=on` (equal-safety) | 11.2 ms ± 0.3 | 0.98× |
| rust `-O` | 11.2 ms ± 0.1 | 0.98× |
| c `clang -O3` | 12.8 ms ± 0.2 | 0.86× |
| go `go build` | 21.9 ms ± 0.4 | 0.50× |

Kāra is 0.98× `rustc -O`, 0.98× equal-safety Rust, 0.86× C and 0.50× Go.
The gaps were not investigated on this host. The legacy backend (dd86e3955) cannot compile this
kata, so there is no legacy count.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 47.0 ms ± 1.5 | 32.7 KiB | 1.0 MiB |
| rust | 86.9 ms ± 1.4 | 455.8 KiB | 1.1 MiB |
| kāra | 110.9 ms ± 2.8 | 66.9 KiB | 1.0 MiB |
| go | — | 2450.4 KiB | 8.2 MiB |

`karac build` is 2.4× clang's cold compile and 1.3× rustc's. Kāra's
68,504-byte binary is 2.0× clang's and 6.8× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`checksum 402009242`).

## Compiler findings

- **No `partition_point` or `lower_bound`.** `Vec.binary_search` answers
  only "is this value present, and where", so a sorted-window query needs a
  hand-written binary search. A library gap rather than a bug; noted for the
  stdlib work.
- **Legacy backends: no `VecDeque.front`.** `karac check` accepts the ★
  arm since kara `5bb4b9d3dd`, but the frozen legacy tree-walk interpreter
  refuses it (`no method 'front' on type 'VecDeque'`) and legacy codegen
  refuses it too (`Vec/String method 'front' is not yet supported in
  codegen`), so the ★ arm and the differential run only under the MIR
  interpreter. Legacy is frozen for the v2 rewrite (kara,
  2026-10-06), so this is noted here and not filed.
