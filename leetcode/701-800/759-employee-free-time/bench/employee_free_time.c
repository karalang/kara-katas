// LeetCode 759 — Employee Free Time: benchmark, the ★ arm in C.
// The schedule is one array per employee; the pool is sorted with qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t start, end;
} Interval;

static int by_start(const void *p, const void *q) {
    const Interval *x = p, *y = q;
    return (x->start > y->start) - (x->start < y->start);
}

static Interval *employee_free_time(Interval schedule[][50], int employees, int per, int *count) {
    int n = employees * per;
    Interval *all = malloc(n * sizeof(Interval));
    for (int e = 0; e < employees; e++)
        for (int i = 0; i < per; i++) all[e * per + i] = schedule[e][i];
    qsort(all, n, sizeof(Interval), by_start);
    Interval *free_time = malloc(n * sizeof(Interval));
    int k = 0;
    int64_t end = all[0].end;
    for (int i = 0; i < n; i++) {
        if (all[i].start > end) free_time[k++] = (Interval){end, all[i].start};
        if (all[i].end > end) end = all[i].end;
    }
    free(all);
    *count = k;
    return free_time;
}

static int64_t seed = 759;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t rounds = 3000, gaps = 0, length = 0, check = 0;
    static Interval schedule[50][50];
    for (int64_t r = 0; r < rounds; r++) {
        for (int e = 0; e < 50; e++) {
            int64_t t = 0;
            for (int i = 0; i < 50; i++) {
                int64_t start = t + wide_random() % 1000000;
                int64_t end = start + 1 + wide_random() % 900000;
                schedule[e][i] = (Interval){start, end};
                t = end + 1;
            }
        }
        int count;
        Interval *free_time = employee_free_time(schedule, 50, 50, &count);
        gaps += count;
        for (int i = 0; i < count; i++) {
            length += free_time[i].end - free_time[i].start;
            check = (check * 31 + free_time[i].start) % 1000000007;
        }
        free(free_time);
    }
    printf("%lld schedules of 50 x 50 intervals: %lld free intervals, %lld free in all, checksum %lld\n",
           (long long)rounds, (long long)gaps, (long long)length, (long long)check);
    return 0;
}
