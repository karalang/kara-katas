# LeetCode #1236: Web Crawler -- Python mirror of the ★ arm: a
# breadth-first crawl with a queue and a set of every url seen, a link
# followed only when its hostname is the start's.

from collections import deque


def hostname(url):
    return url[len("http://"):].split("/")[0]


def crawl(start_url, parser):
    host = hostname(start_url)
    seen = {start_url}
    queue = deque([start_url])
    while queue:
        url = queue.popleft()
        for nxt in parser.get_urls(url):
            if hostname(nxt) == host and nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return list(seen)


# ---- test harness ---------------------------------------------------------

class Site:
    def __init__(self, urls, edges):
        self.links = {u: [] for u in urls}
        for a, b in edges:
            self.links[urls[a]].append(urls[b])

    def get_urls(self, url):
        return list(self.links.get(url, []))


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_site(n, hosts, m, seed):
    names = ["news.yahoo.com", "news.google.com", "yahoo.com", "a.b", "a.b.c", "x-1.org"]
    urls, have = [], set()
    while len(urls) < n:
        url = f"http://{names[next_random(seed) % hosts]}"
        for _ in range(next_random(seed) % 4):
            url += "/" + ["news", "us", "topics", "a", "b"][next_random(seed) % 5]
            if next_random(seed) % 2 == 0:
                url += str(next_random(seed) % 10)
        if next_random(seed) % 4 == 0:
            url += "/"
        if url not in have:
            have.add(url)
            urls.append(url)
    edges = []
    for _ in range(m):
        a = next_random(seed) % n
        edges.append((a, next_random(seed) % n))
    return urls, edges


def crawled(start, web):
    return sorted(crawl(start, web))


def show(v):
    return "[" + ", ".join(v) + "]"


def main():
    urls = ["http://news.yahoo.com", "http://news.yahoo.com/news", "http://news.yahoo.com/news/topics/", "http://news.google.com", "http://news.yahoo.com/us"]
    print(show(crawled(urls[2], Site(urls, [(2, 0), (2, 1), (3, 2), (3, 1), (0, 4)]))))
    print(show(crawled(urls[3], Site(urls, [(0, 2), (2, 1), (3, 2), (3, 1), (3, 0)]))))
    seed = [1236]
    check = 0
    total = 0
    for _ in range(1000):
        n = next_random(seed) % 30 + 1
        hosts = next_random(seed) % 6 + 1
        u, e = random_site(n, hosts, next_random(seed) % (3 * n), seed)
        got = crawled(u[next_random(seed) % n], Site(u, e))
        total += len(got)
        for url in got:
            for b in url.encode():
                check = (check * 131 + b) % 1000000007
    print(f"1000 random webs: {total} urls crawled, checksum {check}")
    chain = [f"http://kara.dev/page/{i}" for i in range(1000)]
    chained = crawled(chain[0], Site(chain, [(i, i + 1) for i in range(999)]))
    u, e = random_site(1000, 1, 2500, seed)
    wide = crawled(u[0], Site(u, e))
    print(f"1000 urls: {len(chained)} along a chain, {len(wide)} of a random web")


main()
