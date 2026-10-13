# Benchmark for #535: the star arm (a counter written in base 62); see
# ../README.md section Benchmarks. Mirrors encode_and_decode_tinyurl.kara.

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


def main():
    rng = Rng(535)
    urls = []
    for i in range(20000):
        if i % 5 == 4:
            urls.append(urls[rng.next() % len(urls)])
        else:
            urls.append(random_url(rng, 100))
    rounds = 50
    right = 0
    length = 0
    for _ in range(rounds):
        codec = Codec()
        shorts = []
        for u in urls:
            s = codec.encode(u)
            length += len(s)
            shorts.append(s)
        for i in range(len(urls)):
            if codec.decode(shorts[i]) == urls[i]:
                right += 1
    print(f"{len(urls)} URLs, {rounds} rounds: {right} back, short length {length}")


main()
