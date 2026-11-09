# 1081. Smallest Subsequence of Distinct Characters

Given a string `s`, return the lexicographically smallest subsequence of
`s` that contains all the distinct characters of `s` exactly once.

```
s = "bcabc"     ->  "abc"
s = "cbacdcbc"  ->  "acdb"
```

**Constraints:** `1 <= s.length <= 1000`; `s` consists of lowercase
English letters.

This is the problem of [316. Remove Duplicate
Letters](../../301-400/316-remove-duplicate-letters/) with a shorter
limit on the text. That kata wrote its arms over bytes; this one writes
the canonical stack again as its ★ and spends
the other arms on the surfaces 316 did not touch: a hash-table version
over `chars()`, a counts version, a recursive one over string methods
(`find`, `slice`, `replace`), bitmasks, the answer `String` itself as
the stack, and LeetCode's Rust template.

The arms take the text as a `Str` and return the answer as a `String`.

## Approaches

| file | mechanism |
|---|---|
| `smallest_subsequence.kara` ★ | a stack of the answer so far over the text's bytes, with an `Array[i64, 26]` of each letter's last place: a letter already placed is passed over; any other pops every larger letter on top that comes again later, then goes on top. O(n) |
| `smallest_subsequence_maps.kara` | the ★ stack over `chars()`, with a `Map[char, i64]` of last places, a `Set[char]` of the letters placed and a `Vec[char]` collected into the answer. O(n) |
| `smallest_subsequence_counts.kara` | the ★ stack with counts in place of last places: how many of each letter are still to come says whether a larger letter on top can go and be placed again later. O(n) |
| `smallest_subsequence_greedy.kara` | the first letter decided, then the rest: the smallest letter whose first place still has every distinct letter at or after it; what follows is the answer for the text after that place with that letter taken out (`find`, `slice`, `replace`). O(26^2 n) |
| `smallest_subsequence_masks.kara` | a letter at a time from `u32` bitmasks of the letters at or after each place: the next letter is the smallest not yet taken whose next place still has every letter not yet taken ahead of it. O(26^2 n) |
| `smallest_subsequence_string.kara` | the ★ stack as the answer `String` itself: `contains` asks whether a letter is placed, `chars().last()` reads the top, `rfind` finds its last place, and `pop` takes it off. O(26 n) |
| `smallest_subsequence_solution.kara` | LeetCode's Rust template (`struct Solution;`, `s.as_bytes()`, a `[0usize; 26]` of last places, `for (i, &c) in s.iter().enumerate()`, `while let Some(&top) = stack.last()`, `String::from_utf8`), carried to Kāra by `karac fix` |
| `differential.kara` | the seven arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and ten
more; the letters kept and a checksum over 300 random texts of 1 to 1000
letters over the first 1 to 26 letters (`3892 letters kept, checksum
244995108`); and 1000 letters of the alphabet written backwards over and
over, whose answer is the alphabet. `smallest_subsequence.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the seven arms and the statement
read literally: the answer holds each distinct letter once, so it is an
ordering of them, and it is the smallest ordering that is a subsequence
of the text. The orderings are tried smallest first, a letter at a time,
each prefix matched against the text from the left, and the first whole
one matched is the answer (no arm's walk is reused). It checks 2000
problems, 1000 texts of 1 to 12 letters over 1 to 4 letters and 1000 of
1 to 150 letters over 1 to 10, each alphabet drawn from `a` to `w`.
Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is a subsequence of the text and holds each of its letters once |
| P3 | the letters moved to other letters in the same order (`a` to `w` into `b` to `y`, one place skipped) move the answer the same way |
| P4 | each run of one letter written once, or each letter written twice, answers the same |
| P5 | the answer, asked again, is itself |
| P6 | a letter smaller than all of them in front and one larger behind (`a` + the moved text + `z`) stand first and last around the moved answer |

All 84,000 checks pass on every arm: `2000 problems: checksum 908640393,
84000 checks over 7 arms: 0 failures`. A Python reading of the same
problems by the first-letter rule gives the same checksum.

## Mutation testing

Thirty-five edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Thirty-one are caught,
each the same way under both backends, and one more stops both with an
index out of bounds (the masks arm taking a letter when any letter still
to be taken is ahead of its place, so the search for the next one runs
off the end). Fifteen are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a popped letter stays placed | P1 1085, P2 1085 |
| M2 | ★: a last place, once set, never moved on | P1 938, P4 652, P6 492 |
| M3 | ★: the text walked from the right | P1 638, P2 638, P5 1433, P6 2000 |
| M4 | maps: the new letter's last place asked, not the top's | P1 412, P2 269, P4 445 |
| M5 | maps: the stack read top first | P1 1525, P2 581, P5 1525, P6 2000 |
| M6 | counts: a top with one copy left kept (`<= 1`) | P1 386, P4 452 |
| M7 | counts: every letter counted once | P1 981, P2 132, P4 1175 |
| M8 | greedy: a first letter taken that loses one letter of the rest | P1 452, P2 452, P5 147 |
| M9 | greedy: each letter tried at its last place (`rfind`) | P1 1104 |
| M10 | masks: each place holds only its own letter | P1 1525, P2 1525, P6 2000 |
| M11 | string: only the last letter checked as placed (`ends_with`) | P1 1291, P2 1291, P5 1062 |
| M12 | string: one top popped at most | P1 594 |
| M13 | solution: a top whose last copy is next kept (`> i + 1`) | P1 128, P4 210 |
| M14 | solution: the first letter passed over (`skip(1)`) | P1 313, P2 224, P4 816, P5 1924, P6 2000 |
| M15 | solution: the bottom of the stack compared (`first()`) | P1 851, P2 448, P6 917 |

P1 catches all fifteen, P2 ten, P4 and P6 six each, P5 five and P3
none. P3 moves the letters to others in the same order, and every edit
here treats a letter by its order alone, so each answers the moved text
exactly as wrongly as the text. M9 and M12 are seen by P1 only: what
they keep is a subsequence with every letter once, just not the
smallest, and they keep it the same way after a run is collapsed or a
letter doubled.

Of the twenty not kept, the crash is above, three are equivalent and
survive, and sixteen fail exactly as a kept edit or as one another. The
equivalent three: the masks arm starting the next search at the letter
just taken rather than after it (the next letter is another letter),
the masks arm reading the letters wanted from what is ahead of its place
rather than from the whole text (every letter not yet taken is ahead of
it), and the solution arm's last places one late (`last > i` and `last
>= i` differ only at a top's own place, which is never the current
one). Five fail alike, each popping smaller tops or trying the largest
letter first, in the ★, counts, greedy, masks and string arms (P1
1374); a popped letter left placed fails as M1 in the maps and
counts arms; a letter pushed again, or never marked, fails alike in the
★, maps, greedy (the letter not taken out of the rest) and solution arms
(P1 1823, P2 1823, P4 2000); the maps arm's first place kept as the last
and the string arm's `find` for `rfind` fail alike (P1 1085); the string
arm's answer reversed fails as M5; and the counts arm counting a letter
before it is passed, and the greedy arm taking the rest from the text's
start, fail in ways of their own but were not needed.

## Verification

Every arm prints the same output as `smallest_subsequence.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file. Under `karac __mir-run`, with the machine busy
with a build, the arms take 0.4 s to 2.7 s (the greedy arm the slowest)
and the differential 22.3 s.

The kata found one diagnostics gap, fixed in kara `5eee63ee71` with
`tests/kata_1081_replace_char_fix.rs`:

- **A `char` handed to `replace` got no fix.** The greedy arm takes
  every copy of a placed letter out of the rest of the text with Rust's
  `rest.replace(c, "")`. Kāra's string methods take a `Str` pattern, and
  `find` and `contains` already met a char with "takes a `Str` pattern,
  found 'char': write it as `c.to_string()`" and an edit; `replace` and
  `replacen` said only "expects String arguments", so `karac fix`
  stopped there. They now take the same fix, on the pattern and on the
  replacement. Kara B-2026-11-09-25.

Every file went through `karac fix`. It wrote `c.to_string()` for the
chars handed to `find`, `contains` and `rfind` in the greedy and string
arms, and `~` for Rust's `!` on an integer in the masks arm. The Rust arm
reaches a clean check in three rounds and gives the text the arm holds:
the syntax (`struct Solution {}`, the `&` dropped from `&c`, `Vec<u8>`
to `Vec[u8]`, `Vec::new()` to `Vec.new()`, `Some(&top) = stack.last()`
to `Some(top) = stack.last().cloned()`, `&&` to `and`, `Solution.` and
`String.from_utf8`); then `s.as_bytes()` to `s.bytes()`; then every
`as usize` to `as i64` and the `0usize` suffix dropped.

## Benchmarks

The bench builds 2000 random texts of 1000 letters once, LeetCode's
longest, the text `t` over the first `t % 26 + 1` letters, and answers
every text with the ★ arm in each of 100 rounds, in an order that
changes with the round, folding each answer's length and middle letter
into a checksum. Every implementation prints `100 rounds over 2000 texts
of 1000 letters: 2697600 letters kept, checksum 651198933`. Each mirror
returns a fresh string per call, as the Kāra arm returns a `String`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `2a1ba88113`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.427 to 0.526 s | 0.467 s |
| C (`clang -O3`) | 0.456 to 0.499 s | 0.480 s |
| Rust (`rustc -O`) | 0.531 to 0.606 s | 0.564 s |
| Kāra (`karac build`) | 0.555 to 0.681 s | 0.572 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.571 to 0.625 s | 0.594 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.556 to 0.662 s | 0.607 s |
| Go | 0.584 to 0.640 s | 0.607 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.582 to 0.698 s | 0.610 s |
| Python | 19.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.56 s) is its real time, and the 6% between the two Kāra
rows is within their spread.

The work is 200 million letters walked by the stack, with one small
allocation per answer. Kāra, Rust and Go are level, within 8% of one
another, and Kāra matches Rust with overflow checks at the same ISA.
C, whose stack is a fixed 27-byte buffer with no bounds checks, takes
23% less. Python runs the same walk at 32x Kāra.
