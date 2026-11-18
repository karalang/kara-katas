# 2264. Largest 3-Same-Digit Number in String

You are given a string `num` representing a large integer. An integer
is **good** if it meets the following conditions:

- It is a **substring** of `num` with length `3`.
- It consists of only one unique digit.

Return *the **maximum good** integer as a **string** or an empty string*
`""` *if no such integer exists.*

Note: a **substring** is a contiguous sequence of characters within a
string, and there may be **leading zeroes** in `num` or a good integer.

```
num = "6777133339"  ->  "777"
num = "2300019"     ->  "000"
num = "42352338"    ->  ""
```

**Constraints:** `3 <= num.length <= 1000`; `num` only consists of
digits.

Every good integer is one digit three times, so there are only ten
candidates, and the largest is the largest digit that is ever seen
three times running. One pass finds it.

## Approaches

| file | mechanism |
|---|---|
| `good.kara` ★ | one pass over the bytes: where `b[i - 2]`, `b[i - 1]` and `b[i]` agree, `b[i]` is a candidate; the largest kept in an `Option[u8]`, then `repeat(3)` |
| `good_digits.kara` | the ten candidates from `999` down to `000`, `d.to_string().repeat(3)`, the first that `num.contains` |
| `good_runs.kara` | the length of the current run over `chars()`, a run reaching three making its digit a candidate, `' '` standing for none |
| `good_struct.kara` | `struct Window` of the last two digits and the best, each an `Option[u8]`; `take` (`mut ref self`) shifts one digit in, a guarded `match` keeping the larger |
| `good_iter.kara` | one chain: `windows(3)`, `filter` where all three agree, `map` to the digit, `max`, then the `Option` mapped to the digit three times, `unwrap_or` "" |
| `good_solution.kara` | LeetCode's Rust template: `String` in, `String` out; `as_bytes().windows(3)`, the best digit an `Option<u8>` folded with `map_or`, the answer `String::from_utf8(vec![c; 3])`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more (the run at the very end, a run of four, `000` the only one, and
none in three digits), each with its answer; then 2000 numbers of 3 to
40 digits from the first 2, 3, 4 or 10, with how many have none (791)
and a checksum of the answers read as numbers, 1000 for none; then
three of the constraints' longest, 1000 digits: random from all ten
(`999`), `1100` repeated (none), and `12` repeated with `9999` at the
end (`999`). `good.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round, reporting 8 edits:
`as_bytes()` to `bytes()`, `Option<u8>` to `Option[u8]`, `&&` to
`and`, `String::from_utf8` and `String::new` to their `.` paths,
`vec![c; 3]` to `Vec.filled(3, c)`, and `struct Solution;` to `struct
Solution {}`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every substring of length 3, kept when the `Set[char]` of its
digits has one member, the largest kept by comparing the substrings
themselves. No running counts and no candidate list. It checks 300
random numbers of 3 to 12 digits from the first 2, 3, 4 or 10; then 30
that alternate two digits and have no good integer; then 30 with a run
of three to five of one digit put in at a random place. All 360 are
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the number reversed: the same answer |
| P3 | every digit `d` made `9 - d`: `9 - d` of the SMALLEST digit seen three times running, or "" for none |
| P4 | "" or one digit three times, and found in the number |
| P5 | `000` put in front: the same answer, or `000` for none |
| P6 | each arm agrees with at least three of the other five |

P3 turns the largest into the smallest, so it checks the order of the
candidates from the other end: an arm that keeps the smallest, or the
first or last found, passes P1 only by luck on one side of it.

The differential prints `360 cases: checksum 453337955, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that keeps
the largest `d * 3` that is `in` the number. On a failure it prints the
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
| M1 | ★: two the same | P1 133, P2 59, P3 136, P4 133, P5 30, P6 133 |
| M4 | ★: the scan from the fourth byte | P1 10, P2 30, P3 11, P5 179, P6 10 |
| M6 | ★: the first and third only | P1 158, P3 163, P4 158, P6 158 |
| M8 | digits: 9 never tried | P1 2, P3 53, P6 2 |
| M9 | digits: the candidate twice over | P1 266, P3 266, P4 266, P5 94, P6 266 |
| M10 | digits: 0 never tried | P1 39, P3 2, P5 258, P6 39 |
| M12 | runs: the run never reset | P1 72, P2 66, P3 77, P4 42, P5 289, P6 72 |
| M13 | runs: the run reset to 0 | P1 93, P3 88, P5 226, P6 93 |
| M14 | runs: the first run of three kept | P1 12, P2 18, P3 6, P5 93, P6 12 |
| M17 | struct: the newer digit never shifted | P1 141, P3 141, P5 360, P6 141 |
| M20 | struct: the answer once | P1 141, P3 141, P4 141, P5 219, P6 141 |
| M21 | struct: the window opened on two zeros | P1 48, P2 57, P3 9, P4 48, P6 48 |
| M22 | iter: windows of two | P1 162, P3 159, P4 162, P6 162 |
| M23 | iter: the min | P1 18, P3 18, P5 88, P6 18 |
| M25 | iter: none as `000` | P1 219, P3 219, P4 219, P6 219 |
| M28 | solution: the last found | P1 6, P2 18, P3 12, P6 6 |
| M29 | solution: two the same | P1 144, P2 59, P3 143, P4 144, P6 144 |

P1, P3 and P6 kill all seventeen, P5 ten, P4 nine, and P2 seven. P3
catches every edit. P4 catches the answers of the
wrong shape or found nowhere: two the same, the ends only, the answer
once, none as `000`. P2 catches the edits that favour one end: the
first or last found, the scan from the fourth byte, a window opened on
zeros. 9 never tried is wrong only in the 2 cases whose answer is
`999`, and P3 alone finds it 53 times, where `000` becomes `999`.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Twelve fail as a kept one does: the ★ arm's
first good one kept and the iter arm's first good window (M2, M26) as
the runs arm's first run kept (M14); the ★ arm's smallest kept, the
digits arm's candidates rising, the struct arm's best replaced by any
smaller and the template's min (M3, M7, M18, M27) as the iter arm's
min (M23); the ★ arm's digit twice and the template's four times (M5,
M30) as the struct arm's answer once (M20); the runs arm's run of two
and the struct arm's older digit never compared (M16, M19) as the iter
arm's windows of two (M22); the iter arm's ends only (M24) as the ★
arm's first and third only (M6); and the runs arm's previous digit
never moved (M15) as the struct arm's newer digit never shifted (M17).
Two fail in ways of their own and are left out because their arms keep
enough: the digits arm's candidate four times over (M11) and the
template's windows of four (M31).

Two edits of the first draft were equivalent and were replaced: the
runs arm's run of exactly three, `run < 4` added beside `run == 3`,
which always holds there; and the struct arm's shift the wrong way,
the new digit into `older` and `older` into `newer`, which swaps the
two slots' roles when the test asks both to equal the digit. They are
now M15 and M21.

## Verification

Every arm prints the same output as `good.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.3 s and the
differential 0.5 s.

## Benchmarks

The bench answers 2000 numbers of the constraints' longest, 1000
digits, from the first 4 and all 10 digits in turn, with the ★ arm in
all five languages, the answer read back as a number for the checksum.
Every implementation prints `2000 numbers of 1000: checksum 774619274`.
Each builds its number a digit at a time from the same generator and
returns a fresh string of the answer.

BENCHTAB
