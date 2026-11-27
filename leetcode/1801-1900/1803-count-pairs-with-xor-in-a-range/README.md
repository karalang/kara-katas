# 1803. Count Pairs With XOR in a Range

Given a (0-indexed) integer array `nums` and two integers `low` and
`high`, return the number of nice pairs. A nice pair is a pair `(i, j)`
where `0 <= i < j < nums.length` and `low <= (nums[i] XOR nums[j]) <=
high`.

```
nums = [1,4,2,7], low = 2, high = 6       ->  6
nums = [9,8,4,2,1], low = 5, high = 14    ->  8
```

**Constraints:** `1 <= nums.length <= 2 * 10^4`, `1 <= nums[i] <= 2 *
10^4`, and `1 <= low <= high <= 2 * 10^4`.

The arms are `fn count_pairs(nums: Vec[i32], low: i32, high: i32) ->
i32`.

## Approaches

| file | mechanism |
|---|---|
| `count_pairs.kara` ★ | a binary trie over the numbers' 15 bits, kept as two flat `Vec`s of child links and counts; the pairs whose XOR is below a limit counted for each number against those before it by walking the limit's bits, a 1 in the limit taking in the whole subtree on the number's own side, and the range taken as the count below `high + 1` less the count below `low`. O(n * 15) |
| `count_pairs_fwht.kara` | every XOR counted at once: the numbers' frequencies, over the least power of two past every number and the range, put through the Walsh-Hadamard transform, squared, and transformed back, which gives the ordered pairs for each XOR value. O(n + V log V) |
| `count_pairs_split.kara` | no trie: the numbers sorted once, and the pairs below a limit counted by splitting runs of the sorted list at each bit with `partition_point`, two runs that agree with the limit so far walked on, and the pairs on the same side of a 1 bit of the limit counted whole. O(n log n) and a split per run per bit |
| `count_pairs_levels.kara` | the trie flattened into one count table per bit, how many numbers so far have each prefix `v >> b`: a `y` before `x` has `x ^ y` below a limit with its first difference at a 1 bit `b` of the limit exactly when `y >> b` is `((x ^ limit) >> b) ^ 1`. O(n * 15) |
| `count_pairs_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `fn count` nested in the method, `Vec<[usize; 2]>` links, `vec![[0, 0]]`, `for &x in nums`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`6 8`); five
edges, one number, two alike, whose XOR of 0 is below a range from 1,
the widest range with a 20000 whose XOR with each small number passes
it, a range of one value, and no pair reaching the range (`0 0 3 1 0`);
the constraints' most, `2 * 10^4` numbers at random in the widest range
and in 4000 to 5000, and `2 * 10^4` alike (`the most: 170136494 9584687
0`); and 3000 random cases of 1 to 20 numbers of up to 64 and a range
inside 1 to 70 (`3000 random cases: checksum 292421823`).
`count_pairs.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, fwht and split arms check clean as first written.
The fwht arm was first written over a fixed `1 << 15` values, which ran
the 3000 random cases through two transforms of 32768 values each, 4.2 s
on the compiled lane; it now sizes the transform to the numbers and the
range, 0.4 s. The levels arm indexed its tables with `((x ^ limit) >> b
^ 1) as i64` and `(x >> b) as i64`, and check warns that each cast is a
widening Kāra does implicitly (`lossless_cast`); `karac fix` removed
both, 2 fixes. The Rust solution takes one round of 26 fixes by `karac
fix`'s count, and its diff is: `struct Solution;` to `struct Solution
{}`; the nested `fn count` moved above the `impl`, its `&Vec<i32>`
parameter to `ref Vec[i32]`; `Vec<[usize; 2]>` to `Vec[Array[i64, 2]]`
and every `as usize` to `as i64`; `vec![[0, 0]]` and `vec![0]` to the
literals `[[0, 0]]` and `[0]`; `let mut res = 0;` annotated `res: i32`;
`for &x in nums` to `for x in nums`; the `&` dropped from `count(&nums,
..)`; `Vec<i32>` to `Vec[i32]`; and `Solution::` to `Solution.`. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every pair `i < j` whose XOR lies from `low` to `high`.
LeetCode's examples, the edges, 4000 numbers of up to `2 * 10^4` at
random in two ranges and 4000 alike, 300 random cases of up to 300
numbers of up to `2 * 10^4`, and 1690 of 1 to 14 numbers of up to 64.
Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, for at most 200 numbers |
| P2 | the numbers in reverse order give the same answer |
| P3 | the range cut in two counts the same pairs between its parts |
| P4 | every number doubled doubles every XOR, so the range from `2 * low` to `2 * high + 1` gives the same answer, while that stays inside the constraints |
| P5 | the range from 1 to the least `2^k - 1` past every number holds every pair of two different numbers |
| P6 | the ★ arm's answer |

The differential's fixed cases are pushed as tuples into a
`Vec[(Vec[i32], i32, i32)]`, and check refused each as a `(Vec[i64],
i32, i32)`, `[1, 4, 2, 7].to_vec()` and `Vec.filled(20000, 20000)`
taking `i64` before the push's element type reaches them, with no fix;
that is B-2026-11-26-6 and B-2026-11-26-86. The first number of the
`.to_vec()` list is suffixed by hand, `[1i32, 4, 2, 7].to_vec()`, while
B-2026-11-26-6 is open; B-2026-11-26-86 is fixed at 95bb5be7d1, and
`Vec.filled(4000, 20000)` now checks as written, its suffix taken off.
`karac fix` dropped one `nums.clone()` handed to a parameter that only
borrows (`redundant_clone`). Its large cases were first written with
`2 * 10^4` numbers, and the interpreter took 8 min 42 s over the
differential; with 4000 it takes 6 min 52 s. All 56,020 checks pass on
every arm: `2000 cases: checksum 754976972, 56020 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the numbers on the wrong side of a 1 bit counted | P1 948, P5 1566, P6 4184 |
| M2 | ★: the range's top left out | P1 249, P3 387, P4 209, P5 776, P6 1248 |
| M3 | fwht: the transform's difference taken the wrong way round | P1 849, P5 1423, P6 947 |
| M4 | fwht: the range's top left out | P1 249, P3 387, P4 209, P5 776, P6 312 |
| M5 | split: only the pairs of two zeros counted where the limit has a 1 | P1 659, P6 757 |
| M6 | split: the pairs within the ones' run left out | P1 622, P5 681, P6 683 |
| M7 | levels: the prefix read without its last bit turned | P1 948, P5 1566, P6 1046 |
| M8 | levels: the lowest level never filled | P1 273, P4 241, P5 964, P6 321 |
| M9 | solution: the walk kept on the same side at a 1 bit | P1 1525, P6 1624 |
| M10 | solution: the limit's bits read inverted | P1 941, P5 1566, P6 1039 |

## Benchmarks

The bench builds 40 random lists of 20000 numbers of up to `2 * 10^4`
once, and makes 100 calls of the ★ arm with a random range, each list
drawn from the checksum so far. It checks clean as first written. Every
implementation prints `100 calls over 40 lists of 20000 numbers:
checksum 208858242`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra is ahead of Rust here at 0.42 s against Rust's 0.46 s (0.48 s with
overflow checks on), C's 0.35 s and Go's 0.70 s; Python takes 16.9 s.
