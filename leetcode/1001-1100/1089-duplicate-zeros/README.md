# 1089. Duplicate Zeros

Given a fixed-length integer array `arr`, duplicate each occurrence of
zero, shifting the remaining elements to the right.

**Note** that elements beyond the length of the original array are not
written. Do the above modifications to the input array in place and do
not return anything.

```
arr = [1,0,2,3,0,4,5,0]  ->  [1,0,0,2,3,0,0,4]
arr = [1,2,3]            ->  [1,2,3]
```

**Constraints:** `1 <= arr.length <= 10^4`; `0 <= arr[i] <= 9`.

The arms take the array as a `mut ref Vec[i64]` and change it in place.

## Approaches

| file | mechanism |
|---|---|
| `duplicate_zeros.kara` ★ | two passes and no second array: the zeros counted, then a walk back from the end (`(0..n).rev()`) in which, with `zeros` the zeros up to and including place i, the digit at i goes to i + zeros, and a 0 also to the place before; a place past the end is dropped. Every write lands at or after the place read. O(n) time, O(1) space |
| `duplicate_zeros_shift.kara` | the statement step by step: at each 0, `insert` another 0 after it, which moves the rest one place right, and `pop` the digit pushed off the end, then step over both zeros. O(n times the zeros) |
| `duplicate_zeros_chain.kara` | an iterator chain: each digit becomes a list of itself, or of two zeros (`flat_map` over an `if` that gives `[0, 0]` or `[x]`, made an iterator with `.into_iter()`), the first n kept (`take`) and collected, then copied back with `into_iter().enumerate()`. O(n) time and space |
| `duplicate_zeros_queue.kara` | a `VecDeque` of the digits still to be written: each place's digit joins the back (a 0 twice) and the place takes the front. The queue holds the digits a write has pushed out of their places. O(n) time, O(the zeros) space |
| `duplicate_zeros_text.kara` | as text: the digits written into a `String` with `push_str`, every `"0"` replaced by `"00"`, and the first n characters read back with `to_digit(10)`. O(n) |
| `duplicate_zeros_solution.kara` | LeetCode's Rust template (`struct Solution;`, `arr: &mut Vec<i32>`, the zeros counted with `filter(\|&&x\| x == 0).count()`, one write index that starts at n + zeros and steps back once for each digit and once more for each 0, `Solution::duplicate_zeros(&mut digits)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and ten more
(a lone 0, all zeros, a 0 at either end), a checksum over 2000 random
arrays of 1 to 20 digits and the zeros left in them (`11892 zeros after,
checksum 850455342`), and a checksum over one array of 10^4 digits,
LeetCode's longest. A third of every random array's digits are 0.
`duplicate_zeros.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every digit written out in order, each 0 twice, and the first
n kept. It checks 2000 problems: 1400 arrays of 1 to 8 digits and 600
of 1 to 30, each with a tail of 1 to 6 digits and one digit to put in
front, a third of all digits 0. Every random choice is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer read back, each 0 followed by its second copy and the pair read as one 0, is the input's first digits, as many as fill the n places (the last 0 may have lost its copy) |
| P3 | more digits after the input leave the answer's first n places as they were |
| P4 | turning every digit but 0 into 10 less it, before the arm or after it, gives the same answer |
| P5 | a 0 put in front of the input gives two zeros and the answer's first n - 1 digits; any other digit gives that digit and the whole answer |
| P6 | the arm run on its own answer gives the input with each 0 written four times, the first n kept |

All 72,000 checks pass on every arm: `2000 problems: checksum 622389284,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, from the digits written out as text, gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All thirty are caught,
each the same way under both backends. Fifteen are kept, no two failing
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second copy of a 0 written as 1 | P1 1712, P2 1712, P4 1712, P5 773, P6 1712 |
| M2 | ★: the walk forward, not back | P1 1432, P2 1432, P3 1380, P5 1284, P6 1382 |
| M3 | ★: a last 0 not taken as a 0 | P1 632, P2 632, P3 791, P5 620, P6 999 |
| M4 | ★: one zero too many counted | P1 1621, P2 1621, P5 1586, P6 1447 |
| M5 | shift: the new 0 doubled again | P1 1107, P2 1107, P5 439, P6 724 |
| M6 | shift: the last two places not looked at | P1 313, P2 313, P3 313, P5 160, P6 282 |
| M7 | shift: a leading 0 not doubled | P1 598, P2 598, P5 864, P6 537 |
| M8 | chain: every other digit doubled too | P1 1548, P2 1548, P5 1210, P6 1387 |
| M9 | chain: 1 doubled in place of 0 | P1 1458, P2 1458, P4 1099, P5 841, P6 1431 |
| M10 | queue: the second 0 put at the front | P1 912, P2 912, P5 480, P6 680 |
| M11 | queue: the 0 doubled after its place is written | P1 714, P2 714, P5 365, P6 447 |
| M12 | text: only a pair of zeros doubled | P1 1306, P2 1306, P5 543, P6 1228 |
| M13 | text: 9 read as 0 | P1 610, P2 610, P4 933, P5 108, P6 472 |
| M14 | solution: the second 0 written where the first goes | P1 1415, P2 1415, P3 1220, P5 1542, P6 1415 |
| M15 | solution: the last place never written | P1 1489, P2 1489, P3 1464, P5 1062, P6 1424 |

P1, P2, P5 and P6 catch all fifteen; P3 five and P4 three. P1 and P2
fail on the same problems for every edit: an answer of length n that
reads back as the input's first digits, as many as fit, can only be the
literal one, so P2 is the statement again, checked from the other end.
P3 sees only the edits that treat the end of the array apart (M2, M3,
M6, M14, M15), since more digits after the input move the end; P4 only
those that write some digit in place of another (M1, M9, M13), since
turning the digits but 0 is invisible to an edit that moves digits
without changing them. M6 is the hardest to see: it is wrong only when
the answer's second last place holds a 0 whose copy belongs in its last
place, 313 of the 2000 problems.

Of the fifteen not kept, two fail exactly as a kept edit and thirteen
fail in ways of their own or alike among themselves but were not
needed. The solution arm's write index one place out fails as M4, and
the queue arm skipping its first place as M7. Four edits that leave
every 0 single (the shift arm putting its new 0 at the end, the chain
arm's `[0]`, the queue arm taking the newest digit, the text arm
replacing nothing) fail alike, as do the queue and solution arms
writing a pair's second copy as 1. Not needed: the ★ arm never placing
its first digit, the shift arm skipping the digit after any other, the
chain arm leaving its last place and copying its answer back a place to
the left, the text arm dropping its first character and writing the
digits in reverse, and the solution arm never placing its last digit.

## Verification

Every arm prints the same output as `duplicate_zeros.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file. Under `karac __mir-run` the differential takes 8 s.

The chain arm found a gap in `karac fix`. Written as Rust writes it,
`flat_map(|x| if x == 0 { [0, 0] } else { [x] })`, it is refused, since
Kāra's `flat_map` wants an `Iterator` and a list is a collection; the
message says to iterate it with `.into_iter()`, but the fix knew where
to put that only after a call, a name or a list, not after an `if` or a
`match`. It now writes it after the closure's whole `if` (kara
B-2026-11-10-3, pinned by `tests/kata_1089_flat_map_if_into_iter.rs`),
which gives the arm as it stands.

Every other file went through `karac fix`. In the text arm it dropped
the `as i64` after `to_digit(10).unwrap()`, which widens by itself. The
Rust arm reaches a clean check in two rounds and gives the text the arm
holds: first the syntax (`struct Solution;` to `struct Solution {}`,
`&mut Vec<i32>` to `mut ref Vec[i32]`, `|&&x|` to `|x|`,
`Solution::duplicate_zeros` to `Solution.duplicate_zeros`, and `&mut
digits` to `mut digits`); then the `as i64` dropped where the digits are
copied back.

## Benchmarks

The bench builds 200 random arrays of 10^4 digits, LeetCode's longest, a
third of them 0, once. Each of 100 rounds copies every array, duplicates
its zeros with the ★ arm and folds two of its places into a checksum.
Every implementation prints `100 rounds over 200 arrays of 10^4 digits:
11391 zeros sampled, checksum 713465633`. Each mirror walks the same two
passes over a copy of the array: Rust `clone()`, C a `malloc` and
`memcpy`, Go `append([]int64(nil), a...)`, Python `list(a)`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `ba29c00d5c`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.943 to 1.100 s | 1.012 s |
| C (`clang -O3`) | 1.030 to 1.198 s | 1.094 s |
| Rust (`rustc -O`) | 1.122 to 1.348 s | 1.157 s |
| Go | 1.385 to 1.706 s | 1.496 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 2.053 to 2.292 s | 2.150 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.030 to 2.570 s | 2.180 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.140 to 2.271 s | 2.219 s |
| Kāra (`karac build`) | 2.036 to 2.350 s | 2.216 s |
| Python | 34.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte (kara B-2026-11-10-1).

The work is 200 million digits each counted, moved and compared, with
an index sum `i + zeros` and a count `zeros -= 1` at every step. Kāra
ties Rust with overflow checks at the same ISA (3% behind). The checks
look like the whole gap to the rest: Rust's own time nearly doubles
with them (1.157 s to 2.150 s), plain `rustc -O` takes 52% of Kāra's
time, C 46%, and Go, which wraps silently and checks only its bounds,
67%. Python takes 15x.
