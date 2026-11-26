// LeetCode #1782: Count Pairs Of Nodes -- the bench in C, mirroring
// count_pairs.kara: two pointers over the sorted degrees less the joined
// pairs. C has no map, so the shared edges go in an open-addressing hash
// table keyed by the ordered pair.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp_int(const void *x, const void *y) {
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}

// (a, b) -> how many edges join them; key 0 marks an empty slot
typedef struct {
    int64_t *keys;
    int *counts;
    size_t mask;
} Table;

static size_t slot_of(const Table *t, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    size_t s = (size_t)(h >> 20) & t->mask;
    while (t->keys[s] != 0 && t->keys[s] != key) s = (s + 1) & t->mask;
    return s;
}

static int *count_pairs(int n, const int (*edges)[2], long m, const int *queries, int k) {
    int *degree = calloc(n + 1, sizeof(int));
    Table t;
    size_t cap = 1;
    while (cap < 2 * (size_t)m) cap <<= 1;
    t.keys = calloc(cap, sizeof(int64_t));
    t.counts = calloc(cap, sizeof(int));
    t.mask = cap - 1;
    for (long e = 0; e < m; e++) {
        int a = edges[e][0] < edges[e][1] ? edges[e][0] : edges[e][1];
        int b = edges[e][0] < edges[e][1] ? edges[e][1] : edges[e][0];
        degree[a] += 1;
        degree[b] += 1;
        int64_t key = (int64_t)a * (n + 1) + b;
        size_t s = slot_of(&t, key);
        t.keys[s] = key;
        t.counts[s] += 1;
    }
    int *sorted = malloc(sizeof(int) * n);
    memcpy(sorted, degree + 1, sizeof(int) * n);
    qsort(sorted, n, sizeof(int), cmp_int);
    int *answers = malloc(sizeof(int) * k);
    for (int j = 0; j < k; j++) {
        int q = queries[j];
        int64_t count = 0;
        long lo = 0, hi = n - 1;
        while (lo < hi) {
            if (sorted[lo] + sorted[hi] > q) {
                count += hi - lo;
                hi -= 1;
            } else {
                lo += 1;
            }
        }
        for (size_t s = 0; s < cap; s++) {
            if (t.keys[s] == 0) continue;
            int a = (int)(t.keys[s] / (n + 1)), b = (int)(t.keys[s] % (n + 1));
            int sum = degree[a] + degree[b];
            if (sum > q && sum - t.counts[s] <= q) count -= 1;
        }
        answers[j] = (int)count;
    }
    free(degree);
    free(sorted);
    free(t.keys);
    free(t.counts);
    return answers;
}

static int64_t seed = 1782;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int (*graphs[10])[2];
    for (int g = 0; g < 10; g++) {
        int64_t span = 50 + (int64_t)g * 2216;
        graphs[g] = malloc(sizeof(int[2]) * 100000);
        for (int e = 0; e < 100000; e++) {
            int64_t a = 1 + next_random() % span;
            int64_t b = 1 + (a + next_random() % (span - 1)) % span;
            graphs[g][e][0] = (int)a;
            graphs[g][e][1] = (int)b;
        }
    }
    int64_t check = 0;
    for (int g = 0; g < 10; g++) {
        int64_t top = 400000 / (50 + (int64_t)g * 2216);
        int queries[20];
        for (int k = 0; k < 20; k++) queries[k] = (int)((check + (int64_t)k * 997) % top);
        int *answers = count_pairs(20000, (const int (*)[2])graphs[g], 100000, queries, 20);
        for (int k = 0; k < 20; k++) check = (check * 31 + answers[k] + 1) % 1000000007;
        free(answers);
    }
    printf("10 graphs of 100000 edges: checksum %lld\n", (long long)check);
    for (int g = 0; g < 10; g++) free(graphs[g]);
    return 0;
}
