# 1047. Remove All Adjacent Duplicates In String

You are given a string `s` consisting of lowercase English letters. A
**duplicate removal** consists of choosing two **adjacent** and **equal**
letters and removing them.

We repeatedly make duplicate removals on `s` until we no longer can.

Return the final string after all such duplicate removals have been made.
It can be proven that the answer is **unique**.

```
s = "abbaca"   ->  "ca"   (bb goes, then aa, leaving "ca")
s = "azxxzy"   ->  "ay"
```

**Constraints:** `1 <= s.length <= 10^5`; `s` consists of lowercase
English letters.

## Approaches

A letter equal to the last one kept cancels it: once everything between
two letters has gone, they are adjacent. Every arm but one keeps the
letters that survive so far as a stack.

| file | mechanism |
|---|---|
| `remove_dups.kara` ★ | a `Vec[char]` stack: pop when the letter equals the top, push otherwise, then `collect` the stack into a `String`. O(n) |
| `remove_dups_string.kara` | the answer itself as the stack: `ends_with` the letter, then `pop` or `push`. O(n) |
| `remove_dups_inplace.kara` | the bytes rewritten in place with two indices, `b[..top]` the answer so far, then `truncate`. O(n), no second buffer |
| `remove_dups_scan.kara` | the statement as it reads: find a pair, `remove` both letters, look again one place back. O(n^2) at worst |
| `remove_dups_fold.kara` | the stack as the accumulator of `chars().fold(..)`, its last letter read with `chars().next_back()`. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: the answers for ten strings,
LeetCode's two examples among them, with `"aa"` (nothing left), `"aaa"`,
`"abccba"` (a cascade to nothing) and `"abcd"` (nothing to remove); for
every string of 1 to 8 letters from a, b, c, the number of cases, the
total length of the answers, how many are empty and a checksum; the same
for 1000 random strings of 1 to 200 letters from a, b, c, and 1000 from
a to z; and three of the largest, `ab` repeated 5000 times (nothing to
remove), 10001 a's (one left) and 5000 letters followed by their reverse
(nothing left). `remove_dups.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: look at every pair of neighbours, take the last equal pair
out, and start again on what is left, until no pair is found. It checks
4779 strings: every string of 1 to 7 letters from a, b, c (3279), 1000
random strings of 1 to 60 letters from a, b, c, where pairs are common,
and 500 from a to z.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer has no two equal letters side by side, and each letter occurs in it as often as in the input, less an even number |
| P3 | the answer is the input with letters taken out (a subsequence of it) |
| P4 | the input followed by its reverse leaves nothing |
| P5 | the answer for a string is the answer for its two halves' answers put together, and the answer for an answer is itself |
| P6 | each arm agrees with at least two of the other four |

P2 holds because a removal takes two of one letter. P4 holds because the
string's own answer, followed by its reverse, cancels from the middle
out. P5 holds because the answer is unique: removing the pairs inside each
half first is one order of removals among the others.

The differential prints `4779 strings: checksum 335843288, 143370 checks
over 5 arms: 0 failures` under `karac __mir-run` (6 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to
each arm. All fifteen are killed, each fails the same way under both
backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the pair not popped, only the second letter dropped | P1 3634, P2 3353, P4 4779, P6 3634 |
| M2 | ★: the stack read top to bottom | P1 3239, P3 2626, P5 3943, P6 3239 |
| M3 | ★: the first letter skipped | P1 4779, P2 4779, P4 4779, P5 4493, P6 4779 |
| M4 | string: two letters popped | P1 3430, P2 3215, P4 4170, P5 1037, P6 3430 |
| M5 | string: `contains` for `ends_with`, so any earlier equal letter cancels | P1 3485, P2 3082, P4 2992, P5 995, P6 3485 |
| M6 | string: an equal letter pushed again, not popped | P1 4149, P2 4149, P4 4779, P6 4149 |
| M7 | inplace: the letter never written down | P1 3420, P2 3333, P5 2780, P6 3420 |
| M8 | inplace: compared with its neighbour in the input, not the top | P1 2068, P2 2044, P4 4416, P5 1604, P6 2068 |
| M9 | inplace: the bottom letter never cancelled | P1 1318, P2 1318, P4 4779, P6 1318 |
| M10 | scan: no look back after a removal | P1 1297, P2 1297, P4 4580, P5 1297, P6 1297 |
| M11 | scan: the last pair never looked at | P1 1315, P2 1315, P4 4779, P6 1315 |
| M12 | scan: steps two places | P1 2201, P2 2201, P4 2526, P5 1240, P6 2201 |
| M13 | fold: compared with the first letter, `next` for `next_back` | P1 4088, P2 3932, P4 4448, P5 1545, P6 4088 |
| M14 | fold: started with an x | P1 4779, P2 4779, P3 4754, P4 4779, P5 4779, P6 4779 |
| M15 | fold: the test turned round | P1 4655, P2 4428, P6 4655 |

P1 and P6 kill all fifteen, P2 fourteen, P4 twelve, P5 ten and P3 two.
P2 misses only M2, whose answer is the right one reversed: no pair, and
the same letters. P3 sees only an answer with letters out of order (M2)
or one the input never had (M14); every other edit keeps letters of the
input in their order, and so leaves a subsequence. P4 misses M2, since
the reverse of nothing is nothing; M7, whose `top` still comes to 0 on
every string followed by its reverse checked here, so it returns nothing
as it should; and M15, which pops an empty accumulator and pushes
nothing, so it returns nothing whatever the input. P5 misses five edits
whose wrong answer for a string is also their answer for its halves'
answers put together: M1, M6, M9, M11 and M15.

Fifteen other edits were set aside. One is equivalent: the scan arm
starting again from the front after a removal, not one place back, is
slower and right. Seven fail exactly as a kept one does: the ★ arm
compared with the bottom and the string arm with the first letter (as
M13), the string and fold arms reading the letters back to front (as
M2), the in-place arm skipping the first letter (as M3), and the scan
arm removing one letter of the pair and the fold arm never popping (as
M1). Seven fail in ways of their own: two pairs fail alike, the ★ arm
clearing the stack and the in-place arm resetting `top` to 0, and the ★
and fold arms pushing each letter twice; and three alone, the string arm
started with an a, the in-place arm never truncated, and the scan arm
leaving out the first letter.

## Verification

Every arm prints the same output as `remove_dups.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara `75832f76f1`.
Under `karac __mir-run` the arms take 0.7 s (in place) to 1.4 s (fold).

The arms went through the Mend loop. Written the way Rust writes them,
four needed it:

- `stack.last() == Some(c)` compares a view with a value; `karac fix`
  writes `stack.last().cloned()`.
- `out.ends_with(c)` passes a `char` where Kāra takes a `Str`; `karac
  fix` writes `c.to_string()`, a one-letter string each turn.
- `top > 0 && ..` is fixed to `and`.
- `fold(String.new(), |mut acc, c| ..)` is refused with "'mut' is a
  reserved keyword and cannot be used as an identifier" and a second
  error at the closing `)`, with no fix. A function parameter written
  `mut x` gets a diagnostic naming the Kāra spelling, `let mut x = x;` in
  the body, which the fold arm uses. Filed as B-2026-11-04-76.

The scan arm takes the pair out with two calls to `remove`. Rust writes
it `v.drain(i..i + 2);`, and Kāra's `Vec` has no `drain`: the check says
only "no method 'drain' on type 'Vec'". Filed as B-2026-11-04-77.

## Benchmarks

The bench builds 100 strings of 200000 letters from a, b, c, d once in
all five languages, then runs the ★ arm on every string ten times,
adding up the answers' lengths and folding each length and last letter
into a checksum. Every implementation prints `100 strings of 200000
letters, 10 rounds: total length 99969840, checksum 368192608`. With four
letters a quarter of the neighbours are equal, and about half the letters
survive.

Each implementation keeps a stack of 32-bit letters and turns it into a
string at the end: Kāra's `Vec[char]` and `collect`, Rust's `Vec<char>`
and `collect`, Go's `[]rune` and `string(..)`, a list and `"".join` in
Python. C's stack is an array of `uint32_t` that doubles when full, with
the answer copied out a byte a letter.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `75832f76f1` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.699 to 0.783 s | 0.738 s |
| Rust (`rustc -O`) | 0.890 to 1.011 s | 0.932 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.856 to 1.028 s | 0.953 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.016 to 1.172 s | 1.106 s |
| Kāra (`karac build`) | 1.050 to 1.236 s | 1.139 s |
| Go | 1.744 to 2.042 s | 1.862 s |
| Python | 11.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.11 s) matches its real time.

Kāra took 1.16 times Rust's median time under overflow checks, and 1.50
times C's.
