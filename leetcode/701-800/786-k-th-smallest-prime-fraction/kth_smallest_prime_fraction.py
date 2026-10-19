# LeetCode 786 — K-th Smallest Prime Fraction, a heap of the next
# fraction for each denominator.
# Mirrors kth_smallest_prime_fraction.kara (the ★ arm) and its harness.
import heapq
from fractions import Fraction


def kth_smallest_prime_fraction(arr, k):
    n = len(arr)
    heap = [(Fraction(arr[0], arr[j]), 0, j) for j in range(1, n)]
    heapq.heapify(heap)
    for _ in range(k - 1):
        _, i, j = heapq.heappop(heap)
        if i + 1 < j:
            heapq.heappush(heap, (Fraction(arr[i + 1], arr[j]), i + 1, j))
    _, i, j = heap[0]
    return [arr[i], arr[j]]


seed = 786


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def primes_below(limit):
    composite = [False] * limit
    out = []
    for p in range(2, limit):
        if not composite[p]:
            out.append(p)
            for m in range(p * p, limit, p):
                composite[m] = True
    return out


def text(v):
    return "[" + ", ".join(map(str, v)) + "]"


def show(arr, k):
    print(f"arr = {text(arr)}, k = {k} -> {text(kth_smallest_prime_fraction(arr, k))}")


def main():
    show([1, 2, 3, 5], 3)
    show([1, 7], 1)
    show([1, 2, 3, 5], 1)
    show([1, 2, 3, 5], 6)
    show([1, 13, 17, 59], 4)
    show([1, 2, 29989], 2)
    primes = primes_below(30000)
    arr = [1] + primes[:999]
    total = 999 * 1000 // 2
    for k in [1, 2, 1000, 250000, total - 1, total]:
        answer = kth_smallest_prime_fraction(arr, k)
        print(f"1 and the first 999 primes, k = {k} -> {text(answer)}")
    s = 0
    check = 0
    for _ in range(300):
        n = 2 + next_random() % 59
        taken = set()
        picked = []
        while len(picked) < n - 1:
            p = primes[next_random() % len(primes)]
            if p not in taken:
                taken.add(p)
                picked.append(p)
        picked.sort()
        arr = [1] + picked
        k = 1 + next_random() % (n * (n - 1) // 2)
        answer = kth_smallest_prime_fraction(arr, k)
        s += answer[0] + answer[1]
        check = (check * 31 + answer[0] * 7 + answer[1]) % 1000000007
    print(f"300 random arrays: terms sum to {s}, checksum {check}")


main()
