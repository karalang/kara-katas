// LeetCode #1697: Checking Existence of Edge Length Limited Paths -- the
// bench's C mirror: the ★ arm on 10 random graphs of 100000 nodes, 100000
// edges and 100000 queries, lengths and limits up to 10^9, all drawn
// first, each answered 5 times. The sorts are qsort's; the answers do not
// depend on the order of equal lengths.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 10
#define ROUNDS 5
#define N 100000

typedef struct {
    int32_t u, v, d;
} triple;

static const triple *by_limit;

static int by_length(const void *a, const void *b) {
    int32_t x = ((const triple *)a)->d, y = ((const triple *)b)->d;
    return (x > y) - (x < y);
}

static int by_query_limit(const void *a, const void *b) {
    int32_t x = by_limit[*(const int64_t *)a].d, y = by_limit[*(const int64_t *)b].d;
    return (x > y) - (x < y);
}

static int64_t find(int64_t *parent, int64_t x) {
    int64_t root = x;
    while (parent[root] != root) {
        root = parent[root];
    }
    while (parent[x] != root) {
        int64_t next = parent[x];
        parent[x] = root;
        x = next;
    }
    return root;
}

static void distance_limited_paths_exist(int64_t n, const triple *edge_list, int64_t e, const triple *queries, int64_t q, uint8_t *answer) {
    triple *edges = malloc((size_t)e * sizeof *edges);
    memcpy(edges, edge_list, (size_t)e * sizeof *edges);
    qsort(edges, (size_t)e, sizeof *edges, by_length);
    int64_t *order = malloc((size_t)q * sizeof *order);
    for (int64_t i = 0; i < q; i++) {
        order[i] = i;
    }
    by_limit = queries;
    qsort(order, (size_t)q, sizeof *order, by_query_limit);
    int64_t *parent = malloc((size_t)n * sizeof *parent);
    for (int64_t i = 0; i < n; i++) {
        parent[i] = i;
    }
    int64_t joined = 0;
    for (int64_t k = 0; k < q; k++) {
        int64_t i = order[k];
        int32_t limit = queries[i].d;
        while (joined < e && edges[joined].d < limit) {
            int64_t a = find(parent, edges[joined].u);
            int64_t b = find(parent, edges[joined].v);
            parent[a] = b;
            joined++;
        }
        answer[i] = find(parent, queries[i].u) == find(parent, queries[i].v);
    }
    free(edges);
    free(order);
    free(parent);
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1697;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide(int64_t bound) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % bound;
}

static void triples(triple *out, int64_t count, int64_t n) {
    for (int64_t i = 0; i < count; i++) {
        int64_t u = wide(n);
        int64_t v = (u + 1 + wide(n - 1)) % n;
        out[i].u = (int32_t)u;
        out[i].v = (int32_t)v;
        out[i].d = (int32_t)(wide(1000000000) + 1);
    }
}

int main(void) {
    triple *edges = malloc((size_t)COUNT * N * sizeof *edges);
    triple *queries = malloc((size_t)COUNT * N * sizeof *queries);
    for (int c = 0; c < COUNT; c++) {
        triples(edges + (int64_t)c * N, N, N);
        triples(queries + (int64_t)c * N, N, N);
    }
    uint8_t *answer = malloc(N);
    int64_t trues = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            distance_limited_paths_exist(N, edges + (int64_t)c * N, N, queries + (int64_t)c * N, N, answer);
            for (int64_t i = 0; i < N; i++) {
                trues += answer[i];
                check = (check * 31 + (answer[i] ? 2 : 1) + r) % 1000000007;
            }
        }
    }
    printf("%d graphs of %d nodes, edges and queries, %d rounds: %lld true, checksum %lld\n", COUNT, N, ROUNDS, (long long)trues, (long long)check);
    free(edges);
    free(queries);
    free(answer);
    return 0;
}
