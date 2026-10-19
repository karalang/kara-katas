# LeetCode 786 — K-th Smallest Prime Fraction: the bench, in Python.
# Mirrors kth_smallest_prime_fraction.kara: a heap of the next fraction
# for each denominator, over the same 64 arrays.
import heapq


class Fraction:
    __slots__ = ("i", "j", "num", "den")

    def __init__(self, i, j, num, den):
        self.i = i
        self.j = j
        self.num = num
        self.den = den

    def __lt__(self, other):
        return self.num * other.den < other.num * self.den


def kth_smallest_prime_fraction(arr, k):
    n = len(arr)
    heap = []
    for j in range(1, n):
        heapq.heappush(heap, Fraction(0, j, arr[0], arr[j]))
    for _ in range(k - 1):
        f = heapq.heappop(heap)
        if f.i + 1 < f.j:
            heapq.heappush(heap, Fraction(f.i + 1, f.j, arr[f.i + 1], f.den))
    f = heapq.heappop(heap)
    return [f.num, f.den]


seed = 786


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    composite = [False] * 30000
    primes = []
    for p in range(2, 30000):
        if not composite[p]:
            primes.append(p)
            for m in range(p * p, 30000, p):
                composite[m] = True
    arrays = []
    for _ in range(64):
        taken = [False] * len(primes)
        count = 0
        while count < 999:
            at = next_random() % len(primes)
            if not taken[at]:
                taken[at] = True
                count += 1
        arrays.append([1] + [primes[at] for at in range(len(primes)) if taken[at]])
    rounds = 64
    total = 0
    check = 0
    for r in range(rounds):
        hi = next_random()
        k = 1 + (hi * 32768 + next_random()) % 499500
        answer = kth_smallest_prime_fraction(arrays[r % 64], k)
        total += answer[0] + answer[1]
        check = (check * 31 + answer[0] * 7 + answer[1]) % 1000000007
    print(f"{rounds} rounds of 1000-number arrays: terms sum to {total}, checksum {check}")


main()
