# 1106. Parsing A Boolean Expression

A boolean expression is an expression that evaluates to either true or
false. It can be in one of the following shapes:

- `'t'` that evaluates to true.
- `'f'` that evaluates to false.
- `'!(subExpr)'` that evaluates to the logical NOT of the inner
  expression `subExpr`.
- `'&(subExpr1, subExpr2, ..., subExprn)'` that evaluates to the logical
  AND of the inner expressions, where `n >= 1`.
- `'|(subExpr1, subExpr2, ..., subExprn)'` that evaluates to the logical
  OR of the inner expressions, where `n >= 1`.

Given a string `expression` that represents a boolean expression, return
the evaluation of that expression. It is guaranteed that the given
expression is valid and follows the given rules.

```
expression = "&(|(f))"      ->  false
expression = "|(f,f,f,t)"   ->  true
expression = "!(&(f,t))"    ->  true
```

**Constraints:** `1 <= expression.length <= 2 * 10^4`; `expression[i]`
is one of `'('`, `')'`, `'&'`, `'|'`, `'!'`, `'t'`, `'f'` and `','`.

The arms are `fn parse_bool_expr(expression: String) -> bool`. The
operands are written with no spaces between them.

## Approaches

| file | mechanism |
|---|---|
| `parse_bool_expr.kara` ★ | recursive descent: an expression is `t`, `f`, or an operator and its operands in parentheses, read left to right from a shared position, a `mut ref i64`, each operand read by the same function and its value kept in a `Vec[bool]` for `all` or `any`. O(n) |
| `parse_bool_expr_stack.kara` | one stack of characters: everything but commas is pushed, and at each `)` the letters down to the `(` are popped and counted, the operator under it applied, and its letter pushed in their place |
| `parse_bool_expr_tree.kara` | parsed into a tree, then evaluated: an `enum` with a variant for each value and operator, the operands in a `Vec`, built by recursive descent over a `Peekable` of the characters and folded by a `match` that hands `eval` itself to `all` and `any` |
| `parse_bool_expr_frames.kara` | a stack of open operators, a `struct` per frame with whether it has seen a true and a false operand: a value or a closed operator reports to the frame below it, so no value is ever pushed, and `)` closes the top frame. Read as bytes |
| `parse_bool_expr_reduce.kara` | by rewriting: the innermost operator, the last `(` and the `)` after it, is replaced by its letter, until one letter is left. Each rewrite rebuilds the string from slices, so O(n^2) |
| `parse_bool_expr_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, a `stk: Vec<char>`, `while let Some(&top) = stk.last()`, `has_t` and `has_f`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm but the reduce arm is O(n). Every arm prints the same 16
lines: the answers for LeetCode's three examples and ten more (each
letter alone, `!` of each, `&` all true and one false, `|` of one false,
three `!` deep, and two mixed), then over 2000 random expressions of up
to 60 operators and letters how many are true (`2000 random expressions,
53073 characters: 1033 true`), and two of LeetCode's longest: one 6000
operators deep, and one `|` over 9999 letters. `parse_bool_expr.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the expression cut at the commas outside every parenthesis
into its operator and operands, each operand read the same way, and the
operator applied as the statement words it. It checks 2000 problems in
four kinds of 500: random expressions of up to 20 operators and letters,
4 deep; a letter under up to 30 nested operators of one operand each;
one `&` or `|` over up to 30 letters, four in five of them `t`; and
random expressions of up to 60, 8 deep. Every random choice is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the answer is the one a second reading gives, from the inside out: the innermost operator replaced by its letter until one letter is left |
| P3 | the expression wrapped in operators that keep its value (`!(!(e))`, `&(e)`, `|(e)`, `&(e,t)`, `|(f,e)`) gives the same answer, and wrapped in ones that fix it (`&(e,f)`, `|(t,e)`) gives that value |
| P4 | `!(e)` is the opposite, `&(e,!(e))` is false and `|(!(e),e)` true |
| P5 | De Morgan at the root: `&(a,b,..)` gives what `!(|(!(a),!(b),..))` does, and `|` the other way round |
| P6 | the root's operands reversed give the same answer, and so does the root's first operand replaced by the arm's own letter for it |

All 72,000 checks pass on every arm: `2000 problems: checksum
606598749, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems gives the same checksum.

P1 reads the statement and P2 reads the expression another way; P3 to
P6 compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `!` never negating | P1 469, P2 469, P4 2000, P5 703 |
| M2 | ★: only the first operand of `&` read | P1 305, P2 305, P3 1245, P4 1245, P5 347, P6 170 |
| M3 | ★: only the last operand of `\|` read | P1 179, P2 179, P3 1115, P4 1115, P5 337, P6 173 |
| M4 | stack: `&` read as `\|` | P1 481, P2 481, P3 2000, P4 2000, P5 687 |
| M5 | stack: the falses never counted | P1 831, P2 831, P3 2000, P4 2000, P5 1194 |
| M6 | stack: each comma pushed as a false | P1 68, P2 68, P3 966, P5 62 |
| M7 | tree: the first operand of `\|` never read | P1 360, P2 360, P3 2000, P4 1118, P5 313, P6 62 |
| M8 | tree: the `(` read as an operand | stops: `unwrap()` on `None` |
| M9 | frames: a true reported to the bottom frame | P1 783, P2 783, P3 2000, P4 2000, P5 59 |
| M10 | frames: `\|` read as `&` | P1 460, P2 460, P3 2000, P4 2000, P5 691 |
| M11 | frames: the bottom frame true from the start | P1 984, P2 984, P3 2000, P4 2000 |
| M12 | reduce: each letter written the other way | P1 1229, P2 1229, P3 2000, P4 2000, P5 706 |
| M13 | solution: an `f` stops the popping | P1 766, P2 766, P3 2000, P4 2000, P5 109 |
| M14 | solution: the `(` pushed | P1 875, P2 875, P3 2000, P4 2000 |
| M15 | solution: a true never noted | P1 770, P2 770, P3 2000, P4 2000, P5 1008 |

Of the fourteen that run to the end, P1 and P2 catch all fourteen, P3
and P4 thirteen, P5 twelve and P6 three. P1 and P2 fail on the same
problems every time: both apply the operators as the statement does,
one from the outside in and one from the inside out, so they agree on
every expression. P3 and P4 fail on every problem for most edits, since
they wrap every problem in `&` and `|` and `!`: an arm that reads `&`
as `|` gives `&(e,f)` as true whatever `e` is. P3 misses only M1: an
`!` that never negates still keeps `!(!(e))`, and P4, built on `!`,
catches it on every problem. P4 misses only M6: a comma read as a false
operand leaves `&(e,!(e))` false and `|(!(e),e)` true. P6 sees only the
three edits that read an operand by its place (M2, M3, M7), which the
operands reversed move. P3 to P6, which compare the arm only with
itself, catch all fourteen. M8 stops: with the `(` read as an operand,
every operator reads more characters than it has, and the tree arm
reads past the end.

Of the fifteen not kept, all fail as a kept edit: `!` never negating in
the other five arms as M1, `&` read as `|` in the other five as M4, `|` read
as `&` in three more as M10, the tree arm reading only the first operand
of `&` as M2, and the reduce arm taking the outermost operator first
stops as M8 does.

## Verification

Every arm prints the same output as `parse_bool_expr.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing
on any file, and `karac fix` has nothing to apply.

The kata found four gaps, each filed in the kara ledger; three are
fixed. The ★ arm was written as Kāra, and the other five as Rust writes
them; `karac fix` carried every Rust spelling it could to a clean check:

- The stack arm in two rounds: `Vec<char>` to `Vec[char]`,
  `Vec::new()` to `Vec.new()`, `let (mut t, mut f)` to `let mut (t,
  f)`, and the bare `t += 1` of an `if` arm to `t += 1;`.
- The Rust solution in three: `struct Solution {}` declared, `vec![]`
  to `Vec.new()`, `||`, `&&` and `!` to `or`, `and` and `not`, and
  `while let Some(&top) = stk.last()` to `while let Some(top) =
  stk.last().cloned()`.
- The frames arm in four: `vec![..]` to `[..]`, `as_bytes()` to
  `bytes()`, `!` to `not`, and `let top = frames.last_mut().unwrap();`
  with its two uses to `frames[frames.len() - 1].seen_true = true;`.
  The last was advice alone: the `last_mut` rewrite covered `match` and
  `if let` but not a `let` (B-2026-11-10-51, fixed).
- The reduce arm in three: `'('` and `'f'` to `"("` and `"f"` where a
  `Str` is wanted, `&s[a..b]` to `s[a..b]`, the parameter to `own
  String` since `s` takes it over, and `format!("{}{}{}", &s[..open -
  1], if value { "t" } else { "f" }, &s[close + 1..])` to an f-string.
  The last was advice alone: the rewrite refused any argument
  containing `f"`, meant to keep an f-string out of a hole, and the
  plain literal `"f"` matched (B-2026-11-10-50, fixed).
- The tree arm in one, then by hand: `use std::iter::Peekable; use
  std::str::Chars;` became `import` lines that `karac check` refuses
  (`std.iter has no item Peekable`, `unknown module std.str`), and
  `&mut Peekable<Chars>` became `mut ref Peekable[Chars]`, which names
  no Kāra type. `Peekable` is in the prelude and a string's `chars()` is
  `StrChars`, so the imports were deleted and the parameter written
  `mut ref Peekable[StrChars, char]` by hand (B-2026-11-10-35, open). The
  one other hand edit is `chars.next();`, whose discarded `Option` draws
  a warning that deliberately has no machine fix: `let _ =
  chars.next();`.

The frames and reduce arms here are the
`karac fix` output verbatim, and match the hand forms the differential
was first run with.

## Benchmarks

The bench builds 32 random expressions once, of 12000 to 15000
characters each, up to LeetCode's longest, 20 deep. Each of 200 rounds
flips one letter in every expression and parses it with the ★ arm: 6400
parses over 92 million characters. Every implementation prints `200
rounds over 32 expressions of 462158 characters: 2687 true, checksum
429929595`. Every language keeps the characters 32 bits wide, as Kāra's
`char` is, and gives each operator a growable array of its operands'
values.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.804 to 0.894 s | 0.841 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.824 to 0.901 s | 0.858 s |
| Rust (`rustc -O`) | 0.938 to 1.021 s | 0.975 s |
| Kāra (`karac build`) | 0.960 to 1.080 s | 0.991 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.957 to 1.092 s | 1.002 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.976 to 1.109 s | 1.011 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.971 to 1.088 s | 1.017 s |
| Go | 1.084 to 1.214 s | 1.146 s |
| Python | 9.290 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra and Rust tie at about 1.2x C's time, and Go takes about
1.13x Kāra's. Python takes about 9x Kāra's time.
