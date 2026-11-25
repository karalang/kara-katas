# LeetCode #1348 bench -- Python: each name's times in the order recorded;
# a query walks them all into per-chunk counts.

SIZE = {"minute": 60, "hour": 3600, "day": 86400}


class TweetCounts:
    def __init__(self):
        self.times = {}

    def record_tweet(self, name, time):
        self.times.setdefault(name, []).append(time)

    def get_tweet_counts_per_frequency(self, freq, name, start, end):
        size = SIZE[freq]
        counts = [0] * ((end - start) // size + 1)
        for t in self.times.get(name, []):
            if start <= t <= end:
                counts[(t - start) // size] += 1
        return counts


def main():
    names = ["n%d" % i for i in range(10)]
    freqs = ["minute", "hour", "day"]
    seed = 1348
    tc = TweetCounts()
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        name = names[(seed // 65536) % 10]
        seed = (seed * 1103515245 + 12345) % 2147483648
        tc.record_tweet(name, (seed // 65536) % 1000001)
    check = 0
    for r in range(10000):
        tc.record_tweet(names[check % 10], check % 1000001)
        start = (check // 11) % 990001
        counts = tc.get_tweet_counts_per_frequency(freqs[(check // 13) % 3], names[(check // 17) % 10], start, start + 10000)
        for n in counts:
            check = (check * 31 + n) % 1000000007
        check = (check * 31 + r) % 1000000007
    print(f"10000 rounds over 100000 tweets: checksum {check}")


main()
