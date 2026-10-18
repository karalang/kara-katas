# 721. Accounts Merge

Given a list of `accounts` where each element `accounts[i]` is a list of
strings, the first element `accounts[i][0]` a name and the rest emails
of the account: two accounts belong to the same person if they have some
email in common, and all accounts of one person have the same name,
though people with the same name may be different people. Merge the
accounts and return each person as their name followed by their emails
in sorted order. The accounts can be returned in any order.

```
[["John", "johnsmith@mail.com", "john_newyork@mail.com"],
 ["John", "johnsmith@mail.com", "john00@mail.com"],
 ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
  ->  [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
       ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
```

**Constraints:** 1 <= `accounts.length` <= 1000; 2 <=
`accounts[i].length` <= 10; 1 <= `accounts[i][j].length` <= 30; names
are English letters, emails are valid.

## Approaches

Sharing an email links two accounts, and a person is everything joined
by a chain of such links, so the people are the connected parts of a
graph, and the arms differ in how they find them.

| file | mechanism |
|---|---|
| `accounts_merge.kara` ★ | every email numbered the first time it is seen and each account's emails joined in a union-find over those numbers, with path compression; the emails gathered by their root, each group sorted under its owner's name; O(E log E), E the emails |
| `accounts_merge_dfs.kara` | each account's first email linked both ways with each of its others, and a depth-first search from every email not yet seen collecting one person's emails |
| `accounts_merge_byaccount.kara` | a union-find over the accounts instead, joining an account with the first account that listed one of its emails; each email then goes into a set under its account's root, so repeats fold |
| `accounts_merge_fold.kara` | a list of the people found so far; each account takes out every person who shares an email with it and goes back as one person with all their emails; O(n * E), with no union-find and no graph |
| `differential.kara` | the four arms against the definition, four properties |

Since the people may come back in any order, the harness prints each
person as a line of name and emails joined by spaces, and sorts the
lines. Every arm prints the same 11 lines: the two LeetCode examples;
one account of one email; an email repeated within an account and again
in a second account; a chain of three accounts listed out of order; two
accounts of one name that share nothing; two people, one listed between
the other's two accounts; a chain of 1,000 accounts, the problem's most,
listed from the far end; 1,000 random accounts of up to 3 emails over
8,000, and 1,000 of up to 9 over 400; and 300 random lists of up to
30 accounts with a checksum. `accounts_merge.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which has no union-find, graph, map or set: it starts with one person
per account, its emails without repeats, and joins any two people who
share an email until no two do. 3,000 random lists are checked, each of
1 to 8 accounts of 1 to 4 emails from a pool of 4 to 40, so shared
emails and chains are common: 1,580 lists have a merge.

| | property |
|---|---|
| P1 | the people are the definition's |
| P2 | the accounts reversed give the same people |
| P3 | each account's emails reversed give the same people |
| P4 | each account split into accounts of two neighbouring emails gives the same people |

It prints `3000 account lists (1580 with a merge), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an email joined in place of its set's root | P1 161, P2 163, P3 280 |
| M2 | ★: each person's emails reversed instead of sorted | P1 1411, P2 841, P3 1610 |
| M3 | ★: every account joined to the first email ever seen | P1 1699, P2 1677, P3 1387 |
| M4 | dfs: links made one way only | P1 475, P2 689, P3 685, P4 148 |
| M5 | dfs: an email marked only once it is searched from | P1 1726, P2 691, P3 1634, P4 983 |
| M6 | dfs: each person's emails reversed instead of sorted | P1 1415, P2 839, P3 1601, P4 686 |
| M7 | byaccount: an account joined in place of its root | P1 86, P2 162, P3 76, P4 145 |
| M8 | byaccount: every email first seen in account 0 | P1 1527, P2 1681, P4 656 |
| M9 | byaccount: each person's emails reversed instead of sorted | P1 1411, P2 841, P3 1610 |
| M10 | fold: a person taken only for sharing their first email | P1 527, P2 601, P4 580 |
| M11 | fold: a person who shares kept apart as well | P1 1580, P4 1231 |
| M12 | fold: the folded person never added back | P1 3000 |
| E1 | fold: the emails still compared after one is shared | 0 |
| E2 | ★: no path compression | 0 |
| E3 | byaccount: the earlier account joined under the later | 0 |

P1 kills all twelve. It is the only property that sees M12, which never
adds anyone back, so every list comes back empty whatever is done to it
first. M11 keeps a person who shares an email apart as well as folding
them in, and fails P1 on exactly the 1,580 lists with a merge. P2 misses
only those two. P3 misses M8 and M10 as well: M8 depends on which
account came first and M10 on a person's smallest email, and reversing
the emails inside each account changes neither. P4 misses
M1, M2, M3, M9 and M12. M2 and M9 list each person's emails in reverse
order of first sight, which splitting the accounts into neighbouring
pairs keeps, so they fail the same checks; M6 does the same to the order
of the dfs arm's search, which the split changes, so P4 sees it.
M3 joins everything to the first email ever seen, still the first after
the split. E1 keeps comparing a person's emails after one is shared,
which only costs time; E2 drops the path compression, which only saves
time later; E3 joins the earlier account under the later, and the root's
name is the same either way, since accounts joined by an email share a
name.

## Verification

Every arm prints the same output as `accounts_merge.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`a73d3c10ad`, whose last compiler change is `3c8e763161`. The runtime
archives were built after that change.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse all four arms, the differential and
the bench program at type checking: at `*root` on a key from a map's
`iter()` in the ★ and byaccount arms, the differential and the bench
program, since legacy gives those by value where v2 gives references;
and at `next_random(mut seed)` in the harness's `random_accounts` and
`root_of(mut parent, ...)` in the byaccount arm's recursion, whose
arguments are already `mut ref`s, where legacy wants the marker dropped
and design.md § Call-site `mut` markers now requires it (kara
B-2026-10-14-25). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages, each with its
own hash map and sort. C has neither, so its mirror hashes the emails
into an open-addressing table by FNV-1a and gathers the groups in lists
indexed by root, as its header says. It makes 20 lists of 1,000 random
accounts once, and in each of 50 rounds changes one account of every
list, its last email becoming the first email of the next account of the
same name, before merging every list, summing the people and the length
of each person's smallest email. Every implementation prints `50 rounds
of 20 lists of 1000 accounts: sum 6857970`, the Kāra program under
`karac __mir-run` included (in 30 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.54 to 0.70 s |
| Rust (`rustc -O`) | 1.05 to 1.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.08 to 1.35 s |
| Go | 1.00 to 1.13 s |
| Python | 1.6 to 1.9 s |
| Kāra (`karac build --mir`) | 1.16 to 1.38 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 7.4 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is about a tenth behind Rust and a fifth behind Go at
the medians of the interleaved runs (1.27 s against 1.16 and 1.05), and
about twice C's 0.58, whose mirror gathers the groups in arrays where
the others use a second map. Under valgrind's cachegrind it runs
12.3 billion instructions against Rust's 10.8 and C's 5.4. Python is
close behind all of them, since the work is hashing and sorting strings,
which its dict and sort do in C. The comparison with C and Rust waits
until after M4.

## Compiler findings

None new.
