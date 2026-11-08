// LeetCode #1509: Minimum Difference Between Largest and Smallest Value in
// Three Moves -- the bench: 20 arrays of 100000 numbers built once, then
// each answered five times by the ★ arm (qsort on a copy).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    long x = *(const long *)a, y = *(const long *)b;
    return (x > y) - (x < y);
}

static long min_difference(const long *nums, long n) {
    if (n <= 4) return 0;
    long *s = malloc(n * sizeof(long));
    memcpy(s, nums, n * sizeof(long));
    qsort(s, n, sizeof(long), cmp);
    long best = s[n - 1] - s[0];
    for (long low = 0; low < 4; low++) {
        long d = s[n - 4 + low] - s[low];
        if (d < best) best = d;
    }
    free(s);
    return best;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    long seed = 1509;
    static long arrays[20][100000];
    for (int a = 0; a < 20; a++) {
        for (int i = 0; i < 100000; i++) {
            long wide = next_random(&seed) * 32768;
            wide += next_random(&seed);
            arrays[a][i] = wide % 2000000001 - 1000000000;
        }
    }
    long check = 0;
    for (int r = 0; r < 5; r++)
        for (int a = 0; a < 20; a++)
            check = (check * 31 + min_difference(arrays[a], 100000) % 1000000007 + 1) % 1000000007;
    printf("100 answers over 20 arrays of 100000 numbers: checksum %ld\n", check);
    return 0;
}
