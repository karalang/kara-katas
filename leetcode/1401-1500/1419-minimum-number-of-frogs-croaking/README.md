# 1419. Minimum Number of Frogs Croaking

You are given the string `croakOfFrogs`, which represents a combination
of the string `"croak"` from different frogs, that is, multiple frogs
can croak at the same time, so multiple `"croak"` are mixed. Return the
minimum number of different frogs to finish all the croaks in the given
string. A valid `"croak"` means a frog is printing five letters `'c'`,
`'r'`, `'o'`, `'a'`, and `'k'` sequentially. The frogs have to print all
five letters to finish a croak. If the given string is not a combination
of a valid `"croak"` return `-1`.

```
croakOfFrogs = "croakcroak"    ->  1     one frog croaking twice
croakOfFrogs = "crcoakroak"    ->  2     the second frog starts before the first is done
croakOfFrogs = "croakcrook"    ->  -1    the last croak has an `o` for its `a`
```

**Constraints:** `1 <= croakOfFrogs.length <= 10^5`, `croakOfFrogs` is
either `'c'`, `'r'`, `'o'`, `'a'`, or `'k'`.

Each arm is `fn min_number_of_frogs(croak_of_frogs: String) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `min_number_of_frogs.kara` ★ | how many times each letter has been heard, the letter's place in `croak` by a `match`: no letter more often than the one before it, the frogs croaking at once those that said `c` and not yet `k`, and every croak finished at the end. O(n) |
| `min_number_of_frogs_stages.kara` | how many frogs wait at each letter of `croak`, the letter's place by `position` in a `let ... else`: a letter moves one frog on from the letter before, and a `c` takes a frog that has finished when there is one and a new frog otherwise. O(n) |
| `min_number_of_frogs_frogs.kara` | every frog a `struct` value of its own, moved between five stacks, one for the letter it last said: each letter pops a frog from the stack of the one before and pushes it onto its own, a `c` reusing a frog that has finished. O(n) |
| `min_number_of_frogs_prefix.kara` | the counts of each letter in every prefix, kept whole: a valid string has, in every prefix, no letter more often than the one before it and the same count of each in the whole, and the frogs needed are the most `c`s not yet matched by a `k` in any prefix. O(n) time and space |
| `min_number_of_frogs_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let mut cnt = [0; 5]`, a `match` on `chars()`, the frogs counted up on `c` and down on `k`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and five
more (`1 2 -1 -1 1 -1 2 2`); the constraints' most, 2 * 10^4 croaks all
at once, one after another, and heard together, a new frog starting one
time in 2 (`10^5 letters: 20000 1 18312`); and 2000 random cases of 1 to
40 croaks heard together, a third of them spoiled by a letter changed,
dropped or swapped with the next (`2000 random cases: 398 invalid,
checksum 955601120`). `min_number_of_frogs.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the stages arm checks clean as first written. In the ★
arm `let mut heard = [0, 0, 0, 0, 0]` and `let mut most = 0` keep the
default `i64` beside the `i32` return, and `karac fix` writes `[0i32, 0,
0, 0, 0]` and `most: i32`; the harness's
`.collect::<Vec<String>>().join("")` is Rust's turbofish, which `karac
fix` writes as `Vec[String].from_iter(..).join("")`, 4 fixes in all. The
frogs arm looked a letter up with `word.find(c)` on a `char`, and `karac
fix` writes `c.to_string()`; the prefix arm bound `s.bytes()`, a
`Slice[u8]`, to a `Vec[u8]`, and `karac fix` adds `.to_vec()`, 1 fix
each. The Rust solution takes one round of 8 fixes by `karac fix`'s
count: `struct Solution;` to `struct Solution {}`, `frogs` and
`max_frogs` declared `: i32`, and `Solution::` to `Solution.`; its `[0;
5]` is taken as written. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the letters shared out among f frogs, tried 1 frog, then 2,
and on, each letter given in turn to any frog whose next letter it is,
every way, a frog not yet heard tried only as the first of them, and f
is enough when some way leaves every frog having said whole croaks,
while the string is at most 20 letters. LeetCode's examples, nine edge
cases (one letter, a lone `k`, one croak, a croak turned round, a croak
missing a letter, croaks overlapping two ways, a `k` too many, a `c` too
many), the constraints' most four ways (all at once, one after another,
heard together with a new frog one time in 2, and one time in 5 and then
spoiled), and 1987 random cases, 1 to 4 croaks half the time and up to
40 otherwise, a new frog starting one time in 1 to 6, a third of them
spoiled. Each case also draws a partner of 1 to 3 croaks for P3 and a
place for P4.

| | property |
|---|---|
| P1 | the statement read literally, while the string is at most 20 letters |
| P2 | no answer, or 1 frog to a fifth of the letters, and no answer when the letters are not a whole number of croaks |
| P3 | two valid strings, one after the other, need the frogs the busier of them needs |
| P4 | a whole croak put between two letters of a valid string needs the same frogs or one more |
| P5 | every letter said twice over needs twice the frogs, and has no answer when the string has none |
| P6 | the ★ arm's answer |

All 50,725 checks pass on every arm: `2003 cases: checksum 914249144,
50725 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. The differential checks
clean as first written. Python, by counting the frogs that wait at each
letter, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the r never checked against the c | P1 16, P6 84 |
| M2 | ★: a frog still croaking at the end allowed | P1 32, P2 47, P3 22, P6 192 |
| M3 | stages: a frog that has finished taken up again only once two have | P1 199, P3 416, P5 703, P6 703 |
| M4 | stages: a frog left waiting after its a not counted against the string | P1 26, P2 41, P3 17, P6 41 |
| M5 | frogs: each letter takes a frog from its own stack, not the one before | P1 816, P6 1516 |
| M6 | frogs: a frog left after its c not counted against the string | P1 2, P2 2, P3 1, P6 2 |
| M7 | prefix: the r never checked against the c | P1 16, P6 21 |
| M8 | prefix: the frogs at once counted to the a, not the k | P1 66, P3 20, P6 491 |
| M9 | solution: the last count of frogs at once kept, not the most | P1 44, P3 971, P4 253, P6 227 |
| M10 | solution: a letter allowed once more than the letter before it | P1 166, P2 146, P5 265, P6 266 |

## Benchmarks

The bench builds a pool of 1000 blocks, each 100 croaks heard together
with a new frog starting one time in 3, and runs the ★ arm, taking its
window as a `Str`, on 500 windows of 200 blocks, 10^5 letters, each
window's first block drawn, so every window is a valid string read to
its end. Every implementation prints `500 windows of 10^5 letters:
checksum 473672458`.

BENCHTAB

Measured by hand, Kāra takes 0.59 s against Rust's 0.50 s (0.51 s with
overflow checks on), C's 0.52 s and Go's 0.52 s; Python takes 8.2 s.
