// LeetCode #1288 bench, C: the same sort and sweep, workload and checksum
// as remove_covered_intervals.kara; an interval is a pair of ints.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define POOL 100000
#define WINDOW 1000

typedef struct {
    int32_t start, end;
} interval_t;

static int by_start_then_longest(const void *pa, const void *pb) {
    const interval_t *a = pa, *b = pb;
    if (a->start != b->start) {
        return a->start < b->start ? -1 : 1;
    }
    if (a->end != b->end) {
        return a->end > b->end ? -1 : 1;
    }
    return 0;
}

static int32_t remove_covered_intervals(const interval_t *intervals, int n) {
    interval_t order[WINDOW];
    memcpy(order, intervals, sizeof(interval_t) * n);
    qsort(order, n, sizeof(interval_t), by_start_then_longest);
    int32_t kept = 0, reach = 0;
    for (int i = 0; i < n; i++) {
        if (order[i].end > reach) {
            kept++;
            reach = order[i].end;
        }
    }
    return kept;
}

int main(void) {
    static interval_t pool[POOL];
    int64_t seed = 1288;
    for (int i = 0; i < POOL; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t start = seed % 100000;
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t end = start + 1 + seed % (100000 - start);
        pool[i].start = (int32_t)start;
        pool[i].end = (int32_t)end;
    }
    int64_t check = 0;
    interval_t window[WINDOW];
    for (int64_t r = 0; r < 3000; r++) {
        int64_t at = (check + r * 7919) % 99001;
        memcpy(window, pool + at, sizeof(interval_t) * WINDOW);
        check = (check * 131 + remove_covered_intervals(window, WINDOW)) % 1000000007;
    }
    printf("3000 windows of 1000 intervals: checksum %lld\n", (long long)check);
    return 0;
}
