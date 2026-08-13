// Benchmark workload for LeetCode #256 — Paint House (C mirror).
// Mirrors paint_house.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>

typedef struct { long a, b, c; } Cost;
static inline long min2(long x, long y) { return x < y ? x : y; }

int main(void) {
    long n = 4000000, rounds = 30;
    Cost *cost = malloc(n * sizeof(Cost));
    long state = 256256, cheap = 0, run_left = 0;
    for (long i = 0; i < n; i++) {
        if (run_left == 0) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            run_left = (state / 65536L) % 9L + 2L;
            state = (state * 1103515245L + 12345L) & 2147483647L;
            cheap = (state / 65536L) % 3L;
        }
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long lo = (state / 65536L) % 10L + 1L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long m1 = (state / 65536L) % 40L + 40L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long m2 = (state / 65536L) % 40L + 40L;
        if (cheap == 0)      { cost[i].a = lo; cost[i].b = m1; cost[i].c = m2; }
        else if (cheap == 1) { cost[i].a = m1; cost[i].b = lo; cost[i].c = m2; }
        else                 { cost[i].a = m1; cost[i].b = m2; cost[i].c = lo; }
        run_left--;
    }

    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        long a = cost[0].a, b = cost[0].b, c = cost[0].c;
        for (long k = 1; k < n; k++) {
            long na = cost[k].a + min2(b, c);
            long nb = cost[k].b + min2(a, c);
            long nc = cost[k].c + min2(a, b);
            a = na; b = nb; c = nc;
        }
        sink = (sink * 31 + min2(a, min2(b, c))) % 1000000007L;
    }
    printf("%ld\n", sink);
    free(cost);
    return 0;
}
