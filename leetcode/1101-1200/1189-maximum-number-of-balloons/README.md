# 1189. Maximum Number of Balloons

Given a string `text`, use its characters to form as many instances of the
word `"balloon"` as possible. Each character of `text` can be used at most
once. Return the maximum number of instances that can be formed.

```
text = "nlaebolko"         ->  1
text = "loonbalxballpoon"  ->  2
text = "leetcode"          ->  0
```

**Constraints:** `1 <= text.length <= 10^4`; `text` consists of lowercase
English letters only.

The arms are `fn max_number_of_balloons(text: String) -> i64`. The two Rust
arms keep the method LeetCode gives Rust users, returning `i32`, inside
`impl Solution`, and a one-line `max_number_of_balloons` calls it.

## Approaches

"balloon" uses `b`, `a` and `n` once and `l` and `o` twice, so the text
makes as many words as its scarcest letter allows: its count of `b`, `a` or
`n`, or half its count of `l` or `o`.

| file | mechanism |
|---|---|
| `max_number_of_balloons.kara` ★ | a `[0; 26]` count of the text's bytes, and the least of the five letters' counts, `l` and `o` halved, read through a closure. O(n) |
| `max_number_of_balloons_map.kara` | the text's letters and the word's counted in two `Map[char, i64]`s, and the least quotient over the word's letters. O(n) |
| `max_number_of_balloons_remove.kara` | the statement as written: the text counted once, then one word at a time, each of its seven letters taken out of the counts, until a letter runs out. O(n + words) |
| `max_number_of_balloons_filter.kara` | each of the five letters counted in the text and in the word by `chars().filter(..).count()`, and the least quotient. O(n), five passes |
| `max_number_of_balloons_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `[0; 26]` count, the five letters read out by index, and `b.min(a).min(l).min(o).min(n)` returned as an `i32`), carried to Kāra by `karac fix` |
| `max_number_of_balloons_chain.kara` | another Rust solution, in iterator chains (both counts `fold`ed into a `HashMap` through `entry(c).or_insert(0)`, then `have.get(c).copied().unwrap_or(0) / k` over the word's letters and `.min().unwrap_or(0)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 12 lines: LeetCode's three examples; the word
itself (`balloon: 1`); the word one `l` short (`baloon: 0`); the letters of
three words shuffled (`...: 3`); two words without an `n` (`ballooballoo:
0`); one letter (`b: 0`); the alphabet twice (`...: 1`); 2000 random texts
of up to 60 letters from the word's letters and two others (`2000 random
texts: 2524 words, checksum 789228858`); and 10^4 letters, the constraints'
most, from the whole alphabet (`10000 letters of 26: 171`) and from the
word's own letters (`10000 letters of balloon: 1417`).
`max_number_of_balloons.py` mirrors the ★ arm and its output is
byte-identical; it also checks every case and every random text against
the statement read literally. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, map, remove and filter arms check clean as written.
The solution arm takes one round of 4 fixes (`struct Solution;` to
`struct Solution {}`, `[0; 26]` to `[0i32; 26]`, `Solution::` to
`Solution.`, and the `as i64` on the widening call dropped) and its output
matches, after the fix below. The chain arm takes one round of 13 (among
them `HashMap::new()` to `Map.new()`, the `use` dropped, `|mut m, c|` to
`|m, c|` and a `let mut m = m;`, and `copied()` to `cloned()`) and its
output matches. The differential took one, `!held[p]` to `not held[p]`.

## Gaps

The solution arm found one, fixed in kara.

- **A copy of an element of a fill gave no fix.** `let mut cnt = [0; 26];
  .. let b = cnt[1]; .. b.min(a).min(l).min(o).min(n)` returned from the
  `i32` method was refused, "implicit coercion from 'i64' to 'i32' would
  narrow or change sign", with no fix; the same fill read directly is told
  "write that literal `0i32`", and `karac fix` writes it. The literal was
  still open at `let b = cnt[1]`, settling only at the `min` on the copy,
  and the trace from a copy back to its fill took only a copy whose literal
  had already settled to `i64`. It now follows an open one too. kara
  B-2026-11-18-2.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the most copies of "balloon" whose letters the text holds at
once, each letter used once, found by taking `k + 1` copies' letters out of
the text for `k = 0, 1, ..` until one is missing. 2000 random texts of 1 to
40 letters; the first 200 from the word's own letters, the rest from the
word's letters and `x` and `y`.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | at most one word per seven letters |
| P3 | the word appended makes one more word |
| P4 | the text reversed makes as many |
| P5 | letters outside the word added (`cdefxyz`) make as many |
| P6 | the text without its first letter makes as many or one fewer |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 texts: checksum 349163915, 84000
checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac run`,
`karac build` and the AddressSanitizer build.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: `l` not halved | P1 308, P2 1, P3 90, P7 1540 |
| S2 | ★: `n` left out | P1 88, P2 1, P7 440 |
| M1 | map: the word's count of `o` is one | P1 338, P3 97, P7 338 |
| M2 | map: a letter the text lacks counts as seven | P1 394, P2 144, P3 394, P6 113, P7 394 |
| R1 | remove: the word taken as `ballon` | P1 338, P3 97, P7 338 |
| R2 | remove: each letter of the text counted twice | P1 1291, P2 180, P3 2000, P6 32, P7 1291 |
| F1 | filter: `n` left out | P1 88, P2 1, P7 88 |
| F2 | filter: a quotient rounded up | P1 536, P2 2, P7 536 |
| X1 | solution: `l` not halved | P1 308, P2 1, P3 90, P7 308 |
| X2 | solution: `m` read for `n` | P1 1032, P3 2000, P7 1032 |
| C1 | chain: the word taken as `baloon` | P1 308, P2 1, P3 90, P7 308 |
| C2 | chain: a letter the text lacks counts as one | P1 132, P2 4, P3 132, P7 132 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. S1, X1 and C1 are one fault in three arms, `l` needed once, and
fail alike; M1 and R1 are one fault too, `o` needed once. P3 catches the
faults that change what a word needs or what the text holds; a letter left
out of the least (S2, F1) or a quotient rounded up (F2) still gains exactly
one word from the appended copy, so P3 misses them and P1 and P7 catch
them, P2 a handful of times. P4 and P5
catch none, since no mutation reads the text's order or a letter outside
the word.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 200 texts of 10^4 letters, the constraints' most, built once (from
the whole alphabet, from the letters of "balloon", and from those and `x`
and `y`, in turn); then 200 rounds over the texts, each answer folded into a
checksum. Every program prints `200 rounds of 200 texts of 10000 letters:
checksum 497395718`. Each call counts the text's bytes into a 26-entry
array and takes the least of the five letters' counts; the count loop is
the whole cost.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `e8dc4f7aa2`
and this kata's fix, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.229 to 0.362 s | 0.280 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.237 to 0.391 s | 0.277 s |
| Rust (`rustc -O`) | 0.202 to 0.297 s | 0.253 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.242 to 0.315 s | 0.280 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.222 to 0.381 s | 0.290 s |
| C (`clang -O3`) | 0.178 to 0.244 s | 0.211 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.167 to 0.232 s | 0.203 s |
| Go | 0.208 to 0.271 s | 0.236 s |
| Python | 13.13 to 13.46 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 3% of wall time for both Kāra
rows, so both ran on one core. Kāra ties Rust with overflow checks on, its
equal-safety twin (0.277 s against 0.280 s), and is about 9% behind plain
Rust, 17% behind Go and 31% behind C; each byte's `b - b'a'` is a checked
subtraction and a checked index in Kāra and the checked Rust, a checked
index alone in plain Rust and Go, and neither in C. No profile was taken,
so that the checks are the gap is inferred, not measured. Python takes
about 48x Kāra's time.
