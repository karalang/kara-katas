# 291. Word Pattern II

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String, Hash Map, Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/word-pattern-ii](https://leetcode.com/problems/word-pattern-ii/)

Given a `pattern` and a string `s`, return whether `s` follows the pattern — a
**bijection** between each letter of `pattern` and a non-empty substring of `s`.

```
"abab", "redblueredblue"  →  true    (a→red,  b→blue)
"aaaa", "asdasdasdasd"    →  true    (a→asd)
"aabb", "xyzabcxzyabc"    →  false
"aba",  "xyzxyzxyz"       →  false   (a→xyz would force b→xyz — not injective)
```

**Constraints:** `1 ≤ pattern.length, s.length ≤ 20`; both are lowercase
letters.

## Approach — backtracking over a bijection

Try every prefix of the remaining suffix as the binding for the current pattern
letter, recurse, and undo on failure. Two structures move together and **must be
undone together**:

- `map: Map[String, String]` — letter → substring;
- `used: Set[String]` — substrings already claimed.

`used` is what makes the mapping *injective* rather than merely functional; drop
it and `"aba" / "xyzxyzxyz"` wrongly returns `true`, which is exactly why that
case is in the test set.

## Why this kata — the shape that broke the compiler

Deliberately chosen by **compiler surface**. This is the intersection that
produced this session's high-severity use-after-free (ledger B-2026-07-25-1):

| Ingredient | Here |
|---|---|
| recursion | `matches` descends per pattern letter |
| owned `String` params consumed more than once | `key` / `cand` into `insert` **and** the undo `remove` |
| heap-keyed map | `Map[String, String]` — heap on *both* halves |
| mutation under recursion | insert/remove around the recursive call |

It also exercises `Map[String, _]`, which still takes the **eager** `keys()`
materialization path (ledger B-2026-07-25-4, open) — so this kata is the natural
home for that measurement when the fix lands.

## What it found

**No new bugs** — and after `karac fix`-style iteration the only source change
the compiler demanded was legitimate, not a workaround: `insert` takes ownership
of both halves, so the ownership checker correctly rejected reusing `key` and
`cand` afterwards (`value 'cand' moved here, used again here`). Adding `.clone()`
at the consuming sites is the honest fix — each structure owns its copy and the
undo path re-derives what it needs.

That is a useful negative result: the recursion + heap-map + undo shape is clean
under codegen after `7ae1e2e`.

## Verification

| Surface | Result |
|---|---|
| `karac run --interp` | ✅ matches `word_pattern_ii.py` |
| `karac run` (LLJIT) | ✅ |
| `karac build` (auto-par default) | ✅ |
| `karac build` + `KARAC_AUTO_PAR=0` | ✅ |
| ASan + **LeakSanitizer** (Linux x86) | ✅ clean — no UAF, no leak |

The sanitizer run matters here: the undo path frees map/set entries in a
recursive frame while the caller still holds slices of the same source string,
which is precisely the aliasing class that failed before.

## Kāra features exercised

- **`Map[String, String]` + `Set[String]`** — heap keys *and* heap values, with
  `insert` / `get` / `remove` / `contains` under recursion.
- **`.clone()` at consume sites** — the ownership checker's move diagnostic
  driving an explicit copy rather than a silent alias.
- **String slicing `s[a..b]`** as a value, compared with `!=` against a bound
  `String`.
- **Recursive `bool` return with early `return true`** from inside a loop.
- **`mut ref` parameters** threaded through recursion with call-site `mut`
  markers.
