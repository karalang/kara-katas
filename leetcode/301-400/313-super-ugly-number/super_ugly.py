"""LeetCode 313 - Super Ugly Number.

Mirror of super_ugly.kara: the same k-way merge with one pointer per prime,
and the same two-pass step -- find the minimum over the stream heads, then
advance EVERY stream that offered it, which is what keeps the output free of
duplicates. Kept algorithm-for-algorithm so the comparison is honest.
"""


def nth_super_ugly(n, primes):
    if n <= 0:
        return 0
    k = len(primes)
    # With no primes at all, 1 is the only super ugly number.
    if k == 0:
        return 1

    ugly = [1]
    # idx[i] is how far stream i has been consumed: the next value it offers
    # is primes[i] * ugly[idx[i]].
    idx = [0] * k

    while len(ugly) < n:
        # Pass 1 - the minimum over the k stream heads.
        best = primes[0] * ugly[idx[0]]
        for i in range(1, k):
            c = primes[i] * ugly[idx[i]]
            if c < best:
                best = c
        # Pass 2 - advance EVERY stream that offered it.
        for i in range(k):
            if primes[i] * ugly[idx[i]] == best:
                idx[i] += 1
        ugly.append(best)

    return ugly[n - 1]


def report(n, primes):
    body = ",".join(str(p) for p in primes)
    print("n=%d [%s] -> %d" % (n, body, nth_super_ugly(n, primes)))


def main():
    report(12, [2, 7, 13, 19])
    report(1, [2, 3, 5])
    report(11, [2, 3, 5])
    report(20, [2, 3, 5])
    report(1, [7])
    report(6, [7])
    report(15, [2, 101])
    report(25, [2, 3, 5, 7, 11, 13])
    report(20, [5, 2, 3])
    report(100, [2, 7, 13, 19])


if __name__ == "__main__":
    main()
