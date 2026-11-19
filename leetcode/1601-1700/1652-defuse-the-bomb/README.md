# 1652. Defuse the Bomb

You have a bomb to defuse, and your time is running out! Your informer
will provide you with a **circular** array `code` of length `n` and a
key `k`.

To decrypt the code, you must replace every number. All the numbers are
replaced **simultaneously**.

- If `k > 0`, replace the `i`th number with the sum of the **next** `k`
  numbers.
- If `k < 0`, replace the `i`th number with the sum of the **previous**
  `k` numbers.
- If `k == 0`, replace the `i`th number with `0`.

As `code` is circular, the next element of `code[n-1]` is `code[0]`, and
the previous element of `code[0]` is `code[n-1]`.

Given the **circular** array `code` and an integer key `k`, return *the
decrypted code to defuse the bomb*!

```
code = [5,7,1,4], k = 3   ->  [12,10,16,13]
code = [1,2,3,4], k = 0   ->  [0,0,0,0]
code = [2,4,9,3], k = -2  ->  [12,5,6,13]
```

**Constraints:** `n == code.length`; `1 <= n <= 100`;
`1 <= code[i] <= 100`; `-(n - 1) <= k <= n - 1`.

## Approaches

| file | mechanism |
|---|---|
| `defuse.kara` ★ | one window of `|k|` numbers slid once round the circle: `1 ..= k` for position 0 when `k > 0`, `n + k ..= n - 1` when `k < 0`, indices modulo `n`; each step adds the number entering and drops the one leaving. O(n) |
| `defuse_brute.kara` | each sum on its own, walking `|k|` steps round the circle from each position. O(n \|k\|) |
| `defuse_prefix.kara` | prefix sums over the code laid out twice, so every window is a plain range of it. O(n) |
| `defuse_solution.kara` | LeetCode's Rust template: the same sliding window with `usize` ends. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, one number
with `k = 0`, and five numbers with `k = 4` and `k = -4`, reaching all
the way round each way; then every answer summed and a checksum for 3000
random codes of up to 8 numbers and 3000 of up to 100. `defuse.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each position, the next `k` or previous `-k` numbers
added one by one round the circle. It checks 3000 random codes of 1 to 8
numbers from 1 to 100, each with a `k` from `-(n - 1)` to `n - 1`. Every
code is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the code turned one place round turns the answer one place round |
| P3 | the code reversed with `k` negated gives the answer reversed |
| P4 | every number doubled doubles every answer |
| P5 | each arm agrees with at least two of the other three |

P3 holds because reversing the code turns "the next `k`" into "the
previous `k`" at the mirrored position.

The differential prints `3000 problems: checksum 522201575, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first window for `k > 0` starts at position 0 | P1 1101, P3 2242, P5 1101 |
| M2 | ★: the number leaving the window never dropped | P1 2242, P2 2242, P3 2242, P5 2242 |
| M3 | ★: the first window one number short | P1 2242, P2 2226, P3 2227, P5 2242 |
| M4 | brute: `k < 0` walks forward | P1 740, P3 1456, P5 740 |
| M5 | brute: each walk starts at the position itself | P1 2242, P5 2242 |
| M6 | prefix: the window for `k > 0` one place early | P1 1101, P3 2242, P5 1101 |
| M7 | prefix: the window for `k < 0` one place late | P1 1141, P3 2242, P5 1141 |
| M8 | prefix: each prefix only its last number | P1 2242, P3 1983, P5 2242 |
| M9 | template: the number entering dropped, not the one leaving | P1 1476, P2 1461, P3 1476, P5 1476 |
| M10 | template: the first window for `k < 0` one number long | P1 1141, P3 2242, P5 1141 |

## Benchmarks

The bench draws 400 random codes of `10^5` numbers from 1 to 100, each
with a `k` from -99999 to 99999, all of them first, then decrypts each by
the ★ arm in all five languages and sums and checksums every answer.
Every implementation prints `400 codes of 100000 numbers: answers sum to
169336435775564, checksum 477717491`. The C build also runs clean under
gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `defuse.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★ arm wrote `let (mut start, mut end)`, which `karac fix` turned into
`let mut (start, end)`, and it declared `sum: i32`, the window's sum
being returned in a `Vec[i32]`. The brute arm's `let mut sum = 0` inside
the closure got the same `sum: i32`.

PREFIXNOTE

LeetCode's Rust template takes one `karac fix` of 12 edits:
`struct Solution;` to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`,
`vec![0; n]` to `Vec.filled(n, 0)`, `let (mut l, mut r)` to
`let mut (l, r)`, `k as usize` to `k as i64`, and the `as usize` on
`(-k)` dropped, an `i32` widening to the `i64` it is subtracted from.
The arm then checks and agrees with no hand edit.
