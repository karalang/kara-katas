# 1177. Can Make Palindrome from Substring

You are given a string `s` and array `queries` where `queries[i] = [left_i,
right_i, k_i]`. We may rearrange the substring `s[left_i...right_i]` for
each query and then choose up to `k_i` of them to replace with any
lowercase English letter.

If the substring is possible to be a palindrome string after the
operations above, the result of the query is `true`. Otherwise, the result
is `false`.

Return a boolean array `answer` where `answer[i]` is the result of the
`i`-th query `queries[i]`.

Note that each letter is counted individually for replacement, so if, for
example `s[left_i...right_i] = "aaa"`, and `k_i = 2`, we can only replace
two of the letters. Also, note that no query modifies the initial string
`s`.

```
s = "abcda", queries = [[3,3,0],[1,2,0],[0,3,1],[0,3,2],[0,4,1]]
    ->  [true,false,false,true,true]
s = "lyb", queries = [[0,1,0],[2,2,1]]  ->  [false,true]
```

**Constraints:** `1 <= s.length, queries.length <= 10^5`,
`0 <= left_i <= right_i < s.length`, `0 <= k_i <= s.length`, `s` consists
of lowercase English letters.

The arms are `fn can_make_pali_queries(s: Str, queries: Vec[Vec[i64]]) ->
Vec[bool]`. The two Rust arms keep the method LeetCode gives Rust users,
over `String` and `Vec[Vec[i32]]`, inside `impl Solution`, and a one-line
`can_make_pali_queries` calls it.

## Approaches

A substring can be rearranged into a palindrome when at most one of its
letters has an odd count. Each replacement turns one odd letter into
another and pairs the two, so a query holds when the odd letters, halved,
are at most `k`. The arms differ in how they count the odd letters.

| file | mechanism |
|---|---|
| `can_make_palindrome.kara` ★ | one bit per letter, the parity masks of every prefix, and each query's odd letters the `count_ones()` of two masks XORed. O(n + q) |
| `can_make_palindrome_counts.kara` | prefix counts in a `Vec[Array[i64, 26]]`, each row copied from the one before, and each query's 26 letters counted by subtraction. O(26 * (n + q)) |
| `can_make_palindrome_direct.kara` | the statement as written: each substring's letters counted afresh into an `Array` of 26 and the odd counts found with `filter(..).count()`. O(q * (n + 26)) |
| `can_make_palindrome_kernighan.kara` | the ★ arm's masks in a `Vec.filled`, each query's set bits counted by hand with `m &= m - 1`, stopping once past `2 * k + 1`. O(n + q) |
| `can_make_palindrome_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `vec![0u32; s.len() + 1]` of parity masks, `as usize` indices and `k` as `u32` against `count_ones()`), carried to Kāra by `karac fix` |
| `can_make_palindrome_prefix.kara` | another Rust solution (prefix counts in a `vec![[0; 26]; n + 1]` over `s.as_bytes()`, `(0..26).filter(\|&j\| ..).count()` against `k as usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five properties |

Every arm prints the same 6 lines: LeetCode's two examples; one letter, a
palindrome as it stands and two letters differing; all 26 letters once,
which need 13 replacements, not 12; 300 random strings of 1 to 40 letters
over the first 1 to 26, 20 queries each (`300 random strings: 4981 of 6000
true, checksum 789008839`); and 100000 letters and 100000 queries, the
constraints' most, 99900 of them over at most 64 letters and 100 over any
range (`100000 letters, 100000 queries: 64008 true, checksum 663494522`).
The direct arm, which counts every substring afresh, would take minutes
under `karac run` on 100000 queries over any range, so the large case's
queries are mostly short. `can_make_palindrome.py` mirrors the ★ arm and
its output is byte-identical; with `lit` it counts each substring
afresh, and its output is the same. Every arm gives the same output under
`karac run` and `karac build`.

The Mend loop: the four Kāra arms take no fixes. The Rust arms take one
round each, 16 fixes and 24. Both: `struct Solution;` to `struct Solution
{}`; `Vec<..>` to `Vec[..]`; `Solution::` to `Solution.`; `&str` to `Str`;
`|&x|` to `|x|`. The mask arm's: `vec![0u32; s.len() + 1]` to
`Vec.filled(s.len() + 1, 0u32)` and `s.bytes()` to `s.bytes().iter()`; its
`as usize` indices and `k as u32` stay. The count arm's: `s.as_bytes()` to
`s.bytes()`, `vec![[0; 26]; n + 1]` to `Vec.filled(n + 1, [0; 26])`, the
`as usize` on the letter's index dropped, `Vec::with_capacity` to
`Vec.with_capacity`, `for q in &queries` to `for q in ref queries`, the
three `as usize` to `as i64`, and `|&j|` to `|j|`. Both arms' outputs
match on the first run.

One compiler gap came up on the way, fixed in kara `a3ae3b2036`:

- The mask arm was refused with no fix (kara B-2026-11-16-212). Its test is
  `(prefix[r + 1] ^ prefix[l]).count_ones() / 2 <= k` with `k` a `u32`. A
  bit count is `i64` in Kāra, so the comparison was `i64 <= u32`, refused
  as mixing signed and unsigned. design.md § Mixed-width operands widens
  the narrower operand of a comparison as of an arithmetic operator when
  that loses nothing, and `u32` widens to `i64`; `i64 * u32` was already
  accepted, but every signed and unsigned pair in a comparison was
  refused. Now a pair where one side holds every value of the other
  compares at the wider type, and only a pair neither side holds (`u32`
  with `i32`, `u64` with `i64`) is refused.

The differential takes no fixes.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each substring's letters sorted and paired off, equal beside
equal; a palindrome takes every pair, one either side, and at most one
letter left over in the middle, and each replacement turns one leftover
into a copy of another, so the leftovers, halved, are the replacements
needed. 400 random strings of 1 to 30 letters over the first 1 to 26, 20
queries each with `k` up to 7.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | one more replacement keeps every query that held, and half the substring's length always suffices |
| P3 | the string reversed, each query over the same letters read from the other end, gives the same answers |
| P4 | the letters renamed by a random permutation of the alphabet give the same answers |
| P5 | the ★ arm's answer |

All 14,400 checks pass on every arm: `400 strings: checksum 751824547,
14400 checks over 6 arms: 0 failures`, in 4.0 s under `karac __mir-run`,
and the same under `karac __mir-llvm-run` and `karac build`.

## Mutation testing

Eighteen edits to the differential, three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All eighteen are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: each substring's last letter dropped | P1 267, P3 165, P5 1335 |
| A2 | ★: one replacement too few allowed | P1 373, P2 394, P5 1865 |
| A3 | ★: no odd letter allowed in the middle | P1 290, P2 378, P5 1450 |
| C1 | counts: even letters counted as odd | P1 400, P2 400, P5 400 |
| C2 | counts: each substring's last letter dropped | P1 267, P3 165, P5 267 |
| C3 | counts: z never counted | P1 1, P4 46, P5 1 |
| D1 | direct: each substring's last letter dropped | P1 267, P3 165, P5 267 |
| D2 | direct: one replacement for each odd letter | P1 389, P2 395, P5 389 |
| D3 | direct: a letter seen once not counted odd | P1 338, P5 338 |
| K1 | kernighan: the count stopped one bit early | P1 346, P5 346 |
| K2 | kernighan: the mask's length counted, not its bits | P1 365, P2 375, P4 382, P5 365 |
| K3 | kernighan: a letter seen twice left odd | P1 243, P3 258, P5 243 |
| X1 | mask: each substring's first letter dropped | P1 274, P3 165, P5 274 |
| X2 | mask: one replacement too many allowed | P1 328, P5 328 |
| X3 | mask: each mask holds one letter | P1 336, P2 258, P3 230, P5 336 |
| R1 | prefix: each row holds one letter | P1 346, P5 346 |
| R2 | prefix: one replacement too few allowed | P1 373, P2 394, P5 373 |
| R3 | prefix: a never counted | P1 106, P4 117, P5 106 |

A mutation of the ★ arm fails P5 on every arm, since P5 compares each arm
with the ★ arm; P1, P2 and P3 name the ★ arm itself. C3 is caught mostly
by P4: the random strings rarely reach z, and a renaming moves another
letter onto it. Three more edits look like faults and pass all 14,400
checks under both backends, since they are equivalent: the ★ arm's
letters one bit up (z's bit 26 still fits), the prefix arm testing `% 2
!= 0` for `% 2 == 1` (no count is negative), and the Kernighan count
stopping at `2 * k + 5` rather than `2 * k + 1` (the stop only saves
work).

## Benchmarks

`bench/` times the ★ arm against the same parity masks in C, Rust, Go and
Python: one string of 100000 letters and 100000 queries over any range
with `k` up to 13, the constraints' most, built once (each query its own
three-value vector, as LeetCode passes them), then 200 calls, each call's
answers folded into a checksum. Every program prints `200 calls: checksum
193628815`.

Timings on a 4-core container (Intel Xeon, 2.3 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `a3ae3b2036`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.164 to 0.179 s | 0.172 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.155 to 0.184 s | 0.167 s |
| Rust (`rustc -O`) | 0.151 to 0.192 s | 0.168 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.183 to 0.204 s | 0.191 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.173 to 0.196 s | 0.185 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.128 to 0.153 s | 0.145 s |
| C (`clang -O3`) | 0.139 to 0.162 s | 0.151 s |
| Go | 0.422 to 0.520 s | 0.469 s |
| Python | 6.15 to 6.24 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 4% of wall time for both Kāra
rows, so both ran on one core. Kāra takes about 0.90x the time of
overflow-checked Rust built for the same baseline, the equal-safety
comparison, 1.15x C's and 0.36x Go's; Python takes about 37x. Each call
builds 100001 masks by `push` and answers 100000 queries scattered over
them, so the time is mostly memory traffic: the masks' growth and the
queries' separate allocations. Go grows its mask slice by `append` and
reads each query through a slice header, and is the slowest compiled
program by 2.5x; why was not profiled, and neither was Kāra's lead over
checked Rust.
