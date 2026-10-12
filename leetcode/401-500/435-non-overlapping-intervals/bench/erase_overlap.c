// Benchmark for #435: mirror of erase_overlap.kara (greedy by end) on
// 100 windows of 100,000 intervals from one pool of 1,000,000. The sort
// is qsort, which is not stable; the count does not depend on the order
// of intervals with equal ends.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t start, end; } Interval;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int by_end(const void *a, const void *b) {
    int64_t x = ((const Interval *)a)->end, y = ((const Interval *)b)->end;
    return (x > y) - (x < y);
}

static int64_t erase_overlap_intervals(Interval *intervals, int64_t n) {
    if (n == 0) {
        return 0;
    }
    qsort(intervals, n, sizeof(Interval), by_end);
    int64_t kept = 1;
    int64_t end = intervals[0].end;
    for (int64_t i = 1; i < n; i++) {
        if (intervals[i].start >= end) {
            kept++;
            end = intervals[i].end;
        }
    }
    return n - kept;
}

int main(void) {
    const int64_t pool_size = 1000000, size = 100000, rounds = 100;
    int64_t seed = 435;
    // Starts anywhere in [-50000, 50000), lengths 1 to 200.
    Interval *pool = malloc(pool_size * sizeof(Interval));
    for (int64_t i = 0; i < pool_size; i++) {
        int64_t hi = next_random(&seed);
        int64_t start = (hi * 32768 + next_random(&seed)) % 100000 - 50000;
        pool[i].start = start;
        pool[i].end = start + 1 + next_random(&seed) % 200;
    }
    Interval *window = malloc(size * sizeof(Interval));
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t at = next_random(&seed) * 32768 % (pool_size - size + 1);
        memcpy(window, pool + at, size * sizeof(Interval));
        int64_t removed = erase_overlap_intervals(window, size);
        total += removed;
        checksum = (checksum * 31 + removed) % 1000000007;
    }
    printf("%lld rounds of %lld intervals: %lld removed, checksum %lld\n",
           (long long)rounds, (long long)size, (long long)total, (long long)checksum);
    free(window);
    free(pool);
    return 0;
}
