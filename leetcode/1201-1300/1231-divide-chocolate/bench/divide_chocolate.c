// LeetCode #1231 bench: the ★ arm in C, over the same 100 random bars and
// 20 passes as the Kāra bench.
#include <stdio.h>
#include <stdlib.h>

static long pieces(const long *sweetness, long n, long m) {
    long count = 0, piece = 0;
    for (long i = 0; i < n; i++) {
        piece += sweetness[i];
        if (piece >= m) {
            count++;
            piece = 0;
        }
    }
    return count;
}

static long maximize_sweetness(const long *sweetness, long n, long k) {
    long total = 0;
    for (long i = 0; i < n; i++) total += sweetness[i];
    long lo = 1, hi = total / (k + 1);
    while (lo < hi) {
        long mid = (lo + hi + 1) / 2;
        if (pieces(sweetness, n, mid) >= k + 1)
            lo = mid;
        else
            hi = mid - 1;
    }
    return lo;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long seed = 1231;
    long *bars = malloc(sizeof(long) * 100 * 10000);
    long cuts[100];
    for (int b = 0; b < 100; b++) {
        for (int i = 0; i < 10000; i++) bars[(long)b * 10000 + i] = next_random(&seed) % 100000 + 1;
        cuts[b] = next_random(&seed) % 10000;
    }
    long check = 0;
    for (int pass = 0; pass < 20; pass++)
        for (int b = 0; b < 100; b++)
            check = (check * 131 + maximize_sweetness(bars + (long)b * 10000, 10000, cuts[b])) % 1000000007;
    printf("100 bars of 10^4 chunks, 20 passes: checksum %ld\n", check);
    free(bars);
    return 0;
}
