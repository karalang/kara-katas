// Benchmark workload for LeetCode #259 — 3Sum Smaller (C mirror).
// Mirrors three_sum_smaller.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *x, const void *y) {
    long a = *(const long *)x, b = *(const long *)y;
    return (a > b) - (a < b);
}

int main(void) {
    long n = 4000, rounds = 26;
    long *base = malloc(n * sizeof(long));
    long state = 259259;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        base[i] = (state / 65536L) % 2001L - 1000L;
    }
    long *probe = malloc(n * sizeof(long));
    memcpy(probe, base, n * sizeof(long));
    qsort(probe, n, sizeof(long), cmp);
    long min_sum = probe[0] + probe[1] + probe[2];
    long max_sum = probe[n-1] + probe[n-2] + probe[n-3];
    long target = (min_sum + max_sum) / 2;

    long *s = malloc(n * sizeof(long));
    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        memcpy(s, base, n * sizeof(long));
        qsort(s, n, sizeof(long), cmp);
        long count = 0;
        for (long a = 0; a + 2 < n; a++) {
            long lo = a + 1, hi = n - 1;
            while (lo < hi) {
                if (s[a] + s[lo] + s[hi] < target) { count += hi - lo; lo++; }
                else hi--;
            }
        }
        sink = (sink * 31 + count % 1000000007L) % 1000000007L;
    }
    printf("%ld\n", sink);
    free(base); free(probe); free(s);
    return 0;
}
