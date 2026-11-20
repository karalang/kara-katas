// LeetCode #1724: Checking Existence of Edge Length Limited Paths II --
// the bench (dist.kara): a union-find by rank, never compressed, each
// node keeping the weight of the edge that hung it under its parent; a
// query climbs from each node while the links stay below the limit.
//
// The edges sorted by qsort on their weight; Kāra's and Rust's
// `sort_by_key` are stable merge sorts, and the union-find's answers do
// not depend on the order of edges of equal weight.

#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 20
#define ROUNDS 50
#define N 10000
#define M 10000
#define ASKED 10000
#define TOP 1000000000

typedef struct {
    int32_t u, v, w;
} Edge;

typedef struct {
    int32_t p, q, limit;
} Query;

typedef struct {
    int64_t parent[N];
    int32_t joined[N];
} Paths;

static int64_t root(const int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        x = parent[x];
    }
    return x;
}

static int by_weight(const void *a, const void *b) {
    int32_t x = ((const Edge *)a)->w, y = ((const Edge *)b)->w;
    return (x > y) - (x < y);
}

static void build(Paths *g, int n, const Edge *edge_list, int m) {
    static Edge edges[M];
    static int32_t rank[N];
    memcpy(edges, edge_list, sizeof(Edge) * m);
    qsort(edges, m, sizeof(Edge), by_weight);
    for (int i = 0; i < n; i++) {
        g->parent[i] = i;
        g->joined[i] = INT32_MAX;
        rank[i] = 0;
    }
    for (int i = 0; i < m; i++) {
        int64_t a = root(g->parent, edges[i].u);
        int64_t b = root(g->parent, edges[i].v);
        if (a == b) {
            continue;
        }
        if (rank[a] < rank[b]) {
            int64_t t = a;
            a = b;
            b = t;
        }
        g->parent[b] = a;
        g->joined[b] = edges[i].w;
        if (rank[a] == rank[b]) {
            rank[a]++;
        }
    }
}

static int64_t root_below(const Paths *g, int64_t x, int32_t limit) {
    while (g->joined[x] < limit) {
        x = g->parent[x];
    }
    return x;
}

static int query(const Paths *g, int32_t p, int32_t q, int32_t limit) {
    return root_below(g, p, limit) == root_below(g, q, limit);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    static Edge edges[COUNT][M];
    static Query queries[COUNT][ASKED];
    static Paths graph;
    int64_t seed = 1724;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < M; i++) {
            int64_t u = wide(&seed) % N;
            int64_t v = wide(&seed) % (N - 1);
            if (v >= u) {
                v++;
            }
            edges[c][i] = (Edge){(int32_t)u, (int32_t)v, (int32_t)(wide(&seed) % TOP + 1)};
        }
        for (int i = 0; i < ASKED; i++) {
            int64_t p = wide(&seed) % N;
            int64_t q = wide(&seed) % (N - 1);
            if (q >= p) {
                q++;
            }
            queries[c][i] = (Query){(int32_t)p, (int32_t)q, (int32_t)(wide(&seed) % TOP + 1)};
        }
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            build(&graph, N, edges[c], M);
            for (int i = 0; i < ASKED; i++) {
                int answer = query(&graph, queries[c][i].p, queries[c][i].q, queries[c][i].limit);
                yes += answer;
                check = (check * 31 + (answer ? 2 : 1) + r) % 1000000007;
            }
        }
    }
    printf("%d graphs of %d nodes and %d edges, %d queries each, %d rounds: %lld paths, checksum %lld\n", COUNT, N, M,
           ASKED, ROUNDS, (long long)yes, (long long)check);
    return 0;
}
