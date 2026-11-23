# LeetCode #2532: Time to Cross a Bridge -- benchmark mirror of the ★ arm
# (bridge.kara): 200 cases built once, then the passes, each asking every
# case from an offset the checksum picks.
import heapq


def find_crossing_time(n, k, time):
    # waiting sides: the least efficient first, as a max-heap on (lr + rl, i)
    left = [(-(t[0] + t[2]), -i) for i, t in enumerate(time)]
    heapq.heapify(left)
    right = []
    picking = []  # (done, i)
    putting = []
    now = 0
    while n > 0 or right or picking:
        while putting and putting[0][0] <= now:
            _, i = heapq.heappop(putting)
            heapq.heappush(left, (-(time[i][0] + time[i][2]), -i))
        while picking and picking[0][0] <= now:
            _, i = heapq.heappop(picking)
            heapq.heappush(right, (-(time[i][0] + time[i][2]), -i))
        if right:
            _, i = heapq.heappop(right)
            i = -i
            now += time[i][2]
            heapq.heappush(putting, (now + time[i][3], i))
        elif n > 0 and left:
            _, i = heapq.heappop(left)
            i = -i
            now += time[i][0]
            n -= 1
            heapq.heappush(picking, (now + time[i][1], i))
        else:
            nxt = 1 << 62
            if picking:
                nxt = min(nxt, picking[0][0])
            if n > 0 and putting:
                nxt = min(nxt, putting[0][0])
            now = nxt
    return now


seed = 2532


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    cases = []
    for _ in range(200):
        n = next_random() % 1000 + 1
        k = next_random() % 100 + 1
        time = [[next_random() % 1000 + 1 for _ in range(4)] for _ in range(k)]
        cases.append((n, k, time))
    passes = 100
    check = 0
    for p in range(passes):
        start = check % 200
        for i in range(200):
            n, k, time = cases[(start + i) % 200]
            check = (check * 31 + find_crossing_time(n, k, time) + p) % 1000000007
    print(f"{passes} passes over 200 cases: checksum {check}")


main()
