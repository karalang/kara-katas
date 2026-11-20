# LeetCode #1268 bench, in Python: the ★ arm (the products sorted, a binary
# search for each prefix typed, and up to three products from there that
# start with it) on 100 random lists of 1000 words of 1 to 10 letters from
# `a` to `d` built once, each searched for its own 20-letter word, 100
# rounds; every suggestion folded into a checksum.
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


seed = 1268


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(longest):
    n = next_random() % longest + 1
    return "".join(chr(ord("a") + next_random() % 4) for _ in range(n))


lists, searches = [], []
for _ in range(100):
    lists.append([random_word(10) for _ in range(1000)])
    searches.append("".join(chr(ord("a") + next_random() % 4) for _ in range(20)))
check = 0
for rnd in range(100):
    for l in range(100):
        for lst in suggested_products(lists[l], searches[l]):
            check = (check * 131 + len(lst) + rnd) % 1000000007
            for w in lst:
                for b in w.encode():
                    check = (check * 131 + b) % 1000000007
print(f"100 rounds of 100 searches among 1000 words: checksum {check}")
