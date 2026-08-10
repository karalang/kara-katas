// Benchmark workload for LeetCode #253 — Meeting Rooms II (C mirror).
// Mirrors min_meeting_rooms.kara algorithm-for-algorithm.
#include <stdio.h>
#include <stdlib.h>

typedef struct { long s, e; } Iv;
static int by_start(const void *a, const void *b) {
    long x = ((const Iv*)a)->s, y = ((const Iv*)b)->s;
    return (x > y) - (x < y);
}

static long *H; static long HN;
static void heap_push(long v) {
    H[HN++] = v;
    long i = HN - 1;
    while (i > 0) {
        long p = (i - 1) / 2;
        if (H[i] < H[p]) { long t = H[i]; H[i] = H[p]; H[p] = t; i = p; } else break;
    }
}
static void heap_pop(void) {
    if (HN == 0) return;
    long last = H[--HN];
    if (HN == 0) return;
    H[0] = last;
    long i = 0;
    for (;;) {
        long l = 2*i+1, r = 2*i+2, sm = i;
        if (l < HN && H[l] < H[sm]) sm = l;
        if (r < HN && H[r] < H[sm]) sm = r;
        if (sm == i) break;
        long t = H[i]; H[i] = H[sm]; H[sm] = t; i = sm;
    }
}

int main(void) {
    long n = 150000, rounds = 25;
    Iv *base = malloc(n * sizeof(Iv));
    long state = 253253;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long jitter = (state / 65536L) % 8L;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long dur = (state / 65536L) % 60L + 1L;
        base[i].s = i + jitter; base[i].e = i + jitter + dur;
    }
    for (long k = n - 1; k > 0; k--) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long sw = (state / 65536L) % (k + 1);
        Iv t = base[k]; base[k] = base[sw]; base[sw] = t;
    }

    Iv *s = malloc(n * sizeof(Iv));
    H = malloc(n * sizeof(long));
    long sink = 0;
    for (long r = 0; r < rounds; r++) {
        for (long c = 0; c < n; c++) s[c] = base[c];
        qsort(s, n, sizeof(Iv), by_start);
        HN = 0;
        long rooms = 0;
        for (long j = 0; j < n; j++) {
            while (HN > 0 && H[0] <= s[j].s) heap_pop();
            heap_push(s[j].e);
            if (HN > rooms) rooms = HN;
        }
        sink = (sink * 31 + rooms) % 1000000007L;
    }
    printf("%ld\n", sink);
    free(H); free(s); free(base);
    return 0;
}
