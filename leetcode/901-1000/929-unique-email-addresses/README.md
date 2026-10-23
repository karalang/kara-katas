# 929. Unique Email Addresses

Every valid email consists of a local name and a domain name, separated
by the `'@'` sign. Besides lowercase letters, the email may contain one
or more `'.'` or `'+'`.

- For example, in `"alice@leetcode.com"`, `"alice"` is the local name,
  and `"leetcode.com"` is the domain name.

If you add periods `'.'` between some characters in the local name part
of an email address, mail sent there will be forwarded to the same
address without dots in the local name. Note that this rule does not
apply to domain names.

- For example, `"alice.z@leetcode.com"` and `"alicez@leetcode.com"`
  forward to the same email address.

If you add a plus `'+'` in the local name, everything after the first
plus sign will be ignored. This allows certain emails to be filtered.
Note that this rule does not apply to domain names.

- For example, `"m.y+name@email.com"` will be forwarded to
  `"my@email.com"`.

It is possible to use both of these rules at the same time.

Given an array of strings `emails` where we send one email to each
`emails[i]`, return the number of different addresses that actually
receive mails.

```
emails = ["test.email+alex@leetcode.com","test.e.mail+bob.cathy@leetcode.com","testemail+david@lee.tcode.com"]  ->  2
emails = ["a@leetcode.com","b@leetcode.com","c@leetcode.com"]                                                    ->  3
```

**Constraints:** `1 <= emails.length <= 100`; `1 <= emails[i].length
<= 100`; `emails[i]` consists of lowercase English letters, `'+'`,
`'.'` and `'@'`; each `emails[i]` contains exactly one `'@'`; all local
and domain names are non-empty; local names do not start with a `'+'`;
domain names end with the `".com"` suffix.

## Approaches

Every arm rewrites each address to the one that receives its mail, the
local name up to its first `'+'` without its dots, then the `'@'` and
the domain as written, and counts the different rewrites.

| file | mechanism |
|---|---|
| `num_unique_emails.kara` ★ | one walk over each address's bytes, dropping dots and a tag in the local name and keeping everything from the `'@'` on; the rewrites go into a `Set[String]`, whose size is the answer. O(total length) |
| `num_unique_emails_split.kara` | `split("@")`, the local name `split("+")` with its first piece's dots taken out by `replace`, and the parts joined again; the rewrites sorted, and each one that differs from the one before counted. O(L log n) for total length L |
| `num_unique_emails_states.kara` | a three-state machine (local name, tag, domain) keeping the bytes each state allows as a `Vec[u8]`; then each rewrite equal to no earlier one counted, comparing pairwise. O(n * L) |
| `num_unique_emails_find.kara` | the `'@'` found, and the first `'+'` before it, then the local name copied without its dots and the domain after it; each rewrite counted in a `Map[String, i64]`, whose number of keys is the answer. O(total length) |
| `num_unique_emails_backward.kara` | each address read from its last byte: the domain up to the `'@'`, then the local name collected backwards without its dots, every `'+'` throwing away what was collected since the `'@'`; the bytes reversed into a `SortedSet[String]`. O(L log n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's two examples and six
more (one address, one address written four ways, dots in the domain
kept, a `'+'` in the domain kept, a tag of dots and `'+'`s, and dots
around a single letter); for 300 random lists of 1 to 100 addresses the
answers' sum and a checksum; and two of LeetCode's largest, 100
addresses of 100 characters, all different and all one address.
`num_unique_emails.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally, with nothing rewritten: two addresses receive the same mail
when their domain names are the same and their local names name the
same box, which two pointers decide by comparing the letters before any
`'+'` and passing over the dots; the answer counts the addresses that
receive mail no earlier one does. It checks 3,200 random lists, each
address a local name of 1 to 3 letters from `ab` with dots among them,
a tag after a `'+'` on half of them, and one of six domains: 3,000 lists
of 1 to 6 addresses against the statement, and 200 of 1 to 100 against
the other properties; 20,450 addresses in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small lists |
| P2 | at least the number of different domains, and at most the number of addresses |
| P3 | the same answer for the list shuffled |
| P4 | the same answer with a `'.'` put somewhere in each local name |
| P5 | the same answer with every address added again, with a tag at the end of its local name |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 lists, 20450 addresses, answers summing to 16683, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (10 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

The six domains are `b.com`, `ab.com`, `xy.com`, `x.y.com`, `x+y.com`
and `x+b.com`. A first draft drew from five domains that no rewrite
could confuse (`x.com`, `y.com`, `x.y.com`, `xy.com`, `x+y.com`), and
five of the mutants below survived it: dropping the `'@'` (four arms)
and starting a tag at a `'+'` in the domain, since with local names
from `ab` and domains starting with `x` or `y` no two addresses could
then collide. The present six give each of those a collision to find
(`aa@b.com` and `a@ab.com` without the `'@'`; `x+y.com` and `x+b.com`
both cut to `x`).

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: dots dropped in the domain too | P1 64, P2 12, P6 226 |
| M2 | ★: the `'@'` not kept | P1 39, P2 10, P6 178 |
| M3 | ★: a `'+'` in the domain dropped | P1 77, P2 15, P6 243 |
| M4 | split: the local name after the last `'+'` | P1 388, P5 3200, P6 554 |
| M5 | split: each address compared with the first, not the one before | P1 175, P5 2677, P6 353 |
| M6 | split: never sorted | P1 149, P3 234, P5 2677, P6 327 |
| M7 | states: an `'@'` after a tag not ending it | P1 387, P2 73, P5 2519, P6 557 |
| M8 | states: a `'+'` in the domain starting a tag | P1 105, P2 19, P6 262 |
| M9 | states: the first address never matched | P1 123, P3 186, P5 2986, P6 214 |
| M10 | find: the `'+'` searched for past the `'@'` | P1 125, P5 2680, P6 297 |
| M11 | find: a dot at the start kept | P1 128, P4 238, P6 297 |
| M12 | find: the local name's last byte dropped | P1 280, P4 312, P5 2680, P6 442 |
| M13 | backward: a `'+'` dropping only itself | P1 130, P5 3200, P6 293 |
| M14 | backward: dots kept in the local name | P1 161, P4 238, P6 335 |
| M15 | backward: the first byte never read | P1 307, P4 382, P6 471 |

P1 and P6 kill all fifteen, P5 eight, P2 five, P4 four and P3 two. P2
sees the mutants that merge addresses across domains (M1, M2, M3 and
M8) and M7, which loses the domain of every tagged address, since each
can then count fewer addresses than there are domains. P3 sees only the
two whose count depends on the list's order (M6 and M9). P4 sees the
mutants that let a dot in the local name matter, directly (M11 and M14)
or by moving which byte is dropped (M12 and M15). P5's tagged copies
catch every mutant that mishandles a `'+'` (M4, M7, M10 and M13), M12,
whose copies keep the byte the originals lose, and the three whose
count depends on the list's makeup (M5, M6 and M9).

Nine other edits were tried and set aside, each failing exactly the same
checks as a kept mutant: split, states and backward dropping dots in
the domain, as M1; split, find and backward losing the `'@'`, as M2;
★ letting a `'+'` drop only itself, as M13; ★ keeping dots in the local
name, as M14; and find dropping the first byte, as M15.

## Verification

Every arm prints the same output as `num_unique_emails.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.5 to 0.7 s each and the
differential 10 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The ★, states, find and backward arms print the same output under the
frozen legacy interpreter, the legacy JIT and both legacy builds, with
and without auto-par. Legacy refuses the split arm and the differential
at `split(...).collect()` ("no method 'collect' on type 'Vec'"), since
its `split` returns a `Vec` where v2's returns an iterator, and the
bench program, which passes `lists[(r + i) % count]` straight to the
function: "cannot move ... out of an index", legacy's owned parameters,
where v2's parameter borrows it. Legacy is frozen, so none of this is
filed.

## Benchmarks

The bench program builds 100 lists of 100 addresses once, each a local
name of 2 to 7 letters from `ab` with a dot before about one letter in
four, a tag of up to 9 letters after a `'+'` on half of them, and one of
eight domains, and in each of 300 rounds runs the ★ arm on every list,
each round starting from a different list. Every implementation prints
`300 rounds over 100 lists of 100 addresses: answers summing to
2780100, checksum 372084198`.

The C program has no set to use, so it keeps the rewrites in one buffer
and an open-addressing table of 256 slots keyed by FNV-1a; Rust uses a
`HashSet<String>`, Go a `map[string]struct{}` and Python a `set`, each
building a string per address as the Kāra program does.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.25 to 0.28 s | 0.26 s |
| Rust (`rustc -O`) | 0.62 to 0.75 s | 0.65 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.75 s | 0.67 s |
| Go | 0.55 to 0.87 s | 0.60 s |
| Python | 4.1 s | |
| Kāra (`karac build --mir`) | 0.74 to 0.80 s | 0.77 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 16 times C's.

v2 takes 1.17 times Rust's median time under overflow checks and 2.97
times C's. Under valgrind's cachegrind v2 runs 6.16 billion
instructions and 1.10 billion branches, mispredicting 65.5 million;
Rust with overflow checks 4.83 billion, 0.75 billion and 49.9 million;
and C 1.40 billion, 0.23 billion and 21.2 million. C's gap is its
design, no allocation per address and a cheaper hash; that the rest of
v2's gap to Rust is its own SipHash-1-3 and the per-address `String`
built through `from_utf8` is inferred, not profiled.
