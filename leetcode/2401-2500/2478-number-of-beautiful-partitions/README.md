# 2478. Number of Beautiful Partitions

You are given a string `s` that consists of the digits `'1'` to `'9'`
and two integers `k` and `minLength`.

A partition of `s` is called **beautiful** if:

- `s` is partitioned into `k` non-intersecting substrings.
- Each substring has a length of **at least** `minLength`.
- Each substring starts with a **prime** digit and ends with a
  **non-prime** digit. Prime digits are `'2'`, `'3'`, `'5'`, and `'7'`,
  and the rest of the digits are non-prime.

Return *the number of **beautiful** partitions of* `s`. Since the
answer may be very large, return it **modulo** `10^9 + 7`.

A **substring** is a contiguous sequence of characters within a string.

```
s = "23542185131", k = 3, minLength = 2   ->  3
s = "23542185131", k = 3, minLength = 3   ->  1
s = "3312958", k = 3, minLength = 1       ->  1
```

**Constraints:** `1 <= k, minLength <= s.length <= 1000`; `s` consists
of the digits `'1'` to `'9'`.

A part ends where the next begins, so every cut inside the string falls
between a non-prime digit and a prime one, and the string itself must
begin with a prime and end with a non-prime. The count of partitions of
the first `i` digits into `j` parts is then the sum of the counts into
`j - 1` parts at the cuts at least `minLength` before `i`, and a
running sum gives each round of `j` in one pass.

## Approaches

| file | mechanism |
|---|---|
| `beauty.kara` ★ | by cuts: the places a part may end marked once; then `k` rounds, each a pass over the places with a running sum of the earlier round at the places at least `minLength` back. O(n k) |
| `beauty_table.kara` | a whole table: `ways[j][i]` for every part count kept, with `starts[j]`, the prefix sums of `ways[j]` over the places a part may begin, read at `i - minLength + 1`. O(n k) time and room |
| `beauty_memo.kara` | top down, memoized: `from(e, j)`, the ways to cut what follows a start `e` into `j` parts, and `after(i, j)`, the sum of `from` over the starts at or past `i`, recursing into each other through a `struct` of flat tables. O(n k) |
| `beauty_cuts.kara` | over the cuts alone: the places a part may end listed in order, and each round a walk over that list with a second index trailing it to the last cut at least `minLength` back. O(n + c k), `c` the cuts |
| `beauty_iter.kara` | iterators: the cuts by `map` over the digits' `windows(2)`, each round by `scan` over the places, its state the running sum, and the rounds by `fold`. O(n k) |
| `beauty_solution.kara` | LeetCode's Rust template: `String` and `i32` in, `i32` out; `as_bytes()`, a `matches!` closure for the primes, and a `vec![vec![0i64; n + 1]; k + 1]` table filled by a running sum per row; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 26 lines: LeetCode's three examples; then
seven more, a prime and a non-prime digit alone, a string that cannot
start, one that cannot end, parts too long for the string, every cut
taken, and two parts asked of a string with no cut inside it; then
three of the constraints' largest, `"21"` 500 times into 500, 250 and
100 parts; a random string of 1000 digits, a prime first and a
non-prime last, with `k` of 1, 10, 100 and 300 and `minLength` of 1, 2
and 3; and 3000 random strings of 1 to 40 digits with `k` and
`minLength` from 1 to the length, as a checksum. `beauty.py` mirrors the
★ arm and its output is byte-identical, and the mirror was checked on
6000 random strings of 1 to 13 digits, half of them from `2`, `7`, `3`
and `1` alone, against a brute force that tries every set of cuts. The
two agreed on every string.

`check` first reports 10 errors on the template, and `karac fix`
carries it in one call, reporting 20 edits: `matches!` becomes a
`match` with a `_ => false` arm, since Kāra has no macros; every `!`
becomes `not`, `||` `or` and `&&` `and`; `as_bytes()` becomes
`bytes()`; the `as usize` casts become `as i64`; `vec![vec![0i64; n +
1]; k + 1]` becomes `Vec.filled(k + 1, Vec.filled(n + 1, 0))` and `0i64`
loses its suffix; and the wrapper's `as i64` on the `i32` answer goes,
since an `i32` widens by itself. The `u8` closure parameter, the byte
literals `b'2'`, the `const` inside the method, `1_000_000_007` and the
`..=` ranges stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every subset of the `n - 1` places between digits is taken
as a set of cuts, and counted when it makes `k` parts, each at least
`minLength` long, beginning with a prime digit and ending with a
non-prime one. No cut list, table or running sum is used. It checks 300
random strings of 1 to 10 digits, then 60 of up to 14, half drawn from
1 to 9 and half from 1, 2, 3 and 4 alone; three in four are then given
a prime first digit and a non-prime last one, `k` is drawn from 1 to
`1 + n / 3` and `minLength` from 1 to `1 + n / (2 k)`, so that 203 of
the 360 have a partition. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | one part: 1 when the whole string begins with a prime, ends with a non-prime and is at least `minLength` long, else 0 |
| P3 | a `minLength` of 1: the ways to choose `k - 1` of the places between a non-prime and a prime digit, when the string begins with a prime and ends with a non-prime, else 0 |
| P4 | every prime digit renamed to another prime and every other digit to another non-prime: the same count |
| P5 | every digit written twice, with a `minLength` of `2 m - 1`: the same count |
| P6 | each arm agrees with at least three of the other five |

P3 holds because with a `minLength` of 1 any `k - 1` distinct cuts make
parts of one digit or more. P4 holds because only whether a digit is
prime is read. P5 holds because a cut never falls between the two
copies of a digit, so the cuts of the doubled string are those of the
original at twice the place, and every part twice as long; a part of
even length is at least `2 m - 1` long exactly when it is at least
`2 m`.

The differential prints `360 cases: checksum 285746460, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries the same subsets. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 9 a prime | P1 51, P2 59, P3 52, P4 83, P6 51 |
| M3 | ★: the last digit not checked | P1 18, P2 21, P3 18, P6 18 |
| M4 | ★: a cut after any non-prime | P1 84, P3 102, P5 136, P6 84 |
| M7 | table: a part one digit longer | P1 36, P2 13, P5 36, P6 36 |
| M9 | table: a part may begin at any prime | P1 80, P3 100, P5 132, P6 80 |
| M10 | table: the sums not accumulated | P1 186, P2 266, P3 204, P5 17, P6 186 |
| M12 | memo: any place a finish | P1 68, P2 154, P3 83, P6 68 |
| M13 | memo: parts one digit short allowed | P1 31, P3 52, P6 31 |
| M15 | memo: the sum skipping every other place | P1 116, P2 139, P3 135, P5 91, P6 116 |
| M18 | cuts: the end not a cut | P1 147, P2 125, P3 138, P6 147 |
| M20 | cuts: an empty part counted | P1 65, P3 65, P6 65 |
| M21 | cuts: the trail one cut short | P1 136, P2 114, P3 138, P6 136 |
| M22 | iter: the pair read backwards | P1 95, P3 123, P6 95 |
| M24 | iter: the earlier round carried into the short places | P1 140, P3 140, P6 140 |
| M26 | iter: one round too many | P1 170, P2 186, P3 159, P6 170 |
| M27 | solution: 7 not a prime | P1 65, P2 82, P3 64, P4 109, P6 65 |
| M28 | solution: only the latest start | P1 74, P2 158, P3 83, P6 74 |

P1 and P6 kill all seventeen, P3 sixteen, P2 eleven, P5 five, and P4
two.

Fourteen are not kept. Three fail exactly as a kept one: the cuts
arm's part exactly `minLength` long refused and the template's
`minLength` one more (M17, M30) as the table arm's part one digit
longer (M7), and the iter arm's sum dropped after each place (M25) as
the table arm's sums not accumulated (M10). Six count nothing at all
and so fail alike, apart from every kept one: the ★ arm's shortest part
skipped, the table arm's end not an end, the cuts arm's first cut never
a start, the iter arm's part exactly `minLength` long refused, and the
template's end never reached and first part never laid (M2, M8, M19,
M23, M29, M31). Two count one part fewer and fail alike: the ★ arm's
one round too few and the memo arm's one part left taken as none (M5,
M16). Two more fail alike: the ★ arm's running sum restarted at each
cut and the memo arm's only the nearest start (M6, M14). The
table arm's part one digit shorter allowed (M11) fails apart from every
kept one, its arm having three kept already. No edit crashes, and every
edit is killed by some check.

Six edits were replaced before this table was drawn, every one of them
surviving every check because it changes nothing the answer reads: the
table arm's first cut place skipped, the cuts arm's last one skipped,
the iter arm's start allowed after the first digit, and the template's
start allowed at the second digit and part allowed to end before any
prime. A cut, or a start, next to either end of the string needs a
non-prime first digit or a prime last one, and the string is refused
for either before any count; a part that ends before two primes in a
row is never read, because no part can begin there. The memo arm's
after table a row too narrow shares a place between the end of one row
and the start of the next, but no count ever asks for a part to begin
at the start.

## Verification

Every arm prints the same output as `beauty.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports no error
or warning on any of them, and `karac fix --dry-run` has nothing to
apply. The memo arm, and the differential that copies it, get one note,
L0002: its `from` and `after` call each other, and their effects are
found together by a fixed point.

Under `karac __mir-run` the arms take 0.8 to 7.1 s and the differential 1.3 s; under `karac __mir-llvm-asan` the arms take 0.6 to 1.9 s and the differential 1.0 s, and under `karac run` the differential takes 0.7 s.

## Benchmarks

The bench builds 20 random strings of 1000 digits once from its own
generator, each with a prime first digit and a non-prime last one, then
makes 90 passes; each answers every string with `k` from 1 to 100 and
`minLength` from 1 to 5 chosen by the checksum so far, so no answer
carries over, folding the count plus the pass into the checksum. The
bench uses the ★ arm in all five languages; Kāra and Python keep each
string as text and read its digits on every call, and C, Rust and Go
keep the digits themselves. Every implementation prints `90 passes over 20
strings of 1000: checksum 651547335`.

BENCHTAB
