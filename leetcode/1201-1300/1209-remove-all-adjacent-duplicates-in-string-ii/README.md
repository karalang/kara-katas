# 1209. Remove All Adjacent Duplicates in String II

You are given a string `s` and an integer `k`, a `k` duplicate removal
consists of choosing `k` adjacent and equal letters from `s` and removing
them, causing the left and the right side of the deleted substring to
concatenate together.

We repeatedly make `k` duplicate removals on `s` until we no longer can.

Return the final string after all such duplicate removals have been made.
It is guaranteed that the answer is unique.

```
s = "abcd", k = 2                                     ->  "abcd"
s = "deeedbbcccbdaa", k = 3                           ->  "aa"
s = "pbbcggttciiippooaais", k = 2                     ->  "ps"
```

**Constraints:** `1 <= s.length <= 10^5`; `2 <= k <= 10^4`; `s` only
contains lowercase English letters.

The arms are `fn remove_duplicates(s: String, k: i64) -> String`. The two
Rust arms keep the method LeetCode gives Rust users, on `k: i32`, inside
`impl Solution`, and a one-line `remove_duplicates` calls it.

## Approaches

| file | mechanism |
|---|---|
| `remove_all_adjacent_duplicates_in_string_ii.kara` ★ | a stack of runs, each a letter and how many times it has come in a row: a letter like the top run's adds one to it, and a run that reaches `k` is popped, so the run beneath it meets the next letter. O(n) |
| `remove_all_adjacent_duplicates_in_string_ii_inplace.kara` | in place: the letters copied down over the string's own bytes, a write index behind the read index, and beside each written letter how many times it comes in a row ending there; a count that reaches `k` steps the write index back by `k`, which unwrites the run. O(n), no stack |
| `remove_all_adjacent_duplicates_in_string_ii_runs.kara` | the runs first: the string cut into runs of one letter in a doubly linked list of indices, each run in turn kept to its length modulo `k`, merged into the run before it when that one holds the same letter (which only happens once a run between them has gone), and unlinked when it comes to nothing. O(n) |
| `remove_all_adjacent_duplicates_in_string_ii_text.kara` | the answer itself the stack: each letter pushed onto a `String`, and beside it a `Vec` of how many times the last letter has come in a row, found with `ends_with`; a count that reaches `k` truncates both by `k`. O(n) |
| `remove_all_adjacent_duplicates_in_string_ii_stack.kara` | a Rust solution as LeetCode's Rust users write it (a `Vec<(char, usize)>` of runs, the top reached by `match stack.last_mut() { Some(top) if top.0 == c => { top.1 += 1; if top.1 == k { stack.pop(); } } _ => stack.push((c, 1)) }`, and the answer by `stack.into_iter().map(\|(c, n)\| c.to_string().repeat(n)).collect()`), carried to Kāra by `karac fix` |
| `remove_all_adjacent_duplicates_in_string_ii_repeat.kara` | another Rust solution (the bytes in a `Vec<(u8, i32)>`, the top written through `if let Some((c, n)) = st.last_mut()` and `*n += 1` with a `continue`, and the answer by `flat_map(\|&(c, n)\| std::iter::repeat(c as char).take(n as usize))`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six more properties |

Every arm prints the same 13 lines: LeetCode's three examples; `aaa`
with `k = 4` (`"aaa"`), `aaaa` and `aaaaa` with `k = 2` (`""` and
`"a"`); a string where each removal makes the next (`"ybth"`);
`abccbaabccba` with `k = 2`, which empties; 1000 random small cases, 1
to 20 letters from the first two or three with `k` from 2 to 4 (`1000
small cases: 602 changed, 6552 letters left, checksum 940328393`); and
four at the constraints' top: 100000 random letters from two with `k =
2` (`156 left`) and from three with `k = 3` (`72970 left`), 50000
letters followed by their reverse with `k = 2`, where every pair at the
middle goes and the next pair meets (`0 left`), and runs of 3000 `c`,
5000 `b`, 10000 `a`, 5000 `b` and 7001 `c` with `k = 10000`, the
largest: the `a` go, the `b` meet and go, and the `c` meet and leave
one (`"c"`). `remove_all_adjacent_duplicates_in_string_ii.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac run` and `karac build`, and under the
AddressSanitizer build.

The Mend loop: the ★, inplace, runs and text arms check clean as
written. The stack arm takes one round of 7 fixes (among them `struct
Solution;` to `struct Solution {}`, `k as usize` to `k as i64` with
`Vec<(char, usize)>` to `Vec[(char, i64)]`, and the `match
stack.last_mut()` to `if stack.len() > 0 and stack[stack.len() - 1].0 ==
c { .. } else { stack.push((c, 1)); }`), and its last `collect()`, of
`String`s into a `String`, is gathered into a `Vec[String]` and joined
by hand, as the error's help says (`String` collects only `char`s,
kara B-2026-11-10-34). The repeat arm takes one round of 9 (among them
`vec![]` to `Vec.new()`, `if let Some((c, n)) = st.last_mut()` to `if
st.len() > 0` with `*c` and `*n` written `st[st.len() - 1].0` and
`st[st.len() - 1].1`, `std::iter::repeat` to `repeat`, and `take(n as
usize)` to `take(n)`). Both outputs match.

## Gaps

The two Rust arms found one, in `karac fix`, now fixed. Before it, each
arm stopped at "no method 'last_mut' on type 'Vec': write through an
index instead" with no machine fix: the `last_mut` rewrite took only
`Some(x)` and refused an arm that names the vector, although Rust's
borrow checker lets the arm name it only after the element's last use,
where an index reads the same; and the stack arm's
`c.to_string().repeat(n)`, with `n` a `usize`, was refused as "'repeat'
expects an integer count, found 'usize'". The rewrite now binds a pair's
fields through the index and allows the vector to be named after the
element's last use, and a `usize` count at `repeat` lets the program's
`usize`s be fixed to `i64` (kara B-2026-11-18-45, fixed at 275ab3ae7f).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the first `k` equal letters in a row removed, and the string
searched again from the start, until none are left. 2000 random cases:
1 to 16 letters from the first two or three, `k` from 2 to 4; 1089 of
them change, and 80 come to nothing.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | no `k` equal letters in a row, and shorter by a multiple of `k` |
| P3 | `s` reversed gives the answer reversed |
| P4 | the answer given again comes back unchanged |
| P5 | `k` copies of a letter put in anywhere give the same |
| P6 | every letter one later gives every letter one later |
| P7 | the ★ arm's answer |

All 84,000 checks pass on every arm: `2000 cases: checksum 340373211,
84000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. A Python reading of
the same cases, removing the first `k` equal letters until none are
left, gives the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a run taken out one letter early | P1 1482, P2 1324, P5 2000, P7 7410 |
| S2 | ★: a new run begun whatever the top's letter | P1 1089, P2 1089, P5 2000, P7 5445 |
| I1 | inplace: a count never taken past two | P1 529, P2 529, P5 1329, P7 529 |
| I2 | inplace: only k - 1 letters taken back | P1 1006, P2 781, P5 1620, P7 1006 |
| R1 | runs: two runs of one letter never joined | P1 283, P2 283, P4 283, P5 126, P7 283 |
| R2 | runs: a run left whole rather than cut to its remainder | P1 1089, P2 1089, P5 2000, P7 1089 |
| E1 | text: a letter's run looked for at the front | P1 1069, P2 573, P3 1116, P5 1312, P7 1069 |
| E2 | text: the streaks kept when the letters go | P1 370, P2 370, P3 217, P4 370, P5 230, P7 370 |
| K1 | stack: a run's count never taken past two | P1 667, P2 609, P5 962, P7 667 |
| K2 | stack: a full run left on the stack | P1 283, P2 283, P4 283, P5 126, P7 283 |
| P1 | repeat: a matching letter pushed as a new run too | P1 1622, P2 1414, P4 1135, P5 1620, P7 1622 |
| P2 | repeat: every run given out once | P1 1013, P2 896, P7 1013 |

A mutation of the ★ arm fails P7 on all six arms, the ★ arm against the
other five. Of the 2000 cases 1089 change. S2 starts a new run for every
letter and R2 never cuts a run to its length modulo `k`, so neither
removes anything: each fails the 1089, and P5, `k` copies of a letter
put in, fails in all 2000 cases, as it does for S1, which removes a run
one letter early and so leaves one of the `k` copies. R1 and K2 are one
fault in two arms: R1 never joins two runs of one letter that meet once
the run between them goes, and K2 leaves a finished run on the stack at
a count of 0, where it keeps the run beneath from meeting the next
letter; they fail alike, and P4, the answer given again, catches both,
since a second pass makes the join the first one missed. I1 and K1 keep
a count from passing two, so with `k = 2` they still answer right, and
fail only where `k` is 3 or 4. P6, every letter one later, catches none
of the twelve: no edit makes an arm treat one letter differently from
another.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a stack of runs, each a letter and how many times it has come in a
row, a run popped when it reaches `k`) on 12 strings of 100000 letters,
the constraints' most, drawn once: four from two letters, four from
three, and four of 50000 letters followed by their reverse; then 10
rounds over the strings with k = 2, 3 and 4, each answer's length and
last letter folded into a checksum. Every program prints `10 rounds over
12 strings of 100000 letters: checksum 253809452`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.301 to 0.399 s | 0.314 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.296 to 0.361 s | 0.309 s |
| Rust (`rustc -O`) | 0.259 to 0.323 s | 0.275 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.256 to 0.324 s | 0.275 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.248 to 0.361 s | 0.262 s |
| C (`clang -O3`) | 0.203 to 0.262 s | 0.212 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.192 to 0.239 s | 0.202 s |
| Go | 1.417 to 1.663 s | 1.515 s |
| Python | 6.404 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 11% ahead of Kāra (0.275 s
against 0.309 s), and the two ranges overlap. C is about 31% ahead of
Kāra (0.212 s against 0.309 s); Go takes about 4.9x Kāra's time. Python
takes about 21x Kāra's time. No profile was taken.
