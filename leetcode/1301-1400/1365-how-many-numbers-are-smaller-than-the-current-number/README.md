# 1365. How Many Numbers Are Smaller Than the Current Number

Given the array `nums`, for each `nums[i]` find out how many numbers in
the array are smaller than it. That is, for each `nums[i]` you have to
count the number of valid `j`'s such that `j != i` and `nums[j] <
nums[i]`.

Return the answer in an array.

```
nums = [8,1,2,2,3]  ->  [4,0,1,1,3]
nums = [6,5,4,8]    ->  [2,1,0,3]
nums = [7,7,7,7]    ->  [0,0,0,0]
```

**Constraints:** `2 <= nums.length <= 500`, `0 <= nums[i] <= 100`.

Each arm is `fn smaller_numbers_than_current(nums: Vec[i32]) ->
Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `smaller_numbers_than_current.kara` ★ | the values counted, 0 to 100, and the counts summed so that below[v] holds how many values are less than v; each answer is then a lookup. O(n + V) for V = 101 values |
| `smaller_numbers_than_current_brute.kara` | for each value, every value of the array compared with it and the smaller ones counted. O(n²) |
| `smaller_numbers_than_current_search.kara` | a sorted copy, and each value's answer the place where it first appears there, found by binary search. O(n log n) |
| `smaller_numbers_than_current_rank.kara` | the places sorted by their values, then walked in order, each run of equal values given the place where the run starts. O(n log n) |
| `smaller_numbers_than_current_solution.kara` | a Rust solution as LeetCode's Rust users write it (`sorted.iter().position(\|y\| y == x).unwrap() as i32` for each value), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, one
value, and the range's two ends (`[4, 0, 1, 1, 3] [2, 1, 0, 3] [0, 0, 0,
0] [0] [2, 0, 2, 0]`); and 2000 random arrays of up to 500 values
folded into a checksum (`2000 random arrays: 81146435 smaller in all,
checksum 580187627`). `smaller_numbers_than_current.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the ★, brute, search and rank arms check clean. The Rust
solution takes 5 fixes: `struct Solution;` becomes `struct Solution
{}`, and `Vec<i32>` becomes `Vec[i32]` in the argument and the result.
`position(..).unwrap() as i32` stands as Rust wrote it. Every arm
matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: for each i, every j other than i with nums[j] < nums[i]
counted. It checks the examples, 1000 random arrays of up to 60 values
and 100 of up to 500, the values from a range of 3, 10 or all 101, so
that some repeat often.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | every value moved by the same amount, up to 100 or down to 0, the same answer |
| P3 | the array reversed, the answer reversed |
| P4 | the answers ordered as the values: smaller where smaller, equal where equal, and each below n |
| P5 | a value above every other put at the end leaves the answers as they were and gets n |
| P6 | the ★ arm's answer |

All 32,555 checks pass on every arm: `1105 cases: checksum 885165231,
32555 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, counting the smaller values of
each, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each value marked once, not counted | P1 1007, P5 914, P6 4028 |
| M2 | ★: the counts summed only up to 50 | P1 723, P2 556, P4 642, P5 619, P6 2892 |
| M3 | brute: equal values counted too | P1 1105, P4 1105, P5 986, P6 1105 |
| M4 | brute: the first value never counted | P1 914, P3 932, P4 276, P5 986, P6 914 |
| M5 | search: the copy never sorted | P1 1077, P3 1087, P4 858, P5 635, P6 1077 |
| M6 | search: the first place not less than x - 1 | P1 1035, P4 1035, P5 986, P6 1035 |
| M7 | rank: every place its own start | P1 1028, P3 1028, P4 1028, P6 1028 |
| M8 | rank: the places sorted largest first | P1 1099, P4 1099, P5 986, P6 1099 |
| M9 | solution: the copy never sorted | P1 1083, P3 1084, P4 1012, P6 1083 |
| M10 | solution: the last place of the value taken | P1 1028, P6 1028 |

P1 and P6 kill all ten, P4 eight, P5 six, P3 four and P2 one. Moving
every value by the same amount (P2) catches only the ★ arm summing up to
50 (M2), since a shift carries values across that line. Reversing the
array (P3) catches the edits that make the answer depend on where a
value sits: the brute arm skipping the first value (M4), a search or a
solution over an unsorted copy (M5, M9), and equal values given
different ranks (M7). The order check (P4) catches every edit that ranks
one value against another wrongly, but not marking each value once (M1)
or taking the value's last place (M10): both still give equal values
equal answers and larger values larger ones, only the wrong amounts. A
new largest value at the end (P5) must get n, which the edits that miss
or over-count a smaller value fail; the three that only reorder ties or
read an unsorted copy (M7, M9, M10) still give it n.

## Benchmarks

The bench builds 20 arrays of 500 values, the constraints' most, once;
then makes 2 * 10^5 rounds, each setting one value of one array, both
drawn from the checksum so far, so no answer carries over, and
answering with the ★ arm. Every implementation prints `200000 rounds
over 20 arrays of 500 values: checksum 342311229`. The work is counting
500 values, summing 101 counts and looking up 500 answers, the same in
every language.

BENCHTAB
