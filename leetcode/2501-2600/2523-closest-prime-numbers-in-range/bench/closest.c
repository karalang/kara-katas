// LeetCode #2523: Closest Prime Numbers in Range -- C mirror of the
// benchmark (closest.kara): the same queries, each answered by a fresh
// sieve, and the same checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void closest_primes(int64_t left, int64_t right, int64_t *a, int64_t *b) {
    char *composite = calloc((size_t)right + 1, 1);
    for (int64_t p = 2; p * p <= right; p++)
        if (!composite[p])
            for (int64_t m = p * p; m <= right; m += p) composite[m] = 1;
    int64_t ba = -1, bb = -1, last = -1;
    for (int64_t x = left < 2 ? 2 : left; x <= right; x++) {
        if (!composite[x]) {
            if (last != -1 && (ba == -1 || x - last < bb - ba)) {
                ba = last;
                bb = x;
            }
            last = x;
        }
    }
    free(composite);
    *a = ba;
    *b = bb;
}

int main(void) {
    const int queries = 150;
    int64_t check = 0;
    for (int q = 0; q < queries; q++) {
        int64_t right = check % 500000 + 500001, a, b;
        closest_primes(right - 10000, right, &a, &b);
        check = (check * 31 + a + q) % 1000000007;
        check = (check * 31 + b) % 1000000007;
    }
    printf("%d queries to 10^6: checksum %lld\n", queries, (long long)check);
    return 0;
}
