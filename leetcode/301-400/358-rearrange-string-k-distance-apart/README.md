# 358. Rearrange String k Distance Apart

Given a string `s` of lowercase letters and an integer `k`, rearrange `s` so
that equal letters are at least `k` positions apart. If that is impossible,
return the empty string.

```
s = "aabbcc",   k = 3  ->  "abcabc"
s = "aaabc",    k = 3  ->  ""
s = "aaadbbcc", k = 2  ->  "abacabcd"
```

**Constraints:** `1 <= s.length <= 3 * 10^5`; `0 <= k <= s.length`.

## Approaches

LeetCode accepts any valid arrangement. Every arm here follows one greedy
rule, which makes the answer unique: at each position, write the letter with
the most copies left among those whose last copy is at least `k` positions
back (or that have not been written yet), and take the smallest letter on a
tie. If no letter may be written, there is no arrangement.

| file | mechanism | cost |
|---|---|---|
| `rearrange.kara` ★ | a max-first `PriorityQueue` of the letters that may go next, and a `VecDeque` of the ones written in the last `k` positions; a letter rejoins the heap when the queue reaches length `k` | `O(n log 26)` |
| `rearrange_ready_at.kara` | the same heap, but each queue entry carries the position at which it may be written again, and the loop peeks the queue's front with `front()` | `O(n log 26)` |
| `rearrange_scan.kara` | no heap: each letter's count and last position, and a scan of all 26 letters at every position | `O(26 n)` |
| `rearrange_sorted.kara` | a list of (copies left, letter, last position) re-sorted at every position; take the first entry that may go | `O(26 log 26 · n)` |
| `differential.kara` | the arms against an oracle that searches every arrangement, 23,013 checks, five properties | — |

Every arm prints the same 15 lines: the three LeetCode examples, eleven edge
cases (`k = 0`, `k = 1`, one letter, one letter repeated with `k = 1` and
`k = 2`, `k` equal to the length, `k` beyond the length, ties, a string whose
most frequent letter just fits, one where every letter fills its slots, one
copy too many), and a checksum over 2,000 random strings. `rearrange.py`
mirrors the ★ arm and its output is byte-identical.

In the ★ arm, every letter written goes to the back of the queue, even its
last copy. That keeps the queue's length equal to the number of positions
since its front entry was written. A version that drops the last copy skips
those positions, so letters rejoin the heap too early. That is mutation M3
below.

## Differential

`differential.kara` holds copies of the heap, scan and sorted arms, plus an
oracle that never uses the greedy rule. The oracle fills positions left to
right with every letter that is still allowed, backtracking, so an
arrangement exists exactly when the search reaches the end. The test draws
3,000 random strings of 0 to 8 letters over the first one to four letters,
with `k` from 0 to 4.

| | property |
|---|---|
| P1 | an arm returns `""` exactly when the oracle finds no arrangement |
| P2 | a non-empty answer uses each letter exactly as often as `s` does |
| P3 | a non-empty answer keeps equal letters at least `k` positions apart |
| P4 | the three arms return the same string |
| P5 | if no arrangement exists for `k`, none exists for `k + 1` |

It prints `3000 cases, 23013 checks, 2037 arrangeable, 0 failures` under
`karac run --interp`, the MIR interpreter, LLJIT, and both builds.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each run. All eleven
are killed.

| # | mutation | how |
|---|---|---|
| M1 | heap: ties pick the larger letter (`(count, c)` in the heap) | the heap stores `c` and negates it back, so the letters go negative and the run panics on an out-of-range index |
| M2 | heap: a letter rejoins one position early | P1, P3 and P4, 1483 failures |
| M3 | heap: the last copy skips the queue | P1 and P4, 620 failures |
| M4 | heap: an empty heap writes nothing and goes on | P2 and P4, 1926 failures |
| M5 | scan: distance `k - 1` allowed | P1, P3 and P4, 1483 failures |
| M6 | scan: ties pick the larger letter | P4, 1023 failures |
| M7 | scan: picks the fewest copies | P1 and P4, 1105 failures |
| M8 | sorted: sorts least copies first | P1 and P4, 1105 failures |
| M9 | sorted: a written letter keeps its old position | P1, P3 and P4, 3187 failures |
| M10 | oracle: ignores the distance | P1, 2889 failures |
| M11 | oracle: does not restore the count when it backtracks | P1 and P5, 457 failures |

M6 is caught only by P4. A greedy that breaks ties the other way is still a
correct answer to the LeetCode problem, so only the comparison between arms
can see it.

## Verification

The heap, scan and sorted arms and the differential print the same output
under `karac run` (LLJIT), `karac run --interp`, `karac __mir-run` (the v2
MIR interpreter), `karac build`, and `KARAC_AUTO_PAR=1 karac build`. The
three arms match `rearrange.py` byte for byte. The bench program prints
`116 of 200 strings can be arranged, checksum 934979344` under `karac build`,
as do its C, Rust, Go and Python mirrors.

`rearrange_ready_at.kara` does not pass `karac check` yet; see below.

## Benchmarks

Not measured yet. The bench programs in `bench/` and their C, Rust, Go and
Python mirrors are written and agree on the printed checksum, but the timings
still have to be taken on a quiet machine. This section will carry the table
when they are.

## Compiler findings

- **`VecDeque.front` is refused by `karac check`** ("no method 'front' on type
  'VecDeque'"), although `docs/library/collections.md` lists `front` and
  `back` and the MIR interpreter implements both. `rearrange_ready_at.kara`
  keeps the natural `match cooling.front() { ... }` and waits for the fix
  (kara main at `63d8e870ed`; handed to the stdlib thread).
- **The MIR interpreter prints nothing on a panic.** Mutant M1 indexes with
  `-2`. Under `karac run --interp` it reports
  `runtime error: index ... out of bounds` with the line. Under
  `karac __mir-run` it exits 101 with empty stderr, and so do `panic("boom")`
  and integer overflow (core-semantics §10.2 asks for the message, location
  and trace). Handed to the MIR interpreter thread.
