// LeetCode #2497: Maximum Star Sum of a Graph -- C mirror of the benchmark
// (star_sum.kara): the same graph, passes and checksum; each node's
// neighbours' values in compressed rows built afresh on every ask, each
// row sorted largest first by qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2497;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

static int larger_first(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a < b) - (a > b);
}

static int64_t max_star_sum(int64_t n, const int64_t *vals, int64_t m, int64_t (*edges)[2], int64_t k) {
    int64_t *start = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        start[edges[i][0] + 1]++;
        start[edges[i][1] + 1]++;
    }
    for (int64_t c = 1; c <= n; c++) start[c] += start[c - 1];
    int64_t *fill = malloc(n * sizeof(int64_t));
    memcpy(fill, start, n * sizeof(int64_t));
    int64_t *beside = malloc((2 * m + 1) * sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) {
        beside[fill[edges[i][0]]++] = vals[edges[i][1]];
        beside[fill[edges[i][1]]++] = vals[edges[i][0]];
    }
    int64_t best = INT64_MIN;
    for (int64_t c = 0; c < n; c++) {
        int64_t lo = start[c], hi = start[c + 1];
        qsort(beside + lo, hi - lo, sizeof(int64_t), larger_first);
        int64_t sum = vals[c], taken = 0;
        for (int64_t e = lo; e < hi; e++) {
            if (taken == k || beside[e] <= 0) break;
            sum += beside[e];
            taken++;
        }
        if (sum > best) best = sum;
    }
    free(start); free(fill); free(beside);
    return best;
}

int main(void) {
    const int64_t n = 100000, passes = 125;
    int64_t *vals = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) vals[i] = wide() % 20001 - 10000;
    // the edges taken so far, in an open-addressed table of their keys
    int64_t cap = 1 << 18;
    int64_t *seen = malloc(cap * sizeof(int64_t));
    for (int64_t i = 0; i < cap; i++) seen[i] = -1;
    int64_t (*edges)[2] = malloc(n * sizeof *edges);
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t a = wide() % n, b = wide() % n;
        if (a == b) continue;
        int64_t key = (a < b ? a : b) * n + (a < b ? b : a);
        int64_t h = (int64_t)(((uint64_t)key * 11400714819323198485ULL) >> 46) & (cap - 1);
        int fresh = 1;
        while (seen[h] != -1) {
            if (seen[h] == key) { fresh = 0; break; }
            h = (h + 1) & (cap - 1);
        }
        if (fresh) {
            seen[h] = key;
            edges[m][0] = a; edges[m][1] = b; m++;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t at = check % n;
        int64_t was = vals[at];
        vals[at] = (check / n + p) % 20001 - 10000;
        int64_t k = check % 50;
        check = (check * 31 + max_star_sum(n, vals, m, edges, k) + p) % 1000000007;
        vals[at] = was;
    }
    printf("%lld passes over 10^5 nodes and %lld edges: checksum %lld\n",
           (long long)passes, (long long)m, (long long)check);
    free(vals); free(seen); free(edges);
    return 0;
}
