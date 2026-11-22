# 2710. Remove Trailing Zeros From a String

Given a **positive** integer `num` represented as a string, return *the
integer* `num` *without trailing zeros as a string*.

```
num = "51230100"  ->  "512301"
num = "123"       ->  "123"
```

**Constraints:** `1 <= num.length <= 1000`; `num` consists of only
digits; `num` doesn't have any leading zeros.

## Approaches

| file | mechanism |
|---|---|
| `zeros.kara` ★ | an index walks back from the end over the zeros; the first digit is not zero, so it stops there at the latest, and the digits before it are the answer. O(n) |
| `zeros_strip.kara` | the library's `strip_suffix` takes one "0" off the end while there is one, each time giving a shorter `Str` view of the same text, and the last view is copied out. O(n) |
| `zeros_iter.kara` | the digits reversed, the zeros now leading skipped by `skip_while`, and what is left reversed back and collected. O(n) |
| `zeros_position.kara` | the last digit that is not zero found by `rposition` over the bytes, and the number cut just after it. O(n) |
| `zeros_solution.kara` | a Rust solution as LeetCode's Rust users write it, the `mut` parameter popped while it `ends_with('0')`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; one digit;
10; the lengths of the answers for a 1 and 999 zeros and for 1000
nines, LeetCode's longest; zeros only inside; zeros inside and out; then
the zeros removed and a checksum for 3000 random numbers of up to 1000
digits, zeros 0 to 3 times in 4, half of them with up to 19 more zeros
on the end, cut to 1000. `zeros.py` mirrors the ★ arm and its output is
byte-identical.

```
512301
123
1
1
1
1000
100000000000000000000000000000000000000000000000000000000000000000001
10203
3000 numbers: 17967 zeros removed, checksum 303096567
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the shortest prefix that gives the number back when only
zeros are written after it, every prefix tried from the shortest. It
checks 1000 random numbers of 1 to 12 digits and 200 of up to 980,
zeros 0 to 3 times in 4, each with 0 to 3 zeros more on the end. Every
case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer does not end in a zero and begins the number |
| P3 | 1 to 20 zeros more on the end: the same answer |
| P4 | the answer with as many zeros written after it as it is shorter: the number |
| P5 | the answer's own answer is itself |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1200 cases: checksum 739695333, 36000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, prefix by prefix, gives the same checksum. On
a failure it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M1, M4 and M9 are one fault in three arms, a
single zero removed at most, and fail the same cases. One first choice,
the position arm's cut one before the last digit, crashed on an
`unwrap()` of `None` for a number of one digit rather than answering
wrong, and was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one zero removed at most | P1 779, P2 779, P3 1189, P5 779, P6 779 |
| M2 | ★: the walk keeps one zero | P1 1020, P2 1020, P3 180, P6 1020 |
| M3 | strip: zeros stripped two at a time | P1 601, P2 601, P3 614, P6 601 |
| M4 | strip: one zero stripped at most | P1 779, P2 779, P3 1189, P5 779, P6 779 |
| M5 | iter: every zero dropped, inside too | P1 761, P2 761, P4 761, P6 761 |
| M6 | iter: the digits left reversed | P1 1001, P2 1001, P4 1001, P5 1001, P6 1001 |
| M7 | position: the first digit that is not zero | P1 1020, P4 1020, P6 1020 |
| M8 | position: the cut never before the number's middle | P1 133, P2 133, P3 768, P5 133, P6 133 |
| M9 | solution: one zero popped at most | P1 779, P2 779, P3 1189, P5 779, P6 779 |
| M10 | solution: two popped for each zero | P1 601, P3 614, P4 601, P6 601 |

## Benchmarks

The bench draws `2 * 10^4` numbers of 1000 digits, LeetCode's longest,
each a random head and a run of 0 to 999 zeros, all of them first, then
answers each 20 times by the ★ arm in all five languages; each answer
walks back over the zeros and copies the head out. Every implementation
prints `20000 numbers of 1000 digits, 20 rounds: 201207920 digits kept,
checksum 796792004`.

BENCHTAB

## Verification

All five arms print the same output as `zeros.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, iterator and position arms checked clean as first written. The
strip arm was first meant as Rust's `trim_end_matches('0')`, which
Kāra's `String` does not have; the library's `strip_suffix` in a loop is
the spelling it offers. `karac fix` added the one `.as_str()` it
needed, where the shrinking `Str` view starts from the `String`.

LeetCode's Rust template took one `karac fix` of 4 edits: `struct
Solution {}` added; the `mut num` parameter, which Kāra does not have,
became `num: own String` with a `let mut num = num;` rebinding, since
popping needs the string owned; and `ends_with('0')` became
`ends_with("0")`, since the pattern is a string.
