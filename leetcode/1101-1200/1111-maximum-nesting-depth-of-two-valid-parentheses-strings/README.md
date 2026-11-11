# 1111. Maximum Nesting Depth of Two Valid Parentheses Strings

A string is a *valid parentheses string* (VPS) if and only if it
consists of `"("` and `")"` characters only, and it is the empty string,
or can be written as `AB` (`A` concatenated with `B`) where `A` and `B`
are VPS's, or can be written as `(A)` where `A` is a VPS.

Its *nesting depth* `depth(S)` is `0` for the empty string,
`max(depth(A), depth(B))` for `A + B`, and `1 + depth(A)` for
`"(" + A + ")"`.

Given a VPS `seq`, split it into two disjoint subsequences `A` and `B`,
such that `A` and `B` are VPS's (and `A.length + B.length =
seq.length`). Choose any such `A` and `B` such that `max(depth(A),
depth(B))` is the minimum possible value.

Return an `answer` array (of length `seq.length`) that encodes such a
choice of `A` and `B`: `answer[i] = 0` if `seq[i]` is part of `A`,
else `answer[i] = 1`. Note that even though multiple answers may exist,
you may return any of them.

```
seq = "(()())"    ->  [0,1,1,1,1,0]
seq = "()(())()"  ->  [0,0,0,1,1,0,1,1]
```

**Constraints:** `1 <= seq.size <= 10000`.

The arms are `fn max_depth_after_split(seq: Str) -> Vec[i32]`. Every arm
gives the same answer: each pair goes to the group of the parity of the
depth it sits at, so a pair inside no other is in `A`. For LeetCode's
second example that is `[0,0,0,1,1,0,0,0]`, which LeetCode accepts
beside its own.

## Approaches

| file | mechanism |
|---|---|
| `max_depth_after_split.kara` ★ | a depth counter: each pair goes to the group of its depth's parity, `(` taking the depth before it opens and `)` the depth after it closes, so the two parts each hold every other level and neither is deeper than half the whole, rounded up. O(n) |
| `max_depth_after_split_stack.kara` | a stack of groups: each `(` takes the group its enclosing pair does not, the first group when nothing encloses it, and each `)` takes the group of the `(` it closes. O(n) |
| `max_depth_after_split_bits.kara` | by position alone: a `(` at index i opens at a depth of i's parity, and a `)` closes to the other parity, so each character's group is `i & 1` flipped for `)`. Written as Rust writes it, over `bytes()` and `enumerate()`, and carried to Kāra by `karac fix`. O(n) |
| `max_depth_after_split_fold.kara` | a `fold` over the characters that carries the depth and the answer together, and a `match` on each character. O(n) |
| `max_depth_after_split_scan.kara` | an iterator chain with the depth carried by `scan`, as Rust writes it, and carried to Kāra by `karac fix`. O(n) |
| `max_depth_after_split_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `String`, a `map` closure that keeps the depth in a captured `mut`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: the answers for LeetCode's two
examples and eight more (one pair, a nest of two and of three, three
pairs side by side, and four mixed), then over 2000 random strings of 1
to 50 pairs, how many characters go to the second group and a checksum
(`2000 random strings: 45076 in the second group, checksum 133623708`),
and two of LeetCode's longest, 10^4 characters: one nest of 5000 pairs
and 5000 pairs at random. `max_depth_after_split.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the least, over every way to give each character to `A` or
`B` with both valid, of the deeper part's depth, found by a search over
the characters in order that keeps, for each depth `A` can be at, the
least peak a split reaching it has had. It checks 2000 problems in four
kinds of 500: up to 12 pairs at random; a nest of up to 15 pairs with a
short random string inside it; up to 10 short random strings side by
side; and up to 30 pairs at random. Every random choice is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer holds only 0 and 1, one per character, both parts are valid, and the deeper part is as shallow as the literal search allows |
| P2 | by a second reading, the pairs: each `)` is in the group of the `(` it closes, a pair inside no other is in the first group, and a pair directly inside another is in the other's other group |
| P3 | another valid string after it leaves its answer alone, and is answered as on its own |
| P4 | wrapped in one more pair, the answer is flipped inside the new pair, which is in the first group |
| P5 | mirrored (reversed, each character turned), the answer is reversed |
| P6 | a `()` put in at a random place leaves the rest of the answer alone, the new pair in one group |

All 72,000 checks pass on every arm: `2000 problems: checksum
649948932, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, the same literal search, gives the same checksum.

P1 judges an answer only by what the statement asks, so any minimal
split passes it; P2 pins the one answer every arm gives, by its pairs.
P3 to P6 compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a `(` given the depth after it opens | P1 1702, P2 2000, P4 2000, P5 2000, P6 2000 |
| M2 | ★: every `(` below the top level in the second group | P1 1327, P2 1327, P4 1775, P5 1327, P6 489 |
| M3 | ★: a `)` grouped by its depth's remainder by three | P1 895, P2 947, P4 1327, P5 947, P6 378 |
| M4 | bits: every group swapped | P2 2000, P4 2000 |
| M5 | bits: the index halved first | P1 1774, P2 2000, P3 883, P4 2000, P5 1037, P6 2000 |
| M6 | bits: or for exclusive or | P1 2000, P2 2000, P4 2000, P5 2000, P6 1058 |
| M7 | stack: every pair in the first group | P1 1775, P2 1775, P4 2000 |
| M8 | stack: every enclosing pair taken as in the first group | P1 1775, P2 1775, P4 2000, P5 1775, P6 1431 |
| M9 | scan: the depth carried no higher than two | P1 1327, P2 1327, P3 972, P4 1775, P5 1327, P6 409 |
| M10 | scan: the walk ended when the first pair closes | P1 2000, P2 2000, P3 1706, P4 2000, P5 1581, P6 2000 |
| M11 | fold: a `)` never lowers the depth | P1 1765, P2 1894, P3 883, P4 1037, P5 1850, P6 1838 |
| M12 | fold: the branches for the two characters swapped | P1 2000, P2 2000, P4 2000 |
| M13 | fold: the answer cut to its first 40 entries at each step | P1 201, P2 201, P3 308, P4 238, P5 201, P6 238 |
| M14 | solution: the depth held at three | P1 947, P2 947, P3 681, P4 1327, P5 947, P6 181 |
| M15 | solution: a final `))` dropped | P1 1419, P2 1419, P3 1201, P4 581, P5 1581, P6 1504 |

P2 and P4 catch all fifteen, P1 fourteen, P5 and P6 twelve, and P3
seven. P1 misses M4: every group swapped is a split as shallow as the
right one, which the statement accepts; P2, which pins the one answer
every arm gives, sees it, and so does P4, which wants the new outer pair
in the first group. P4 catches all thirty edits: one more pair around
the string moves every pair a level down, and a rule that is not the
parity of the depth answers some level wrong. P5 and P6 miss the edits
whose answer reads the same from either end and with a pair put in
anywhere: M4, every pair in one group (M7), and the two characters'
branches swapped (M12). P3 sees only the edits that look at more than
the depth a pair sits at: where a character is in the string (M5,
M13), where the walk ends (M10, M15), or a depth that does not come
back to zero where the second string starts (M9, M11, M14).

Of the fifteen not kept, ten fail as a kept edit: eight as M1, the
other ways of putting each pair a level off (a `)` given the depth
before it closes in the ★, scan, fold and solution arms, a `(` given
the depth after it opens in the stack, scan and solution arms, and the
stack arm putting a `)` in the other group from its `(`), and two as
M4, the scan and solution arms starting the depth at one. Two more
fail alike: the ★ arm never answering the first character and the bits
arm never answering the last. The stack arm walking the characters
backwards stops: its first `)` pops an empty stack, and `unwrap()` on
`None` panics. The other two fail in ways of their own but were not
needed: the bits arm reading the wrong bit of the index, and the fold
arm counting each `(` twice.

## Verification

Every arm prints the same output as `max_depth_after_split.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found three gaps, all fixed. The ★, stack and fold arms were
written as Kāra, the bits, scan and solution arms as Rust writes them.
`karac fix` carried the bits arm to a clean check in two rounds (`&str`
to `Str`, `Vec<i32>` to `Vec[i32]`, `seq.bytes()` to
`seq.bytes().iter()`) and the solution arm in three (`struct Solution
{}` declared and `Solution::` to `Solution.`, and the captured `let mut
depth = 0` to `let mut depth: i32 = 0`, since the closure's items are
`i32`). The scan arm had no fix at first: Rust's `scan` writes its
state through `*depth` inside an `if`, and the rewrite to Kāra's
`Some((state, item))` was withheld for a write below the closure body's
own statements (B-2026-11-11-27); now it copies the state with `let mut depth =
depth;` and writes the copy. Its start `0` then took the literal default
`i64`, so its items did too, and the collect into a `Vec[i32]` had no
fix (B-2026-11-11-28); the fix is `scan(0i32, ..)`. The third came from a mutation
of the stack arm: `match open.last() { Some(g) => g - g, None => 0 }`
over a `Vec[i32]` was refused as `ref i32` against an `i64` literal,
where beside an owned `i32` the literal takes `i32` (B-2026-11-11-29).

## Benchmarks

The bench builds 16 random strings of 10^4 characters once, LeetCode's
longest, and notes where each one's depth comes back to zero. Each of
1000 rounds answers a valid prefix of every string with the ★ arm, cut
at a different one of those places each time: 16,000 calls over 33
million characters. Every implementation prints `1000 rounds over 16
strings of 10000 characters: 32959640 characters, 16226268 in the second
group, checksum 113551820`. Each answer is a fresh array in every
language: a `Vec[i32]` in Kāra, a `Vec<i32>` made with its capacity in
Rust, a slice in Go, a list in Python, and a `malloc`ed array in C,
freed after the call.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `3402c1954a`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.046 to 0.067 s | 0.047 s |
| C (`clang -O3`) | 0.050 to 0.059 s | 0.051 s |
| Rust (`rustc -O`) | 0.207 to 0.288 s | 0.215 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.211 to 0.264 s | 0.216 s |
| Kāra (`karac build`) | 0.220 to 0.274 s | 0.224 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.226 to 0.317 s | 0.237 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.220 to 0.289 s | 0.239 s |
| Go | 0.251 to 0.318 s | 0.265 s |
| Python | 1.975 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra is level with Rust and about 1.1x faster than Go. C takes
about a fifth of their time: it writes each answer by index into an
array allocated at the string's length, where the others push onto a
vector made with that capacity; the gap was not traced further. Python
takes about 8x Kāra's time.
