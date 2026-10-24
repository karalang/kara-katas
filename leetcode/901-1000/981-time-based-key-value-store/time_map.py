# LeetCode #981: Time Based Key-Value Store -- mirror of the ★ arm
# (time_map.kara), a list per key, binary search.


class TimeMap:
    def __init__(self):
        self.store = {}

    def set(self, key, value, timestamp):
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key, timestamp):
        lst = self.store.get(key)
        if lst is None:
            return ""
        # the first place whose timestamp is after the one asked
        lo, hi = 0, len(lst)
        while lo < hi:
            mid = (lo + hi) // 2
            if lst[mid][0] <= timestamp:
                lo = mid + 1
            else:
                hi = mid
        return "" if lo == 0 else lst[lo - 1][1]


# ---- test harness ---------------------------------------------------------

seed = 981


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, s):
    b = s.encode()
    h = (check * 131 + len(b)) % 1000000007
    for x in b:
        h = (h * 131 + x) % 1000000007
    return h


def session(ops, keys):
    names = ["foo", "bar", "love", "high", "low", "k", "key2", "zz"]
    words = ["bar", "bar2", "high", "low", "x", "", "v"]
    tm = TimeMap()
    now = 0
    found = 0
    check = 0
    for _ in range(ops):
        key = names[next_random() % keys]
        if next_random() % 2 == 0:
            now += 1 + next_random() % 3
            value = f"{words[next_random() % len(words)]}{now % 7}"
            tm.set(key, value, now)
        else:
            t = 1 + next_random() % (now + 3)
            got = tm.get(key, t)
            if len(got) > 0:
                found += 1
            check = fold(check, got)
    return found, check


def main():
    tm = TimeMap()
    tm.set("foo", "bar", 1)
    print(f"get(foo, 1) = {tm.get('foo', 1)}")
    print(f"get(foo, 3) = {tm.get('foo', 3)}")
    tm.set("foo", "bar2", 4)
    print(f"get(foo, 4) = {tm.get('foo', 4)}")
    print(f"get(foo, 5) = {tm.get('foo', 5)}")
    print(f"get(foo, 0) = [{tm.get('foo', 0)}]")
    print(f"get(bar, 9) = [{tm.get('bar', 9)}]")
    tm.set("love", "high", 10)
    tm.set("love", "low", 20)
    print(f"get(love, 5) = [{tm.get('love', 5)}]")
    print(f"get(love, 10) = {tm.get('love', 10)}")
    print(f"get(love, 15) = {tm.get('love', 15)}")
    print(f"get(love, 20) = {tm.get('love', 20)}")
    print(f"get(love, 25) = {tm.get('love', 25)}")
    print(f"get(foo, 25) = {tm.get('foo', 25)}")
    for count, ops in [(300, 12), (3000, 60), (4, 3000)]:
        found = 0
        check = 0
        for _ in range(count):
            keys = 2 if count == 300 else 1 + next_random() % 8
            f, c = session(ops, keys)
            found += f
            check = (check * 31 + c) % 1000000007
        print(f"{count} random sessions of {ops} operations: {found} values found, checksum {check}")


main()
