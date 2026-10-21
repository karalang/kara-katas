# 831. Masking Personal Information

A string `s` is either an email address or a phone number. Return it
masked.

An email is a name, `@` and a domain. The name is at least two English
letters; the domain is letters with one `.` somewhere in the middle. To
mask it, lower every letter, and replace the name's middle letters by
exactly five `*`.

A phone number holds 10 to 13 digits and any of the separators `+`, `-`,
`(`, `)` and space. Its last 10 digits are the local number and those
before them the country code. To mask it, drop the separators and write
`***-***-XXXX` with `XXXX` the last four digits, preceded by nothing for
a number with no country code and by `+*-`, `+**-` or `+***-` for a
country code of 1, 2 or 3 digits.

```
s = "LeetCode@LeetCode.com"  ->  "l*****e@leetcode.com"
s = "AB@qq.com"              ->  "a*****b@qq.com"
s = "1(234)567-890"          ->  "***-***-7890"
```

**Constraints:** `s` is a valid email or phone number; an email has 8 to
40 characters, a phone number 10 to 20.

## Approaches

An email is told from a phone number by its `@`, and each is masked by
its own rule.

| file | mechanism |
|---|---|
| `mask_pii.kara` ★ | `find` for the `@`; an email lowered whole and sliced around it, a phone number's digits gathered and its mask written with `repeat` for the country code, both in an f-string. O(n) |
| `mask_pii_scan.kara` | one scan per kind: an email read byte by byte, keeping the name's first and last letter and copying the domain, each lowered as it passes; a phone number read from its end, keeping the first four digits met and counting the rest. O(n) |
| `mask_pii_split.kara` | an email lowered and split at the `@` into name and domain; a phone number's mask built as a list of parts joined with `-`. O(n) |
| `mask_pii_iter.kara` | an email's name read at both ends through `chars` and its domain the rest by `skip`; a phone number's digits a `filter` over `chars`, `collect`ed, and the country code's mask a `map` over a range. O(n) |
| `differential.kara` | the four arms against the statement read character by character, four properties |

Every arm prints the same 10 lines: LeetCode's three examples; six more
(a name of two letters, a capitalised one, ten digits and no separators,
and phone numbers with country codes of 1, 2 and 3 digits); and 400
random strings, emails and phone numbers in turn, with their total
length and a checksum. `mask_pii.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, one character at a time: for an email, the name's first and
last letter lowered around five `*`, then `@` and the domain lowered;
for a phone number, one `*` per digit of the country code between a `+`
and a `-`, then `***-***-` and the last four digits. Its 1,600 cases
come in four kinds of 400: emails with names of two or three letters,
where the name's two ends meet or nearly; emails with names of up to 12;
phone numbers with a separator before about one digit in five; and phone
numbers with one before every digit.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | an email with every letter's case drawn afresh, or a phone number with its separators drawn afresh, gives the same mask |
| P3 | an email with the name's middle letters drawn afresh, or a phone number with every digit but the last four drawn afresh, gives the same mask |
| P4 | the mask's length: the domain's plus 8 for an email, 12 for a local phone number and 2 more plus one per country digit otherwise |

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the name's last letter dropped | P1 800, P4 800 |
| M2 | ★: nothing lowered | P1 797, P2 748 |
| M3 | ★: one `*` too many in the country code | P1 628, P4 628 |
| M4 | scan: the first letter not held, so the last one shown twice | P1 763 |
| M5 | scan: `Z` not lowered | P1 150, P2 83 |
| M6 | scan: ten digits given a country code | P1 172, P4 172 |
| M7 | split: the name's second-last letter shown | P1 775, P3 540 |
| M8 | split: the four digits one place early | P1 800, P3 729 |
| M9 | split: eleven digits given no country code | P1 175, P4 175 |
| M10 | iter: the name's second-last letter shown | P1 775, P3 540 |
| M11 | iter: every character but a space kept as a digit | P1 748, P2 794, P4 748 |
| M12 | iter: the `@` dropped from the domain | P1 800, P4 800 |

P1 kills all twelve, and each edit is seen by at most two other
properties, which split along the rules: P2 sees the edits to lowering
and to separators (M2, M5, M11), P3 those that show a character the mask
should hide (M7, M8, M10), and P4 those that get the mask's length
wrong. M4 shows a letter the mask may show, in the wrong place, so only
P1 sees it. M5 fails P1 on only 150 cases, those where a capital `Z`
reaches the mask. M7 and M10 are the same mistake in two arms and fail
the same cases.

## Verification

Every arm prints the same output as `mask_pii.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check`, `__mir-run` and the mutation runs is at kara
`eafbee2147`; the debug build that runs `__mir-llvm-run`,
`__mir-llvm-asan` and `build --mir` is at `90714715b1`, 13 commits
earlier, none of them in the runtime; the runtime archives match both.
Under `karac __mir-run` each arm takes about 0.2 s and the differential
1.2 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends disagree with one another here. The legacy
interpreter (`karac run --interp`) prints the right output for the ★,
scanning and iterator arms, and the legacy JIT (`karac run`), `karac
build` and an auto-par build for the scanning arm only: the ★ and
iterator arms abort in all three with `free(): double free detected`.
Legacy refuses the split-and-join arm and the differential that copies
it on every backend, since its `split` returns a `Vec` and wants
`.iter()` before `map`, where v2's returns an iterator, as design.md §
Strings specifies. Its checker refuses the bench program, which passes
`strings[round % count]` to a bare parameter and so, under legacy's
rules, moves it out of an index. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
strings once, emails and phone numbers in turn: an email with a name of
2 to 20 letters and two domain parts of 1 to 8, within LeetCode's 40
characters, and a phone number of 10 to 13 digits with a separator
before about one in three. Each of 12,000,000 rounds masks the next
string into a fresh string. Every implementation prints `12000000 rounds
of 64 strings: 192750000 characters, checksum 565076245`, the Kāra
program under `karac __mir-run` included, in 282 s with the
interpreter's step limit raised by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, eight runs of each compiled
program and 13 of v2's, five of them interleaved, and three of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.48 to 0.56 s |
| Rust (`rustc -O`) | 1.63 to 2.13 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.75 to 2.11 s |
| Go | 2.21 to 2.50 s |
| Python | 12.2 to 13.6 s |
| Kāra (`karac build --mir`) | 1.72 to 2.29 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.89 s, against Rust's
1.94 (1.92 under overflow checks), C's 0.55 and Go's 2.41: level with
Rust, and 3.4 times C's time. The C program lowers and copies bytes into
buffers it sizes itself, where Rust's `format!` and `to_lowercase`, Go's
string concatenation and `strings.ToLower`, and Kāra's f-strings and
`to_lowercase` go through general string machinery. Under valgrind's
cachegrind C runs 5.8 billion instructions, Rust 18.6 billion and v2
22.7 billion; Rust also mispredicts 53 million indirect branches, most
likely in `format!`'s dispatch through its formatting traits (not
traced). Built for `x86-64-v3`, the target `karac build` uses, C takes
0.52 to 0.56 s and Rust with overflow checks 1.65 to 1.81 s, against
v2's 1.72 to 2.15 s in the same five interleaved runs. Python takes 12.6
s, about 23 times C's time and 6.7 times v2's. The comparison with C and
Rust waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written. Two spellings follow the checker rather
than first habits, and neither is a gap: `String` has no `insert`, which
design.md does not list, so the scanning arm collects the last four
digits in a `Vec[u8]`; and `split` yields `Str` views, as design.md §
Strings specifies, so collecting them into a `Vec[String]` takes a `map`
to `to_string` first. The checker's message for the second names the
item type `StringSlice` where design.md calls it `Str`.
