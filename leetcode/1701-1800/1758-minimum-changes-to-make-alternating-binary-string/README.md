# 1758. Minimum Changes To Make Alternating Binary String

You are given a string `s` consisting only of the characters `'0'` and
`'1'`. In one operation, you can change any `'0'` to `'1'` or vice
versa. The string is called alternating if no two adjacent characters
are equal. For example, the string `"010"` is alternating, while the
string `"0100"` is not. Return the minimum number of operations needed
to make `s` alternating.

```
s = "0100"  ->  1
s = "10"    ->  0
s = "1111"  ->  2
```

**Constraints:** `1 <= s.length <= 10^4` and `s[i]` is either `'0'` or
`'1'`.

The arms are `fn min_operations(s: String) -> i32`.

## Approaches

There are only two alternating strings of each length, `"0101..."` and
`"1010..."`, and a character that differs from one agrees with the
other, so the two counts sum to the length.

| file | mechanism |
|---|---|
| `min_operations.kara` ★ | one pass over the bytes counting the characters that differ from `"0101..."`; the answer is the smaller of that count and the length less it. O(n) |
| `min_operations_both.kara` | both alternating strings built with `String.push`, and each compared with `s` through `chars().zip(..).filter(..).count()`. O(n) |
| `min_operations_fold.kara` | one `fold` over the bytes carrying both counts as a tuple. O(n) |
| `min_operations_greedy.kara` | a walk that flips each character equal to the one before it, once with the first character kept and once with it flipped, the flip counted. O(n) |
| `min_operations_solution.kara` | a Rust solution as LeetCode's Rust users write it (`c as u8 - b'0'` against `i % 2` as `usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's three examples (`1 0 2`);
seven edges, one character either way, two the same, alternating from
either end at odd and even length, and every character the same at odd
and even length (`0 0 1 0 0 4 5`); the constraints' most, 10000
characters all ones, alternating, a few ones, and evenly mixed (`10000
characters: 5000 0 4994 4922`); and 3000 random strings of 1 to 20
characters (`3000 random strings: checksum 591180653`).
`min_operations.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ and both arms check clean as first written. The
fold arm's `fold((0, 0), ..)` took 1 fix, to `fold((0i32, 0i32), ..)`,
since its counts are returned as an `i32`. The greedy arm was first
written with Rust's `&&` twice, and `karac fix` wrote `and` in 2 fixes.
The Rust solution takes one round of 5 fixes by `karac fix`'s count, and
its diff is: `struct Solution;` to `struct Solution {}`, `let mut cnt =
0` to `let mut cnt: i32 = 0`, `(c as u8 - b'0') as usize` to `(c as u32
as u8 - b'0') as i64`, and `Solution::` to `Solution.`. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every string of the same length, one bit of a mask for each
character, kept when no two neighbours are equal, and the fewest
characters of `s` that differ from one of them. LeetCode's examples, the
edges, and 1990 random strings of 1 to 12 characters, the chance of a
`'1'` drawn for each string. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | the string reversed needs the same |
| P3 | every character flipped needs the same |
| P4 | no more than half the characters |
| P5 | one more character changes the answer by at most one |
| P6 | the ★ arm's answer |

P4 was first written `got as i64 <= s.len() / 2`, and `karac fix`
dropped the cast. All 60,000 checks pass on every arm: `2000 cases:
checksum 77611728, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.
Python, reading every alternating string with `itertools.product`, gives
the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: only the changes to "0101..." counted | P1 717, P2 512, P3 1527, P4 717, P6 2868 |
| M2 | ★: each differing character counted twice | P1 1696, P2 512, P3 1527, P5 19, P6 6784 |
| M3 | both: "0101..." compared twice and "1010..." never | P1 717, P2 512, P3 1527, P4 717, P6 717 |
| M4 | both: each target one character short | P1 834, P2 515, P6 834 |
| M5 | fold: a character counted against both patterns | P1 717, P2 512, P3 1527, P4 717, P6 717 |
| M6 | fold: the larger count taken | P1 1527, P4 1527, P6 1527 |
| M7 | greedy: flipping the first character costs nothing | P1 829, P2 515, P6 829 |
| M8 | greedy: the second character never flipped | P1 994, P2 760, P4 147, P6 994 |
| M9 | solution: the pattern taken as 0, 1, 2 repeating | P1 1019, P2 713, P3 1032, P6 1019 |
| M10 | solution: the length taken one short | P1 1190, P2 512, P3 1527, P6 1190 |

## Benchmarks

The bench builds 2000 strings of 1 to 20000 characters once, each with
its own chance of a `'1'`, and makes 30000 calls of the ★ arm, each on a
string chosen from the checksum so far, about 300 million characters in
all. Every implementation prints `30000 calls over 2000 strings:
checksum 286952140`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.96 s against Rust's 0.15 s (1.1 s with overflow checks on),
C's 0.14 s and Go's 1.2 s; Python takes 19.8 s. Rust with overflow
checks on takes about as long as Kāra, which checks integer overflow by
default, and plain Rust about as long as C.
