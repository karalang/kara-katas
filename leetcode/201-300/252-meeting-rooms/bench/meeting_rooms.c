// Benchmark workload for LeetCode #252 — Meeting Rooms (C mirror).
// Mirrors meeting_rooms.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>

typedef struct { long s, e; } Iv;

static int by_start(const void *a, const void *b) {
    long x = ((const Iv *)a)->s, y = ((const Iv *)b)->s;
    return (x > y) - (x < y);
}

int main(void) {
    long n = 120000, rounds = 40;

    Iv *base = malloc(n * sizeof(Iv));
    long state = 252252, cursor = 0;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long dur = (state / 65536L) % 7L + 1L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long gap = (state / 65536L) % 3L;
        base[i].s = cursor; base[i].e = cursor + dur;
        cursor += dur + gap;
    }
    for (long k = n - 1; k > 0; k--) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long swap = (state / 65536L) % (k + 1);
        Iv t = base[k]; base[k] = base[swap]; base[swap] = t;
    }

    Iv *s = malloc(n * sizeof(Iv));
    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        for (long c = 0; c < n; c++) s[c] = base[c];
        qsort(s, n, sizeof(Iv), by_start);
        int ok = 1;
        for (long j = 1; j < n; j++) if (s[j].s < s[j-1].e) ok = 0;
        sink = ok ? (sink * 31 + 1) % 1000000007L : (sink * 31) % 1000000007L;
        sink = (sink * 131 + s[n-1].e - s[0].s) % 1000000007L;
    }
    printf("%ld\n", sink);
    free(s); free(base);
    return 0;
}
