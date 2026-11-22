// LeetCode #2819: Minimum Relative Loss After Buying Chocolates -- the
// bench's C mirror of the ★ arm: the prices sorted by qsort, prefix sums,
// and a binary search per query for how many come from the cheap end.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int ascending(const void *a, const void *b) {
    long long x = *(const long long *)a, y = *(const long long *)b;
    return (x > y) - (x < y);
}

static void minimum_relative_losses(const long long *prices, long long n, const long long *queries,
                                    long long q, long long *out) {
    long long *sorted = malloc(n * sizeof *sorted), *prefix = malloc((n + 1) * sizeof *prefix);
    memcpy(sorted, prices, n * sizeof *sorted);
    qsort(sorted, n, sizeof *sorted, ascending);
    prefix[0] = 0;
    for (long long i = 0; i < n; i++) prefix[i + 1] = prefix[i] + sorted[i];
    for (long long j = 0; j < q; j++) {
        long long k = queries[2 * j], m = queries[2 * j + 1], lo = 0, hi = m;
        while (lo < hi) {
            long long mid = (lo + hi) / 2;
            if (sorted[mid] + sorted[n - m + mid] < 2 * k) lo = mid + 1;
            else hi = mid;
        }
        long long dear = prefix[n] - prefix[n - m + lo];
        out[j] = prefix[lo] + 2 * k * (m - lo) - dear;
    }
    free(sorted);
    free(prefix);
}

static long long seed = 2819;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long wide(void) {
    long long a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    enum { COUNT = 10, ROUNDS = 3, N = 100000 };
    static long long prices[COUNT][N], queries[COUNT][2 * N], out[N];
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) prices[c][i] = wide() % 1000000000 + 1;
        for (int i = 0; i < N; i++) {
            queries[c][2 * i] = wide() % 1000000000 + 1;
            queries[c][2 * i + 1] = wide() % N + 1;
        }
    }
    long long negative = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            minimum_relative_losses(prices[c], N, queries[c], N, out);
            for (int i = 0; i < N; i++) {
                if (out[i] < 0) negative++;
                check = ((check * 31 + out[i] + r) % 1000000007 + 1000000007) % 1000000007;
            }
        }
    printf("%d shops of %d, %d rounds: %lld losses below 0, checksum %lld\n", COUNT, N, ROUNDS, negative, check);
    return 0;
}
