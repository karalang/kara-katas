# LeetCode #535: Encode and Decode TinyURL -- a counter written in base
# 62. Mirrors encode_and_decode_tinyurl.kara and its harness.

PREFIX = "http://tinyurl.com/"


def digit(d):
    if d < 10:
        return chr(ord("0") + d)
    if d < 36:
        return chr(ord("a") + d - 10)
    return chr(ord("A") + d - 36)


def base62(n):
    rev = []
    m = n
    while True:
        rev.append(digit(m % 62))
        m //= 62
        if m == 0:
            break
    return "".join(reversed(rev))


class Codec:
    def __init__(self):
        self.by_code = {}
        self.by_url = {}
        self.next = 0

    def encode(self, long_url):
        code = self.by_url.get(long_url)
        if code is None:
            code = base62(self.next)
            self.next += 1
            self.by_code[code] = long_url
            self.by_url[long_url] = code
        return PREFIX + code

    def decode(self, short_url):
        return self.by_code[short_url[len(PREFIX):]]


# ---- test harness

class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_url(rng, most):
    marks = "/-_.?=&"
    out = ["https://"]
    host = 3 + rng.next() % 8
    for _ in range(host):
        out.append(chr(ord("a") + rng.next() % 26))
    out.append(".com/")
    path = rng.next() % (most + 1)
    for _ in range(path):
        k = rng.next() % 69
        if k < 26:
            out.append(chr(ord("a") + k))
        elif k < 52:
            out.append(chr(ord("A") + k - 26))
        elif k < 62:
            out.append(chr(ord("0") + k - 52))
        else:
            out.append(marks[k - 62])
    return "".join(out)


def sum_of(s, start):
    h = start
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def well_formed(short):
    if not short.startswith(PREFIX) or len(short) == len(PREFIX):
        return False
    return all(c.isascii() and c.isalnum() for c in short[len(PREFIX):])


def b(x):
    return "true" if x else "false"


def run(urls, rng):
    codec = Codec()
    shorts = [codec.encode(u) for u in urls]
    n = len(urls)
    order = list(range(n))
    for i in range(n - 1, 0, -1):
        j = rng.next() % (i + 1)
        order[i], order[j] = order[j], order[i]
    right = 0
    checksum = 0
    for i in order:
        back = codec.decode(shorts[i])
        if back == urls[i]:
            right += 1
        checksum = sum_of(back, checksum)
    owner = {}
    distinct = True
    formed = True
    for i in range(n):
        if shorts[i] in owner:
            if owner[shorts[i]] != urls[i]:
                distinct = False
        else:
            owner[shorts[i]] = urls[i]
        if not well_formed(shorts[i]):
            formed = False
    return f"{right} of {n} back, distinct {b(distinct)}, well formed {b(formed)}, checksum {checksum}"


def main():
    url = "https://leetcode.com/problems/design-tinyurl"
    codec = Codec()
    short = codec.encode(url)
    print(f"{url} -> back {codec.decode(short)}")
    again = codec.encode(url)
    print(f"encoded twice: back {b(codec.decode(short) == url)} and {b(codec.decode(again) == url)}")
    first = Codec()
    second = Codec()
    a = first.encode("https://a.com/x")
    bb = second.encode("https://b.com/y")
    c = first.encode("https://c.com/z")
    print(f"two codecs: {first.decode(a)} {second.decode(bb)} {first.decode(c)}")
    rng = Rng(535)
    close = ["https://x.com/" + p for p in ["AaAa", "AaBB", "BBAa", "BBBB", "Aa", "BB"]]
    print(f"Aa for BB: {run(close, rng)}")
    print(f"shortest: {run(['h://a'], rng)}")
    long = ["https://long.com/"]
    length = len(long[0])
    while length < 10000:
        long.append(chr(ord("a") + rng.next() % 26))
        length += 1
    print(f"10000 characters: {run([''.join(long)], rng)}")
    total = 0
    count = 0
    checksum = 0
    all_distinct = True
    all_formed = True
    for _ in range(300):
        n = 1 + rng.next() % 40
        count += n
        urls = []
        for _ in range(n):
            kind = rng.next() % 4
            if kind == 0 and urls:
                j = rng.next() % len(urls)
                urls.append(urls[j])
            elif kind == 1 and urls:
                j = rng.next() % len(urls)
                u = urls[j]
                if u.endswith("Aa"):
                    urls.append(u[:-2] + "BB")
                elif u.endswith("BB"):
                    urls.append(u[:-2] + "Aa")
                else:
                    urls.append(u + "Aa")
            else:
                urls.append(random_url(rng, 60))
        codec = Codec()
        shorts = [codec.encode(u) for u in urls]
        for i in range(n):
            back = codec.decode(shorts[i])
            if back == urls[i]:
                total += 1
            checksum = sum_of(back, checksum)
            if not well_formed(shorts[i]):
                all_formed = False
            for j in range(i):
                if shorts[j] == shorts[i] and urls[j] != urls[i]:
                    all_distinct = False
    print(f"300 random rounds: {total} of {count} back, distinct {b(all_distinct)}, well formed {b(all_formed)}, checksum {checksum}")
    urls = []
    for i in range(10000):
        if i % 5 == 4:
            j = rng.next() % len(urls)
            urls.append(urls[j])
        else:
            urls.append(random_url(rng, 200))
    print(f"10000 URLs: {run(urls, rng)}")


main()
