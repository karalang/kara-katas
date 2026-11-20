// LeetCode #1235 bench: the ★ arm in C, over the same 20 sets of 50000 jobs
// and 10 passes as the Kāra bench.
#include <stdio.h>
#include <stdlib.h>

static const long *sort_ends;

static int by_end(const void *a, const void *b) {
    long x = sort_ends[*(const long *)a], y = sort_ends[*(const long *)b];
    return (x > y) - (x < y);
}

static long job_scheduling(const long *start, const long *end, const long *profit, long n) {
    long *order = malloc(n * sizeof(long));
    long *ends = malloc(n * sizeof(long));
    long *best = calloc(n + 1, sizeof(long));
    for (long i = 0; i < n; i++) order[i] = i;
    sort_ends = end;
    qsort(order, n, sizeof(long), by_end);
    for (long k = 0; k < n; k++) ends[k] = end[order[k]];
    for (long k = 0; k < n; k++) {
        long job = order[k];
        long lo = 0, hi = n;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            if (ends[mid] <= start[job]) lo = mid + 1; else hi = mid;
        }
        long take = best[lo] + profit[job];
        best[k + 1] = best[k] > take ? best[k] : take;
    }
    long answer = best[n];
    free(order);
    free(ends);
    free(best);
    return answer;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long seed = 1235;
    long n = 50000;
    long *start = malloc(20 * n * sizeof(long));
    long *end = malloc(20 * n * sizeof(long));
    long *profit = malloc(20 * n * sizeof(long));
    for (long t = 0; t < 20; t++) {
        long len = 1000000 * (t % 4 + 1);
        for (long i = 0; i < n; i++) {
            long a = next_random(&seed) * 32768;
            long s = (a + next_random(&seed)) % 999000000 + 1;
            start[t * n + i] = s;
            long b = next_random(&seed) * 32768;
            end[t * n + i] = s + (b + next_random(&seed)) % len + 1;
            profit[t * n + i] = next_random(&seed) % 10000 + 1;
        }
    }
    long check = 0;
    for (int pass = 0; pass < 10; pass++)
        for (long t = 0; t < 20; t++)
            check = (check * 131 + job_scheduling(start + t * n, end + t * n, profit + t * n, n)) % 1000000007;
    printf("20 sets of 50000 jobs, 10 passes: checksum %ld\n", check);
    free(start);
    free(end);
    free(profit);
    return 0;
}
