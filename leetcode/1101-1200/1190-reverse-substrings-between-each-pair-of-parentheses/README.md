# 1190. Reverse Substrings Between Each Pair of Parentheses

You are given a string `s` that consists of lowercase English letters and
brackets. Reverse the strings in each pair of matching parentheses,
starting from the innermost one. Your result should not contain any
brackets.

```
s = "(abcd)"          ->  "dcba"
s = "(u(love)i)"      ->  "iloveu"
s = "(ed(et(oc))el)"  ->  "leetcode"
```

**Constraints:** `1 <= s.length <= 2000`; `s` only contains lowercase
English characters and parentheses; all parentheses are balanced.

The arms are `fn reverse_parentheses(s: String) -> String`. The two Rust
arms keep the method LeetCode gives Rust users, inside `impl Solution`, and
a one-line `reverse_parentheses` calls it.

## Approaches

A letter inside `k` pairs is reversed `k` times, so it ends up read in the
direction `k` turns leave. Reversing each group as its `)` arrives costs
the group's length once per pair around it, O(n · depth); pairing the
brackets first and walking once, turning at each bracket, costs O(n).

| file | mechanism |
|---|---|
| `reverse_parentheses.kara` ★ | each bracket paired with its match by a stack of open positions, then one walk over the bytes that, at a bracket, jumps to its match and turns around. O(n) |
| `reverse_parentheses_strings.kara` | a stack of the strings each `(` interrupted: a `)` reverses the current string and appends it to the one set aside. O(n · depth) |
| `reverse_parentheses_chars.kara` | one stack of characters: at a `)`, the characters back to its `(` popped, which reverses them, and pushed back in the order they came off. O(n · depth) |
| `reverse_parentheses_recursive.kara` | recursive descent: a group reads letters up to its `)`, each inner group read by a recursive call and appended reversed. O(n · depth) |
| `reverse_parentheses_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `Vec<Vec<char>>` stack, `stack.last_mut().unwrap().extend(top)` after `top.reverse()`, and `into_iter().collect()`), carried to Kāra by `karac fix` |
| `reverse_parentheses_jump.kara` | another Rust solution, the ★ arm's walk over `s.as_bytes()` (`for (i, &c) in s.iter().enumerate()`, `let (mut i, mut d) = (0i32, 1i32)`, `while (i as usize) < n`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's three examples; one letter
(`"a" -> "a"`); an empty pair (`"()" -> ""`); a pair inside a pair (`"((ab))"
-> "ab"`); one long group around a short one (`"a(bcdefghijkl(mno)p)q" ->
"apmnolkjihgfedcbq"`); empty pairs beside deep ones (`"ta()usw((((a))))" ->
"tauswa"`); three pairs side by side (`"(a)(b)(c)" -> "abc"`); 2000 random
strings of up to 40 characters (`2000 random strings: 24623 letters,
checksum 33249746`); and the constraints' longest, 2000 characters, as 500
pairs nested (`500 nested pairs: 1000 letters, digest 191919548`) and at
random (`2000 random characters: 1009 letters, digest 256864982`).
`reverse_parentheses.py` mirrors the ★ arm and its output is
byte-identical; it also checks every answer against the statement read
literally. Every arm gives the same output under `karac run` and `karac
build`, and under the AddressSanitizer build.

The Mend loop: the ★ and recursive arms were first written to copy the
bytes, `let bytes: Vec[u8] = s.bytes().collect();`, which `karac check`
refuses ("no method 'collect' on type 'Slice'") with a fix to
`s.bytes().iter().collect()`; both arms now read the view `s.bytes()`
itself, with no copy. The strings and chars arms check clean as written,
and the harness took one fix, an unneeded `as i64` on a byte. The solution
arm takes one round of 10 fixes (among them `struct Solution;` to `struct
Solution {}`, `Vec<Vec<char>>` to `Vec[Vec[char]]`, `vec![vec![]]` to
`[Vec.new()]`, and both `stack.last_mut().unwrap()` to
`stack[stack.len() - 1]`) and its output matches, after the fix below. The jump arm takes one
round of 15 (among them `s.as_bytes()` to `s.bytes()`, `vec![0; n]` to
`Vec.filled(n, 0)`, the `&` of `for (i, &c)`, `let (mut i, mut d)` to `let
mut (i, d)`, the `as usize` of each index, and `||` to `or`) and its output
matches. The differential took two, `"".to_string()` to `""` and `ref
got[i]` for an element only read.

## Gaps

The solution arm found one, fixed in kara.

- **A call through `last_mut().unwrap()` gave no fix.**
  `stack.last_mut().unwrap().extend(top)` and `_ =>
  stack.last_mut().unwrap().push(c)` were refused, "no method 'last_mut'
  on type 'Vec': write through an index instead", with no fix, where
  `*v.last_mut().unwrap() = x` and the `let`, `match` and `if let` shapes
  are rewritten. A call, a field or an element read or written through
  `v.last_mut().unwrap()` (or `first_mut`, or `.expect(..)`) now takes the
  index `v[v.len() - 1]` (or `v[0]`), unless the call's arguments or the
  index name `v`. kara B-2026-11-18-30.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the pair the first `)` closes, which holds no other, reversed
and its brackets dropped, until no pair is left. 2000 random strings of 1
to 30 characters drawn as the harness draws them; the first 200 from the
letters `a` and `b`, the rest from `a` to `f`.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the same letters as the input, every one |
| P3 | the whole string in a pair reverses the answer |
| P4 | two pairs around the whole string change nothing |
| P5 | two strings side by side answer side by side (each string with the one before it) |
| P6 | the mirror image (read right to left, each bracket turned around) answers in reverse |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 strings: checksum 858776275,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: no turn at a bracket | P1 1594, P2 1594, P3 1777, P4 1777, P7 7970 |
| S2 | ★: a bracket written out as it is passed | P1 1807, P3 2000, P4 2000, P7 9035 |
| T1 | strings: a group appended unreversed | P1 1172, P3 1825, P7 1172 |
| T2 | strings: a group put before the text it interrupted | P1 1481, P5 1565, P6 1524, P7 1481 |
| C1 | chars: a run pushed back in its first order | P1 1172, P3 1825, P7 1172 |
| C2 | chars: a run popped past its own `(` | P1 1541, P5 1589, P6 1588, P7 1541 |
| R1 | recursive: a group appended unreversed | P1 1172, P3 1825, P7 1172 |
| R2 | recursive: a `)` read as a letter | P1 1807, P3 2000, P4 2000, P5 1721, P6 1741, P7 1807 |
| X1 | solution: a group not reversed | P1 1172, P3 1825, P7 1172 |
| X2 | solution: a group appended to the outermost | P1 804, P3 1434, P4 1664, P6 865, P7 804 |
| J1 | jump: no turn at a bracket | P1 1594, P2 1594, P3 1777, P4 1777, P7 1594 |
| J2 | jump: letters walked right to left dropped | P1 1519, P2 1519, P3 1963, P7 1519 |

A mutation of the ★ arm fails P7 on every arm. T1, C1, R1 and X1 are one
fault in four arms, a group left unreversed, and fail alike, P3 most: a
pair around the whole string reverses the answer only when every group is
reversed. S1 and J1 are one fault too, a jump without a turn, which skips
the group and so fails P2, the letters kept. P5 and P6 catch the faults
that move a group past the text beside it (T2, C2, R2, X2), which a single
string's own answer can hide.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 200 strings of about 2000 characters, the constraints' most, built
once (in turn, random letters and pairs as the harness draws them, and 500
pairs nested with a random letter before each `(` and after each `)`);
then 200 rounds over the strings, each answer's digest folded into a
checksum. Every program prints `200 rounds of 200 strings of about 2000
characters: checksum 326922208`. Each call allocates the pairing (one index
per byte), a stack of open positions and the answer, and walks the string
twice; the digest walks the answer once more.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`,
on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.612 to 0.783 s | 0.729 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.573 to 0.769 s | 0.713 s |
| Rust (`rustc -O`) | 0.653 to 0.822 s | 0.731 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.674 to 0.827 s | 0.755 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.636 to 0.798 s | 0.752 s |
| C (`clang -O3`) | 0.518 to 0.663 s | 0.634 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.569 to 0.695 s | 0.627 s |
| Go | 0.927 to 1.057 s | 0.956 s |
| Python | 12.74 to 13.46 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 1% of wall time for both Kāra
rows, so both ran on one core. Kāra is within the spread of plain Rust
(0.713 s against 0.731 s) and about 6% ahead of Rust with overflow checks
on, its equal-safety twin; C is about 11% ahead of Kāra, and Kāra about
25% ahead of Go. The ranges overlap between Kāra, Rust and C, so only C's
lead and Go's gap stand out of the noise; no profile was taken. Python
takes about 18x Kāra's time.
