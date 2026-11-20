# 1249. Minimum Remove to Make Valid Parentheses

Given a string `s` of `'('`, `')'` and lowercase English characters, your
task is to remove the minimum number of parentheses (`'('` or `')'`, in
any positions) so that the resulting parentheses string is valid, and
return *any* valid string.

Formally, a parentheses string is valid if and only if it is the empty
string or contains only lowercase characters, or it can be written as
`AB` (`A` concatenated with `B`) where `A` and `B` are valid strings, or
it can be written as `(A)` where `A` is a valid string.

```
s = "lee(t(c)o)de)"  ->  "lee(t(c)o)de"   ("lee(t(co)de)" and "lee(t(c)ode)" are accepted too)
s = "a)b(c)d"        ->  "ab(c)d"
s = "))(("           ->  ""
```

**Constraints:** `1 <= s.length <= 10^5`; `s[i]` is `'('`, `')'` or a
lowercase English letter.

The arms are `fn min_remove_to_make_valid(s: Str) -> String`.

Any valid string with the fewest removals is accepted, and two arms here
choose differently: the counting arm drops the last `(` left open, the
others the `(` that nothing closes, so on `(a(b)` one gives `(ab)` and
the others `a(b)`. The harness therefore checks each answer, as LeetCode
does, rather than printing it: its parentheses balance, it is the input
with characters taken out and every letter kept, and it has the fewest
removals, which the Python mirror and the differential's literal reading
pin.

## Approaches

| file | mechanism |
|---|---|
| `min_remove_to_make_valid.kara` ★ | a stack of the places of the `(` not yet closed: a `)` with nothing to close is marked as it is met, and the `(` left on the stack at the end are marked too, in a `Vec[bool]` of the characters to keep |
| `min_remove_to_make_valid_passes.kara` | two passes with a count: left to right, a `)` with no `(` open is dropped; right to left over the rest, a `(` with no `)` waiting after it is dropped; then reversed back |
| `min_remove_to_make_valid_count.kara` | one pass that drops each `)` with no `(` open and counts the `(` left open, then that many `(` dropped from the end of what was kept: the last ones |
| `min_remove_to_make_valid_set.kara` | the places to drop gathered in a `Set[i64]`, the `(` still open added with `extend`, and the string rebuilt with `enumerate`, `filter` and `map` |
| `min_remove_to_make_valid_solution.kara` | a Rust solution as LeetCode's Rust users write it (the characters in a `Vec<char>`, each removed one overwritten with `'*'`, then filtered out), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, four more properties |

Every arm prints the same 3 lines: LeetCode's three examples; the total
removed, the number of answers found invalid and a checksum of the
removal counts for 1000 random strings of 1 to 2000 characters, each
with its own share of parentheses, a third leaning to `(` and a third to
`)` (`83511 removed, 0 invalid, checksum 93137835`); and two strings of
100000 characters, the constraints' top: 50000 `(` then 50001 `)`, and
random parentheses only. `min_remove_to_make_valid.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac run` and `karac build`, and under the AddressSanitizer
build.

The Mend loop: the four Kāra arms checked clean as first written. The
solution arm takes one round of fixes, 5 by `karac fix`'s count, and
then checks clean: `struct Solution;` to `struct Solution {}`,
`Vec<char>` to `Vec[char]`, `Vec::new()` to `Vec.new()`, and `|&c|` to
`|c|`.

## Gaps

None found: every arm, as written, checks after its fixes, and runs and
builds alike.

## Differential

`differential.kara` holds copies of the five arms, renamed, and the
statement read literally: every set of the string's parentheses tried as
the ones removed, smallest sets first, until what is left is valid; the
size of the first such set. 2000 random strings of 1 to 14 characters,
each with its own share of parentheses, a third leaning to `(` and a
third to `)`.

| | property |
|---|---|
| P1 | the number removed is the statement's, read literally |
| P2 | the answer is valid: its parentheses balance, and it is the input with characters taken out, every letter kept |
| P3 | the string mirrored, reversed with `(` and `)` swapped, loses as many |
| P4 | the string with its letters taken out loses as many |
| P5 | the answer asked again comes back unchanged |
| P6 | as many removed as by the ★ arm |

All 60,000 checks pass on every arm: `2000 strings: checksum 435927093,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the first `(` left open kept | P1 1001, P2 1001, P3 1030, P6 4004 |
| S2 | ★: a `)` checks for an open `(` but closes none | P1 764, P2 873, P3 600, P5 873, P6 3056 |
| P1 | passes: the second pass's characters left reversed | P2 1626, P5 1626 |
| P2 | passes: no `)` dropped in the first pass | P1 1035, P2 1035, P3 1030, P6 1035 |
| C1 | count: one `(` too few dropped from the end | P1 1001, P2 1001, P3 1030, P6 1001 |
| C2 | count: the kept characters left reversed | P2 1626, P5 1626 |
| T1 | set: the `(` left open never added to the set | P1 1001, P2 1001, P3 1374, P6 1001 |
| T2 | set: a `)` checks for an open `(` but closes none | P1 764, P2 873, P3 600, P5 873, P6 764 |
| L1 | solution: the first `(` left open kept | P1 1001, P2 1001, P3 1030, P6 1001 |
| L2 | solution: an unmatched `)` turned into the letter `x` | P1 1035, P2 1035, P3 1374, P6 1035 |

All ten are caught, every one by P2, the answer checked as LeetCode
would. P1, the number removed, and P6 catch the eight that remove the
wrong number; the two that reverse the answer (P1, C2) remove the right
number of the right characters and are caught by P2 and by P5, since a
reversed answer asked again changes. P3, the mirror, catches the same
eight as P1. P4, the letters taken out, catches none: no mutation looks
at a letter, only at the parentheses.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a stack of the places of the `(` not yet closed, and a `Vec[bool]`
of the characters to keep) on 50 random strings of 100000 characters
built once, each with its own share of parentheses, each asked 4 times;
every kept string folded into a checksum. Every program prints `4 rounds
of 50 strings of 100000 characters: checksum 233187458`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.269 to 0.328 s | 0.279 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.269 to 0.334 s | 0.283 s |
| Rust (`rustc -O`) | 0.303 to 0.341 s | 0.315 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.292 to 0.343 s | 0.303 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.299 to 0.349 s | 0.308 s |
| C (`clang -O3`) | 0.262 to 0.296 s | 0.280 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.261 to 0.304 s | 0.270 s |
| Go | 0.385 to 0.471 s | 0.416 s |
| Python | 6.563 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is about 7% ahead of Rust with overflow checks on (0.283 s
against 0.303 s), and the two ranges overlap. C runs level with Kāra
(0.280 s against 0.283 s); Kāra is about 32% ahead of Go (0.283 s
against 0.416 s). Python takes about 23x Kāra's time. No profile was
taken.
