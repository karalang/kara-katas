# 1108. Defanging an IP Address

Given a valid (IPv4) IP `address`, return a defanged version of that IP
address.

A defanged IP address replaces every period `"."` with `"[.]"`.

```
address = "1.1.1.1"        ->  "1[.]1[.]1[.]1"
address = "255.100.50.0"   ->  "255[.]100[.]50[.]0"
```

**Constraints:** the given `address` is a valid IPv4 address.

The arms are `fn defang_ip_addr(address: String) -> String`. A valid
address is four numbers from 0 to 255 with no leading zero, so it has
three periods and at most 15 characters, and its answer six more.

## Approaches

| file | mechanism |
|---|---|
| `defang_ip_addr.kara` ★ | one pass over the characters: each period written as `[.]` with `push_str`, every other character as itself with `push`, into a `String.with_capacity` of the answer's length. O(n) |
| `defang_ip_addr_replace.kara` | the library's `replace`: every `.` replaced by `[.]` in one call, as most of LeetCode's solutions in every language write it |
| `defang_ip_addr_split.kara` | split and joined: the four numbers cut out at the periods into a `Vec[Str]` with `from_iter`, and joined again with `[.]` between them |
| `defang_ip_addr_bytes.kara` | over the bytes: the address is ASCII, so its bytes are copied into a `Vec[u8]`, a period as the three bytes of `b"[.]"` with `extend_from_slice`, and the vector turned back into a `String` with `String.from_utf8`, checked as UTF-8 |
| `defang_ip_addr_flat_map.kara` | an iterator: each character mapped to the characters it becomes, an array of three for a period and of one for any other, flattened with `flat_map` and collected into a `String` |
| `defang_ip_addr_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `defang_i_paddr`, a `match` on each character with `res += "[.]"`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's two
examples and seven more (all zeros, all 255, and five ordinary
addresses), then over 2000 random addresses the characters of the
answers and a checksum of every one of them (`2000 random addresses:
32586 characters, checksum 471278978`). `defang_ip_addr.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every period replaced by `[.]`, one at a time from the last,
the text before and after it kept as it is. It checks 2000 problems in
four kinds of 500: numbers of one, two or three digits at random; every
number one digit; every number three digits; and numbers from the
edges, 0, 1, 9, 10, 99, 100, 199, 200, 254 and 255. Every random choice
is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | read back, every `[.]` as one period, the answer is the address, it has no other bracket or period, and it is six characters longer |
| P3 | the address in pieces, each number and each period defanged alone, gives the same answer piece by piece |
| P4 | the numbers in the other order give the same characters, as many of each |
| P5 | every digit written twice, before or after defanging, gives the same |
| P6 | the digits 1 to 9 moved by a permutation, before or after defanging, give the same |

All 72,000 checks pass on every arm: `2000 problems: checksum
568967330, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, by `str.replace`, gives the same checksum.

P1 builds the answer and P2 reads it back; P3 to P6 compare the arm
only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a zero never written | P1 1128, P2 1128 |
| M2 | ★: a period late in the address kept bare | P1 2000, P2 2000, P3 2000, P4 429, P5 530 |
| M3 | ★: the first character dropped | P1 2000, P2 2000, P3 2000, P4 1468, P5 2000 |
| M4 | replace: only the first period | P1 2000, P2 2000, P3 2000 |
| M5 | replace: the last character cut | stops: string slice out of range |
| M6 | replace: a zero after a period dropped | P1 325, P2 325, P3 325, P4 215, P5 325 |
| M7 | split: the first number dropped | P1 2000, P2 2000, P3 2000, P4 1878 |
| M8 | split: the numbers that are 0 dropped | P1 416, P2 416, P3 416, P5 416 |
| M9 | bytes: a zero defanged in place of the period | P1 2000, P2 2000, P5 1128 |
| M10 | bytes: each digit one higher | P1 2000, P2 2000, P5 985, P6 1999 |
| M11 | flat_map: the characters reversed | P1 1993, P2 1993, P3 1988 |
| M12 | flat_map: the test turned round | P1 2000, P2 2000, P5 2000 |
| M13 | solution: the period never defanged | P1 2000, P2 2000 |
| M14 | solution: a 1 taken for a period | P1 1481, P2 1481, P5 1481, P6 1525 |
| M15 | solution: the first two characters dropped | P1 2000, P2 2000, P3 2000, P4 1832, P5 2000 |

Of the fourteen that run to the end, P1 and P2 catch all fourteen, P5
nine, P3 eight, P4 five and P6 two. P1 and P2 fail on the same problems
every time: an answer that reads back as the address, with nothing but
`[.]` added, is the literal one. P3, P5 and P6 compare the arm with
itself on pieces of the address, on its digits doubled and on its
digits moved, so they see the edits that depend on where a character
is or what it is next to: the start of the address (M3, M15), a period
late in it (M2), the first period only (M4), a zero after a period
(M6). P6 sees only the two edits that change a digit by its value (M10,
M14): moving the digits first moves what the edit does. P4,
which only counts characters, sees the edits that lose or move
characters by place. P3 to P6 miss M1 and M13: an arm that writes every
period or every zero wrongly in the same way agrees with itself however
the address is cut, ordered, doubled or renumbered. M5 stops on P3's first piece: one number alone is shorter
than the five characters the edit cuts to.

Of the fifteen not kept, fourteen fail as a kept edit: thirteen that
write every period, every bracket or every digit wrongly in the same
way (the `]` never written in the ★ and bytes arms, a comma for the
period, two periods sought, the period dropped from its brackets in the
replace and flat_map arms, bare periods or a space in the split arm's
join, the period kept after its brackets, every digit twice or dropped,
the brackets the wrong way round, and each period defanged twice) as
M13, and the split arm taking only three numbers as M7. The bytes arm
dropping its last byte fails in a way of its own but was not needed.

## Verification

Every arm prints the same output as `defang_ip_addr.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found two gaps, each filed in the kara ledger and fixed. The ★
arm was written as Kāra, and the other five as Rust writes them; `karac
fix` carried every Rust spelling to a clean check:

- The replace arm needed nothing: Rust's `address.replace(".", "[.]")`
  is Kāra too.
- The split arm in two rounds: `split('.')` to `split(".")`, and
  `.collect::<Vec<&str>>().join("[.]")` to `Vec[Str].from_iter(..)
  .join("[.]")`. The last was advice alone: a turbofish on a `collect`
  whose result is the receiver of a further call cannot move its type
  to a `let` without reordering the chain, and the collection's own
  `from_iter`, which names the type at the call, did not lower when that
  was decided. It does now, so the fix writes it, with Rust's `&str`,
  `HashSet` and `BTreeMap` spelled `Str`, `Set` and `SortedMap`
  (B-2026-11-10-42, fixed). Its `collect::<String>()` form gives
  `String.from_iter(it)`, which checked and then stopped in the MIR
  builder with "a call with no resolved callee"; it now reaches the
  library's `impl FromIterator[char] for String` (B-2026-11-10-43,
  fixed).
- The bytes arm in two: `Vec<u8>` to `Vec[u8]`, `Vec::with_capacity`
  and `String::from_utf8` to `Vec.with_capacity` and `String.from_utf8`,
  and `for &b in address.as_bytes()` to `for b in address.bytes()`.
- The flat_map arm in one: `vec!['[', '.', ']']` and `vec![c]` to array
  literals, with `.into_iter()` written after the `if`.
- The Rust solution in two: `struct Solution {}` declared, `String::new()`
  to `String.new()` and `Solution::defang_i_paddr` to
  `Solution.defang_i_paddr`.

## Benchmarks

The bench builds 1024 random addresses once. Each of 10000 rounds
replaces one address with a new one, written with an f-string, and
defangs every address with the ★ arm: 10.24 million calls, each
answer a new string. Every implementation prints `10000 rounds over
1024 addresses: 10240000 calls, 197601373 characters, checksum
516858752`, the checksum over every 64th answer. C `malloc`s each
answer and frees it after use, as each is its own string in the other
languages; Go writes it with a `strings.Builder` grown to the length.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.261 to 0.298 s | 0.264 s |
| C (`clang -O3`) | 0.262 to 0.344 s | 0.283 s |
| Rust (`rustc -O`) | 0.430 to 0.513 s | 0.447 s |
| Kāra (`karac build`) | 0.436 to 0.540 s | 0.452 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.427 to 0.553 s | 0.460 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.433 to 0.560 s | 0.469 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.438 to 0.519 s | 0.469 s |
| Go | 0.958 to 1.152 s | 1.022 s |
| Python | 8.100 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra ties Rust at about 1.7x C's time; each call returns a fresh
string in every language, and C writes its answer with a hand loop into
one `malloc`. Go takes about 2.2x Kāra's time and Python about 17x.
