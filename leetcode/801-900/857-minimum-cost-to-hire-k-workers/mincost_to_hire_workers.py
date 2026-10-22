# LeetCode #857: Minimum Cost to Hire K Workers -- Python mirror of the ★
# arm (workers by wage per unit of quality, the k smallest qualities in a
# max-heap).
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


def show(quality, wage, k):
    cost = mincost_to_hire_workers(quality, wage, k)
    print(f"quality = {quality}, wage = {wage}, k = {k} -> {cost:.5f}")


seed = 857


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_workers(n, top_q, top_w):
    quality = []
    wage = []
    for _ in range(n):
        quality.append(1 + next_random() % top_q)
        wage.append(1 + next_random() % top_w)
    return quality, wage


def main():
    show([10, 20, 5], [70, 50, 30], 2)
    show([3, 1, 10, 10, 1], [4, 8, 2, 2, 7], 3)
    show([7], [13], 1)
    show([5, 5, 5], [10, 10, 10], 3)
    show([4, 2, 8], [8, 4, 16], 2)
    show([1, 10000], [10000, 1], 1)
    show([1, 10000], [10000, 1], 2)
    show([3, 1, 4, 1, 5, 9, 2, 6], [2, 7, 1, 8, 2, 8, 1, 8], 4)
    show([10000, 10000, 10000], [10000, 10000, 10000], 2)
    quality, wage = random_workers(1000, 10000, 10000)
    k = 300
    print(f"1000 random workers, k = 300 -> {mincost_to_hire_workers(quality, wage, k):.5f}")
    total = 0.0
    for _ in range(300):
        n = 1 + next_random() % 30
        k = 1 + next_random() % n
        top = 1 + next_random() % 100
        quality, wage = random_workers(n, top, top)
        total += mincost_to_hire_workers(quality, wage, k)
    print(f"300 random groups of up to 30 workers: costs sum to {total:.5f}")


main()
