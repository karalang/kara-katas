# LeetCode #1268: Search Suggestions System -- Python mirror of the ★ arm
# (the products sorted, a binary search for each prefix, and up to three
# products from there that start with it), with the same harness.
from bisect import bisect_left


def suggested_products(products, search_word):
    s = sorted(products)
    out = []
    for end in range(1, len(search_word) + 1):
        prefix = search_word[:end]
        i = bisect_left(s, prefix)
        lst = []
        while i < len(s) and len(lst) < 3 and s[i].startswith(prefix):
            lst.append(s[i])
            i += 1
        out.append(lst)
    return out


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_word(longest, letters, rng):
    n = rng.next() % longest + 1
    return "".join(chr(97 + rng.next() % letters) for _ in range(n))


def random_products(n, longest, letters, rng):
    seen = set()
    out = []
    while len(out) < n:
        w = random_word(longest, letters, rng)
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out


def fold(check, lists):
    for lst in lists:
        check = (check * 131 + len(lst)) % 1000000007
        for w in lst:
            for b in w.encode():
                check = (check * 131 + b) % 1000000007
    return check


def show(lists):
    return "[" + ", ".join("[" + ", ".join(l) + "]" for l in lists) + "]"


def main():
    print(show(suggested_products(["mobile", "mouse", "moneypot", "monitor", "mousepad"], "mouse")))
    print(show(suggested_products(["havana"], "havana")))
    print(show(suggested_products(["bags", "baggage", "banner", "box", "cloths"], "bags")))
    rng = Rng(1268)
    shown = check = 0
    for _ in range(1000):
        n = rng.next() % 40 + 1
        letters = rng.next() % 3 + 2
        products = random_products(n, 6, letters, rng)
        search = random_word(7, letters, rng)
        got = suggested_products(products, search)
        shown += sum(len(l) for l in got)
        check = fold(check, got)
    print(f"1000 random searches: {shown} suggestions, checksum {check}")
    products = random_products(1000, 20, 3, rng)
    search = products[0]
    while len(search) < 1000:
        search += chr(97 + rng.next() % 3)
    got = suggested_products(products, search)
    lens = [len(l) for l in got[:12]]
    print(f"{len(got)} lists, the first sizes [{', '.join(map(str, lens))}], checksum {fold(0, got)}")


main()
