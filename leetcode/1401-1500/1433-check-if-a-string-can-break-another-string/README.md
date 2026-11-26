# 1433. Check If a String Can Break Another String

Given two strings `s1` and `s2` with the same size, check if some
permutation of string `s1` can break some permutation of string `s2` or
vice-versa. In other words `s2` can break `s1` or vice-versa. A string
`x` can break string `y` (both of size `n`) if `x[i] >= y[i]` (in
alphabetical order) for all `i` between `0` and `n - 1`.

```
s1 = "abc", s2 = "xya"                 ->  true     "ayx" breaks "abc"
s1 = "abe", s2 = "acd"                 ->  false
s1 = "leetcodee", s2 = "interview"     ->  true
```

**Constraints:** `s1.length == n`, `s2.length == n`, `1 <= n <= 10^5`,
all strings consist of lowercase English letters.

Each arm is `fn check_if_can_break(s1: String, s2: String) -> bool`.

## Approaches

| file | mechanism |
|---|---|
| `check_if_can_break.kara` ★ | both strings' bytes sorted, and one at least the other at every place, by `zip` and `all` each way round: if any order of one breaks the other, its letters sorted break the other's sorted. O(n log n) |
| `check_if_can_break_counts.kara` | the letters counted, and one string breaks the other when for every letter it has at most as many letters up to that one, so its k-th smallest is never below the other's. O(n) |
| `check_if_can_break_heap.kara` | each string's letters in a `PriorityQueue`, smallest first, the two taken from in step through `while let (Some(x), Some(y))`. O(n log n) |
| `check_if_can_break_chars.kara` | the letters as a `Vec[char]` through `chars().collect()`, sorted, each way round tried by a function over two `Slice[char]`s. O(n log n) |
| `check_if_can_break_solution.kara` | a Rust solution as LeetCode's Rust users write it (`s1.into_bytes()` into a `Vec<u8>`, `sort_unstable()`, the two ways round by `zip` and `all`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's three examples and five
more (`true false true true true false true false`); the constraints'
most, 10^5 a's against 10^5 z's, two drawn strings, and a drawn string
against itself with each letter nudged up by 0 or 1 (`10^5 letters: true
false true`); and 2000 random pairs of 1 to 60 letters, of the first 1
to 26 of the alphabet, the second drawn alone half the time and the
first nudged up otherwise (`2000 random pairs: 1404 can break, checksum
558863968`). `check_if_can_break.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★ and counts arms check clean as first written. The
harness first passed `one.clone()` to an arm, which checks with a
warning that the parameter only borrows it, and `karac fix` drops the
clone, 1 fix. The heap arm asked for `PriorityQueue.min_first()`, which
`karac check` refuses, saying a queue that pops the smallest first is
`PriorityQueue.new()`, and `karac fix` writes it, 2 fixes. The chars arm
called `sort_unstable()`, which is refused, the library having only the
stable `sort`, and `karac fix` writes `sort()`, 2 fixes. The Rust
solution takes one round of 15 fixes by `karac fix`'s count: `struct
Solution;` to `struct Solution {}`, `Vec<..>` to `Vec[..]`,
`s1.into_bytes()` to `s1.bytes().to_vec()`, `sort_unstable()` to
`sort()`, `||` to `or`, and `Solution::` to `Solution.`. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every order of `s1` against every order of `s2`, either way
round, while there are at most 5 letters. LeetCode's examples, six edge
cases (one letter alike, one letter apart, two letters swapped, each
string ahead at one place, `ac` against `bb`, and one string all below
the other), the constraints' most three ways (10^5 a's against 10^5 z's,
two drawn strings, and a drawn string against itself nudged up), and
1991 random pairs, 1 to 5 letters a third of the time and up to 60
otherwise, drawn as the harness draws them. Each case also draws the
letters P5 adds and the turn P3 makes.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 5 letters |
| P2 | either way round the same answer |
| P3 | a string breaks itself turned round |
| P4 | the letters mirrored through the alphabet, a to z and z to a, give the same answer |
| P5 | the same letters added to both give the same answer |
| P6 | the ★ arm's answer |

All 53,975 checks pass on every arm: `2003 cases: checksum 501398912,
53975 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by `sorted`,
gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: one way round asked for more at every place, not at least as much | P1 46, P2 1085, P4 1085, P5 71, P6 584 |
| M2 | ★: the second string left unsorted | P1 307, P2 39, P3 1656, P4 205, P5 329, P6 4252 |
| M3 | counts: one way round asked for fewer up to every letter, not at most as many | P1 122, P2 1326, P4 1326, P6 224 |
| M4 | counts: each letter of the second string counted twice | P1 356, P2 1039, P4 932, P5 319, P6 971 |
| M5 | heap: the second string's letters taken largest first | P1 418, P3 1761, P5 260, P6 1175 |
| M6 | heap: one way round allowed a letter one below | P1 26, P2 242, P4 242, P5 16, P6 203 |
| M7 | chars: a letter equal to the other's not allowed | P1 431, P3 2003, P5 216, P6 1228 |
| M8 | chars: only the one way round tried | P1 431, P2 1326, P4 1326, P6 1102 |
| M9 | solution: the other way round asked for more at every place | P1 272, P2 1085, P4 1085, P5 145, P6 939 |
| M10 | solution: the first string left unsorted | P1 302, P2 39, P3 1639, P4 206, P5 331, P6 1056 |

## Benchmarks

The bench draws a pool of 10^6 letters, of the first 25 of the alphabet,
and the same pool with each letter nudged up by 0 or 1, and runs the ★
arm, taking its strings as `Str` windows, on 400 pairs of windows of
10^5 letters: half the time the pool's against the nudged pool's at the
same start, and the pool's at two drawn starts otherwise. Each
implementation copies each window's letters into a fresh array and sorts
it with its own library's sort; C's is `qsort`, through a comparison
function on every pair, which is most of C's time. Every implementation
prints `400 pairs of 10^5 letters: 207 can break`.

BENCHTAB

Measured by hand, Kāra takes 0.42 to 0.47 s against Rust's 0.30 s (0.30
s with overflow checks on), C's 10.3 to 10.4 s and Go's 2.0 s; Python
takes 9.2 s.
