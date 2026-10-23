# 920. Number of Music Playlists

Your music player contains `n` different songs. You want to listen to
`goal` songs (not necessarily different) during your trip. To avoid
boredom, you will create a playlist so that:

- every song is played at least once;
- a song can only be played again only if `k` other songs have been
  played.

Given `n`, `goal` and `k`, return the number of possible playlists that
you can create. Since the answer can be very large, return it modulo
`10^9 + 7`.

```
n = 3, goal = 3, k = 1  ->  6   ([1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1])
n = 2, goal = 3, k = 0  ->  6   ([1,1,2], [1,2,1], [2,1,1], [2,2,1], [2,1,2], [1,2,2])
n = 2, goal = 3, k = 1  ->  2   ([1,2,1], [2,1,2])
```

**Constraints:** `0 <= k < n <= goal <= 100`.

## Approaches

Between two plays of a song at least `k` other songs are played, and no
song repeats inside that stretch either, so the last `k` songs played
are always `k` different songs.

| file | mechanism |
|---|---|
| `num_music_playlists.kara` ★ | a table `dp[i][j]` of the playlists of `i` songs using exactly `j` distinct ones: the last song is new, one of `n - j + 1`, or a repeat, one of the `j - k` heard but not just played. O(goal * n) |
| `num_music_playlists_incl.kara` | inclusion and exclusion over the songs left out: from `m` songs, ignoring the rule that all are played, there are `m!/(m - k)! * (m - k)^(goal - k)` playlists, and the answer sums `(-1)^i * C(n, i)` of those for `m = n - i`, with `C(n, i)` from Pascal's triangle and the power by squaring. O(n * goal) |
| `num_music_playlists_memo.kara` | the same recurrence from the top: a recursive `count(i, j)` that remembers each answer in a table. O(goal * n) states, `goal` deep |
| `num_music_playlists_row.kara` | the table kept as one row, updated from the right so that entry `j - 1` still holds the previous row's value. O(goal * n) time, O(n) space |
| `num_music_playlists_first.kara` | songs named 1 to `n` in the order first heard: the shapes of named playlists need no choice for a new song, and each shape with all `n` names stands for `n!` playlists. O(goal * n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's three examples; one song
played once and five times, five songs each once with the longest gap,
four songs repeated nine plays with the longest gap, three songs with no
gap, and 10 songs over 20 plays with a gap of 3; LeetCode's largest
(`n = goal = 100` with `k` 0 and 99, `n = 50` with `k = 10`, `n = 99`,
and one song played 100 times); every `n`, `goal` and `k` with `goal`
up to 30 (4,960 cases, answers summing to 2,148,678,725,271, and a
checksum); and 300 random cases up to the limit.
`num_music_playlists.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: build every playlist one song at a time, playing a song only
when at least `k` other songs have been played since it was last played,
and count the playlists of `goal` songs in which every song appears. It
checks 3,200 random cases: 3,000 of 1 to 7 plays of 1 to 4 songs against
the statement, and 200 up to 100 plays against the other properties.

| | property |
|---|---|
| P1 | the statement's count, on the small cases |
| P2 | as many plays as songs (`goal = n`): `n!` |
| P3 | no gap (`k = 0`): every way to play each song at least once, a Stirling number of the second kind times `n!` |
| P4 | one play more than songs (`goal = n + 1`): `n!` orders times the `(n - k)(n - k + 1) / 2` places the one repeat can take |
| P5 | the longest gap (`k = n - 1`): the first `n` songs repeat in order, `n!` |
| P6 | each arm agrees with at least two of the other four |

P2 to P5 ask each arm a second question beside the case it was given,
with `goal`, `k` or both changed. It prints `3200 cases, answers summing
to 77157130922, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (16 s) and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one fewer new song to choose from | P1 3000, P2 3200, P3 3200, P4 3200, P5 3200, P6 3200 |
| M2 | ★: a repeat allowed to be any song heard | P1 780, P4 1227, P5 1460, P6 937 |
| M3 | ★: each sum reduced modulo `10^9 + 9` | P3 155, P4 113, P6 129 |
| M4 | incl: the first `k` songs given one factor too few | P1 1060, P2 1227, P4 1227, P5 1945, P6 1227 |
| M5 | incl: one later song too few in the free count | P1 1124, P2 1288, P3 1945, P4 1288, P6 1288 |
| M6 | incl: a difference left negative | P2 43, P3 71, P4 51, P6 60 |
| M7 | memo: a playlist of no songs counted whatever its distinct songs | P1 1940, P2 1973, P3 3200, P4 1973, P5 1255, P6 1973 |
| M8 | memo: one fewer song for a repeat | P1 2094, P3 2281, P4 3200, P5 2281, P6 2281 |
| M9 | memo: every product reduced modulo `10^9 + 9` | P2 115, P3 161, P4 121, P5 115, P6 145 |
| M10 | row: the empty playlist counted `n` times | P1 1759, P2 1945, P3 1945, P4 1945, P5 1945, P6 1945 |
| M11 | row: the row updated from the left | P1 1375, P2 1552, P3 1185, P4 1552, P5 1945, P6 1552 |
| M12 | row: the gap taken as one song whatever `k` is | P1 1593, P3 2281, P4 2505, P5 1747, P6 1770 |
| M13 | first: the `n!` names reduced modulo `10^9 + 9` | P2 115, P3 115, P4 115, P5 115, P6 115 |
| M14 | first: no repeat at all when `k` is 0 | P1 1314, P3 2281, P4 1973, P5 821, P6 1344 |
| M15 | first: a repeat kept off only the song just played | P1 279, P4 532, P5 926, P6 426 |

P4 and P6 kill all fifteen; P3 and P5 twelve, P1 eleven and P2 nine. P1
misses the four mistakes of modulus (M3, M6, M9, M13), which show only
once a count passes 10^9, far beyond the small cases. P2 asks for a
playlist with no repeat, so it misses the five that only miscount
repeats (M2, M8, M12, M14, M15). P3 sets `k` to 0 and misses the three
that are right there (M2, M4, M15); P5 misses M3, M6 and M5, whose free
count is a power of 1 when `k = n - 1`.

The failures are counted by case, so every edit that goes wrong on the
same cases fails the same checks, and 24 other edits were set aside for
that reason or another. Ten failed every check, as M1 does: in ★ a
repeat counted from the playlists with one song fewer; in incl the
signs alternating the wrong way and the count from `k + 1` songs taken
as zero; in memo one fewer new song and a table filled with 0 rather
than -1; in row the newest column never started, a repeat read from the
entry to its left and entry 1 never updated; in first the empty shape
counted twice and a repeat counted from the shapes with one song fewer.
Four failed exactly where some song repeats, as M8 does (★ and first
with one more song for a repeat, memo with no repeat once only `k + 1`
songs are heard, row with the empty playlist kept after the first
song); two as M5 (Pascal's triangle missing its right edge, the power's
bits read the wrong way); three as M10 (in first, `(n - 1)!` names,
`n^n` names, and a new song counted as any of the names heard); and two
as M9 (the same wrong modulus in row and in first). Of the rest, memo
refusing `j > n` is equivalent, since `j` never exceeds `n`; memo reading
a remembered answer from the wrong column ran past the 200 s limit; and
first multiplying a new song's count by `j` without reducing it
overflowed.

## Verification

Every arm prints the same output as `num_music_playlists.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.7 to 1.4 s each and the
differential 16 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every arm and the differential also print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par, and the legacy build of the bench program prints
the same line as the others.

## Benchmarks

The bench program runs the ★ arm on every `n`, `goal` and `k` with
`goal` up to 64, 45,760 cases. Every implementation prints `every case
with goal up to 64: 45760 cases, answers summing to 22235829426871,
checksum 950549034`. Kāra, Rust, Go and Python build the table as a
vector of rows, as LeetCode's solutions usually do; C allocates it as
one flat block, the idiomatic C table.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.13 to 0.17 s | 0.14 s |
| Rust (`rustc -O`) | 0.22 to 0.27 s | 0.24 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.22 to 0.26 s | 0.24 s |
| Go | 0.40 to 0.48 s | 0.44 s |
| Python | 7.9 s | |
| Kāra (`karac build --mir`) | 0.20 to 0.24 s | 0.23 s |
| Kāra (`karac build --legacy`) | 0.21 to 0.27 s | 0.24 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about sixty times
C's.

v2 takes 0.93 times Rust's median time under overflow checks, 0.94
times legacy's and 1.65 times C's. Under valgrind's cachegrind v2 runs
3.28 billion instructions and 0.45 billion branches, against 3.55
billion and 0.47 billion for Rust with overflow checks and 3.53 billion
and 0.49 billion for legacy; they mispredict 5.8, 6.9 and 7.0 million.
C runs 2.47 billion instructions and 0.74 billion branches but
mispredicts only 3.7 million; its single flat table, with no row to look
up and no bounds check, is the likely reason it leads, though that is
inferred, not profiled.
