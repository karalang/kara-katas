# LeetCode #1606: Find Servers That Handled Most Number of Requests -- the
# bench in Python, mirroring servers.kara: the free servers kept sorted (a
# list with bisect), the busy ones in a heap.
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



def main():
    seed = 1606

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    problems = []
    for _ in range(20):
        arrival, load = [], []
        t = 0
        for _ in range(100000):
            t += next_random() % 3 + 1
            arrival.append(t)
            a = next_random()
            load.append((a * 32768 + next_random()) % 30000 + 1)
        problems.append((arrival, load))
    check = busiest = 0
    for arrival, load in problems:
        servers = busiest_servers(10000, arrival, load)
        for s in servers:
            check = (check * 31 + s + 1) % 1000000007
        busiest += len(servers)
    print(f"20 problems of 10000 servers and 100000 requests: {busiest} busiest, checksum {check}")


main()
