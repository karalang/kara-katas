"""LeetCode 313 - Super Ugly Number.

Mirror of ugly.kara: the same k-way merge with one pointer per prime and a
two-pass step (find the minimum, then advance every stream that offered it).
Same build-once + punch shape, same per-pass prime swap, same masked sink.
Kept algorithm-for-algorithm so the benchmark lane is honest.
"""

TERMS = 100000
PASSES = 30
MASK = 1073741823


def main():
    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
        59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
        127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
    ]
    k = len(primes)
    pool = [179, 181, 191, 193, 197, 199, 211, 223]

    ugly = [0] * TERMS
    idx = [0] * k

    checksum = 0
    for _pass in range(PASSES):
        slot = checksum % k
        keep = primes[slot]
        primes[slot] = pool[checksum % len(pool)]

        for i in range(k):
            idx[i] = 0
        ugly[0] = 1
        for m in range(1, TERMS):
            best = primes[0] * ugly[idx[0]]
            for i in range(1, k):
                c = primes[i] * ugly[idx[i]]
                if c < best:
                    best = c
            for i in range(k):
                if primes[i] * ugly[idx[i]] == best:
                    idx[i] += 1
            ugly[m] = best

        checksum = (checksum + ugly[TERMS - 1]) & MASK
        primes[slot] = keep

    print("checksum", checksum)


if __name__ == "__main__":
    main()
