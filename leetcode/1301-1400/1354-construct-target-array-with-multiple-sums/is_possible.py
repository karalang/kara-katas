# LeetCode #1354 -- Python mirror of the ★ arm: the moves undone from the
# target, largest value first, many undos of one value as one remainder.
import heapq


def is_possible(target):
    if len(target) == 1:
        return target[0] == 1
    total = sum(target)
    heap = [-x for x in target]
    heapq.heapify(heap)
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


def b(v):
    return "true" if v else "false"


def main():
    e1 = is_possible([9, 3, 5])
    e2 = is_possible([1, 1, 1, 2])
    e3 = is_possible([8, 5])
    one = is_possible([1])
    two = is_possible([2])
    far = is_possible([1, 1000000000])
    coprime = is_possible([999999999, 1000000000])
    shared = is_possible([1000000000, 999999998])
    ones = [1] * 50000
    big = reached(50000, 100, 1000000000)
    made = is_possible(big)
    at = next(i for i, x in enumerate(big) if x > 1)
    big[at] += 1
    off = is_possible(big)
    print(" ".join(b(v) for v in [e1, e2, e3, one, two, far, coprime, shared, is_possible(ones), made, off]))
    yes = 0
    check = 0
    for c in range(2000):
        n = 1 + next_random() % 8
        if c % 2 == 0:
            target = reached(n, next_random() % 31, 1000000000)
        else:
            top = 10 if c % 6 == 1 else 1000 if c % 6 == 3 else 1000000000
            target = [1 + next_random() % top for _ in range(n)]
        if c % 8 == 0:
            i = next_random() % n
            target[i] += 1 + next_random() % 2
        got = is_possible(target)
        if got:
            yes += 1
        check = (check * 131 + (1 if got else 2)) % 1000000007
    print(f"2000 random targets: {yes} possible, checksum {check}")


main()
