# 1242. Web Crawler Multithreaded

Given a url `startUrl` and an interface `HtmlParser`, implement a
**multi-threaded** web crawler to crawl all links that are under the
**same hostname** as `startUrl`.

Return all urls obtained by your web crawler in **any** order.

Your crawler should:

- Start from the page `startUrl`.
- Call `HtmlParser.getUrls(url)` to get all urls from a webpage of a
  given url.
- Not crawl the same link twice.
- Explore only the links that are under the **same hostname** as
  `startUrl`.

The hostname of `http://example.org/foo/bar` is `example.org`. Every url
is in the format `http://` followed by its hostname and an optional
path, and every link a page holds is to another url of the same web.

`getUrls(url)` simulates an HTTP request: treat it as a blocking call
that waits for the request to finish. Single-threaded solutions exceed
the time limit, so the crawl should fetch several pages at once.

```
urls = ["http://news.yahoo.com", "http://news.yahoo.com/news", "http://news.yahoo.com/news/topics/",
        "http://news.google.com", "http://news.yahoo.com/us"]
edges = [[2,0],[2,1],[3,2],[3,1],[0,4]], startUrl = "http://news.yahoo.com/news/topics/"
  ->  ["http://news.yahoo.com", "http://news.yahoo.com/news", "http://news.yahoo.com/news/topics/", "http://news.yahoo.com/us"]
edges = [[0,2],[2,1],[3,2],[3,1],[3,0]], startUrl = "http://news.google.com"
  ->  ["http://news.google.com"]
```

`edges[i] = [from, to]` means the page `urls[from]` links to `urls[to]`.
The judge knows the urls and edges; the crawler sees only `getUrls`.

**Constraints:** `1 <= urls.length <= 1000`; `1 <= urls[i].length <=
300`; `startUrl` is one of the urls; a hostname is 1 to 63 characters of
letters, digits and `-`, in labels joined by `.`; no url holds a port,
and no url ends in a query.

**Follow up:** with 10,000 nodes and a billion urls, each node running
the same code and unable to talk to the others, how would the crawl be
split, kept from crawling a url twice, and kept going when a node
fails? And how would it know it is done?

The judge's interface is `trait HtmlParser { fn get_urls(self, url:
String) -> Vec[String]; }`, which a task may call: the arms take the
parser as `dyn HtmlParser + CrossTask` (a `dyn` value may cross a task
only when its concrete type is `CrossTask`, design.md § `dyn Trait`). The harness's judge is the
one 1236 uses, a `struct Site` holding each url's links in a
`Map[String, Vec[String]]`, and its `get_urls` returns at once; nothing
here measures the speedup of fetching in parallel, only that each arm
crawls the same urls whatever order its tasks run in. LeetCode offers no
Rust for this problem, so no arm here is carried from Rust.

## Approaches

| file | mechanism |
|---|---|
| `web_crawler_multithreaded.kara` ★ | a crawl by levels: each level's pages fetched by one task each in a `TaskGroup`, the handles joined in the level's order, and the links of the start's hostname not seen before making the next level. The group lives in an inner block, so it joins its tasks before the next level is built (core semantics §9.5) |
| `web_crawler_multithreaded_par.kara` | the same levels with `par for`, whose value is the `Vec` of the pages' link lists in the level's order, then a `flat_map` and a `filter` that tests the hostname and inserts into the `Set` of urls seen. The parser is a `dyn` parameter, and the `par for` is checked with the parser each caller passes |
| `web_crawler_multithreaded_chan.kara` | a task per url and one channel back: each task sends its page's links on a clone of one `Sender`; the calling task receives them, spawns a task for each new url of the start's hostname, and counts the pages still out |
| `web_crawler_multithreaded_pool.kara` | a fixed pool of four workers, each owning the receiving end of its own request channel and answering on one shared reply channel with its number and the page's links; the calling task keeps the urls still to fetch in a `VecDeque` and hands one to each idle worker, so no channel holds more than one message per worker, and dropping the request senders ends the workers' loops |
| `differential.kara` | the four arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples, sorted; the
number of urls crawled and a checksum of their text, for 1000 random
webs of 1 to 30 urls on 1 to 6 hostnames (`2132 urls crawled, checksum
732003344`); and two crawls at the constraints' top, 1000 urls on one
hostname: along a chain (`1000`) and through 2500 random links (`906`).
`web_crawler_multithreaded.py` mirrors the levels arms with a
`ThreadPoolExecutor`, and its output is byte-identical. Every arm gives
the same output under `karac run` and `karac build`. The crawl's answer
comes out of a `Set`, whose order is random in each process, and the
harness sorts it before printing.

The Mend loop: the ★ arm was first written with Rust's `vec![..]`, `!`
and `&&`, and walking the handles and each page's list with a bare
`for`, which borrows; the fix writes `[..]`, `not` and `and`, adds
`.into_iter()` to both loops, and adds `+ CrossTask` to the parser's
type, which a task may not capture without it. It then checks with one
error, E0516 at `level = next_level`: the group, declared in the loop
body, holds its tasks' borrows of `level` until it drops at the body's
end. The message advised a clone, which does not end the borrow; it now
says the group holds the borrow until it drops and joins its tasks, and
to put the group in an inner block that ends first
(B-2026-11-19-112), which is the repair, by hand. The par arm was
first written with `dyn HtmlParser` and `.into_iter().flatten()`;
`flatten` needs items that are themselves iterators, and its E0200 says
to write `.flat_map(|v| v.into_iter())` but carries no edit, so that is
by hand, and beside it came a spurious E0500 whose fix clones the `Set`
of urls seen (B-2026-11-19-88, filed from kata 1236), taken back out by hand.
A `par for` over a `dyn` parameter was then refused (below, fixed now). The pool arm was first written
handing `start_url`, a borrowed parameter, to `send`; the fix makes it
`own String`, which ripples out to the harness's calls as `.clone()`s.
Its walk of a page's list with a bare `for`, sending each url, got
E0509 (a view of the list stored in a channel) with no edit, and
`.into_iter()` was by hand; `karac fix` now adds it when nothing names
the list after the loop (B-2026-11-19-111). That first pool sent every new url to the
next worker in turn, on channels of 64, and deadlocked on the random web
of 1000 urls: the calling task blocked sending to a full worker while
that worker blocked sending its reply to the calling task. The runtime
reported it (`deadlock: every task waits on a channel that no running
task sends to or receives from`, at the send), and the arm was
rewritten with the idle list. All four check clean.

## Gaps

Six gaps were met writing and probing these arms; five are fixed now.

- **A task borrowed a `for` binding** (B-2026-11-19-107, fixed at
  b03a13d177). The chan arm's natural form spawns a task per url straight
  from the loop over a page's links, `for next in links.into_iter() { ..
  group.spawn(|| back.send(parser.get_urls(next))); }`. Core semantics
  §9.5 moves a captured place that drops before the group into the task,
  and a loop's binding drops at the end of each iteration, but the
  binding of a `for`, `while let`, `if let` or `match` arm was borrowed,
  for E0516 at the loop. A `let url = next;` in the body checked clean.
- **A `par for` through a `dyn` parameter ignored the effects its type
  declares** (B-2026-11-19-108, fixed at 6dd4c8f6fc). Over a parameter
  of type `dyn HtmlParser + CrossTask with ()`, or of a trait whose
  method writes its own clause, two iterations were said to conflict on
  `calls(p2.get_urls)`.
- **With neither clause, as the judge's interface is written, a `par
  for` through a `dyn` parameter was refused** (B-2026-11-19-109,
  fixed at 77f1c15163), where the same loop over a generic parameter is
  checked per instance and accepted. A parameter that does not escape
  has the effects of the value passed (design.md § `dyn Trait`), and the
  loop is now checked with what each caller passes: the par arm takes
  `dyn HtmlParser + CrossTask` again, and a caller passing a parser whose
  `get_urls` writes a resource is refused, naming the caller.
- **A `par for` at a function's tail was read as a statement**
  (B-2026-11-19-110, fixed at 7980991545). The par arm's level
  written as a helper, `fn pages(..) -> Vec[Vec[String]] { par for url in
  level.iter() { parser.get_urls(url) } }`, got E0213 "this block has no
  value".
- The E0516 advice and the missing E0509 edit above
  (B-2026-11-19-112 and B-2026-11-19-111, fixed at
  cec16d44a9).

One remains open. The pool arm's `karac build` binary sometimes stops
with a false "deadlock: every task waits on a channel that no running
task sends to or receives from", 10 runs in 300 (and the differential 1
in 6), though no task can wait forever: a worker loops on its request
channel's `recv` until the calling task drops the senders. Reduced, a
task draining a channel its spawner sends one value on and drops, run
10,000 times, fails in every build run and never under `karac
__mir-run` (B-2026-11-19-64).

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, the closure of the matrix of links between urls of the
start's hostname, from kata 1236's differential, for up to 40 urls.
2000 cases, a third with 1 to 12 urls, a third with 13 to 40 and a third
with 41 to 300, on 1 to 6 hostnames, with up to `3n` random links.

| | property |
|---|---|
| P1 | the statement read literally (up to 40 urls) |
| P2 | the start is crawled, and only urls of its hostname are |
| P3 | no url is crawled twice |
| P4 | every link from a crawled url to its hostname leads to a crawled url |
| P5 | each page's links listed backwards give the same urls |
| P6 | the ★ arm's urls |

All 48,000 checks pass on every arm: `2000 cases: checksum 990117476,
48000 checks over 4 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac build` (but for the pool arm's false deadlock, above).

## Mutation testing

Five edits to the differential, at least one to each arm, each run under
`karac __mir-run`.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: links to any hostname followed | P1 654, P2 1026, P6 3078 |
| M2 | par: each level's last page not fetched | P1 428, P4 691, P6 691 |
| M3 | chan: the first reply taken and no more awaited | P1 428, P4 691, P6 691 |
| M4 | pool: the crawl ends with one worker still busy | P1 63, P4 107, P5 133, P6 107 |
| M5 | chan: the hostname compared as a bare prefix | P1 12, P2 33, P6 33 |

All five are caught, and each fails P1, the statement read literally.
M2 and M3 fail the same cases: both crawl the start alone (M2 fetches no
page of the first level, which holds only the start), so each misses
whatever the start links to. P4 catches the three that stop a crawl
short. M4 is the one whose failures depend on the order the tasks run
in: the last reply it leaves unread is whichever worker finishes last,
so P5, the same web with each page's links listed backwards, fails
where the two crawls end differently; a `karac build` run of it gave P1
63, P4 108, P5 111, P6 108. P2 catches the arms that cross to another
hostname (M1, and M5, which takes `http://a.b.c` for a url of `a.b`).
P3 catches none: every arm keeps the urls it has seen in a `Set`.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm (a crawl by levels, each level's pages fetched by one task each in a
`TaskGroup`, the handles joined in order) on 50 random webs of 1000 urls
on 3 hostnames with 5000 links each, built once, crawled from 4 starts
each, 10 passes. The parser answers at once, so this measures what a
task per page costs. Every program prints `50 webs of 1000 urls, 4
starts, 10 passes: checksum 938861813`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.228 to 1.411 s | 1.308 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.197 to 1.429 s | 1.295 s |
| Rust (`rustc -O`) | 3.981 to 6.170 s | 4.776 s |
| Rust (`rustc -O -C overflow-checks=on`) | 4.305 to 5.535 s | 4.619 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 4.220 to 5.244 s | 4.588 s |
| C (`clang -O3`) | 4.305 to 4.867 s | 4.500 s |
| C (`clang -O3 -march=x86-64-v3`) | 4.240 to 5.049 s | 4.407 s |
| Go | 0.609 to 0.836 s | 0.670 s |
| Python | 13.53 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on takes about 3.6x Kāra's time. C
takes about 3.5x Kāra's time; Kāra takes about 1.9x Go's time (1.295 s
against 0.670 s). Python takes about 10x Kāra's time. No profile was
taken.
