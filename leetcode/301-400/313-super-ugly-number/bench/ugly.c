/* LeetCode 313 - Super Ugly Number.
 *
 * Mirror of ugly.kara: the same k-way merge with one pointer per prime and a
 * two-pass step (find the minimum, then advance every stream that offered it).
 * Same build-once + punch shape, same per-pass prime swap, same masked sink.
 * Kept algorithm-for-algorithm so the benchmark lane is honest.
 */
#include <stdio.h>
#include <stdlib.h>

#define TERMS  100000
#define PASSES 30
#define MASK   1073741823LL

int main(void) {
    long long primes[] = {
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
        59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
        127, 131, 137, 139, 149, 151, 157, 163, 167, 173
    };
    const long long k = (long long)(sizeof primes / sizeof primes[0]);
    long long pool[] = {179, 181, 191, 193, 197, 199, 211, 223};
    const long long npool = (long long)(sizeof pool / sizeof pool[0]);

    long long *ugly = calloc(TERMS, sizeof *ugly);
    long long *idx = calloc((size_t)k, sizeof *idx);
    if (!ugly || !idx) return 1;

    long long checksum = 0;
    for (long long pass = 0; pass < PASSES; pass++) {
        long long slot = checksum % k;
        long long keep = primes[slot];
        primes[slot] = pool[checksum % npool];

        for (long long i = 0; i < k; i++) idx[i] = 0;
        ugly[0] = 1;
        for (long long m = 1; m < TERMS; m++) {
            long long best = primes[0] * ugly[idx[0]];
            for (long long i = 1; i < k; i++) {
                long long c = primes[i] * ugly[idx[i]];
                if (c < best) best = c;
            }
            for (long long i = 0; i < k; i++) {
                if (primes[i] * ugly[idx[i]] == best) idx[i]++;
            }
            ugly[m] = best;
        }

        checksum = (checksum + ugly[TERMS - 1]) & MASK;
        primes[slot] = keep;
    }

    printf("checksum %lld\n", checksum);
    free(ugly);
    free(idx);
    return 0;
}
