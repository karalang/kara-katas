// Benchmark for #363 -- mirror of max_sum.kara (the merge-sort arm).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t best_pair(int64_t *p, int lo, int hi, int64_t k, int64_t *scratch) {
    if (hi - lo < 2) return INT64_MIN;
    int mid = (lo + hi) / 2;
    int64_t best = max64(best_pair(p, lo, mid, k, scratch), best_pair(p, mid, hi, k, scratch));
    int j = mid;
    for (int i = lo; i < mid; i++) {
        while (j < hi && p[j] <= p[i] + k) j++;
        if (j > mid) best = max64(best, p[j - 1] - p[i]);
    }
    int a = lo, b = mid, out = lo;
    while (a < mid || b < hi) {
        if (b == hi || (a < mid && p[a] <= p[b])) scratch[out++] = p[a++];
        else scratch[out++] = p[b++];
    }
    memcpy(p + lo, scratch + lo, (size_t)(hi - lo) * sizeof(int64_t));
    return best;
}

static int64_t max_sum_submatrix(int64_t m[N][N], int rows, int cols, int64_t k) {
    int64_t best = INT64_MIN;
    int64_t sums[N], prefix[N + 1], scratch[N + 1];
    for (int top = 0; top < rows; top++) {
        memset(sums, 0, sizeof sums);
        for (int bottom = top; bottom < rows; bottom++) {
            for (int c = 0; c < cols; c++) sums[c] += m[bottom][c];
            prefix[0] = 0;
            for (int c = 0; c < cols; c++) prefix[c + 1] = prefix[c] + sums[c];
            best = max64(best, best_pair(prefix, 0, cols + 1, k, scratch));
        }
    }
    return best;
}

int main(void) {
    static int64_t m[N][N];
    int64_t seed = 363, checksum = 0;
    for (int it = 0; it < 20; it++) {
        int64_t least = 100;
        for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++) {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                int64_t v = (seed / 65536) % 201 - 100;
                if (v < least) least = v;
                m[r][c] = v;
            }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t k = max64(least, (seed / 65536) % 20001 - 10000);
        checksum = (checksum * 31 + max_sum_submatrix(m, N, N, k) + 1000000) % 1000000007;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
