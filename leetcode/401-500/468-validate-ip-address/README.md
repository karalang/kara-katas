# 468. Validate IP Address

Given a string `queryIP`, return `"IPv4"` if it is a valid IPv4
address, `"IPv6"` if it is a valid IPv6 address, or `"Neither"` if it
is not a valid IP address of any type.

A valid IPv4 address is an IP in the form `"x1.x2.x3.x4"` where
`0 <= xi <= 255` and `xi` cannot contain leading zeros. For example,
`"192.168.1.1"` and `"192.168.1.0"` are valid IPv4 addresses, while
`"192.168.01.1"`, `"192.168.1.00"` and `"192.168@1.1"` are invalid.

A valid IPv6 address is an IP in the form
`"x1:x2:x3:x4:x5:x6:x7:x8"` where `1 <= xi.length <= 4` and `xi` is a
hexadecimal string, which may contain digits, lowercase English
letters (`'a'` to `'f'`) and uppercase English letters (`'A'` to
`'F'`). Leading zeros are allowed in `xi`. For example,
`"2001:0db8:85a3:0000:0000:8a2e:0370:7334"` and
`"2001:db8:85a3:0:0:8A2E:0370:7334"` are valid IPv6 addresses, while
`"2001:0db8:85a3::8A2E:037j:7334"` and
`"02001:0db8:85a3:0000:0000:8a2e:0370:7334"` are invalid.

```
queryIP = "172.16.254.1"                       ->  "IPv4"
queryIP = "2001:0db8:85a3:0:0:8A2E:0370:7334"  ->  "IPv6"
queryIP = "256.256.256.256"                    ->  "Neither"
```

**Constraints:** `queryIP` consists only of English letters, digits
and the characters `'.'` and `':'`.

## Approaches

Every arm is `fn valid_ip_address(query_ip: String) -> String`, and
borrows the query.

| file | mechanism |
|---|---|
| `validate_ip.kara` ★ | a `'.'` makes it a candidate IPv4 and a `':'` a candidate IPv6; split on that separator and check every part: 4 parts of 1 to 3 decimal digits, at most 255 and without a leading zero, or 8 groups of 1 to 4 hex digits. O(n) |
| `validate_ip_scan.kara` | one pass, a character at a time: the first separator decides the kind, a different one later means neither, and each part is checked at the separator after it from its length, its first digit, whether it held a non-decimal hex digit, and its decimal value. O(n) |
| `validate_ip_parse.kara` | a parser for each grammar over the characters, with a cursor: 4 `dec`s of 1 to 3 digits or 8 `hex`es of 1 to 4 digits, a separator between each two, and the end of the input right after the last. O(n) |
| `validate_ip_canon.kara` | rewrite into a canonical form: IPv4 reads the four numbers and writes them back out, and is valid when that gives the query unchanged (which rules out leading zeros, empty parts and stray characters at once); IPv6 pads every group of 1 to 4 characters to 4 with zeros and lowers its case, and is valid when that gives exactly 39 characters with a `':'` at every fifth and a hex digit in each other place. O(n) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 22 lines: the three LeetCode examples,
eighteen edge cases (`0.0.0.0` and `255.255.255.255`, leading zeros,
three and eight parts, a separator at either end or doubled, a letter
in IPv4, a port after an IPv4 address, short and mixed-case IPv6
groups, an empty group, a group of 5 digits, a trailing `':'`, a `G`,
one letter), and for 300 random queries how many of each answer and a
checksum of the answers in order. The random queries are two fifths
IPv4-like and two fifths IPv6-like, half of each with one fault (a part
too many or too few, a leading zero, a number above 255, a group of 5
digits, an empty part or a letter out of place), and a fifth jumbles of
the characters an address uses. `validate_ip.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | an address built with a known answer gets it: four numbers up to 255 (a quarter of them at a boundary such as 0, 9, 10, 99, 100, 249, 250 or 255) or eight groups of 1 to 4 hex digits are valid, and one fault (a part too many or too few, a leading zero, a number from 256 up, a group of 5 digits, an empty group, a letter out of place, or one separator of the other kind) makes it neither |
| P2 | swapping the case of every letter keeps the answer, on those addresses and on jumbles of up to 40 characters |
| P3 | a valid address with one character replaced by a letter outside its alphabet is neither |
| P4 | a zero put in front of one part makes an IPv4 address neither, and keeps an IPv6 address valid exactly when that group had fewer than 4 digits |
| P5 | a valid address with one separator removed, doubled or replaced by the other kind is neither |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a part of two digits may start with 0 | P1 6, P4 58 |
| M2 | ★: a group may have 5 digits | P1 87, P4 178 |
| M3 | scan: the two separators may be mixed | P1 119, P5 367 |
| M4 | scan: 256 is taken as a part | P1 12 |
| M5 | parse: anything may follow the eighth group | P1 48, P3 36, P4 21 |
| M6 | parse: a group may have 5 digits | P1 87, P4 178 |
| M7 | canon: the numbers are not written back | P1 24, P4 284 |
| M8 | canon: `g` counts as a hex digit | P1 17, P3 189 |

The first version of the differential let M3 and M4 survive. Nothing in
it put a separator of one kind into an address of the other, and only
1 in 744 of its numbers above 255 was 256. P1 now draws a quarter of
its IPv4 numbers from the boundaries and half of its numbers above 255
from 256 to 259, and gains the other-kind separator as a fault; P5
gains it as an edit. Both mutants are killed now, M4 by the 12 P1
checks whose number came out at 256.

M2 and M6 make the same mistake in two arms and fail the same checks.
P2 sees none of the eight: it compares an arm with itself, and none of
the mutants treats the two cases differently.

## Verification

All four arms print the same output as `validate_ip.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`.
The differential prints `30000 checks, 0 failures` on both. The four
arms and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

`karac check` passes the differential and refuses the four arms, on
the harness's `show(query_ip: Str)`: it treats a `Str` as move-only, so
`String.from(query_ip)` followed by a second use of `query_ip` reads as
a use after a move (B-2026-10-12-14, below). The MIR backends accept it.
The arms keep the natural form.

On the frozen legacy backends every arm and the differential match
under `karac run --interp`. LLJIT and `karac build` stop in the legacy
code generator: on the ★ arm and the differential with "no handler for
method 'len'" on a piece of the split, and on the other three arms with
a panic in `src/codegen/assoc_call.rs` (exit 101). Legacy `karac build`
rejects the bench program (see Benchmarks). Legacy is frozen, so this
is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100,000 queries once with
the harness's generator, then validates every one in each of 20 rounds.
Every implementation prints `20 rounds of 100000 queries: 400420 IPv4,
398700 IPv6, checksum 588242433`, the Kāra program under
`karac __mir-run` included (in 46 s).

The legacy `karac build` rejects the bench program (it moves
`queries[i]` out of the index, where v2 borrows it), so `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend. That edit is by hand, on top of the `scripts/new-bench.sh`
output.

The mirrors split the same way where the language has a lazy splitter:
Rust's `split` and Go's `strings.SplitSeq` yield views, and C scans for
the next separator; Python's `split` builds a list. Rust returns a
fresh `String` as the Kāra arm does; C, Go and Python return a
constant. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.22 to 0.26 s |
| Rust (`rustc -O`) | 0.48 to 0.55 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.45 to 0.60 s |
| Go | 0.69 to 0.72 s |
| Python | 3.5 to 3.7 s |
| Kāra (`karac build --mir`) | 0.98 to 1.21 s |

The `--mir` row is timed at kara `cca50041a7`. Kāra's `split` copies
every part into a new `String` in a new `Vec` (B-2026-10-12-7, below);
callgrind puts 47% of the validation's instructions there, so that is
likely most of the gap to Rust (inferred, not measured with a lazy
split). Under `karac __mir-llvm-run` the
program prints the same line in 5.7 s, compile included; that JITs the
MIR's IR without optimization passes, so it is not a benchmark.

## Compiler findings

- **B-2026-10-12-14** (`karac check`, open): `karac check` treats `Str`
  as move-only. Every arm's harness passes its `query_ip: Str` to
  `String.from` and then prints it, and check refuses the second use.
- **B-2026-10-12-7** (open): `split` returns an eager `Vec[String]` of
  copies where the library spec gives a lazy iterator of `Str` views
  (docs/library/strings.md). Besides refusing the spec's own
  `line.split(",").collect()`, it costs this kata's bench a `Vec` and a
  heap `String` per part: under `karac build --mir` callgrind puts 47%
  of the validation phase's instructions in `karac_mir_str_split` and
  the allocator calls under it.
