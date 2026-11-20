# 1221. Split a String in Balanced Strings

**Balanced** strings are those that have an equal quantity of `'L'` and
`'R'` characters.

Given a **balanced** string `s`, split it into some number of substrings
such that each substring is balanced. Return the **maximum** number of
balanced strings you can obtain.

```
"RLRRLLRLRL"  ->  4    "RL", "RRLL", "RL", "RL"
"RLRRRLLRLL"  ->  2    "RL", "RRRLLRLL"
"LLLLRRRR"    ->  1    "LLLLRRRR"
```

**Constraints:** `2 <= s.length <= 1000`; each `s[i]` is `'L'` or `'R'`;
`s` is balanced.

The arms are `fn balanced_string_split(s: String) -> i64`. The two Rust
arms keep the method LeetCode gives Rust users, on `i32`, inside `impl
Solution`, and a one-line `balanced_string_split` calls it.

## Approaches

| file | mechanism |
|---|---|
| `split_a_string_in_balanced_strings.kara` ★ | walk the string keeping the count of L's less R's; every time it comes back to zero a balanced piece ends, and cutting there is never worse than going on. O(n) |
| `split_a_string_in_balanced_strings_bytes.kara` | the bytes walked with a `match` on `b'L'`, the balance an `i32`, a piece added as `if balance == 0 { 1 } else { 0 }` |
| `split_a_string_in_balanced_strings_fold.kara` | one `fold` over the characters carrying the pair (balance, pieces), the closure returning the next pair |
| `split_a_string_in_balanced_strings_prefix.kara` | every prefix's balance kept in a `Vec`; a piece can end exactly where a prefix is balanced, so the answer is the count of nonempty balanced prefixes, `prefix[1..].iter().filter(..).count()`. O(n) space |
| `split_a_string_in_balanced_strings_counter.kara` | a Rust solution as LeetCode's Rust users write it: an `i32` balance and answer over `s.chars()`, carried to Kāra by `karac fix` |
| `split_a_string_in_balanced_strings_scan.kara` | another Rust solution: `s.as_bytes().iter().scan(0, ..)` for the running balance, `.filter(|&b| b == 0).count() as i32` for the answer, carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 7 lines: LeetCode's three examples and two
more, the total and a checksum of the answers for 1000 shuffled strings
of 2 to 16 letters (`2688`, `418076078`), and the answers at the
constraints' top, 1000 letters: `LR` over and over (`500`), 500 L's then
500 R's (`1`), and shuffled (`26`).
`split_a_string_in_balanced_strings.py` mirrors the ★ arm, and its output
is byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, bytes, fold and prefix arms check clean. The
counter arm takes one round of 2 fixes (`struct Solution;` to `struct
Solution {}`, and the wrapper's `as i64`, which widening makes
needless) and checks clean. The scan arm takes one round of 6 fixes:
those two, `as_bytes()` to `bytes()`, the patterns `|b, &c|` and `|&b|`
to `|b, c|` and `|b|`, and the closure itself, which Rust writes as
`*b += ..; Some(*b)` through a `&mut` state, rewritten to Kāra's `scan`,
whose closure takes the state by value and returns `Some((next state,
item))`: `let b = b + ..; Some((b, b))`. It then checks clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way to cut the string, each of the `2^(n − 1)` sets of
places between letters, kept when every piece holds as many L's as R's,
and the most pieces of those kept. 2000 cases, each a shuffle of 1 to 7
of each letter, with a second shuffle of 1 to 4 of each to join to it.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the string reversed gives the same answer |
| P3 | every L an R and every R an L gives the same answer |
| P4 | two balanced strings joined give the sum of their answers |
| P5 | from 1 to half the string's length |
| P6 | the ★ arm's answer |

P2 and P3 hold because reversing or swapping the letters keeps a piece
balanced. P4 holds because no piece of the best split of the joined
string crosses the join: the balance is zero there, so a piece that
crossed it could be cut in two.

All 72,000 checks pass on every arm: `2000 cases: checksum 810596661,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a piece counted wherever more L's than R's have been read | P1 1479, P2 1826, P3 1826, P5 1225, P6 7395 |
| S2 | ★: an R counted as an L | P1 2000, P5 2000, P6 10000 |
| B1 | bytes: an L counted twice | P1 1831, P2 1300, P3 1546, P4 691, P5 1078, P6 1831 |
| B2 | bytes: a piece counted wherever R's lead | P1 1570, P2 1826, P3 1826, P5 1295, P6 1570 |
| F1 | fold: the pieces begun at one | P1 2000, P4 2000, P5 723, P6 2000 |
| F2 | fold: the count dropped while a piece is open | P1 1459, P4 2000, P6 1459 |
| P1 | prefix: the empty prefix counted | P1 2000, P4 2000, P5 723, P6 2000 |
| P2 | prefix: an R left out of the balance | P1 1769, P2 1426, P3 2000, P4 996, P5 993, P6 1769 |
| C1 | counter: an L counted down | P1 2000, P5 2000, P6 2000 |
| C2 | counter: the answer begun at one | P1 2000, P4 2000, P5 723, P6 2000 |
| N1 | scan: the state never carried | P1 2000, P5 2000, P6 2000 |
| N2 | scan: the answer every nonzero balance | P1 1277, P5 1277, P6 1277 |

A mutation of the ★ arm fails P6 on all six arms, the ★ arm against the
other five. P1 catches every mutation. Three mutations make the balance
never come back to zero, so the answer is always 0 (S2, C1, N1): P5
alone of the other properties catches them, since a 0 is the same
reversed, swapped, and joined. Three start the count at one (F1, P1,
C2): P4 catches them in every case, a joined string gaining one where
the sum gains two, and P5 catches them where every piece is two letters
and the answer is already half the length. F2, which forgets the count
whenever a piece is open, answers 1 for every string, since every piece
is open after its first letter: only P1 and P4 see it. P2 and P3 catch
the mutations that treat L and R differently (S1, B1, B2, P2) and no
others, as they should. N2 counts the balances that are not zero, the
string's length less its pieces: every symmetry and the joining law
keep that, so only P1 and P5 catch it, and neither where every piece is
two letters, where the length less the pieces is the pieces.

A first F2 counted a piece where the balance was zero before the letter
was read, not after, and no check failed: on a balanced string that
counts each piece at its start rather than its end, the same number. It
is not a mutation, and the one above replaced it.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, walk the string keeping L's count less R's and count the returns to
zero, over 2000 random balanced strings of 1000 letters drawn once, 20
passes; checksum of the answers. Every program prints `2000 strings of
1000 letters, 20 passes: pieces total 1517220, checksum 696920861`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.263 to 0.309 s | 0.271 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.260 to 0.306 s | 0.270 s |
| Rust (`rustc -O`) | 0.048 to 0.084 s | 0.050 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.230 to 0.271 s | 0.241 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.250 to 0.303 s | 0.256 s |
| C (`clang -O3`) | 0.203 to 0.240 s | 0.209 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.199 to 0.234 s | 0.206 s |
| Go | 0.051 to 0.068 s | 0.052 s |
| Python | 3.175 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 11% ahead of Kāra (0.241 s
against 0.270 s), and the two ranges overlap. C is about 23% ahead of
Kāra (0.209 s against 0.270 s); Kāra takes about 5.2x Go's time (0.270 s
against 0.052 s). Python takes about 12x Kāra's time. No profile was
taken.
