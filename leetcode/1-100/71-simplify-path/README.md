# 71. Simplify Path

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Stack &nbsp;·&nbsp; **Source:** [leetcode.com/problems/simplify-path](https://leetcode.com/problems/simplify-path/)

Given an absolute Unix-style path, return its canonical form.

A canonical path:

- starts with `/`,
- has each adjacent pair of directories separated by exactly one `/`,
- contains no `.` or `..` navigation tokens,
- does not end with a trailing `/` unless the result is the root itself.

```
"/home/"                            →  "/home"
"/home//foo/"                       →  "/home/foo"
"/home/user/Documents/../Pictures"  →  "/home/user/Pictures"
"/../"                              →  "/"
"/.../a/../b/c/../d/./"             →  "/.../b/d"   ("..." is a name, not a navigation token)
```

**Constraints:** `1 ≤ path.length ≤ 3000`; `path` consists of English letters, digits, `'.'`, `'/'`, `'_'`; `path` is an absolute path starting with `/`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| One-pass scan + (start, end) index stack | O(n) time, O(n) space | [`simplify.kara`](simplify.kara) ✓ via `karac run` / `karac build` | [`simplify.py`](simplify.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 24 test cases.

## Why a stack — and why index pairs, not strings

The canonical form is determined by what's left on the stack after walking the input. Components fall into three classes:

| Component | Action |
|---|---|
| `'.'` | skip — same directory |
| `'..'` | pop one entry (or stay at root if empty) |
| anything else | push |

A naïve implementation would split the input on `/` into a `Vec[String]`, then push/pop those strings. That works, but allocates a fresh `String` per component and keeps both the input *and* the parts buffer live for the whole walk. The stack here instead holds **`(start, end)` index pairs into the snapshotted input chars** — 16 bytes per entry regardless of how long the component is, and no per-component allocation. The output walk reads characters back out of the input buffer at the recorded positions.

Pseudocode for the inner loop:

```
i = 0
while i < n:
    while i < n and cs[i] == '/': i += 1        # collapse the slash run
    if i >= n: break
    j = i
    while j < n and cs[j] != '/': j += 1        # consume non-slash run
    match (j - i, cs[i], cs[i+1] if j-i>=2):
        (1, '.', _)        → skip
        (2, '.', '.')      → pop                 # stay at root if empty
        else               → push (i, j)
    i = j
```

The length is part of the discriminator on purpose. `"..."` is a three-character file name and must be pushed, not interpreted as "parent of parent" — the `/.../a/../b/c/../d/./` LeetCode example exists to catch implementations that look only at the leading byte.

## The pop saturates at root

`'..'` from an empty stack is a no-op, not an error. That's how `/../` and `/../../../` both reduce to `/`. The guard

```
if top > 0 { top = top - 1 }
```

handles both: the stack stays empty across however many `'..'`s the input throws at it.

## `top`-counter pop, not `Vec.pop`

The interpreter doesn't yet have a `Vec.pop` dispatch arm (the typechecker accepts it and codegen lowers it, but `karac run` panics with "method 'pop' not found" — surfaced by the first probe of this kata). Instead, this solution keeps a `top: i64` counter as the live stack size and *reuses* slots past `top` with indexed writes, growing the underlying `Vec` only when `top` reaches its length. Same big-O, same semantics, runs under both `karac run` and `karac build` from one source.

If the interpreter's `Vec.pop` lands later, the algorithm shape doesn't change — pop becomes `starts.pop(); ends.pop();` and the `top < starts.len()` branch goes away. The (start, end) representation is the bigger structural choice.

## Kāra features exercised

- **`ref String` parameter + `for c in s.chars()`** — read-only string borrow, iterated per Unicode scalar value. The kata's input alphabet is ASCII per LeetCode #71, so `chars` and `bytes` would both work; `chars` is chosen so the per-character output append (`f"{out}{c}"`) gets a `char` directly without a `u8 as char` round-trip.
- **`Vec[char]` snapshot via `push` in a `for` loop** — `s.chars()` is a forward iterator with no `len()`, but the algorithm needs random access (`cs[i + 1]` for the second dot of `'..'`) and post-scan position-indexed reads, so one pass into a `Vec[char]` pays for itself immediately.
- **Parallel `Vec[i64]` start/end stacks + a `top` counter** — the (start, end) representation is 16 bytes per entry regardless of component length; the `top` counter is the live size, and indexed writes (`starts[top] = i`) reuse stale slots so `Vec.push` only fires when the stack grows past its all-time-high. Same shape as the bench-style "single-allocation hot loop" used elsewhere in the kata corpus.
- **`char` equality and arithmetic on `i64` indices** — `cs[i] == dot` / `cs[i + 1i64] == dot` compare `char` to a `char`-typed constant; the `i64` arithmetic is the standard kata-style index type.
- **`and` short-circuit inside `while` and compound `let` conditions** — `while i < n and cs[i] == slash` is the boundary-safe slash-skip; `let is_dotdot = len == 2 and cs[i] == dot and cs[i + 1] == dot` shortcuts the second `cs[]` read when the length doesn't match.
- **`return` from the empty-stack root special case** — `if top == 0i64 { return "/"; }` exits before the output loop runs; the literal materializes as a fresh `String` per design.md § Part 1½ Rule 4.
- **f-string interpolation as the String-builder** — `out = f"{out}/"` and `out = f"{out}{c}"` are the available append shape (kara doesn't have `String + String` concatenation today and has no `substring` method either, so f-string append is the per-character build path). Total cost is O(n) over the output length, since each character is appended exactly once.

No `Map`, no shared structs, no `Vec[String]`.

## Edge cases worth exercising

| Input | Expected | Why it's interesting |
|---|---|---|
| `"/"` | `"/"` | Root passes through unchanged. |
| `"//"` / `"///"` | `"/"` | Runs of slashes collapse to a single component boundary. |
| `"/home/"` | `"/home"` | Trailing slash drops; the cheapest happy-path case. |
| `"/home//foo/"` | `"/home/foo"` | Doubled slash inside the input collapses too. |
| `"/../"` | `"/"` | `'..'` from root saturates at root, doesn't underflow. |
| `"/../../../"` | `"/"` | Same saturation across multiple `'..'`s. |
| `"/a/../../b"` | `"/b"` | Pop past root then push — the saturation guard must leave the stack ready for a subsequent push. |
| `"/a/./b/../../c/"` | `"/c"` | All three component classes mixed; exhaustive small case. |
| `"/a//b////c/d//././/.."` | `"/a/b/c"` | Pathological slash runs + dots; one component popped at the end. |
| `"/..."` | `"/..."` | Three dots is a name — exactly the discriminator the kata is named after. |
| `"/...."` | `"/...."` | Four dots is a name too — length 4 doesn't pattern-match `'.'` or `'..'`. |
| `"/.hidden"` | `"/.hidden"` | Leading dot in a longer run is still a name. |
| `"/..hidden"` | `"/..hidden"` | Two leading dots in a longer run is still a name — length is 8, not 2. |
| `"/...hidden"` | `"/...hidden"` | Three leading dots in a longer run is still a name. |
| `"/abc_123"` | `"/abc_123"` | Underscore + digits in the alphabet — passes through unchanged. |
| `"/./"` | `"/"` | Single dot in the middle of slashes — skips, leaves the stack empty. |
| `"/a/./b/./c/."` | `"/a/b/c"` | Dot at end + interior — both skipped. |
| `"/a/b/c/../.."` | `"/a"` | Two pops at the end shrink the stack by exactly two. |
| `"/a/b/../c/../../d"` | `"/d"` | Pop / push / pop / pop / push churn — the (start, end) reuse path. |
| `"/home/user/Documents/../Pictures"` | `"/home/user/Pictures"` | Canonical "user navigates up then sideways" example. |
| `"/.../a/../b/c/../d/./"` | `"/.../b/d"` | The LeetCode-spec example that catches "leading-byte-only" implementations. |

All 24 cases run in `main` and the output is diffed against [`simplify.py`](simplify.py).

## API shape

`simplify(s: ref String) -> String` is the algorithm; `report(s: ref String)` prints `simplify "<input>" -> "<output>"`; `main` calls `report` per case. Logic is separated from I/O so the function would slot into a future test harness unchanged. The Python file mirrors this with `simplify(s: str) -> str` and the same `report` / `main` shape.

Each `main` case passes its string literal directly to `report` — `ref String` accepts any source per design.md § Part 1½ Rule 4, and the codegen materializes the literal into a stack temp at the call site automatically.

## Running

```bash
# Kāra — interpreter and codegen both produce the same output today.
karac run   simplify.kara
karac build simplify.kara && ./simplify

# Python
python3 simplify.py

# Verify they agree
diff <(./simplify) <(python3 simplify.py) && echo OK
diff <(karac run simplify.kara) <(python3 simplify.py) && echo OK
```
