# 1639. Number of Ways to Form a Target String Given a Dictionary

You are given a list of strings of the **same length** `words` and a
string `target`.

Your task is to form `target` using the given `words` under the following
rules:

- `target` should be formed from left to right.
- To form the `i`th character (**0-indexed**) of `target`, you can choose
  the `k`th character of the `j`th string in `words` if
  `target[i] = words[j][k]`.
- Once you use the `k`th character of the `j`th string of `words`, you
  **can no longer** use the `x`th character of any string in `words`
  where `x <= k`. In other words, all characters to the left of or at
  index `k` become unusable for every string.
- Repeat the process until you form the string `target`.

**Notice** that you can use **multiple characters** from the **same
string** in `words` provided the conditions above are met.

Return *the number of ways to form `target` from `words`*. Since the
answer may be too large, return it **modulo** `10^9 + 7`.

```
words = ["acca","bbbb","caca"], target = "aba"   ->  6
words = ["abba","baab"], target = "bab"          ->  4
```

**Constraints:** `1 <= words.length <= 1000`;
`1 <= words[i].length <= 1000`; all strings in `words` have the same
length; `1 <= target.length <= 1000`; `words[i]` and `target` contain
only lowercase English letters.

## Approaches

| file | mechanism |
|---|---|
| `ways.kara` ★ | only how many words hold each letter in each column matters: walk the columns with `ways[i]`, the ways to have formed the first i target letters so far, and let each column add letter i + 1 to them once per word that has it there, updating i from the top down so one array serves. O(Lw + Lt) for w words of length L and a target of t letters |
| `ways_table.kara` | the letter counts of every column in a `Vec[Array[i64, 26]]`, then the full table `formed[i][k]` over target prefixes and columns, each column either skipped or supplying the next letter. O(Lw + Lt) time and O(Lt) space |
| `ways_memo.kara` | recursion on (letter, column) with a `Map[(i64, i64), i64]` memo: a column is skipped or supplies the letter, and a target that cannot fit in the columns left gives 0 at once. O(Lw + Lt) |
| `ways_solution.kara` | LeetCode's Rust template: the counts in `vec![[0i64; 26]; m]`, then one array of ways updated from the top down. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples, a target
longer than the words (0), a target letter no word has (0), and one word
that is the target (1); then the ways summed and a checksum for 3000
random dictionaries of up to 4 words of up to 5 letters from a and b,
100 of up to 50 words of up to 60 letters from a to c, and 3 of up to
1000 words of up to 1000 letters from the whole alphabet. `ways.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: build the target letter by letter, each from some word's
letter at a column right of the last one used, and count every way of
choosing the columns and the words, one recursive walk over all of them.
It checks 3000 random dictionaries of 1 to 3 words of 1 to 5 letters,
with targets of 1 to 4 letters, every other one from the letters a and
b, the rest a to c. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the ways are the statement read literally |
| P2 | the words in reverse order give the same ways |
| P3 | the letters renamed alike, a to b, b to c, c to a, give the same ways |
| P4 | every word listed twice multiplies the ways by 2 for each target letter |
| P5 | a target longer than the words has no way, and no target has more ways than C(L, t) choices of columns times n^t choices of words |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 146611501, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property. The ways of
cases this small never reach the modulus; the arms' reduction is
exercised by the arm files' last two batches, against `ways.py`.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first tries survived and are
equivalent, and were replaced: the table arm seeding the empty prefix in
every column but the last (that cell is read only for an empty target,
which never occurs), and the memo arm looking a state up as `(k, i)`
while storing it as `(i, k)` (a state always has k at least i, so the
swapped key is another state's only when i equals k, where it is the
same key).

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the prefixes updated from the bottom up, so one column can supply two letters | P1 846, P5 64, P6 846 |
| M2 | ★: a column supplies a letter once, however many words have it | P1 755, P4 1420, P6 755 |
| M3 | ★: the empty prefix counted twice | P1 1420, P5 238, P6 1420 |
| M4 | table: a letter taken from the same column as the one before | P1 1363, P5 510, P6 1363 |
| M5 | table: the empty prefix seeded in the first column only | P1 953, P6 953 |
| M6 | memo: a skipped column skips the letter too | P1 1907, P4 2139, P5 209, P6 1907 |
| M7 | memo: gives up one column early | P1 1094, P6 1094 |
| M8 | memo: each answer stored under the next column | P1 528, P5 6, P6 528 |
| M9 | template: the last target letter never formed | P1 1420, P6 1420 |
| M10 | template: the empty prefix never counted | P1 1420, P6 1420 |

## Benchmarks

The bench draws 40 random dictionaries of 1000 words of 1000 letters,
LeetCode's largest, with targets of 500 letters, all over the letters a
to e and all of them first, then counts each one's ways by the ★ arm in
all five languages: the column counts in a 26-slot array, then the ways
array. Every implementation prints `40 dictionaries of 1000 words:
checksum 946308031`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.171 s |
| Rust (`rustc -O`) | 0.190 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.191 s |
| Kāra (`karac build`) | 0.196 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.199 s |
| Go | 0.484 s |
| Python | 12 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.171 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.181 s and
0.197 s on one run).

## Verification

All four arms print the same output as `ways.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The ★ arm first indexed its counts with `(goal[i] - b'a') as i64`, as
Rust's `as usize` would be, and the `lossless_cast` lint called the cast
unnecessary: a `u8` widens to an `i64` index by itself. `karac fix`
dropped both. The table and memo arms then checked clean as first
written, the memo's `Map` keyed by a tuple and its `if let Some(known) =
memo.get((i, k))` included.

LeetCode's Rust template takes one `karac fix` of 13 edits, among them
`vec![[0i64; 26]; m]` to `Vec.filled(m, [0; 26])`, `for w in &words` to
`for w in ref words`, `w.bytes().enumerate()` to
`w.bytes().iter().enumerate()` (a string's `bytes()` is a `Slice[u8]`),
`target.as_bytes()` to `target.bytes()`, and the harness wrapper's
`as i64` dropped as lossless. Its `(c - b'a') as usize` indices are left
as they are: Kāra has `usize`, and an index of that type checks. The arm
then checks and agrees with no hand edit.
