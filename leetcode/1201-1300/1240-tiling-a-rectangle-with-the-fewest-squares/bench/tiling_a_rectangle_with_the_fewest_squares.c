// LeetCode #1240: the benchmark, mirroring the Kāra file.
#include <stdio.h>
#include <stdlib.h>

static void fill(long long *heights, int m, long long n, long long count, long long *best) {
    if (count >= *best) return;
    int at = 0;
    for (int j = 1; j < m; j++)
        if (heights[j] < heights[at]) at = j;
    long long base = heights[at];
    if (base == n) {
        *best = count;
        return;
    }
    long long width = 0;
    while (at + width < m && heights[at + width] == base && width < n - base) width++;
    for (long long size = width; size >= 1; size--) {
        for (long long j = at; j < at + size; j++) heights[j] = base + size;
        fill(heights, m, n, count + 1, best);
        for (long long j = at; j < at + size; j++) heights[j] = base;
    }
}

static long long tiling_rectangle(long long n, long long m) {
    long long *heights = calloc(m, sizeof(long long));
    long long best = n * m;
    fill(heights, (int)m, n, 0, &best);
    free(heights);
    return best;
}

int main(void) {
    long long total = 0, check = 0;
    for (int pass = 0; pass < 200; pass++)
        for (long long n = 1; n <= 13; n++)
            for (long long m = 1; m <= 13; m++) {
                long long t = tiling_rectangle(n, m);
                total += t;
                check = (check * 131 + t) % 1000000007;
            }
    printf("169 rectangles, 200 passes: total %lld, checksum %lld\n", total, check);
    return 0;
}
