/* Benchmark workload — Max Points on a Line, O(n^2 log n) sort-based variant.
 * Algorithmic mirror of bench/max_points.kara / .rs / .py / go-seq. See
 * ../README.md § Benchmarks for N / K and the deterministic LCG generator. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t igcd(int64_t a, int64_t b) {
    while (b != 0) { int64_t t = b; b = a % b; a = t; }
    return a;
}

static int cmp_i64(const void *pa, const void *pb) {
    int64_t a = *(const int64_t *)pa, b = *(const int64_t *)pb;
    return (a > b) - (a < b);
}

static int64_t max_points(const int64_t *xs, const int64_t *ys, int64_t n,
                          int64_t *slopes) {
    if (n <= 2) return n;
    int64_t best = 1;
    for (int64_t i = 0; i < n; i++) {
        int64_t m = 0, dup = 0;
        for (int64_t j = i + 1; j < n; j++) {
            int64_t dx = xs[j] - xs[i];
            int64_t dy = ys[j] - ys[i];
            if (dx == 0 && dy == 0) { dup++; continue; }
            int64_t g = igcd(dx < 0 ? -dx : dx, dy < 0 ? -dy : dy);
            dx /= g; dy /= g;
            if (dx < 0 || (dx == 0 && dy < 0)) { dx = -dx; dy = -dy; }
            slopes[m++] = dx * 4096 + dy;
        }
        qsort(slopes, (size_t)m, sizeof(int64_t), cmp_i64);
        int64_t local = 0, run = 0;
        for (int64_t k = 0; k < m; k++) {
            run = (k == 0 || slopes[k] != slopes[k - 1]) ? 1 : run + 1;
            if (run > local) local = run;
        }
        int64_t cand = local + dup + 1;
        if (cand > best) best = cand;
    }
    return best;
}

int main(void) {
    const int64_t N = 1200;
    int64_t *xs = malloc((size_t)N * sizeof(int64_t));
    int64_t *ys = malloc((size_t)N * sizeof(int64_t));
    int64_t *slopes = malloc((size_t)N * sizeof(int64_t));
    int64_t state = 12345;
    for (int64_t i = 0; i < N; i++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        xs[i] = state & 1023;
        state = (state * 1103515245 + 12345) & 2147483647;
        ys[i] = state & 1023;
    }
    int64_t sum = 0;
    for (int k = 0; k < 8; k++) sum += max_points(xs, ys, N, slopes);
    printf("%lld\n", (long long)sum);
    free(xs); free(ys); free(slopes);
    return 0;
}
