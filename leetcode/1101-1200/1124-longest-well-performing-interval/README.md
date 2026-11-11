# 1124. Longest Well-Performing Interval

We are given `hours`, a list of the number of hours worked per day for a
given employee.

A day is considered to be a tiring day if and only if the number of
hours worked is (strictly) greater than `8`.

A well-performing interval is an interval of days for which the number
of tiring days is strictly larger than the number of non-tiring days.

Return the length of the longest well-performing interval.

```
hours = [9,9,6,0,6,6,9]   ->  3
hours = [6,6,6]           ->  0
```

**Constraints:** `1 <= hours.length <= 10^4`; `0 <= hours[i] <= 16`.

The arms are `fn longest_wpi(hours: Vec[i32]) -> i64`.

## Approaches

Each arm keeps a running score, +1 for a tiring day and -1 for any
other: an interval is well-performing when the score is higher at its
end than before its start.

| file | mechanism |
|---|---|
| `longest_wpi.kara` ★ | one pass: a positive score makes the whole prefix well-performing; otherwise the longest interval ending here starts where the score first stood one lower, kept in a `Map` from score to its first index. O(n) |
| `longest_wpi_stack.kara` | a monotonic stack: the prefix scores, the indices where the score falls to a new low kept on a stack, then a walk from the right end popping every low the score at the end stands above and measuring from it. O(n) |
| `longest_wpi_table.kara` | the ★ arm's pass with the map as a `Vec`: the score runs from `-n` to `n`, so each score's first index sits at `score + n + 1`, -1 until it is met. O(n) |
| `longest_wpi_lows.kara` | the score moves one step at a time, so it first reaches each value below zero when it falls to a new low: the first indices are a list in the order of the lows, and a score of `s` looks up `lows[-s]`. O(n) |
| `longest_wpi_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, a `HashMap<i32, usize>` filled through `entry().or_insert()`, `&h` and `&j` patterns), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's two
examples and seven more (every day tiring, none, a lone other day, a
lone tiring day, alternating days whose whole span leads by one, a
well-performing run at the end, and 8 hours, which is not tiring), then
over 2000 random schedules of up to 10^4 days, every other one tilted
towards tiring days, the answers summed and a checksum (`2000 random
schedules: answers total 4838814, checksum 931356691`).
`longest_wpi.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every interval, its tiring and other days counted one by
one, and the longest with more tiring days kept. It checks 2000 problems
in four kinds of 500: up to 30 days of any hours, tiring two days in
five; up to 30 days of 8 and 9 hours alone, half tiring; up to 40 days
tiring three in five; and up to 40 days in runs of one to six alike, 8
and 9 hours. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | by a second reading, from a running count of tiring days: some interval of the answer's length has more than half its days tiring, and no longer one does |
| P3 | the days reversed give the same answer |
| P4 | each tiring day made 16 hours and each other 0 gives the same answer |
| P5 | `n + 1` tiring days appended make the whole span of `2n + 1` well-performing |
| P6 | `n + 1` other days put in front never shorten the answer, and lengthen it only when some first days are well-performing |

All 60,000 checks pass on every arm: `2000 problems: checksum
213889993, 60000 checks over 5 arms: 0 failures`. A Python reading of
the same problems, by every interval, gives the same checksum.

## Mutation testing

Twenty-five edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All twenty-five are caught. Fifteen are kept, no two failing
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a prefix counted only when two tiring days ahead | P1 396, P2 396, P3 521, P5 61 |
| M2 | ★: measured from where the score stood two lower | P1 624, P2 624, P3 640, P6 620 |
| M3 | ★: 8 hours counted as tiring | P1 829, P2 829, P4 829, P6 239 |
| M4 | stack: one low popped at each end | P1 777, P2 777, P3 1128, P5 1518 |
| M5 | stack: the ends walked from the left | P1 1811, P2 1811, P3 1216, P5 1939, P6 1545 |
| M6 | stack: the empty prefix never a low | P1 1163, P2 1163, P3 521, P5 2000 |
| M7 | table: measured from where the score stood level | P1 752, P2 752, P3 454, P6 31 |
| M8 | table: a first index of 0 taken for unmet | P1 100, P2 100, P3 165, P6 63 |
| M9 | table: 9 hours not tiring | P1 1351, P2 1351, P4 1351, P5 2000 |
| M10 | lows: a low recorded again at each return to it | P1 384, P2 384, P3 368 |
| M11 | lows: the last interval kept, not the longest | P1 391, P2 391, P3 579 |
| M12 | lows: the deepest low never measured from | P1 180, P2 180, P3 199, P6 143 |
| M13 | solution: a tiring day counted twice | P1 982, P2 982, P6 166 |
| M14 | solution: an interval measured one day long | P1 776, P2 776, P3 403 |
| M15 | solution: a prefix with as many tiring days as other ones taken | P1 576, P2 576, P3 559, P6 576 |

P1 and P2 catch all fifteen, P3 twelve, P6 eight, P5 five and P4 two.
P2 fails on exactly the problems P1 does: it reads the answer as the
longest well-performing length, which pins it as tightly as the literal
count does. P3 is the strongest self-comparison: an interval reads the
same backwards, but the arms find it from its end, so an edit that
measures from the wrong place, or keeps the wrong one of two equal
lengths, gives a different answer for the reversed days. P6 sees the
edits that misjudge where an interval may start, since the days put in
front push every start along and add new lows below the old ones. P5
sees the edits that get the whole span wrong, the case a positive score
decides, and P4 only the two that move the line between tiring and not,
since 16 and 0 hours sit far from it. P3 to P6 together catch all
fifteen.

Of the ten not kept, three fail alike in three arms: keeping each
score's last index rather than its first (★, table and solution), and
taking a well-performing prefix one day short (table, lows and
solution). The lows arm looking up where the score stood level stops:
at a score of 0 the lookup is at index -1, out of bounds. The other three fail in ways of their own but were not needed:
the ★ arm measuring an interval one day short, and the stack arm taking
an end level with the low and counting an other day as nothing. One
edit first tried for the stack arm, pushing a low that ties the one
below it, was equivalent and was replaced by M4: the later twin is
popped first and the earlier one still gives the longer interval.

## Verification

Every arm prints the same output as `longest_wpi.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found one gap, now fixed. The ★, stack, table and lows arms
were written as Kāra, the solution arm as Rust writes it. `karac fix`
carried it to a clean check in three rounds: the `use` line dropped,
`Vec<..>` and `HashMap<..>` to `[..]`, `::` to `.`, the `&h` and `&j`
patterns to `h` and `j` with `.cloned()` on the lookup, which copies the
first index out of the `Option[ref i64]` a `Map` lends; then `struct
Solution {}` declared and `HashMap` to `Map`; then `usize` to `i64` and
the `as i64` at the call dropped, an `i32` widening by itself. The gap:
Rust writes `seen.get(&(score - 1))`, parenthesized so the `&` borrows
the whole difference, and the fix took the `&` and left
`seen.get((score - 1))`. It now takes the parentheses with the `&`
when they wrap the whole argument, and keeps a tuple's
(B-2026-11-11-83).

## Benchmarks

The bench builds 16 random schedules of 10^4 days once, LeetCode's
largest, hours from 0 to 16. Each of 300 rounds turns one day in every
schedule from tiring to not or back and solves the schedule with the ★
arm: 4800 passes over 10^4 days. Every implementation prints `300
rounds over 16 schedules of 10^4 days: answers total 7346454, checksum
203683112`. Kāra keeps the first indices in a `Map`, Rust in a
`HashMap` filled through `entry().or_insert()`, Go in a `map`, Python in
a `dict`, and C in a table of its own: open addressing over 2^15 slots,
a multiplicative hash, cleared with `memset` for each call.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `46ef5d349a`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.122 to 0.154 s | 0.146 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.142 to 0.191 s | 0.149 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.861 to 1.086 s | 0.970 s |
| Rust (`rustc -O`) | 0.849 to 1.058 s | 0.974 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.868 to 1.076 s | 0.991 s |
| Go | 0.923 to 1.159 s | 1.040 s |
| Kāra (`karac build`) | 0.966 to 1.194 s | 1.091 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.080 to 1.282 s | 1.138 s |
| Python | 6.68 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.2x Rust's time and 1.1x Go's, which keep the same
map from score to index in their own library maps; Kāra's `Map` and
Rust's `HashMap` both hash each key with SipHash-1-3 under a random key.
C is about 8x faster than Kāra: its table hashes with one multiply,
under no random key, into slots allocated once, where the three library
maps do more for each key and allocate as they grow. The gap to C was
not traced further. Python takes about 6x Kāra's time.
