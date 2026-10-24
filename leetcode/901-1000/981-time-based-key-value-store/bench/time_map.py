# Benchmark: LeetCode #981 Time Based Key-Value Store -- the ★ arm, a
# list per key and binary search, on LeetCode's largest sessions of
# 200,000 calls. Mirrors time_map.kara, .rs, .c and go-seq/.


class TimeMap:
    def __init__(self):
        self.store = {}

    def set(self, key, value, timestamp):
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key, timestamp):
        lst = self.store.get(key)
        if lst is None:
            return ""
        lo, hi = 0, len(lst)
        while lo < hi:
            mid = (lo + hi) // 2
            if lst[mid][0] <= timestamp:
                lo = mid + 1
            else:
                hi = mid
        return "" if lo == 0 else lst[lo - 1][1]


seed = 981


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 20
    calls = 200000
    keys = [f"user{i * 7919 % 100000}" for i in range(1000)]
    values = [f"value{i * 104729 % 1000000}" for i in range(100)]
    found = 0
    check = 0
    for _ in range(rounds):
        tm = TimeMap()
        now = 0
        for _ in range(calls):
            k = next_random() % 1000
            if next_random() % 2 == 0:
                now += 1 + next_random() % 3
                tm.set(keys[k], values[next_random() % 100], now)
            else:
                t = 1 + next_random() % (now + 3)
                got = tm.get(keys[k], t)
                if len(got) > 0:
                    found += 1
                check = (check * 131 + len(got)) % 1000000007
                for b in got.encode():
                    check = (check * 131 + b) % 1000000007
    print(f"{rounds} rounds of {calls} calls on 1000 keys: {found} values found, checksum {check}")


main()
