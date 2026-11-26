# 1797. Design Authentication Manager

An authentication system works with tokens. Each session gets a new
token that expires `timeToLive` seconds after the `currentTime` it was
made at; a renewal moves the expiry to `timeToLive` seconds after the
renewal's own `currentTime`. Implement the `AuthenticationManager`
class:

- `AuthenticationManager(int timeToLive)` makes the manager and sets
  `timeToLive`.
- `generate(string tokenId, int currentTime)` makes a new token
  `tokenId` at `currentTime`.
- `renew(string tokenId, int currentTime)` renews the unexpired token
  `tokenId` at `currentTime`. If there is no unexpired token `tokenId`,
  nothing happens.
- `countUnexpiredTokens(int currentTime)` returns the number of tokens
  unexpired at `currentTime`.

A token that expires at second `t` has expired before anything else that
happens at `t`.

```
["AuthenticationManager", "renew", "generate", "countUnexpiredTokens", "generate", "renew", "renew", "countUnexpiredTokens"]
[[5], ["aaa", 1], ["aaa", 2], [6], ["bbb", 7], ["aaa", 8], ["bbb", 10], [15]]
->  [null, null, null, 1, null, null, null, 0]
```

**Constraints:** `1 <= timeToLive <= 10^8`, `1 <= currentTime <= 10^8`,
`1 <= tokenId.length <= 5`, `tokenId` holds only lowercase letters,
every `generate` has a new `tokenId`, `currentTime` strictly increases
from call to call, and there are at most 2000 calls in all.

The arms are `struct AuthenticationManager` with `fn new(time_to_live:
i32)`, `generate`, `renew` and `count_unexpired_tokens(current_time:
i32) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `authentication_manager.kara` ★ | a `Map` from each token to the second it expires: making a token sets it, renewing one moves it only while it lies ahead, and a count walks the map for the expiries still ahead. O(1) a make or renewal, O(n) a count |
| `authentication_manager_queue.kara` | a `Map` and a `VecDeque` of `(expiry, token)`: the clock only moves forward, so each expiry set is later than the one before and the queue stays in order; a count drops the expired entries from its front, removing a token from the map unless a renewal has moved it since, and the map's size is the answer. O(1) a call, amortized |
| `authentication_manager_tree.kara` | a `SortedSet` of `(expiry, token)` beside the `Map`: a renewal swaps the token's pair for its new one, a count pops the expired pairs from the set's front, and the set's size is the answer. O(log n) a call, amortized |
| `authentication_manager_retain.kara` | a `Map` pruned as it is counted: a count keeps only the tokens whose expiry lies ahead, with `retain`, and the map's size is the answer. O(1) a make or renewal, O(n) a count |
| `authentication_manager_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap` with `get_mut` for the renewal), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's example (`1 0`); the
edges, a token counted the second before it expires and not at the
second it does, a renewal at that second ignored, a renewal that moves
the expiry, and a renewal of a token never made (`1 0 1 0`); the
constraints' most, 2000 calls with tokens that live `10^8` seconds, 1000
made one a second then 1000 counts summed, and 2000 random calls with
the clock moving up to 50000 seconds a call, its counts folded (`the
most: 1000000 124152117`); and 3000 random runs of 1 to 40 calls (`3000
random runs: checksum 577357478`). `authentication_manager.py` mirrors
the ★ arm, and its output is byte-identical. Every arm gives the same
output under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the four Kāra arms were first written with `token_id:
String` on `generate` and `renew`, and check refused each map write
`self.expiry[token_id] = ..`: a bare parameter borrows, and the write
may insert, so the map needs the key owned. `karac fix` took the
parameter as `own String` wherever the key is stored, and put a
`.clone()` where the arm stores it twice: 2 fixes in the ★ and retain
arms, 4 in the queue arm (its `set` helper and both callers, the key
also going into the queue), and 5 in the tree arm, which was also first
written with `self.live.first()`, where a `SortedSet` has `min()`, 1
more. The harness folds each count with `as i64`, which check calls
unnecessary, an `i32` widening to `i64` by itself; `karac fix` removes
both, 2 fixes in every arm. The Rust solution takes one round of 14
fixes by `karac fix`'s count, the harness's 2 among them, and its diff
is: the `use` line dropped, `HashMap<String, i32>` to `Map[String,
i32]`, `HashMap::new()` to `Map.new()`, `&mut self` to `mut ref self`
twice, `&self` to `self`, `generate`'s `token_id: String` to `token_id:
own String`, `get_mut(&token_id)` to `get_mut(token_id)`, and `|&&exp|`
to `|exp|`. Its renewal writes through `get_mut`, so its `renew` keeps
borrowing. Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: at each count, every call before it replayed from the start,
token by token, a token made at `g` expiring at `g + ttl` and a renewal
at `r` moving the expiry to `r + ttl` only while the expiry is still
after `r`. LeetCode's example, the edges, two runs of 300 calls, and
1996 random runs of 1 to 40 calls with tokens that live 1 to 30 seconds.
Each arm runs every case's calls and meets six properties on the counts:

| property | what it checks |
|---|---|
| P1 | the statement read literally |
| P2 | every time 1000 seconds later gives the same counts |
| P3 | every time and the time to live doubled give the same counts |
| P4 | the renewals of tokens never made, left out, change nothing |
| P5 | a time to live one second longer never lowers a count |
| P6 | the ★ arm's counts |

The differential was first written with the two hand-made cases pushed
as `cases.push((5, [(1, "aaa", 1), ..].iter().map(..).collect()))`, and
check refused both with no fix, `expected '(i32, Vec[(i64, String,
i32)])', found '(i64, C)'`: B-2026-11-26-6 again, the `5` keeping its
default `i64` inside a pushed tuple, and the message naming the
`collect` result by its type parameter `C`. The `5` is suffixed by hand,
`5i32`. Check also warned that the solution's copy is handed
`c.1.clone()` where its `renew` only borrows, and `karac fix` passed
`c.1`, 1 fix. All 60,000 checks pass on every arm: `2000 cases: checksum
477610065, 60000 checks over 5 arms: 0 failures`, under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.
Python, running the ★ arm's mirror over the same cases, gives the same
checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a token renewed at the second it expires | P1 46, P6 184 |
| M2 | ★: a token counted at the second it expires | P1 390, P6 1560 |
| M3 | queue: an entry left in the queue at the second it expires | P1 390, P6 390 |
| M4 | queue: a token dropped at an old expiry its renewal has moved | P1 466, P6 466 |
| M5 | tree: a renewal that never drops the expired pairs first | P1 569, P6 569 |
| M6 | tree: a pair dropped a second before it expires | P1 427, P6 427 |
| M7 | retain: a token kept at the second it expires | P1 390, P6 390 |
| M8 | retain: a token not yet pruned renewed at the second it expires | P1 46, P6 46 |
| M9 | solution: a renewal that adds the time to live to the old expiry | P1 432, P6 432 |
| M10 | solution: a new token living one second short | P1 383, P3 383, P6 383 |

## Benchmarks

The bench builds 50 random scripts of 2000 calls once, with tokens that
live 1 to 100000 seconds and the clock moving 1 to 100 seconds a call,
and makes 2000 runs of the ★ arm, each on a new manager and each script
drawn from the checksum so far. Rust and Go use their standard hash
maps; C has no standard map, so its mirror is an open-addressing table
of 4096 slots hashed with FNV-1a, and its count walks every slot where
the others walk only the tokens. It checks clean as first written. Every
implementation prints `2000 runs over 50 scripts of 2000 calls: checksum
361567146`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.77 s against Rust's 0.72 s (0.73 s with overflow checks
on), C's 1.7 s and Go's 3.7 s; Python takes 9.8 s.
