// Benchmark for #857: Minimum Cost to Hire K Workers -- the ★ arm,
// mirroring mincost_to_hire_workers.kara. The heap is written out, as C
// has none; the sort is `qsort` on the indices, its comparator reading
// the current set through two file-level pointers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t *cur_q, *cur_w;

static int by_rate(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    int64_t l = cur_w[a] * cur_q[b], r = cur_w[b] * cur_q[a];
    if (l != r) return (l > r) - (l < r);
    return (a > b) - (a < b);  // keep equal rates in index order, as a stable sort does
}

// A max-heap of qualities.
static void heap_push(int64_t *h, int64_t *len, int64_t v) {
    int64_t i = (*len)++;
    h[i] = v;
    while (i > 0 && h[(i - 1) / 2] < h[i]) {
        int64_t p = (i - 1) / 2, t = h[p];
        h[p] = h[i];
        h[i] = t;
        i = p;
    }
}

static int64_t heap_pop(int64_t *h, int64_t *len) {
    int64_t top = h[0];
    h[0] = h[--(*len)];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < *len && h[l] > h[m]) m = l;
        if (r < *len && h[r] > h[m]) m = r;
        if (m == i) break;
        int64_t t = h[m];
        h[m] = h[i];
        h[i] = t;
        i = m;
    }
    return top;
}

static double mincost_to_hire_workers(const int64_t *quality, const int64_t *wage, int64_t n, int64_t k) {
    int64_t *order = malloc(n * sizeof(int64_t));
    int64_t *heap = malloc((n + 1) * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) order[i] = i;
    cur_q = quality;
    cur_w = wage;
    qsort(order, n, sizeof(int64_t), by_rate);
    int64_t len = 0, sum = 0, best_num = -1, best_den = 1;
    for (int64_t t = 0; t < n; t++) {
        int64_t i = order[t];
        heap_push(heap, &len, quality[i]);
        sum += quality[i];
        if (len > k) sum -= heap_pop(heap, &len);
        if (len == k) {
            int64_t num = wage[i] * sum, den = quality[i];
            if (best_num < 0 || num * best_den < best_num * den) {
                best_num = num;
                best_den = den;
            }
        }
    }
    free(order);
    free(heap);
    return (double)best_num / (double)best_den;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    enum { COUNT = 16, N = 10000 };
    int64_t rounds = 600, seed = 857;
    static int64_t qualities[COUNT][N], wages[COUNT][N];
    for (int g = 0; g < COUNT; g++)
        for (int i = 0; i < N; i++) {
            qualities[g][i] = 1 + next_random(&seed) % 10000;
            wages[g][i] = 1 + next_random(&seed) % 10000;
        }
    double total = 0.0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % COUNT;
        total += mincost_to_hire_workers(qualities[g], wages[g], N, 1 + g * 600);
    }
    printf("%lld rounds of 16 sets: costs sum to %.5f\n", (long long)rounds, total);
    return 0;
}
