# 2731. Movement of Robots

Some robots are standing on an infinite number line with their initial
coordinates given by a **0-indexed** integer array `nums` and will start
moving once given the command to move. The robots will move a unit
distance each second.

You are given a string `s` denoting the direction in which robots will
move on command. `'L'` means the robot will move towards the left side
or negative side of the number line, whereas `'R'` means the robot will
move towards the right side or positive side of the number line.

If two robots collide, they will start moving in opposite directions.

Return *the sum of distances between all the pairs of robots* `d`
*seconds after the command.* Since the sum can be very large, return it
modulo `10^9 + 7`.

**Note:** for two robots at the index `i` and `j`, pair `(i,j)` and pair
`(j,i)` are considered the same pair. When robots collide, they
**instantly change** their directions without wasting any time.
Collision happens when two robots share the same place in a moment; for
example, two robots at positions 0 and 2 moving towards each other
collide at position 1 after 1 second, and two at 0 and 1 moving towards
each other collide at the next second, after 0.5 seconds, at position
0.5.

```
nums = [-2, 0, 2], s = "RLL", d = 3  ->  8
nums = [1, 0],     s = "RL",  d = 2  ->  5
```

**Constraints:** `2 <= nums.length <= 10^5`, `-2 * 10^9 <= nums[i] <= 2 * 10^9`,
`0 <= d <= 10^9`, `nums.length == s.length`, `s` holds only `'L'` and
`'R'`, and `nums[i]` are unique.

## Approaches

Two robots that collide and turn back leave the same two places behind
as two that pass through each other, only with the names swapped, and
the sum of distances does not ask which robot is which. So every arm
moves each robot d its own way and never looks at a collision.

| file | mechanism |
|---|---|
| `robots.kara` ★ | the places after d seconds, sorted; the k-th place lies to the right of the k before it, so it adds k times itself less their sum, kept running. All mod `10^9 + 7`. O(n log n) |
| `robots_gaps.kara` | the sorted places' gaps instead: the gap after the k-th place lies between (k + 1)(n - k - 1) pairs. Each factor is taken mod `10^9 + 7` before the product, since a gap of `6 · 10^9` times `2.5 · 10^9` pairs overflows `i64`. O(n log n) |
| `robots_merge.kara` | the left-goers and the right-goers sorted apart, each side keeping its order since all of it moves together, then merged in order with a running sum, as in the ★ arm. O(n log n) |
| `robots_iter.kara` | the places built by `zip`, `map` and `collect`, sorted, and one `fold` over them with `enumerate` carrying the total and the running sum as a tuple. O(n log n) |
| `robots_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `const MOD` inside the method, `as_bytes()`, the places built by `enumerate` and `map` with `i32`-to-`i64` casts, sorted, and a prefix sum, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one robot;
two at the ends of the range moving apart for `10^9` seconds; 2000
random cases of 1 to 30 robots up to 10 apart for up to 50 seconds; 20
of 1000 robots up to `10^6` apart for up to `10^9` seconds, each batch
with the sum of its answers and a checksum; and `10^5` robots,
LeetCode's most, from `-2 · 10^9` up, for `10^9` seconds. `robots.py`
mirrors the ★ arm and its output is byte-identical.

```
8
5
0
999999965
2000 small cases: sums sum to 15946108, checksum 120858874
20 cases of 1000 robots: sums sum to 10868725804, checksum 318407865
794079067
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, with no passing through: the places doubled so that every
meeting falls on a whole number, every robot moved half a unit a tick
for 2d ticks, and both robots of any pair on one spot turned round. It
draws 1000 random cases of 1 to 10 robots up to 5 apart for 0 to 20
seconds, then 500 of up to 200 robots up to `10^7` apart for up to
`10^9` seconds, all before any arm answers; the literal reading is asked
only of the first 1000.

| | property |
|---|---|
| P1 | up to 10 robots, the answer is the literal reading's |
| P2 | the line mirrored, every place negated and every L made R and R L: the same answer |
| P3 | every robot shifted by the same amount, up to `5 · 10^8` either way: the same answer |
| P4 | the robots listed in reverse order: the same answer |
| P5 | the answer is between 0 and `10^9 + 6`; and with every robot facing right, it is the same after d seconds as after none |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1500 cases: checksum 130951130, 45000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same half-unit simulation gives the
same checksum. On a failure it prints the first ten and then the count
by property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2 and M8 change which way robots go and fail
only the literal reading and the vote, since mirroring and shifting a
wrong rule still agree with themselves.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the places never sorted | P1 837, P2 1397, P4 1397, P5 661, P6 1328 |
| M2 | ★: a left-goer moved right | P1 767, P6 1259 |
| M3 | gaps: a gap counted (k + 1)(n - k) times | P1 908, P2 1258, P6 1402 |
| M4 | gaps: the first gap left out | P1 900, P2 1153, P6 1394 |
| M5 | merge: the larger head taken first | P1 805, P2 43, P5 1197, P6 1297 |
| M6 | merge: the places seen never counted | P1 898, P2 1391, P3 1402, P5 1356, P6 1392 |
| M7 | iter: the running sum never grows | P1 908, P2 1391, P3 1402, P5 1388, P6 1402 |
| M8 | iter: the right-goers moved left | P1 712, P6 1204 |
| M9 | solution: the prefix keeps only the last place | P1 822, P2 1302, P3 1314, P5 1290, P6 1314 |
| M10 | solution: a left-goer one short | P1 799, P6 1291 |

## Benchmarks

The bench draws 10 cases of `10^5` robots, LeetCode's most, up to 40000
apart from `-2 · 10^9` and shuffled, each facing either way, for up to
`10^9` seconds, all of them first, then answers each 10 times by the ★
arm in all five languages: the places built, sorted and summed. C sorts
with `qsort` and a comparison function, Go with `slices.Sort`, and Rust
and Kāra with their own `sort`. Every implementation prints `10 cases of
100000 robots, 10 rounds: sums mod p sum to 49466077990, checksum
619278280`.

BENCHTAB

## Verification

All five arms print the same output as `robots.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 15 edits, the wrapper
included: `struct Solution {}` added, `Vec<i32>` and `Vec<i64>` became
`Vec[i32]` and `Vec[i64]`, `s.as_bytes()` became `s.bytes()`, the `&x`
patterns in the closure and the `for` became `x`, `i as i64 * x` dropped
its cast, and in the wrapper `Solution::` became `Solution.`, with the
`.clone()` and the `as i64` dropped. The `const MOD` stays inside the
method, where Kāra accepts it, unlike the nested `fn` items of 2719,
which the fix hoists.
