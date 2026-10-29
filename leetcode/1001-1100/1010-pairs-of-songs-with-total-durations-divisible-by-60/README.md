# 1010. Pairs of Songs With Total Durations Divisible by 60

You are given a list of songs where the `i`th song has a duration of
`time[i]` seconds.

Return *the number of pairs of songs for which their total duration in
seconds is divisible by* `60`. Formally, we want the number of indices
`i`, `j` such that `i < j` with `(time[i] + time[j]) % 60 == 0`.

```
time = [30,20,150,100,40]  ->  3   (30+150, 20+100, 20+40)
time = [60,60,60]          ->  3
```

**Constraints:** `1 <= time.length <= 6 * 10^4`;
`1 <= time[i] <= 500`.

## Approaches

Two durations add up to a multiple of 60 exactly when their remainders
mod 60 add up to 0 or 60, so four arms count remainders and one counts
durations.

| file | mechanism |
|---|---|
| `num_pairs.kara` ★ | remainder counts in one pass: each song pairs with every earlier song of remainder `(60 - r) % 60`, then joins the counts. O(n) |
| `num_pairs_tally.kara` | tally, then combine: count every remainder first; `r` and `60 - r` pair across for `r` from 1 to 29, and 0 and 30 each pair among themselves, `c * (c - 1) / 2`. O(n) |
| `num_pairs_map.kara` | the one-pass count kept in a `Map` from remainder to count. O(n) map operations |
| `num_pairs_sort.kara` | sorted remainders and binary search: for each song, the later songs in sorted order with the remainder it needs are one run, found by a lower and an upper bound. O(n log n) |
| `num_pairs_durations.kara` | counts by duration: durations run from 1 to 500, so count each, and for each `a` step `b` by 60 from the smallest `b >= a` with `a + b` a multiple of 60. O(n + 500 * 500 / 60) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines. The first eight are LeetCode's two
examples and six more: one song; two 30s; songs whose remainders are 59,
1, 1, 59 and 2; five multiples of 60; eight songs pairing 10 with 50,
20 with 40 and 30 with 30; and songs mixing durations near 500. Then
four playlists of LeetCode's longest, 60,000 songs: all 60, which gives
1,799,970,000 pairs, more than 32 bits hold; 30 and 90 alternating,
the same count through remainder 30; durations cycling from 1 to 500;
and all 7, which gives none. Then totals over random playlists with
durations from 1 to 500: 3,000 of up to 10 songs, 300 of up to 1,000
and 5 of up to 60,000. `num_pairs.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every pair of indices `i < j`, counted when the two
durations add up to a multiple of 60. It checks 3,300 random
playlists, each with durations from 1 to a random top, so short tops
repeat remainders often: 3,000 of 1 to 40 songs against the statement,
and 300 of up to 2,000 against the other properties.

| | property |
|---|---|
| P1 | the statement's count, on the first 3,000 playlists |
| P2 | the songs in reverse order give the same count |
| P3 | moving each duration by a multiple of 60, within 1 to 500, gives the same count |
| P4 | the playlist played twice has 4 times the pairs, plus one for each song that is a multiple of 30 |
| P5 | one more song adds the number of earlier songs it pairs with |
| P6 | each arm agrees with at least two of the other four |

P4 holds because each pair of the playlist appears four times between
the two copies, and a song pairs with its own copy when twice its
duration is a multiple of 60.

It prints `3300 playlists of 354344 songs: checksum 4630292, 97500
checks over 5 arms: 0 failures` under `karac __mir-run` (35 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Twenty-five edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a song counted before it looks | P1 1209, P4 1490, P5 117, P6 1490 |
| M2 | ★: the same remainder looked up | P1 2227, P4 3297, P5 1391, P6 2519 |
| M3 | ★: remainders mod 30 | P1 2115, P5 1064, P6 2398 |
| M4 | tally: the 30s left out | P1 161, P4 1036, P5 16, P6 428 |
| M5 | tally: 30 paired across with itself | P1 759, P5 68, P6 1036 |
| M6 | tally: the two counts added | P1 2997, P4 3297, P5 2562, P6 3297 |
| M7 | map: one pair for each song that has any | P1 916, P2 1254, P4 2385, P5 424, P6 1194 |
| M8 | map: 0 needing 60 | P1 110, P4 919, P5 15, P6 352 |
| M9 | map: the first song of a remainder not counted | P1 2135, P2 1254, P4 2404, P5 1061, P6 2418 |
| M10 | sort: every song searched, not the later ones | P1 2266, P4 1490, P5 1147, P6 2549 |
| M11 | sort: the remainders not sorted | P1 1946, P2 2117, P4 2363, P5 1821, P6 2228 |
| M12 | sort: the upper bound stops short of the end | P1 2000, P4 2333, P5 681, P6 2293 |
| M13 | durations: `b` never `a` itself | P1 120, P3 257, P4 1490, P5 8, P6 383 |
| M14 | durations: `b` steps by 30 | P1 1847, P3 1818, P5 969, P6 2110 |
| M15 | durations: 500 never a partner | P5 5 |

P5 kills all fifteen, P1 and P6 fourteen each, P4 eleven, P2 three and
P3 two. The checks draw no random number that depends on an answer, so
every mutant sees the same playlists and their counts can be compared.
P3 sees only the durations arm, the one arm that looks at durations
rather than remainders: moving a duration by 60 changes which `b` it
meets. P2 sees only the edits whose count depends on the order of the
songs: counting a song once for any partner or skipping the first of
each remainder, which depends on which song comes first, and binary
search over unsorted remainders. M15 is the one edit only P5 sees. A
song of 500 seconds, remainder 20, misses only partners of remainder
40, and the playlists' random tops make 500 rare; P5 adds a song drawn
from the whole range, and the edit fails five of those checks.

Ten other edits were tried and set aside. Four change no answer: the ★
arm looking up `(120 - r) % 60`, the map arm inserting a new remainder
by index, the binary search taking its midpoint as `(a + b) / 2`, and
the durations arm not skipping durations no song has. Two failed
exactly the same checks as a kept one: the ★ arm and the map arm each
marking a remainder seen instead of counting it, as M7, since a song
then pairs once with any earlier partner. Four were killed but beyond
three an arm: the tally pairing a multiple of 60 with itself and
marking remainders seen, the lower bound past the run, and the
durations arm pairing a duration with itself.

## Verification

Every arm prints the same output as `num_pairs.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build is at kara
`8b6e8a9088`, with the runtime archives rebuilt there. Under `karac
__mir-run` the arms take 1.1 s (tally) to 4.7 s (sort).

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages: 20 playlists of 60,000
songs, LeetCode's longest, with durations from 1 to 500, drawn once,
and 250 rounds that each count the pairs of every playlist, starting
from a different one, and fold each count into a checksum. Every
implementation prints `250 rounds over 20 playlists of 60000 songs:
checksum 808685184`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `8b6e8a9088`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.627 to 0.755 s | 0.677 s |
| Rust (`rustc -O`) | 0.586 to 0.698 s | 0.621 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.665 to 0.742 s | 0.696 s |
| Go | 0.815 to 0.933 s | 0.861 s |
| Python | 26.4 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.666 to 0.793 s | 0.714 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` finds nothing to run in
parallel here, since each song reads the counts the songs before it
wrote, and its binary runs on one core in the same time. Python's run
is about 37 times Kāra's.

v2 took 1.03 times Rust's median time under overflow checks and 1.05
times C's. Under valgrind's cachegrind v2 ran 8,426 million
instructions, Rust with overflow checks 7,808 million, Rust without
them 6,903 million and C 6,317 million. Branches are no factor: C
mispredicts 11 thousand and v2 33 thousand, while both Rust builds
mispredict 4.9 million, and still run as fast.
