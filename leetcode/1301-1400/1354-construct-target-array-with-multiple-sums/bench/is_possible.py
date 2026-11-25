# LeetCode #1354 -- bench, Python: the ★ arm: the moves undone from the
# target, largest value first, many undos of one value as one remainder.
import heapq


def is_possible(target):
    if len(target) == 1:
        return target[0] == 1
    total = sum(target)
    heap = []
    for x in target:
        heapq.heappush(heap, -x)
    while True:
        x = -heapq.heappop(heap)
        rest = total - x
        if x == 1 or rest == 1:
            return True
        if x <= rest or x % rest == 0:
            return False
        before = x % rest
        heapq.heappush(heap, -before)
        total = rest + before


seed = [1354]


def next_random():
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def reached(n, moves, top):
    arr = [1] * n
    total = n
    for _ in range(moves):
        if total > top:
            break
        i = next_random() % n
        was = arr[i]
        arr[i] = total
        total = 2 * total - was
    return arr


def main():
    # 20 targets of 5 * 10^4 values, each reached from the ones by moves
    # until a value would pass 10^9, built once; then 2000 rounds, each
    # changing one place of one target, drawn from the checksum so far,
    # answering, and putting the place back; one round in four leaves the
    # value as it was
    targets = [reached(50000, 100, 1000000000) for _ in range(20)]
    check = 0
    for r in range(2000):
        k = check % 20
        at = (check // 20) % 50000
        was = targets[k][at]
        if r % 4 != 0:
            targets[k][at] = was + 1 + (check // 7) % 3
        got = 1 if is_possible(targets[k]) else 0
        targets[k][at] = was
        check = (check * 31 + got * 1000 + r) % 1000000007
    print(f"2000 rounds over 20 targets of 5 * 10^4 values: checksum {check}")


main()
