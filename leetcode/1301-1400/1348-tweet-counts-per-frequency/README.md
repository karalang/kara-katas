# 1348. Tweet Counts Per Frequency

A social media company wants to monitor activity by counting the tweets
that occur in select periods of time, partitioned into smaller chunks by
a frequency: every minute (60 seconds), hour (3600 seconds) or day
(86400 seconds). The period `[10, 10000]` by the minute is the chunks
`[10, 69]`, `[70, 129]`, ..., `[9970, 10000]`; the last chunk may be
shorter, and always ends at the period's end.

Implement `TweetCounts`:

- `TweetCounts()` makes an empty counter.
- `recordTweet(tweetName, time)` stores the tweet `tweetName` at `time`
  (in seconds).
- `getTweetCountsPerFrequency(freq, tweetName, startTime, endTime)`
  returns the number of tweets named `tweetName` in each chunk of the
  period `[startTime, endTime]`, in order, for `freq` one of `"minute"`,
  `"hour"` or `"day"`.

```
recordTweet("tweet3", 0); recordTweet("tweet3", 60); recordTweet("tweet3", 10)
getTweetCountsPerFrequency("minute", "tweet3", 0, 59)    ->  [2]
getTweetCountsPerFrequency("minute", "tweet3", 0, 60)    ->  [2, 1]
recordTweet("tweet3", 120)
getTweetCountsPerFrequency("hour", "tweet3", 0, 210)     ->  [4]
```

**Constraints:** `0 <= time, startTime, endTime <= 10^9`, `0 <= endTime
- startTime <= 10^4`, at most `10^4` calls in all.

Each arm is a `struct TweetCounts` with `fn new() -> TweetCounts`, `fn
record_tweet(mut ref self, name: Str, time: i32)` and `fn
get_tweet_counts_per_frequency(self, freq: Str, name: Str, start: i32,
end: i32) -> Vec[i32]`.

## Approaches

| file | mechanism |
|---|---|
| `tweet_counts.kara` ★ | a `Map` from each name to its times in the order recorded; a query makes one count per chunk and walks every time of the name, adding the ones in the period to the chunk `(time - start) / size`. O(1) to record, O(k) to answer for k times of the name |
| `tweet_counts_sorted.kara` | each name's times in a `SortedMap` from time to how many tweets were recorded then; a query walks only the times in the period, through `range_inclusive`. O(log k) to record, O(log k + r) to answer for r distinct times in the period |
| `tweet_counts_search.kara` | each name's times kept sorted, each new time inserted where `partition_point` puts it; a query counts each chunk as the gap between two searches, the first time at or after the chunk's start and the first after its end. O(k) to record, O(c log k) to answer for c chunks |
| `tweet_counts_log.kara` | every tweet in one list of name and time; a query walks the whole list. O(1) to record, O(N) to answer for N tweets in all |
| `tweet_counts_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<String, BTreeMap<i32, i32>>` filled through `*self.tweets.entry(tweet_name).or_insert_with(BTreeMap::new).entry(time).or_insert(0) += 1`, and a query walking `m.range(start_time..=end_time)` with `for (&t, &c)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's example (`[2] [2, 1]
[4]`); a name never recorded, a period of one second, and a tweet at the
last second, 10^9, recorded twice, counted by the day over the widest
period, 10^4 seconds, and by the minute, the 167 chunks' first and last
(`[0, 0, 0] [2] [3] 167 1 2`); 10^4 calls, the constraints' most, 5000
tweets under three names at times up to 10^4 and then 5000 queries over
periods of up to 10^4 seconds (`10^4 calls: checksum 867915163`); and
500 random sessions of 1 to 40 calls, records and queries mixed, under
two names, at times near 0 or near 10^9 (`500 random sessions: checksum
214096655`). `tweet_counts.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac __mir-run`,
`karac run` and `karac __mir-llvm-run`.

The Mend loop: the harness was written with `let names = ["alpha",
"beta", "gamma"];` and `let name = names[k];`; a list of literals is a
`Vec[String]`, and `karac check` refuses to move a `String` out of an
index (E_INDEX_MOVE_NON_COPY), with the fix, `ref names[k]`, which
`karac fix` applies. The ★ arm's `self.times[name] = Vec.new()` stored a
`Str` as a `String` key, and `karac fix` adds the `.to_string()`
(E0200). The sorted and log arms check clean. The search arm's `c as
i32` is redundant, its loop variable already an `i32` (`redundant_cast`),
and `karac fix` drops it. The Rust solution takes one round of 25 fixes
by `karac fix`'s count: the two `use std::collections::..` lines
deleted, `HashMap` and `BTreeMap` to `Map` and `SortedMap`, `<..>` to
`[..]` and `::` to `.`, `&mut self` and `&self` to `mut ref self` and
`self`, the name taken `own String` since `entry` keeps it (so the
harness passes `name.clone()`), `vec![0; n as usize]` to
`Vec.filled(n, 0i32)`, `get(&tweet_name)` to `get(tweet_name)`,
`m.range(start_time..=end_time)` to `m.range_inclusive(start_time,
end_time)`, and `for (&t, &c)` to `for (t, c)`. Every arm matches on the
first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the chunks laid out one after another from the start, each
`size` seconds or what is left before the end, and every tweet ever
recorded tested against each. 2000 cases in four kinds, 500 each, of 0
to 15 tweets under the names a and b and then 1 to 4 queries of either
name at any frequency: times and periods within 200 seconds; within
10^4, the widest period; at 0, 59, 60, 61, 119 and 120, either side of
the first minutes' edges; and at 0, 3599, 3600 and 7200, the hours'.
Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the tweets recorded in the opposite order: the same answers |
| P3 | every time and period moved up by the same amount, near 10^9: the same answers |
| P4 | each query asked by the day, one chunk since no period reaches a day: its counts' sum |
| P5 | one more tweet of a query's name at its start: that query's first chunk one higher, the rest the same |
| P6 | the ★ arm's answers |

All 60,000 checks pass on every arm: `2000 cases: checksum 523978889,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, putting each tweet straight
into its chunk, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a tweet at the start second left out | P1 708, P5 2000, P6 2832 |
| M2 | ★: a day of 8640 seconds | P1 3, P4 23, P6 12 |
| M3 | sorted: the end second left out | P1 724, P5 424, P6 724 |
| M4 | sorted: each distinct time counted once | P1 559, P5 708, P6 559 |
| M5 | search: the last chunk not cut at the end | P1 1062, P4 705, P6 1062 |
| M6 | search: each new time put last, unsorted | P1 1127, P2 1237, P5 1373, P6 1127 |
| M7 | log: every name's tweets counted | P1 1588, P6 1588 |
| M8 | log: a chunk marked, not counted | P1 1046, P4 463, P5 1466, P6 1046 |
| M9 | solution: a minute taken as an hour | P1 829, P6 829 |
| M10 | solution: a time's first tweet counted twice | P1 1584, P5 1681, P6 1584 |

P1 and P6 kill all ten, P5 six, P4 three, P2 one and P3 none. One more
tweet at each query's start (P5) catches every edit that miscounts it:
left out (M1, in every case), lost in a one-second period whose end is
its start (M3), miscounted beside an earlier tweet at the same second
(M4, M10) or in the same chunk (M8), or put out of order (M6). Asking by the day (P4) catches
the edits whose chunks do not add up to the period: a day too short to
hold 10^4 seconds (M2, only in the widest kind, so the weakest edit), a
last chunk running past the end (M5), and a chunk marked instead of
counted (M8). Only the search arm depends on the order of the records,
so reversing them (P2) catches only its unsorted insert (M6). Every
edit counts by distance from the period's start, so moving all times up
(P3) catches none; it guards a time near 10^9 against overflow, which
none of the arms risks. A wrong name (M7) and a wrong chunk size for the
minute (M9) are caught only by the statement and the other arms.

## Benchmarks

The bench records 100,000 tweets under ten names at times up to 10^6
once; then makes 10,000 rounds, each recording one more tweet and asking
one query over the constraints' widest period, 10^4 seconds, with the
name, time, start and frequency all drawn from the checksum so far, so
no answer carries over, answered by the ★ arm's walk over the name's
times, and folds every count and the round into the checksum. C keeps
the names in a small table searched with `strcmp`, Rust uses a `HashMap`,
Go a map. Every implementation prints `10000 rounds over 100000 tweets:
checksum 849888685`.

BENCHTAB
