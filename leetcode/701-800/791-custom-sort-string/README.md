# 791. Custom Sort String

`order` is a string of different lowercase letters, and `s` a string of
lowercase letters. Rearrange the letters of `s` so that the letters
`order` names come in `order`'s order: if `x` comes before `y` in
`order`, every `x` comes before every `y` in the answer. Letters `order`
does not name may go anywhere, and any such answer is accepted.

```
order = "cba",   s = "abcd"  ->  "cbad"
order = "bcafg", s = "abcd"  ->  "bcad"
```

**Constraints:** `order` has 1 to 26 different lowercase letters, and
`s` 1 to 200 lowercase letters.

## Approaches

Since many answers are accepted, every arm gives the same one so that
the arms can be compared: the letters `order` names first, in its order,
then the others in the order `s` has them.

| file | mechanism |
|---|---|
| `custom_sort_string.kara` ★ | count each letter of `s`, write out the letters of `order` in turn, each as many times as `s` has it, then the letters of `s` that `order` does not name, in place; O(n + 26) |
| `custom_sort_string_sortby.kara` | each letter ranked by its place in `order`, 26 for the rest, and the letters of `s` sorted by rank with the library's stable `sort_by`; O(n log n) |
| `custom_sort_string_buckets.kara` | a `Map` from each letter of `order` to its bucket, one `String` per bucket and one for the rest, each letter of `s` appended to its bucket and the buckets joined; O(n + 26) |
| `custom_sort_string_filter.kara` | for each letter of `order`, the letters of `s` equal to it kept with `filter`, then the letters `order` does not name, found with `any` over `order`'s letters; O(26 n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: LeetCode's two examples; a third with
a letter twice; a one-letter order; the whole alphabet forwards and
backwards over a pangram; an order naming none of the letters; and 300
random cases, an order of 1 to 26 letters and a string of 1 to 200, with
the letters in all and a checksum. `custom_sort_string.py` mirrors the ★
arm and its output is byte-identical.

`String.contains` takes a `Str` (docs/library/strings.md), not a `char`,
so the filter arm asks whether `order` has a letter with
`order.chars().any(|o| o == x)`.

## Differential

`differential.kara` holds copies of the four arms and the definition:
the letters of `s` put in order by insertion sort on their rank, each
moved left only past letters of a larger rank, so letters of equal rank
keep their order in `s`. Its 1,600 cases are a quarter with any order
and string, a quarter with all 26 letters in the order, a quarter whose
string has only letters the order does not name, or only three letters
when it names all 26, and a quarter whose string has only letters the
order names; one string in four has up to 200 letters, the rest up
to 12.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer has the same letters as `s`, as many of each |
| P3 | the letters' ranks never go down along the answer |
| P4 | the letters `order` does not name come in the order `s` has them |

It prints `1600 cases (48197 letters), 4 arms, 25600 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each letter of order written once | P1 760, P2 760 |
| M2 | ★: the named letters written again instead of the rest | P1 1600, P2 1600, P3 1031, P4 722 |
| M3 | ★: no letter marked as named | P1 1161, P2 1161, P3 1082 |
| M4 | sort_by: the ranks compared the wrong way round | P1 1091, P3 1091 |
| M5 | sort_by: the letters order does not name ranked first | P1 282, P3 282 |
| M6 | sort_by: every pair compared as equal | P1 1045, P3 1045 |
| M7 | buckets: the rest put in the first bucket | P1 282, P3 282 |
| M8 | buckets: the buckets joined last first | P1 1091, P3 1091 |
| M9 | buckets: every letter of order given the same bucket | P1 1045, P3 1045 |
| M10 | filter: the letters of order kept once each | P1 760, P2 760 |
| M11 | filter: the rest taken as the letters order does name | P1 1600, P2 1600, P3 1031, P4 722 |
| M12 | filter: the rest left out | P1 722, P2 722, P4 722 |

P1 kills all twelve. P2 misses every edit that only reorders letters,
and P3 every edit that keeps the ranks rising but loses or repeats
letters; P4 sees only the edits that drop those letters or write others
in their place.

## Verification

Every arm prints the same output as `custom_sort_string.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept the ★ and filter arms unchanged and
refuse the other two at the type check, the sort_by arm at
`out.push(*c)` over `letters.iter()` and the buckets arm at `Some(b) =>
*b` over `bucket_of.get(c)`, since they take those items for `char` and
`i64` rather than references. They refuse the differential for the same
`*`s, and in its closure `|c| rank_of(named, c)` they take `named` as
moved, so the closure can run once; a copy with those `*`s removed and
`rank_of` taking `ref Vec[char]` prints the differential's line under
the legacy interpreter (`karac run --interp`), the legacy JIT (`karac
run`), `karac build` and an auto-par build. The arms, with those `*`s
removed, print the first seven lines right under all four, and a
different eighth line, `300 random strings: 31048 letters, checksum
725178055`: in the harness's `for j in 0..1 + next_random(mut seed) % 26
{ order.push(pool[j]); }` legacy calls `next_random` twice, so its
random cases are other ones. That loop alone, from a fixed seed over the
alphabet, shows it under the legacy interpreter: 17 letters and the seed
two steps on, where v2 and Python give 15 letters and the seed one step
on. Legacy also refuses the bench program's `custom_sort_string(orders[r
% 64], strings[(r / 64) % 64])` as moves out of an index; a copy with
the parameters written `ref String` builds and prints `checksum
850790155`, as it makes its orders with the same loop, and the bench
timing below is of it. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 orders of 1
to 26 different letters and 64 strings of 200 letters, LeetCode's
longest, are made once. Each of 1,000,000 rounds sorts one of the
strings by one of the orders, and every 1,000th answer goes into the
checksum. Every implementation prints `1000000 rounds of 200-letter
strings: 200000000 letters, checksum 460688317`, the Kāra program under
`karac __mir-run` included (in 597 s).

The bench measures counting the letters of a string and building a new
one a letter at a time. Kāra and Rust push `char`s onto a `String`, Go
writes bytes to a `strings.Builder`, C writes bytes into a buffer it
allocates at the string's length, and Python joins a list. Spot timings
on a shared 4-core container, eight runs of each compiled program, five
of them interleaved, and two of Python (`bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.89 to 0.99 s |
| Rust (`rustc -O`) | 1.56 to 1.81 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.49 to 1.98 s |
| Go | 2.01 to 2.30 s |
| Python | 25.40 to 26.78 s |
| Kāra (`karac build --mir`) | 2.25 to 2.57 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 10.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 2.46 s,
against C's 0.95, Rust's 1.71 (1.59 under overflow checks) and Go's
2.15. Under valgrind's cachegrind v2 runs 16.0 billion instructions and
3.19 billion branches, against C's 2.61 billion and 0.54 billion and
Rust's 8.73 billion and 1.98 billion. Where v2's extra instructions lie
is not profiled. The legacy build of the copy ran 1.57 to 2.00 s, a
median of 1.76 s in the interleaved runs, so v2 takes 1.40 times legacy,
though the copy's orders are not the same ones (see Verification). The
comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
