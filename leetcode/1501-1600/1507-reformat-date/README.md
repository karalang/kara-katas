# 1507. Reformat Date

Given a date string in the form `Day Month Year`, where `Day` is one of
`1st`, `2nd`, `3rd`, `4th`, ..., `30th`, `31st`, `Month` is one of `Jan`,
`Feb`, ..., `Dec`, and `Year` is in `[1900, 2100]`, convert it to the
form `YYYY-MM-DD`.

```
"20th Oct 2052"  ->  "2052-10-20"
"6th Jun 1933"   ->  "1933-06-06"
"26th May 1960"  ->  "1960-05-26"
```

**Constraints:** the given dates are guaranteed to be valid.

## Approaches

| file | mechanism |
|---|---|
| `reformat.kara` ★ | split at the spaces; the day is the first word's leading digits (`take_while`), the month its place in a table plus one (`position`), the year the last word as it is; `f"{year}-{month:02}-{day:02}"` |
| `reformat_match.kara` | the month by a `match` on its name, and the day with whichever two-letter suffix it has stripped (`strip_suffix`) |
| `reformat_bytes.kara` | one pass over the bytes: the day's digits until the first letter, the month from its three letters against `"JanFeb...Dec"`, the year from the last four bytes, and the answer pushed byte by byte |
| `reformat_iter.kara` | the three words reversed (`split_whitespace().rev()`), each mapped to its field by its place, joined with dashes. Refused by `karac check` until B-2026-11-08-15 was fixed |
| `reformat_solution.kara` | LeetCode's Rust template (`Vec<&str>`, `parts[0][..len - 2].parse()`, `position(\|&m\| ..)`, `format!`), carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more (the first and last days of the range, a 22nd, a
3rd, and a 29th of February), a checksum of every byte of the answer for
every day of 1900, 1901, 2000, 2052 and 2100 (1827 dates), and one for 3000
random dates from 1900 to 2100. `reformat.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the
statement read literally: try every day and month, and take the one whose
written form (`20th Oct `) starts the date, with the rest as the year. It
checks 2000 dates from 1900 to 2099. Every random choice of a problem is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is ten bytes: four digits, a dash, two digits, a dash, two digits |
| P3 | the answer's fields, written back in the statement's form, are the date |
| P4 | the next day's answer is larger, as a string |
| P5 | the same day a year later changes only the answer's year |
| P6 | each arm agrees with at least two of the other four |

The differential prints `2000 problems: checksum 371941383, 60000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The iterator arm
joined it once B-2026-11-08-15 was fixed; the mutations below were run
with the four arms before it, and none was added for it.

## Mutation testing

Twenty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept, three to
each arm. Seventeen are killed, each the same way under both backends and
none by a crash; one survives and is equivalent, and one is refused by
`karac check`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the day and month written the other way round | P1 1931, P3 1931, P4 62, P6 1931 |
| M2 | ★: only the day's first digit read | P1 1419, P3 1419, P4 1297, P6 1419 |
| M3 | ★: the day not padded to two digits | P1 581, P2 581, P4 74, P6 581 |
| M4 | match: `Sep` read as month 8 | P1 151, P3 151, P4 6, P6 151 |
| M5 | match: a `0` appended to the day once its suffix is stripped | P1 2000, P2 1419, P3 2000, P4 74, P6 2000 |
| M6 | match: the month not padded to two digits | P1 1480, P2 1480, P4 6, P6 1480 |
| M7 | bytes: only the day's last digit kept | P1 1419, P3 1419, P4 200, P6 1419 |
| M8 | bytes: only the year's last three digits copied | P1 2000, P2 2000, P3 2000, P5 2000, P6 2000 |
| M9 | bytes: a month matched on its first and last letters only | P1 169, P3 169, P4 5, P6 169 |
| M10 | Rust: the day padded to three digits | P1 2000, P2 2000, P6 2000 |
| M11 | Rust: `Nov` and `Dec` swapped in the table | P1 342, P3 342, P4 6, P6 342 |
| M12 | Rust: the month padded with a space, not a zero | P1 1480, P2 1480, P6 1480 |

P1 and P6 kill all twelve, P3 eight, P4 nine, P2 six, and P5 one: M8, the
only edit that damages the year. P4 sees most edits only on the dates
where the damage reorders two neighbours (a month's last day and the next
month's first), so its counts stay small.

The other five that are killed (the ★ arm without the month's `+ 1`, the
same in the Rust arm shifted by two, the ★ arm's `Jun` and `Jul` swapped,
the match arm's `May` arm written `Mar`, the bytes arm skipping two bytes
for three before the month, and its last digit taken mod 9) fail with
signatures close to the kept ones. One survives and is equivalent: the
match arm's `_ => 0` arm returning 13, which no valid date reaches. One
is refused: the Rust arm's `let day: u8` for `u32`, which `karac check`
rejects as an implicit narrowing.

## Iterator arm: B-2026-11-08-15

`karac check` refuses `date.split_whitespace().rev()`: `no method 'rev' on
type 'StrWords'`, and `s.split(" ").rev()` the same for `StrSplit`. The
library's double-ended iterators (`docs/library/iterators.md`) do not
include the string-splitting ones, though Rust's `split_whitespace` is
double-ended and reversing words is a common idiom. With the words
collected first and then `words.reverse()`, the arm checks and prints the
expected output, so `rev` is the only gap. The diagnostic gives no hint
and `karac fix` has no edit. Fixed in kara `fd8d318ca`: `StrSplit` and
`StrWords` keep a back cursor and are double-ended, and the arm checks as
written and agrees on every lane.

## Rust template

The Rust arm was written as LeetCode's Rust template plus a thin wrapper.
`karac fix` made 6 edits and then 2, and the arm checks and prints the ★
arm's output on every lane: `Vec<&str>` became `Vec[Str]`,
`date.split(' ')` became `date.split(" ")`,
`parts[0][..len - 2].parse()` with the binding's `u32` became
`u32.parse(parts[0][..len - 2])`, `|&m|` became `|m|`, and `format!` an
f-string.

## Benchmarks

The bench builds 100000 random dates once, then reformats each ten times
by the ★ arm in all five languages, folding every byte of every answer
into a checksum. Every implementation prints `1000000 dates reformatted,
100000 built once: checksum 25339289`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `acb9d4c5b` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.160 s |
| Rust (`rustc -O`) | 0.240 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.244 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.264 s |
| Kāra (`karac build`) | 0.295 s |
| Go | 0.461 s |
| Python | 2.02 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is its real time (0.331 s and 0.336 s on one run), and the gap
between the two Kāra rows is noise between runs.

Kāra is 1.08x Rust under overflow checks by median. Each reformat
allocates the split words, the day's digits and the answer in every
language but C, which writes into one buffer.

## Verification

All five arms print the same output as `reformat.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the arms take about 0.5 s and the differential
4.8 s.

## Writing it

The arms were written in Kāra. `karac fix` made 1 to 4 edits to each: a
`b as i64` that widens implicitly anyway, a turbofish
`collect::[Vec[u8]]()` moved to the binding's type, the `.iter()` that
`s.bytes().collect()` needs, a `while` count loop as a `for` over a range,
and a parameter that is given away taken `own`.
