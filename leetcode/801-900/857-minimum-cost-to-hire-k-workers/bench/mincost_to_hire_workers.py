# Benchmark for #857: Minimum Cost to Hire K Workers -- the ★ arm,
# mirroring mincost_to_hire_workers.kara.
import functools
import heapq


def mincost_to_hire_workers(quality, wage, k):
    n = len(quality)
    order = sorted(range(n), key=functools.cmp_to_key(
        lambda a, b: (wage[a] * quality[b] > wage[b] * quality[a]) - (wage[a] * quality[b] < wage[b] * quality[a])))
    heap = []
    total = 0
    best_num = -1
    best_den = 1
    for i in order:
        heapq.heappush(heap, -quality[i])
        total += quality[i]
        if len(heap) > k:
            total += heapq.heappop(heap)
        if len(heap) == k:
            num = wage[i] * total
            den = quality[i]
            if best_num < 0 or num * best_den < best_num * den:
                best_num = num
                best_den = den
    return best_num / best_den


seed = 857


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count, rounds, n = 16, 600, 10000
    qualities = []
    wages = []
    for _ in range(count):
        quality = []
        wage = []
        for _ in range(n):
            quality.append(1 + next_random() % 10000)
            wage.append(1 + next_random() % 10000)
        qualities.append(quality)
        wages.append(wage)
    total = 0.0
    for round_ in range(rounds):
        g = round_ % count
        total += mincost_to_hire_workers(qualities[g], wages[g], 1 + g * 600)
    print(f"{rounds} rounds of 16 sets: costs sum to {total:.5f}")


main()
