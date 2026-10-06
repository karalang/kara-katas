# 355. Design Twitter

Design a simplified Twitter. Users post tweets, follow and unfollow each
other, and read a news feed of the ten most recent tweets posted by
themselves or by anyone they follow, newest first.

- `postTweet(userId, tweetId)` posts a new tweet; every call uses a unique
  `tweetId`.
- `getNewsFeed(userId)` returns up to ten tweet ids, most recent first.
- `follow(followerId, followeeId)` and `unfollow(followerId, followeeId)`.

```
postTweet(1, 5); getNewsFeed(1)  ->  [5]
follow(1, 2); postTweet(2, 6); getNewsFeed(1)  ->  [6, 5]
unfollow(1, 2); getNewsFeed(1)  ->  [5]
```

**Constraints:** `1 <= userId, followerId, followeeId <= 500`;
`0 <= tweetId <= 10^4`; at most `3 * 10^4` calls.

## Approaches

| file | mechanism | cost of a feed |
|---|---|---|
| `twitter.kara` ★ | each user keeps their tweets in posting order with a global timestamp; a feed seeds a max-first `PriorityQueue` with each author's newest tweet and, on every pop, pushes that author's next older one | `O(f + 10 log f)` for `f` authors |
| `twitter_scan.kara` | one global log of every post; a feed walks it from the end and keeps tweets by the user or someone they follow | up to the whole log |
| `twitter_linked.kara` | each user's tweets form a linked list of `shared` nodes, newest at the head; a feed keeps one cursor per author and ten times takes the newest head | `O(10 f)` |
| `twitter_sort.kara` | each author contributes at most their ten newest tweets to a pool, which is sorted newest-first and cut to ten | `O(10 f log(10 f))` |
| `differential.kara` | the four arms and an independent oracle, 18,320 checks, five properties | — |

Every arm prints the same 12 lines: the LeetCode example, eight edge cases
(nobody has posted, following yourself, unfollowing yourself, unfollowing a
stranger, an author with fifteen tweets, interleaved authors, following
twice, and a follower's feed not leaking into the followee's), and a checksum
over 20,000 random operations on 40 users. `twitter.py` mirrors the ★ arm and
its output is byte-identical.

Following yourself is the trap: an arm that adds each followee's tweets
without checking for the user shows every one of their tweets twice.

## Differential

`differential.kara` holds copies of the four arms and an oracle that shares
no data structure with them: every post in one list and the follow relation
as a boolean matrix, the feed found by walking the list backwards. 600
random operation sequences over 1, 2, 4 or 8 users, 0 to 60 operations each,
with a feed read after every operation.

| | property |
|---|---|
| P1 | every arm's feed equals the oracle's after every operation |
| P2 | a feed has `min(10, visible tweets)` entries |
| P3 | a feed is newest-first: tweet ids rise with posting order, so each feed is strictly decreasing |
| P4 | a user's own newest tweet is in their feed exactly when fewer than ten visible tweets are newer |
| P5 | right after `unfollow(a, b)` with `a != b`, `a`'s feed holds no tweet of `b` |

It prints `600 cases, 18320 feed checks, 0 failures` on every surface, and a
Python replay of the random stream gives the same check count.

Two mutants survived the first version, and both pointed at the driver
rather than the arms. It took `seed % users` from consecutive generator
states, and with a power-of-two user count the low bits made `a` and `b`
never equal, so nobody ever followed themself (M11 survived). And with two
or more users no single author ever filled a feed alone, so an arm that took
only nine tweets per author passed (M9). The draws now use the generator's
high bits (`seed / 65536`) and one case in four has a single user. The first
statement of P4 ("a user's own newest tweet is always in their feed") was
false, and the unmutated run caught it.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each built and run.
All eleven are killed.

| # | mutation | how |
|---|---|---|
| M1 | heap: a smallest-first queue | P1, 5155 failures |
| M2 | heap: never push an author's older tweet | P1, 12564 failures |
| M3 | heap: `unfollow` does nothing | P1 and P5, 1316 failures |
| M4 | scan: the user's own tweets are not shown | P1, 9021 failures |
| M5 | scan: a nine-tweet feed | P1, 3400 failures |
| M6 | linked: take the oldest head | P1, 5155 failures |
| M7 | linked: stop when one author runs out | P1, 4333 failures |
| M8 | sort: oldest first | P1, 12968 failures |
| M9 | sort: nine tweets per author | P1, 1648 failures |
| M10 | oracle: a user does not see their own tweets | P1 and P4, 45090 failures |
| M11 | sort: a self-follow counts the user twice | P1, 6407 failures |

## Verification

All four arms and the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and the four arms match
`twitter.py` byte for byte. The bench program prints `803178784` under LLJIT
and both builds, as do its C, Rust, Go and Python mirrors.
Under valgrind at `KARAC_OPT_LEVEL=0`, `twitter.kara`, `twitter_scan.kara`
and `twitter_sort.kara` end with `in use at exit: 0 bytes in 0 blocks` and
`ERROR SUMMARY: 0 errors`. `twitter_linked.kara` reads and writes nothing it
should not (no invalid access) but leaks: `definitely lost: 1,440 bytes in
45 blocks`, `indirectly lost: 255,168 bytes in 7,974 blocks` -- the list
heads it reads with `Map.get`, each still holding the rest of its list, which is
**B-2026-10-06-123** below. The other three arms never read a `shared`
value out of a `Map`.

## Benchmarks

Not measured yet. The bench programs in `bench/` and their C, Rust, Go and
Python mirrors are written and agree on the printed checksum, but the timings
still have to be taken on a quiet machine. This section will carry the table
when they are.

## Workarounds to revert

Each of these is the natural spelling, replaced because of an open compiler
bug, with a comment at the site naming the row.

- `twitter.kara`: the merge queue holds a `Candidate` struct with derived
  `Ord` rather than the tuple `(time, tweet, author, index)`, because a
  `PriorityQueue` of tuples does not build (**B-2026-10-06-87**).
- `twitter.kara`: `or_insert(Vec.new())` rather than design.md's
  `or_insert_with(Vec.new)` (**B-2026-10-06-118**).
- `twitter.kara`: `unfollow` uses `contains_key` and `m[k].remove(x)` rather
  than `entry(k).and_modify(|set| { set.remove(x); })`
  (**B-2026-10-06-119**).
- `twitter_linked.kara`: the cursors are a `Vec[Node]` that drops exhausted
  authors rather than a `Vec[Option[Node]]` advanced with
  `cursors[i] = node.next`, which frees nodes that are still linked
  (**B-2026-10-06-121**).

## Compiler findings

- **B-2026-10-06-114 (fixed in kara, interp): a place rooted at a `Map`
  entry chain did not behave like its bound spelling.**
  `m.entry(k).or_insert(d).field` panicked the interpreter,
  `….push_str(s)` and a `mut ref self` method on the slot lost their writes,
  and `*m.entry(k).or_insert(noisy()) += 1` ran `noisy()` twice. Fixed in kara `ba60f6339`.
- **B-2026-10-06-115 (open, codegen):** `karac build` refuses field,
  tuple-element and index places on an entry-chain result, bound or not.
- **B-2026-10-06-116 (open, high, codegen): a `mut ref self` method
  called on an entry chain does not write the slot compiled.** Silent.
- **B-2026-10-06-117 (open, codegen):** a type's associated function used
  as a value (`let f = Bag.new`, `or_insert_with(Bag.new)`) panics or fails
  `karac build`.
- **B-2026-10-06-118 (open, typecheck):** a builtin constructor
  (`Vec.new`, `String.new`, `Set.new`) is not accepted as a function value,
  although design.md's own example is `or_insert_with(Vec.new)`.
- **B-2026-10-06-119 (open, codegen):** a method on a collection-valued
  `and_modify` parameter does not build.
- **B-2026-10-06-120 (open, high, codegen): `m[k].field` on a `Map` or
  `SortedMap` of a `shared struct` reads 0 compiled.** Silent; found while
  minimising the linked-list arm.
- **B-2026-10-06-121 (open, high, codegen): an `Option[shared]`
  stored into a `Vec` element or a `Map`, or read back with `Map.get`, is
  not retained,** so a linked-list walk frees nodes that are still linked.
  The linked-list arm's first version corrupted the heap with it.
- **B-2026-10-06-123 (open, codegen): `m.get(k)` on a `Map` of a
  `shared struct` leaks one reference per call.** See Verification.
- **B-2026-10-06-122 (open, codegen): `o.clone().unwrap()` on an
  `Option` of a `shared struct` leaks one reference.**
- **B-2026-10-06-87 (open, codegen, found re-probing kata 23):** a
  `PriorityQueue` of tuples does not build.

The author already knows the language, so none of this counts toward the
machine-fix rate.
