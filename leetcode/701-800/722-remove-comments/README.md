# 722. Remove Comments

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Array &nbsp;·&nbsp; **Source:** [leetcode.com/problems/remove-comments](https://leetcode.com/problems/remove-comments/)

Given a C++ source as a list of lines, strip `//` line comments and
`/* ... */` block comments and return the surviving lines (dropping any
line that becomes empty).

```
["/*Test program */", "int main()", "{ ",
 "  // variable declaration ", "int a, b, c;",
 "/* This is a test", "   multiline  ", "   comment for ",
 "   testing */", "a = b + c;", "}"]
  →  ["int main()", "{ ", "  ", "int a, b, c;", "a = b + c;", "}"]

["a/*comment", "line", "more_comment*/b"]  →  ["ab"]
```

A block comment can span lines, fusing code before its `/*` with code
after the matching `*/` into one output line; the implicit newline between
list entries is consumed inside the block. The first effective marker
wins: inside a block, a `//` is inert; inside a line comment, a `/*` is
inert. LeetCode guarantees the source has no quote characters, so there is
no string-literal state to track.

**Constraints:** `1 ≤ source.length ≤ 100`; `0 ≤ source[i].length ≤ 80`;
every opened block comment is eventually closed; no quote characters.

## Why this kata — the lexer's comment slice

This is the corpus's highest-fidelity stand-in for the self-hosted lexer's
**comment slice** (the `//` line and `/* */` block arms). It exercises the
same machinery the lexer's compiled binary stands on:

| Lexer surface | This kata |
|---|---|
| maximal-munch two-char lookahead (`/`+`/`, `/`+`*`, `*`+`/`) | the marker dispatch |
| in-comment **mode flag** carried across input | `in_block`, the only cross-line state |
| `String.push(char)` accumulation into a token/line buffer | the output buffer |
| **multi-line span advance** (L3 — newline / line boundary) | block comments that cross list entries; markers that may *not* span the implicit newline |

## Approaches

Both styles produce byte-identical output to the Python oracle across all
16 cases, under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| Index-heavy: snapshot each line into `Vec[char]`, `cs[i+1]` lookahead | [`remove_comments.kara`](remove_comments.kara) | the lexer's array-cursor form |
| Streaming: `for c in line.chars()`, carry the half-seen marker in a flag | [`remove_comments_stream.kara`](remove_comments_stream.kara) | the lexer's forward-cursor form |
| Reference oracle | [`remove_comments.py`](remove_comments.py) | known-correct LeetCode answer |

The **streaming** variant is the more lexer-faithful of the two: no random
access, the marker decided the instant its second char lands, and the
pending-`/`/pending-`*` flags reset at each line boundary because a `*`
ending one line and a `/` starting the next must **not** form a `*/`
(LeetCode's newline is a real separator). It flushed no new defect — the
flat-curve signal — once the bug below was fixed.

## What this kata uncovered

`buffer.push_str(name)` where `name: ref String` — appending a **borrowed**
String into an output buffer — was rejected by `karac build` with
`'push_str' expects a String argument, found 'ref String'`, while `karac
run` only *warned* (the interpreter's known typecheck-bypass; `build` is
the real gate). The typechecker's `push_str` arm accepted only an owned
`Type::Str`, so the lexer's natural shape — appending borrowed
keyword/identifier text into a buffer — did not compile.

The same one-line gate also sat on `contains` and `starts_with`, the lexer's
keyword-membership and prefix-check ops. All three read their argument's
bytes and copy/scan them; there is no ownership reason to demand a move.

Per the project's **no workarounds — fix the compiler** discipline, karac's
typechecker was extended (an `is_str_like` helper in
`src/typechecker/stdlib_seq.rs` that accepts `String` *or* a `ref` / `mut
ref` borrow of one) so `push_str` / `contains` / `starts_with` all take a
borrowed String. Codegen already consumed the argument as a by-value string
struct, so no codegen change was needed — confirmed by the binary matching
the oracle. A typechecker regression test
(`test_string_methods_accept_borrowed_str_arg`) pins the behavior.

## Kāra features exercised

- **`String.push(char)` accumulation** — char-by-char buffer build, the
  lexer's heaviest op (42 uses in `selfhost/src/main.kara`).
- **`String.push_str(ref String)`** — append a borrowed String (the gap
  this kata closed); also `push_str` of string literals for the output
  render.
- **`Vec[String]` literal + index** — `["a", "b"]` array literal coerced to
  `Vec[String]`, `source[li]` indexed, `.chars()` iterated per line.
- **Cross-line state machine** — `in_block` is the single piece of state
  that legitimately survives a line boundary; the streaming variant
  additionally carries per-line pending-marker flags that must reset at the
  newline.
