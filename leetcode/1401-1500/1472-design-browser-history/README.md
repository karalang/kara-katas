# 1472. Design Browser History

You have a browser of one tab where you start on the `homepage` and you
can visit another `url`, get back in the history number of `steps` or
move forward in the history number of `steps`.

Implement the `BrowserHistory` class: `BrowserHistory(string homepage)`
initializes the object with the `homepage` of the browser; `void
visit(string url)` visits `url` from the current page and clears up all
the forward history; `string back(int steps)` moves `steps` back in
history, and if you can only return `x` steps in the history and
`steps > x`, you will return only `x` steps, returning the current `url`
after moving back in history at most `steps`; `string forward(int
steps)` moves `steps` forward in history, and if you can only forward
`x` steps in the history and `steps > x`, you will forward only `x`
steps, returning the current `url` after forwarding in history at most
`steps`.

```
BrowserHistory("leetcode.com"), visit("google.com"), visit("facebook.com"),
visit("youtube.com"), back(1), back(1), forward(1), visit("linkedin.com"),
forward(2), back(2), back(7)
    ->  null, null, null, null, "facebook.com", "google.com", "facebook.com",
        null, "linkedin.com", "google.com", "leetcode.com"
```

**Constraints:** `1 <= homepage.length <= 20`, `1 <= url.length <= 20`,
`1 <= steps <= 100`, `homepage` and `url` consist of '.' or lower case
English letters, and at most `5000` calls will be made to `visit`,
`back`, and `forward`.

The arms are `struct BrowserHistory` with `fn new(homepage: Str)`, `fn
visit(mut ref self, url: Str)`, `fn back(mut ref self, steps: i32) ->
String` and `fn forward(mut ref self, steps: i32) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `browser_history.kara` ★ | the pages in one list, the place of the current page, and the end of the history: a visit overwrites the place after the current page, or adds it, and the history now ends there, so the pages it drops stay in the list unread until a later visit overwrites them. O(1) a call |
| `browser_history_stacks.kara` | two stacks, the pages behind the current one and the pages ahead of it, a step moving one page from one to the other through `mem.replace` on the current page; a visit clears the pages ahead. O(steps) a step call |
| `browser_history_truncate.kara` | one list that ends at the last page: a visit cuts off the pages ahead with `truncate` and appends. O(1) a step call |
| `browser_history_linked.kara` | a doubly linked list of `shared struct Page`s held from the homepage: each page holds the next one and points back at the one before it by a `weak` link, so the pages a visit drops from ahead of the current one are freed. O(steps) a step call |
| `browser_history_solution.kara` | a Rust solution as LeetCode's Rust users write it (`cur: usize`, `self.cur.saturating_sub(steps as usize)`, `std::cmp::min`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's example; the edges, back
and forward on the homepage alone and a visit that drops the pages ahead
(`home.org home.org home.org c.org home.org c.org`); and 2000 random
sessions of 1 to 100 calls, a visit to a fresh page one time in three,
else back or forward 1 to 10 steps, each answer folded into a checksum
(`2000 random sessions: 102084 calls, checksum 828105979`).
`browser_history.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the ★, truncate and linked arms check clean as first
written, the linked arm's `forward` after following check's advice. It
was first written `match self.current.next { Some(p) => self.current =
p, .. }`, and check refused the assignment while `p`, a borrow of
`self.current`'s field, is live, with the advice to copy at the borrow:
`match self.current.next.clone()`, a second handle to the next page. The
linked arm holds `home` beside `current` because the homepage is the
list's only owner; with `current` alone, a step back would leave the
pages ahead held by nothing. The stacks arm, written with Rust's
`std::mem::replace` as `std.mem.replace`, takes 3 fixes by `karac fix`'s
count, each `std.mem.replace` to `mem.replace`. The Rust solution takes
one round of 15 fixes by `karac fix`'s count: `Vec<String>` to
`Vec[String]`, each `usize` to `i64`, `homepage: String` and `url:
String` to `own String`, `vec![homepage]` to `[homepage]`, each `&mut
self` to `mut ref self`, `std::cmp::min` to `min` with the `steps as
usize` cast dropped, and `saturating_sub(steps as usize)` to
`saturating_sub(steps as i64).max(0)`: an `i64` saturates at its own
lowest value, not at 0, so the fix adds the floor `usize` gave. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms, each driven through
the same list of calls, and the statement read literally: before each
answer, every call so far replayed from the start on a plain list of
pages and a place in it, a visit keeping the pages up to the place and
adding its own. LeetCode's example, the edges (the homepage alone, a
visit that drops the pages ahead, steps past each end), 2000 random
sessions, half of 1 to 10 calls and half of 1 to 100, and one of the
constraints' most, 5000 calls. Each arm meets six properties on each
case:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | every page renamed under a prefix, the homepage too, renames the answers the same way |
| P3 | a forward of 1000 steps right after a visit stays on the page visited |
| P4 | a back of 1000 steps reaches the homepage, after any call |
| P5 | the forward of 1000 steps after it reaches the last page visited, the end of the history |
| P6 | the ★ arm's answers |

P3 to P5 add their probes to the cases of at most 100 calls, where 1000
steps reach either end.

With the fix below it checks clean. All 60,105 checks pass on every arm:
`2004 cases: checksum 738868522, 60105 checks over 5 arms: 0 failures`,
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`. Python, over the same cases, gives the same checksum.

The random cases are drawn as Rust writes them, `ops.push(if r == 0 {
(0, 0, f"c{c}.p{j}") } else { (r, steps, String.new()) })` into a
`Vec[(i64, i32, String)]` with `steps: i32`, and check refused it as an
`(i64, i64, String)`. That is B-2026-11-27-17: the `if` took its first
branch's type for the join, and the `0`s of that branch's tuple were
settled at `i64` where they were written, though a tuple's literals are
open in a `let` or pushed alone. The join itself was the larger fault:
two branches whose tuples, `Option`s or lists hold different number
types joined at the first, and a value of the second was narrowed into
it silently, `if c { (r, steps) } else { (r, r) }` with `r = 3000000000`
giving `-1294967296` in its `i32` place, and `if c { (r, steps) } else {
(0, 3000000000) }` the same. Fixed at 0c8496bc2e: such a join is
refused, as two different number types are at the top (design.md § Least
upper bound, rule 4), and a branch's tuple of literals takes its numbers
from the sibling branch.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash. The ★ arm's
first back edit was to stop one page short of the homepage, `.max(1)`;
on a history of the homepage alone that reads past the list's end, a
crash rather than a failure, so the edit now goes back one step fewer
than asked.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a visit keeps the dropped pages ahead | P1 806, P6 3224 |
| M2 | ★: back goes one step fewer than asked | P1 931, P6 3724 |
| M3 | stacks: a visit keeps the pages ahead | P1 975, P6 975 |
| M4 | stacks: forward walks back | P1 1359, P5 1774, P6 1359 |
| M5 | truncate: a visit keeps one dropped page | P1 693, P6 693 |
| M6 | truncate: back goes one step short | P1 931, P6 931 |
| M7 | linked: a visit never links the page after the current one | P1 1294, P5 1774, P6 1294 |
| M8 | linked: each page points back at the homepage | P1 717, P6 717 |
| M9 | solution: a visit keeps the history's end | P1 806, P6 806 |
| M10 | solution: back goes one step too far | P1 717, P6 717 |

## Benchmarks

The bench makes 1000 page names once, then runs 400 sessions of 5000
calls on the ★ arm, the constraints' most: a visit to one of the names
one time in three, else back or forward 1 to 10 steps, each answer's
bytes folded into a checksum. A visit copies its page into the history
in Kāra, Rust (LeetCode's `url: String`, a clone of the name) and C (a
`malloc`ed copy); Go and Python store the shared string. Back and
forward return a fresh `String` in Kāra and Rust, as their signatures
say, and the stored page in C, Go and Python. Every implementation
prints `400 sessions of 5000 calls: checksum 324606256`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.16 s against Rust's 0.16 s (0.18 s with overflow checks
on), C's 0.16 s and Go's 0.14 s; Python takes 3.3 s.
