// LeetCode 757 — Set Intersection Size At Least Two: benchmark, the ★ arm in C.
// Intervals are pairs in one array, sorted with qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t start, end;
} Interval;

static int by_end_then_narrowest(const void *p, const void *q) {
    const Interval *x = p, *y = q;
    if (x->end != y->end) return x->end < y->end ? -1 : 1;
    if (x->start != y->start) return x->start > y->start ? -1 : 1;
    return 0;
}

static int64_t intersection_size_two(const Interval *intervals, size_t n) {
    Interval *order = malloc(n * sizeof(Interval));
    memcpy(order, intervals, n * sizeof(Interval));
    qsort(order, n, sizeof(Interval), by_end_then_narrowest);
    int64_t count = 0, second = -1, largest = -1;
    for (size_t i = 0; i < n; i++) {
        int64_t start = order[i].start, end = order[i].end;
        if (start > largest) {
            count += 2;
            second = end - 1;
            largest = end;
        } else if (start > second) {
            count += 1;
            second = largest;
            largest = end;
        }
    }
    free(order);
    return count;
}

static int64_t seed = 757;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t rounds = 2000, total = 0, check = 0;
    Interval intervals[3000];
    for (int64_t r = 0; r < rounds; r++) {
        for (int i = 0; i < 3000; i++) {
            int64_t width = 1 + next_random() % 100000;
            int64_t a = next_random() * 32768 % (100000000 - width + 1);
            intervals[i].start = a;
            intervals[i].end = a + width;
        }
        int64_t answer = intersection_size_two(intervals, 3000);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    printf("%lld sets of 3000 intervals: %lld points in all, checksum %lld\n", (long long)rounds,
           (long long)total, (long long)check);
    return 0;
}
