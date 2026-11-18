# LeetCode #1606: Find Servers That Handled Most Number of Requests -- the
# Python mirror of servers.kara (the ★ arm): the free servers kept sorted
# (a list with bisect, where Kāra has a SortedSet), the busy ones in a
# heap. Its output is byte-identical to the Kāra arms'.
import bisect
import heapq


def busiest_servers(k, arrival, load):
    free = list(range(k))
    busy = []
    handled = [0] * k
    for i, now in enumerate(arrival):
        while busy and busy[0][0] <= now:
            _, s = heapq.heappop(busy)
            bisect.insort(free, s)
        if free:
            j = bisect.bisect_left(free, i % k)
            if j == len(free):
                j = 0
            s = free.pop(j)
            heapq.heappush(busy, (now + load[i], s))
            handled[s] += 1
    most = max(handled)
    return [s for s in range(k) if handled[s] == most]


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536

    def big(self):
        a = self.next()
        return a * 32768 + self.next()


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most_k, most_n, gap, longest, rng):
    check = requests = busiest = 0
    for _ in range(count):
        k = rng.next() % most_k + 1
        n = rng.big() % most_n + 1
        arrival, load = [], []
        t = 0
        for _ in range(n):
            t += rng.next() % gap + 1
            arrival.append(t)
            load.append(rng.next() % longest + 1)
        servers = busiest_servers(k, arrival, load)
        for s in servers:
            check = mix(check, s)
        check = mix(check, -1)
        busiest += len(servers)
        requests += n
    print(f"{count} problems of up to {most_k} servers and {most_n} requests: {requests} requests, {busiest} busiest, checksum {check}")


def main():
    examples = [
        (3, [1, 2, 3, 4, 5], [5, 2, 3, 3, 3]),
        (3, [1, 2, 3, 4], [1, 2, 1, 2]),
        (3, [1, 2, 3], [10, 12, 11]),
        (1, [1, 2, 3, 4], [1, 5, 1, 1]),
        (2, [1, 2, 3, 4], [100, 100, 100, 100]),
        (3, [1, 2, 3, 4, 5, 6], [9, 9, 1, 9, 9, 9]),
    ]
    for k, arrival, load in examples:
        print(f"[{','.join(str(s) for s in busiest_servers(k, arrival, load))}]")
    rng = Rng(1606)
    batch(3000, 4, 10, 3, 8, rng)
    batch(300, 100, 3000, 5, 400, rng)
    batch(3, 1000, 100000, 10, 10000, rng)


main()
