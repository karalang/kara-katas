# 401. Binary Watch

A binary watch shows the hour (0 to 11) on 4 LEDs and the minute (0 to
59) on 6, each LED one bit. Given `turned_on`, the number of LEDs that
are lit, return every time the watch could show, as `"h:mm"`: the hour
with no leading zero, the minute with two digits.

```
turned_on = 1  -> ["0:01","0:02","0:04","0:08","0:16","0:32","1:00","2:00","4:00","8:00"]
turned_on = 9  -> []
```

**Constraints:** `0 <= turned_on <= 10`. Any order is accepted; every
arm here returns the times in time order.

## Approaches

| file | mechanism | work |
|---|---|---|
| `binary_watch.kara` ★ | try every time: walk the 720 times in order and keep those whose hour and minute have `turned_on` set bits between them | 720 popcounts |
| `binary_watch_backtrack.kara` | choose which LEDs are lit: a recursion picks `turned_on` of the ten in increasing order, adding each to the hour or the minute, and drops a choice once the hour passes 11 or the minute 59; sorted at the end | at most C(10, `turned_on`) choices |
| `binary_watch_split.kara` | group the hours and the minutes by their number of set bits, then pair every hour of `k` bits with every minute of `turned_on - k`; sorted at the end | one pass over 72 numbers, then the output |
| `binary_watch_masks.kara` | every 10-bit display: the top 4 bits are the hour and the low 6 the minute; keep the masks with `turned_on` set bits and both parts in range; sorted at the end | 1,024 masks |
| `differential.kara` | the four arms for every LED count, checked against the times read back from their text, and 3,000 random times, five properties | — |

The input has only eleven values, so every arm prints the whole answer
space: one line per LED count from 0 to 10, with the full list when it
holds ten times or fewer and otherwise its size, first and last time,
and a hash of the list. `binary_watch.py` mirrors the ★ arm and its
output is byte-identical.

The three arms that collect `(hour, minute)` pairs format them with
`for (h, m) in found.iter() { times.push(f"{*h}:{*m:02}"); }`, as the
items of `Vec.iter()` are references. Until the fixes that closed kara
`B-2026-10-12-9` (the destructured `Vec` tuple item that kata 399 added
to the row), `karac __mir-run` refused the `*` as `found 'i64'` and the
arms wrote `{h}` and `{m:02}`.

## Differential

`differential.kara` holds copies of the four arms. Each arm is asked
for every LED count from 0 to 10, and then probed with 3,000 random
times. Its `parse` reads a time back from its text and refuses
anything that is not `h:mm`.

| | property |
|---|---|
| P1 | every time listed for `n` LEDs has `n` set bits between its hour and minute, read back from the text |
| P2 | the eleven lists together hold each of the 720 times exactly once |
| P3 | each list is in time order, with no time twice |
| P4 | each time is written `h:mm`: an hour from 0 to 11 with no leading zero, a two-digit minute below 60 |
| P5 | a random time is in the list for its own LED count |

It prints `4 arms, 12136 checks, 0 failures` under `karac __mir-run`,
and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | all: the hours run to 12 | P4 6 |
| M2 | all: the minute is written without its leading zero | P2 1, P4 7, P5 538 |
| M3 | backtrack: an hour of 12 is allowed | P4 6 |
| M4 | backtrack: an LED may be chosen twice | P1 9, P2 1, P3 8 |
| M5 | backtrack: the times are left in LED order | P3 7 |
| M6 | split: the hour always takes at least one LED | P2 1, P5 284 |
| M7 | masks: the hour takes 5 bits and the minute 5 | P1 7, P2 1, P5 2208 |
| M8 | masks: the bit count is the mask's length, not its set bits | P1 9, P5 2983 |

The first M6 forbade the minute all six of its LEDs. It cannot change
an answer: six lit minute LEDs make 63, which is not a minute, so that
mutant is equivalent. M1 and M3 are one mistake in two arms. They are
caught only by P4, once for each list that gains a `12:mm` time: 12
has two set bits, so those are the lists for 2 to 7 LEDs.

## Verification

All four arms print the same output as `binary_watch.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The ★, backtracking and mask
arms also match under `karac run --interp`, LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build`. The differential prints `12136 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`; the
latter runs it since compiler commit 62f5f6de04 added the
`String.as_str` native that `parse`, which takes a `Str` and is passed
a `String`, needs. The frozen legacy typechecker refuses `*h` on the
items of `hours[k].iter()` in the split arm and the differential, as in
katas 382 to 398; not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 50,000 calls, cycling the
LED count through 0 to 10, each building its list of times as strings,
and counts the times and their characters. Every implementation prints
`50000 calls: 3272748 times, 13636421 characters`; a 500-call cut of
the Kāra program under `karac __mir-run` prints the same as the C
program cut the same way. C has no string type, so its mirror formats
each time with `snprintf` into a heap copy and frees the list after each
call, as the other mirrors' strings are freed. Spot timings on a
shared 4-core container (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Kāra (legacy `karac build`) | 0.42 to 0.56 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.54 s |
| C (`clang -O3`) | 0.58 s |
| Rust (`rustc -O`) | 0.64 s |
| Go | 0.91 s |
| Python | 19 s |

Most of the time is spent formatting and freeing 3.3 million short
strings. The Kāra program also prints the same line under
`karac __mir-llvm-run` in 8.8 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark. The
`karac build` time is the frozen legacy backend.

## Compiler findings

No new findings. The arms ran into the `Vec` tuple-item gap that kata
399 added to kara `B-2026-10-12-9`, since fixed. The differential ran into the
missing `String.as_str` native on `karac __mir-llvm-run`, which
compiler commit 62f5f6de04 has since added.
