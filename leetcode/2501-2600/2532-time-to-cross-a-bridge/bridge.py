# LeetCode #2532: Time to Cross a Bridge -- Python mirror of the ★ arm.
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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    fixed = [
        (1, 3, [[1, 1, 2, 1], [1, 1, 3, 1], [1, 1, 4, 1]]),
        (3, 2, [[1, 9, 1, 8], [10, 10, 10, 10]]),
        (1, 1, [[1, 1, 1, 1]]),
        (1000, 1, [[1, 1, 1, 1]]),
        (2, 3, [[5, 1, 5, 1], [1, 1, 9, 1], [9, 1, 1, 1]]),
        (5, 2, [[1, 1000, 1, 1000], [1000, 1, 1000, 1]]),
        (4, 4, [[3, 3, 3, 3]] * 4),
        (10, 3, [[2, 7, 4, 1], [6, 1, 1, 9], [3, 3, 3, 3]]),
    ]
    for n, k, t in fixed:
        print(f"n {n} k {k} {t} -> {find_crossing_time(n, k, t)}")
    seed = [2532]
    for count, boxes, workers, most in [(2000, 10, 5, 10), (40, 1000, 100, 1000)]:
        total = 0
        check = 0
        for _ in range(count):
            n = next_random(seed) % boxes + 1
            k = next_random(seed) % workers + 1
            t = [[next_random(seed) % most + 1 for _ in range(4)] for _ in range(k)]
            a = find_crossing_time(n, k, t)
            total += a
            check = (check * 31 + a) % 1000000007
        print(f"{count} random cases of up to {boxes} boxes and {workers} workers: total {total}, checksum {check}")


if __name__ == "__main__":
    main()
