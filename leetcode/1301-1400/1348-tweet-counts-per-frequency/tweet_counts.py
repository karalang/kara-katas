# LeetCode #1348 -- Python mirror of the ★ arm: each name's times in the
# order they were recorded; a query walks them all into per-chunk counts.

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


seed = [0]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def fold(check, counts):
    c = (check * 131 + len(counts)) % 1000000007
    for n in counts:
        c = (c * 131 + n) % 1000000007
    return c


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    tc = TweetCounts()
    tc.record_tweet("tweet3", 0)
    tc.record_tweet("tweet3", 60)
    tc.record_tweet("tweet3", 10)
    q1 = tc.get_tweet_counts_per_frequency("minute", "tweet3", 0, 59)
    q2 = tc.get_tweet_counts_per_frequency("minute", "tweet3", 0, 60)
    tc.record_tweet("tweet3", 120)
    q3 = tc.get_tweet_counts_per_frequency("hour", "tweet3", 0, 210)
    print(show(q1), show(q2), show(q3))
    tc = TweetCounts()
    tc.record_tweet("late", 1000000000)
    tc.record_tweet("late", 1000000000)
    tc.record_tweet("late", 999990000)
    none = tc.get_tweet_counts_per_frequency("minute", "nobody", 0, 120)
    one = tc.get_tweet_counts_per_frequency("hour", "late", 1000000000, 1000000000)
    day = tc.get_tweet_counts_per_frequency("day", "late", 999990000, 1000000000)
    minutes = tc.get_tweet_counts_per_frequency("minute", "late", 999990000, 1000000000)
    print(show(none), show(one), show(day), len(minutes), minutes[0], minutes[166])
    seed[0] = 1348
    names = ["alpha", "beta", "gamma"]
    freqs = ["minute", "hour", "day"]
    tc = TweetCounts()
    for _ in range(5000):
        name = names[next_random() % 3]
        tc.record_tweet(name, next_random() % 10001)
    check = 0
    for _ in range(5000):
        freq = freqs[next_random() % 3]
        name = names[next_random() % 3]
        start = next_random() % 10001
        end = start + next_random() % 10001
        check = fold(check, tc.get_tweet_counts_per_frequency(freq, name, start, end))
    print(f"10^4 calls: checksum {check}")
    check = 0
    for c in range(500):
        base = 0 if c % 2 == 0 else 1000000000 - 5000
        tc = TweetCounts()
        calls = 1 + next_random() % 40
        for _ in range(calls):
            name = names[next_random() % 2]
            if next_random() % 3 < 2:
                tc.record_tweet(name, base + next_random() % 5001)
            else:
                freq = freqs[next_random() % 3]
                start = base + next_random() % 5001
                end = min(start + next_random() % 300, base + 5000)
                check = fold(check, tc.get_tweet_counts_per_frequency(freq, name, start, end))
    print(f"500 random sessions: checksum {check}")


main()
