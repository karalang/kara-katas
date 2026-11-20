# LeetCode #1242: Web Crawler Multithreaded -- Python mirror of the Kara
# kata: a crawl by levels, every page of a level fetched on a thread pool,
# the links filtered to the start's hostname and the urls not seen before.
from concurrent.futures import ThreadPoolExecutor


class Site:
    def __init__(self, urls, edges):
        self.links = {u: [] for u in urls}
        for a, b in edges:
            self.links[urls[a]].append(urls[b])

    def get_urls(self, url):
        return list(self.links.get(url, []))


def hostname(url):
    return url[len("http://"):].split("/")[0]


def crawl(start_url, parser):
    host = hostname(start_url)
    seen = {start_url}
    level = [start_url]
    with ThreadPoolExecutor(max_workers=8) as pool:
        while level:
            pages = list(pool.map(parser.get_urls, level))
            nxt = []
            for links in pages:
                for u in links:
                    if hostname(u) == host and u not in seen:
                        seen.add(u)
                        nxt.append(u)
            level = nxt
    return list(seen)


SEED = [0]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def random_site(n, hosts, m):
    names = ["news.yahoo.com", "news.google.com", "yahoo.com", "a.b", "a.b.c", "x-1.org"]
    urls, have = [], set()
    while len(urls) < n:
        url = "http://" + names[next_random() % hosts]
        for _ in range(next_random() % 4):
            url += "/" + ["news", "us", "topics", "a", "b"][next_random() % 5]
            if next_random() % 2 == 0:
                url += str(next_random() % 10)
        if next_random() % 4 == 0:
            url += "/"
        if url not in have:
            have.add(url)
            urls.append(url)
    edges = []
    for _ in range(m):
        a = next_random() % n
        b = next_random() % n
        edges.append((a, b))
    return urls, edges


def crawled(start, web):
    return sorted(crawl(start, web))


def show(v):
    return "[" + ", ".join(v) + "]"


def main():
    urls = ["http://news.yahoo.com", "http://news.yahoo.com/news",
            "http://news.yahoo.com/news/topics/", "http://news.google.com",
            "http://news.yahoo.com/us"]
    print(show(crawled(urls[2], Site(urls, [(2, 0), (2, 1), (3, 2), (3, 1), (0, 4)]))))
    print(show(crawled(urls[3], Site(urls, [(0, 2), (2, 1), (3, 2), (3, 1), (3, 0)]))))
    SEED[0] = 1242
    check = total = 0
    for _ in range(1000):
        n = next_random() % 30 + 1
        hosts = next_random() % 6 + 1
        m = next_random() % (3 * n)
        u, e = random_site(n, hosts, m)
        got = crawled(u[next_random() % n], Site(u, e))
        total += len(got)
        for url in got:
            for b in url.encode():
                check = (check * 131 + b) % 1000000007
    print(f"1000 random webs: {total} urls crawled, checksum {check}")
    chain = [f"http://kara.dev/page/{i}" for i in range(1000)]
    chained = crawled(chain[0], Site(chain, [(i, i + 1) for i in range(999)]))
    u, e = random_site(1000, 1, 2500)
    wide = crawled(u[0], Site(u, e))
    print(f"1000 urls: {len(chained)} along a chain, {len(wide)} of a random web")


main()
