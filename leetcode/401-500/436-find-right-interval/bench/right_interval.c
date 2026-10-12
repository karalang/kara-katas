// Benchmark for #436: mirror of right_interval.kara (sorted starts and
// binary search) on 100 random sets of 20,000 intervals. The index
// sort is qsort, which is not stable; starts are distinct, so the order
// is the same.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t start, end; } Interval;

static const Interval *sort_by;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int by_start(const void *a, const void *b) {
    int64_t x = sort_by[*(const int64_t *)a].start, y = sort_by[*(const int64_t *)b].start;
    return (x > y) - (x < y);
}

static void find_right_interval(const Interval *intervals, int64_t n, int64_t *order, int64_t *right) {
    for (int64_t i = 0; i < n; i++) {
        order[i] = i;
    }
    sort_by = intervals;
    qsort(order, n, sizeof(int64_t), by_start);
    for (int64_t i = 0; i < n; i++) {
        int64_t end = intervals[i].end;
        int64_t lo = 0, hi = n;
        while (lo < hi) {
            int64_t mid = (lo + hi) / 2;
            if (intervals[order[mid]].start < end) {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        right[i] = lo < n ? order[lo] : -1;
    }
}

int main(void) {
    const int64_t size = 20000, rounds = 100;
    int64_t seed = 436;
    Interval *intervals = malloc(size * sizeof(Interval));
    int64_t *order = malloc(size * sizeof(int64_t));
    int64_t *right = malloc(size * sizeof(int64_t));
    int64_t found = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // Distinct starts, one in each step of 100 across the range,
        // each interval up to 32,767 long, then shuffled.
        for (int64_t i = 0; i < size; i++) {
            int64_t start = -1000000 + 100 * i + next_random(&seed) % 100;
            int64_t end = start + next_random(&seed);
            intervals[i].start = start;
            intervals[i].end = end < 1000000 ? end : 1000000;
        }
        for (int64_t i = 0; i < size; i++) {
            int64_t j = i + next_random(&seed) % (size - i);
            Interval t = intervals[i];
            intervals[i] = intervals[j];
            intervals[j] = t;
        }
        find_right_interval(intervals, size, order, right);
        for (int64_t i = 0; i < size; i++) {
            if (right[i] >= 0) {
                found++;
            }
            checksum = (checksum * 31 + right[i] + 2) % 1000000007;
        }
    }
    printf("%lld rounds of %lld intervals: %lld right intervals, checksum %lld\n",
           (long long)rounds, (long long)size, (long long)found, (long long)checksum);
    free(right);
    free(order);
    free(intervals);
    return 0;
}
