# 736. Parse Lisp Expression

Given a string `expression` in a Lisp-like syntax, return the integer it
evaluates to. An expression is an integer, which may be negative; a
variable, a lowercase letter followed by letters or digits; or one of
three forms. `(add e1 e2)` is the sum of its two expressions and `(mult
e1 e2)` their product. `(let v1 e1 v2 e2 ... vn en expr)` assigns
`v1` the value of `e1`, then `v2` the value of `e2`, and so on, each
assignment seeing the ones before it, and then takes the value of
`expr`. A variable's value is that of its innermost assignment; `add`,
`let` and `mult` are never variable names.

```
(let x 2 (mult x (let x 3 y 4 (add x y))))  ->  14
(let x 3 x 2 x)                             ->  2
(let x 1 y 2 x (add x y) (add x y))         ->  5
```

**Constraints:** 1 <= `expression.length` <= 2000; there are no spaces
at either end and exactly one space between tokens; the expression is
valid and evaluates to an integer; every value along the way fits in a
32-bit integer.

## Approaches

A let's items are names and values in turn and then one last expression,
so a name is told from the last expression by what follows it: a name is
followed by its value, the last expression by the let's closing
parenthesis. Every arm uses that test.

| file | mechanism |
|---|---|
| `parse_lisp_expression.kara` ★ | split the text into tokens, then evaluate by recursion with a stack of scopes, a `Map` for each open let, a name looked up from the innermost; O(n) tokens |
| `parse_lisp_expression_tree.kara` | parse the text first into a tree, a `shared enum` with one variant for each form, then evaluate the tree with the assignments in force in one list, newest last, that a let cuts back to its start when it is done |
| `parse_lisp_expression_flat.kara` | no tokens and no tree: evaluate by recursion straight off the text's bytes, each call reading one expression, with the same one list of assignments |
| `parse_lisp_expression_iterative.kara` | no recursion: the tokens read left to right with an explicit stack of the open forms, each value handed to the form on top as an operand, the value of a pending name, or a let's last expression |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 14 lines: the three LeetCode examples; an add,
and a mult of an add; a variable assigned from one assigned before it; a
let inside an add whose assignment hides the outer one only inside it; a
negative assignment and a mult of negative numbers; a bare negative
number; 80 lets each inside the last, 1,733 characters, the longest of
these near the problem's limit; adds of 1 to 150 nested 149 deep; x
doubled in 30 lets that each hide the last, to 2^30; and 300 random
expressions with a checksum of their values. `parse_lisp_expression.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which cuts the text into tokens at spaces once every parenthesis has
spaces around it, finds a let's items first by skipping each one whole,
and gives the let its own copy of the assignments around it, extended by
each name in turn. Each of 3,000 random cases is an expression of up to
3 levels of forms that may use `x` and `y`, inside a let that assigns
them random numbers; the expressions under it assign names from `x`,
`y`, `z`, `a1` and `b2`, use only names assigned around them, and hold
numbers from -10 to 10. 89,241 characters are checked in all.

| | property |
|---|---|
| P1 | the value is the definition's |
| P2 | every variable renamed, the same value |
| P3 | `y` assigned in a let of its own inside the one that assigns `x`, the same value |
| P4 | for two more random expressions, an add of them and a mult of them take the sum and the product of their values |

It prints `3000 expressions (89241 characters), 4 arms, 48000 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a let's assignments outliving it | P1 68 |
| M2 | ★: a negative number read as a variable | P1 1686 |
| M3 | ★: every assignment made in the outermost let | P1 68 |
| M4 | tree: a let's assignments outliving it | P1 68 |
| M5 | tree: a name looked up from its oldest assignment | P1 147 |
| M6 | tree: an add taking its first operand twice | P1 605, P4 2921 |
| M7 | flat: each assignment put at the oldest end | P1 259 |
| M8 | flat: a negative number read as a variable | P1 1686 |
| M9 | flat: a number's digits added, not placed | P1 415 |
| M10 | iterative: a let's assignments outliving it | P1 68 |
| M11 | iterative: a closing let dropping every assignment | P1 190 |
| M12 | iterative: a name's oldest assignment found | P1 147 |
| E1 | tree: a name assigned when a space, not a parenthesis, follows it | 0 |
| E2 | flat: a let item starting with - tried as a name first | 0 |
| E3 | iterative: an open form found by the stack's length | 0 |

P1 kills all twelve; the other properties see little. M1, M4 and M10 are
one mistake in three arms, a let's assignments left in force after it
closes, and fail the same 68 cases: the mistake shows only when an inner
let assigns a name that the expression goes on to use from an outer let
after the inner one closes. M5 and M12 are one mistake in two arms, a
name's oldest assignment found rather than its newest, and fail the same
147. M2 and M8 read a negative number as a variable, which is never
assigned, and so has the value 0. M3 makes every assignment in the
outermost let, so that an inner let's assignment overwrites the outer
one for good, which fails the same cases as a let's assignments
outliving it. M7 puts each assignment at the oldest end of the list, so
that an outer assignment hides a newer one; M9 adds a number's digits
rather than placing them, so that 10 reads as 1; and M11 drops every
assignment, outer ones too, when a let closes. M6 is the only edit
P4 sees, since an add of two expressions then takes the first twice.
P2 and P3 see none: renaming every variable and splitting the outer let
in two leave every one of these mistakes in place. E1 assigns a name
when a space follows it rather than when no parenthesis does, the same
test; E2 tries a let's item starting with `-` as a name first, which it
gives back as soon as it finds the closing parenthesis after it;
E3 finds an open form by the stack's length rather than its top index.

## Verification

Every arm prints the same output as `parse_lisp_expression.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`3df39964e7`, whose last compiler change is `56339e6224`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends refuse the ★ arm, the differential and the
bench program at type checking, at the `*v` on the value a `Map`'s `get`
finds, since legacy gives it by value where v2 gives a reference. They
accept the other three arms, with ownership warnings that legacy takes a
bare parameter as owned. The iterative arm prints the right output under
the legacy `karac run` and `karac build`, and under
`KARAC_AUTO_PAR=1`; under the legacy interpreter it and the flat arm
print every line right but the last, where the random expressions come
out different (6,385 characters instead of 6,056). The flat and tree
arms crash with a segmentation fault under the legacy `karac run` and
`karac build`, and the tree arm does not finish under the legacy
interpreter within a minute. Legacy is frozen, so all of this is noted,
not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It makes
1,000 random expressions of 500 to 2,000 characters once, of up to
8 levels of forms, where a mult takes a number from -2 to 2 as its
second operand so that values stay small, and evaluates every one in
each of 40 rounds, keeping a checksum of the values. As C would, the C
program's tokens are pointers into the text with lengths, and each scope
is a short array searched in turn; the Kāra, Rust, Go and Python
programs copy each token into a string of its own and give each scope a
hash map, as the ★ arm does. Every implementation prints `40 rounds of
1000 expressions of 707115 characters in all: checksum 771126287`, the
Kāra program under `karac __mir-run` included (in 1.5 minutes).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.34 to 0.45 s |
| Rust (`rustc -O`) | 1.14 to 1.31 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.10 to 1.29 s |
| Go | 1.15 to 1.26 s |
| Python | 3.4 s |
| Kāra (`karac build --mir`) | 1.29 to 1.54 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; the legacy `karac build` refuses it (above). That
edit is by hand, on top of the `scripts/new-bench.sh` output. Under
`karac __mir-llvm-run` the program prints the same line in 7.4 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

So the v2 build is 3.7 times C at the medians of the interleaved runs
(1.42 s against 0.38), a seventh behind Rust (1.25) and a fifth behind
Go (1.18) and Rust under overflow checks (1.20). Python, at 3.4 s, is
only 2.4 times the v2 build, most likely because its string work runs in
C. C's lead is most likely the copying it leaves out: under valgrind's
cachegrind it runs 2.0 billion instructions, against 11.2 for Rust and
13.6 for the v2 build, which allocate a string for every token and hash
every name into a map. The two also take 1.8 and 2.3 billion branches,
against C's 0.28. Where the v2 build's extra instructions over Rust go
was not traced. The comparison with C and Rust waits until after M4.

## Compiler findings

None new.
