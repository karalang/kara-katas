# LeetCode #1236 bench: the ★ arm in Python, over the same 50 webs of 1000
# urls, 4 starts and 100 passes as the Kāra bench.

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


class Site:
    def __init__(self, links):
        self.links = links

    def get_urls(self, url):
        return list(self.links.get(url, []))


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    names = ["news.yahoo.com", "news.google.com", "yahoo.com"]
    seed = [1236]
    webs = []
    for _ in range(50):
        urls = [f"http://{names[next_random(seed) % 3]}/page/{i}" for i in range(1000)]
        links = {u: [] for u in urls}
        for _ in range(5000):
            a = next_random(seed) % 1000
            b = next_random(seed) % 1000
            links[urls[a]].append(urls[b])
        webs.append((urls, Site(links)))
    check = 0
    for _ in range(100):
        for urls, web in webs:
            for s in range(4):
                check = (check * 131 + len(crawl(urls[s * 250], web))) % 1000000007
    print(f"50 webs of 1000 urls, 4 starts, 100 passes: checksum {check}")


main()
