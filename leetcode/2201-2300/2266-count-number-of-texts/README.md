# 2266. Count Number of Texts

Alice is texting Bob using her phone. The keys `2` to `9` each map to
three letters, except `7` (`pqrs`) and `9` (`wxyz`), which map to four.
To add a letter, Alice has to press the key of the corresponding digit
`i` times, where `i` is the position of the letter in the key. Due to
an error in transmission, Bob did not receive Alice's text message but
received a string of pressed keys instead.

Given a string `pressedKeys` representing the string received by Bob,
return *the **total number of possible text messages** Alice could have
sent*. Since the answer may be very large, return it **modulo**
`10^9 + 7`.

```
pressedKeys = "22233"                                 ->  8
pressedKeys = "222222222222222222222222222222222222"  ->  82876089
```

**Constraints:** `1 <= pressedKeys.length <= 10^5`; `pressedKeys` only
consists of digits from `'2'` to `'9'`.

The last letter of a message took the last 1, 2 or 3 presses of one
key, or 4 on `7` and `9`, so the count for a prefix is the sum of the
counts for the prefixes that many presses shorter, as far as the run
of that key reaches. O(n).

## Approaches

| file | mechanism |
|---|---|
| `texts.kara` ★ | a table `ways` over the prefixes, `ways[i]` adding `ways[i - j]` while the `j` presses back are the same key, up to 3 or 4 |
| `texts_runs.kara` | by runs of one key: the counts multiply across runs, and a run of `n` on a key of `k` letters counts the ordered sums of `n` in parts 1 to `k`, from two tables filled first |
| `texts_rolling.kara` | the ★ arm's table cut to its last four entries, `let mut (a, b, c, d)`, with the run's length kept as it grows |
| `texts_struct.kara` | `struct Keypad` of the last four counts in an `Array[i64, 4]`, the run's key and its length; `press` (`mut ref self`) takes one key, and `Keypad.letters` matches `b'7' \| b'9'` |
| `texts_iter.kara` | by runs, in chains: a `fold` gathers `(key, length)` pairs, a `fold` over each length carries the last four counts with `take(parts).sum()`, and a last `fold` multiplies |
| `texts_solution.kara` | LeetCode's Rust template: `String` in, `i32` out; a `const MOD` inside the method, `vec![0i64; n + 1]`, and an inner `for k in 1..=max` that breaks at the first different key; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one press, 1; four presses of `2`, 7; four of `7`, 8; two keys
alternating, 1; five of `7`, 15), each with its count; then 2000
strings of 1 to 40 presses from `2`, `79`, `27`, `234` or all eight
keys, with a checksum; then three of the constraints' longest, 10^5
presses: all `7` (472399532), all `2` (111787461), and random from `7`
and `9` (548739371). `texts.py` mirrors the ★ arm and its output is
byte-identical.

The harness passes each case's key set as `["2", "79", ..][t % 5]`
straight to `presses`. Bound first as `let keys: Str = ["2", "79",
..][t % 5];`, it is refused, as the strings chapter says: the array's
literals are `String`s, the annotation's `Str` does not reach them
through the index, and a `String` is passed as a `Str` only at a call.
`karac check` says so and names `.as_str()`.

`karac fix` carries the template in one round, reporting 7 edits:
`as_bytes()` to `bytes()`, `vec![0i64; n + 1]` to `Vec.filled(n + 1,
0)`, the two `||` to `or`, `struct Solution;` to `struct Solution {}`,
and the adapter's `as i64` dropped. The `const MOD` inside the method
and `1..=max` are Kāra as they stand.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to cut the presses into letters, each letter one
to three presses of one key, or four on `7` and `9`, counted one by one
by recursion. No table and no runs. It checks 300 random strings of 1
to 12 presses from `2`, `7`, `79`, `27`, `234` or all eight keys; then
30 runs of one key; then 30 that alternate two keys. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the count is the literal reading's |
| P2 | the presses reversed: the same count |
| P3 | the keys relabelled, `2 3 4 5 6 8` in a ring and `7` with `9`: the same count |
| P4 | one more press of a key unlike the last: the same count |
| P5 | the presses twice over with a key unlike both ends between: the count squared, modulo 10^9 + 7 |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 581415628, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that splits
the presses with `itertools.groupby` and counts each run by memoised
recursion. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every key of four letters | P1 58, P6 58 |
| M5 | ★: the empty prefix counted 2 | P1 360, P5 360, P6 360 |
| M6 | ★: the run compared with the first press | P1 192, P4 168, P5 168, P6 192 |
| M7 | runs: the runs added | P1 355, P4 360, P5 329, P6 355 |
| M8 | runs: the tables swapped | P1 125, P6 125 |
| M10 | runs: parts up to two | P1 95, P6 95 |
| M12 | rolling: the run never grows | P1 271, P6 271 |
| M14 | rolling: the shift skipping `c` | P1 44, P6 44 |
| M16 | rolling: the run's reach by the key only | P1 192, P2 60, P4 360, P5 360, P6 192 |
| M18 | struct: 9 of three letters | P1 9, P3 67, P6 9 |
| M19 | struct: the reach one more | P1 192, P2 115, P4 360, P5 360, P6 192 |
| M21 | struct: the start counted 0 | P1 360, P6 360 |
| M22 | iter: the parts one fewer | P1 161, P6 161 |
| M25 | iter: the runs summed | P1 186, P4 360, P5 360, P6 186 |
| M26 | iter: every run of three-letter keys | P1 67, P6 67 |
| M27 | solution: max one more | P1 102, P6 102 |
| M28 | solution: the break a continue | P1 124, P4 57, P5 295, P6 124 |

P1 and P6 kill all seventeen, P5 seven, P4 six, P2 two, and P3 one.
This kata's properties are weak, and P1 carries it: most edits miscount
every run the same way wherever it stands, so a reversed, relabelled or
repeated string is miscounted consistently. P4 and P5 catch the edits
that let a letter span two keys or that combine runs wrongly; P2 the
two that reach past the run's start; and P3 only 9 of three letters,
which relabelling swaps onto `7`. Every key of four letters passes P3
because the ring keeps the three-letter keys among themselves.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Thirteen fail as a kept one does: the ★ arm's run
not checked and the struct arm's run kept across keys (M3, M20) as the
rolling arm's reach by the key only (M16); the ★ arm's only 7 of four
letters (M2) as the struct arm's 9 of three letters (M18); the ★ arm's
letters of at most two presses (M4) as the iter arm's parts one fewer
(M22); the runs arm's run one shorter and each run of one press, the
rolling arm's last key never kept, the struct arm's oldest count never
shifted out, and the iter arm's run of n counted as n - 1 and new run
on every press (M9, M11, M15, M17, M23, M24) as the rolling arm's run
never grows (M12); the
rolling arm's four-back count never added (M13) as the iter arm's
three-letter keys (M26); the template's table from `dp[1]` (M30) as
the struct arm's start counted 0 (M21); and the template's key compared
with the first press (M29) as the ★ arm's (M6). One fails in a way of
its own and is left out because its arm keeps enough: the template's
last two presses only (M31).

The template's key compared with the next press, `s[i - k + 1]`, read
past the end of the table and stopped with an index out of bounds
under both backends; it was replaced by the comparison with the first
press, now M29.

## Verification

Every arm prints the same output as `texts.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the rolling arm takes 0.7 s, the ★ arm 0.9 s,
the differential 1.0 s, the template 1.4 s, the runs arm 1.7 s, the
iter arm 2.6 s, and the struct arm 2.8 s.

## Benchmarks

The bench answers 40 strings of the constraints' longest, 10^5
presses, from `2`, `79`, `234` and all eight keys in turn, with the ★
arm in all five languages. Every implementation prints `40 strings of
10^5: checksum 435193927`. Each builds its string a press at a time
from the same generator and allocates the table per call.

BENCHTAB
