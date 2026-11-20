# 1236. Web Crawler

Given a url `startUrl` and an interface `HtmlParser`, implement a web
crawler to crawl all links that are under the **same hostname** as
`startUrl`.

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

The judge's interface is `trait HtmlParser { fn get_urls(self, url:
String) -> Vec[String]; }`, and the arms are `fn crawl(start_url: String,
parser: dyn HtmlParser) -> Vec[String]`, the parser borrowed as a `dyn`
view (a parameter borrows by default, so `karac fix` writes LeetCode's
`ref dyn HtmlParser` without the `ref`). The harness's judge is a `struct
Site` holding each url's links in a `Map[String, Vec[String]]`, and
`get_urls` hands back a copy of a page's list. LeetCode offers no Rust
for this problem, so no arm here is carried from Rust.

## Approaches

| file | mechanism |
|---|---|
| `web_crawler.kara` ★ | a breadth-first crawl: a `VecDeque` of urls to fetch, a `Set[String]` of every url seen, and a link followed only when its hostname, the text between `"http://"` and the next `/` (`strip_prefix` and `split`), is the start's. O(urls + links) |
| `web_crawler_dfs.kara` | a depth-first crawl by recursion, each url marked in a `Set` before its links are followed, the hostname compared as the url's prefix up to the first `/` past `"http://"`, found by `find` on a `Str` view |
| `web_crawler_stack.kara` | a depth-first crawl with an explicit stack, generic over the parser (`[P: HtmlParser]`, which the `dyn` view fills), the urls seen in a `SortedSet`, whose `insert` says whether the url is new, and the hostname the third piece of the url split at `/` |
| `web_crawler_levels.kara` | a crawl by levels: each level the urls linked from the last (`flat_map` over the parser's lists), kept by a `filter` whose closure both tests the hostname, the url equal to `"http://host"` or starting with it and a `/`, and inserts into the `Set` of urls seen |
| `differential.kara` | the four arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples, sorted; the
number of urls crawled and a checksum of their text, for 1000 random
webs of 1 to 30 urls on 1 to 6 hostnames (`2223 urls crawled, checksum
492396128`); and two crawls at the constraints' top, 1000 urls on one
hostname: along a chain (`1000`) and through 2500 random links (`906`).
`web_crawler.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac run` and `karac build`, and
under the AddressSanitizer build. The crawl's answer comes out of a
`Set`, whose order is random in each process, and the harness sorts it
before printing; the stack arm's comes out of a `SortedSet` in order.

The Mend loop: the dfs and stack arms were first written with a `char`
for `find`, `find('/')`, which the fix makes `find("/")`. The ★ and stack
arms were first written walking the parser's list with a bare `for next
in parser.get_urls(url)`, which borrows each url, and pushing it onto the
queue or stack; the fix walks it with `.into_iter()`, which moves them
out. The dfs arm first passed a clone of the start to a parameter that
only borrows it, and the fix drops the `.clone()`. And `karac fix`'s style
lint writes each `parser: ref dyn HtmlParser` and `parser: ref P` as
`parser: dyn HtmlParser` and `parser: P`. The levels arm was first
written with `flat_map(|u| parser.get_urls(u))`, a closure returning the
list itself, and the fix adds `.into_iter()`; in the same round it also
cloned the `Set` of urls seen at `seen.into_iter()` after the loop, for a
spurious E0500 (below), and that clone is taken back out by hand. All
four check clean.

## Gaps

The levels arm came up against three gaps, all fixed now. Its
`level = level.iter().flat_map(..).filter(|v| .. seen.insert(..)).collect();`
was refused, E0500 "value 'seen' is moved inside a loop", at the
`seen.into_iter()` after the loop, since the checker counted a closure in
an assignment's method chain as able to run after the statement
(B-2026-11-19-36, fixed at 8c77282690). A Rust-style list of owned
strings, `["http://news.yahoo.com", ..].map(|u| u.to_string())`, got
E0236 with no fix (B-2026-11-19-35, fixed at 8c77282690), and a `dyn
HtmlParser` in a signature above the trait's declaration was refused
(B-2026-11-19-37, fixed at 516ae1c47a).

One remains. While the chain does not yet type, with the closure handing
`flat_map` a list rather than an iterator (E0200), the same E0500 comes
back beside it, and `karac fix` applies both fixes in one round: the
`.into_iter()` and a needless `seen.clone()` (B-2026-11-19-88).
With the first alone the arm checks clean, so the clone is taken out.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the matrix of links between urls of the start's hostname,
the hostname read character by character, closed under composition by
the Floyd–Warshall loop, and the urls the start reaches, for up to 40
urls. 2000 cases, a third with 1 to 12 urls, a third with 13 to 40 and a
third with 41 to 300, on 1 to 6 hostnames, with up to `3n` random links.

| | property |
|---|---|
| P1 | the statement read literally (up to 40 urls) |
| P2 | the start is crawled, and only urls of its hostname are |
| P3 | no url is crawled twice |
| P4 | every link from a crawled url to its hostname leads to a crawled url |
| P5 | each page's links listed backwards give the same urls |
| P6 | the ★ arm's urls |

All 48,000 checks pass on every arm: `2000 cases: checksum 42650607,
48000 checks over 4 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python, with the
links closed by repeated passes, gives the same checksum and the same
urls.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: the start left out | P1 1008, P2 1598, P6 4794 |
| S2 | ★: links to any hostname followed | P1 649, P2 1017, P6 3051 |
| S3 | ★: only the start's own links followed | P1 213, P4 374, P6 1122 |
| D1 | dfs: the hostname one character short | P1 173, P4 237, P6 237 |
| D2 | dfs: a url's links not followed past the first | P1 213, P4 374, P6 374 |
| D3 | dfs: a url with no path read as having an empty hostname | P1 192, P2 25, P4 241, P6 257 |
| K1 | stack: the hostname taken from the second piece | P1 450, P4 702, P6 702 |
| K2 | stack: a url pushed though already seen | HANGS |
| L1 | levels: the hostname compared as a bare prefix | P1 18, P2 35, P6 35 |
| L2 | levels: the start left out of the urls seen | P1 1008, P2 1598, P6 1598 |

All ten are caught. Nine fail P1, the statement read literally, and
P6, which fails on the other three arms too when the ★ arm is the one
mutated (S1 to S3); K2, the stack arm pushing a url it has already seen, walks a cycle
of links forever, and the run is stopped at its 25-minute limit under
both modes. The same mistake made in two arms fails the same cases: the
★ arm following only the start's own links (S3) and the dfs arm
following no url's links past the first (D2) both stop one link out, 213
cases of P1 and 374 of P4, every link from a crawled url to its hostname
leading to a crawled url. P2, the start crawled and only urls of its
hostname, catches the ★ arm that leaves out the start (S1) or follows
any hostname (S2), and the dfs arm that reads a url with no path as
having an empty hostname (D3), which from such a start follows path-less
urls of any hostname, 25 cases. It also catches the levels arm comparing
the hostname as a bare prefix (L1), which takes `http://a.b.c` for a url
of `a.b`, 35 cases, and leaving the start out of the urls seen (L2),
the same 1598 cases as S1, since the start is then crawled only when a
link leads back to it. P4 catches the five that stop a crawl
short. P3, no url crawled twice, and P5, each page's links listed
backwards, catch none: every arm keeps the urls it has seen in a set,
and no mutation here depends on the order of a page's links.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, a breadth-first crawl with a queue and a `Set` of every url seen, a
link followed only when its hostname is the start's. Every program
prints `50 webs of 1000 urls, 4 starts, 100 passes: checksum 35333735`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 3.217 to 3.607 s | 3.481 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 3.253 to 3.590 s | 3.430 s |
| Rust (`rustc -O`) | 2.445 to 2.782 s | 2.611 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.499 to 2.837 s | 2.649 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 2.427 to 2.716 s | 2.674 s |
| C (`clang -O3`) | 1.960 to 2.350 s | 2.147 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.977 to 2.641 s | 2.236 s |
| Go | 1.914 to 2.454 s | 2.127 s |
| Python | 5.054 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 23% ahead of Kāra (2.649 s
against 3.430 s). Kāra takes about 1.6x C's time (3.430 s against 2.147
s); Kāra takes about 1.6x Go's time (3.430 s against 2.127 s). Kāra is
about 32% ahead of Python (3.430 s against 5.054 s). No profile was
taken.
