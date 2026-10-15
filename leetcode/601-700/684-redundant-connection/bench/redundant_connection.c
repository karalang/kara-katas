// LeetCode #684: Redundant Connection -- union-find. Bench.
//
// 100 random trees of 20,000 vertices, each with one more edge, are
// built once; then 30 rounds answer every graph.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t a, b;
} Edge;

static int64_t find(int64_t *parent, int64_t x) {
    int64_t v = x;
    while (parent[v] != v) {
        parent[v] = parent[parent[v]];
        v = parent[v];
    }
    return v;
}

static Edge find_redundant_connection(const Edge *edges, int64_t n) {
    int64_t *parent = malloc((size_t)(n + 1) * sizeof(int64_t));
    int64_t *size = malloc((size_t)(n + 1) * sizeof(int64_t));
    for (int64_t v = 0; v <= n; v++) {
        parent[v] = v;
        size[v] = 1;
    }
    Edge out = {0, 0};
    for (int64_t i = 0; i < n; i++) {
        int64_t ra = find(parent, edges[i].a);
        int64_t rb = find(parent, edges[i].b);
        if (ra == rb) {
            out = edges[i];
            break;
        }
        if (size[ra] < size[rb]) {
            parent[ra] = rb;
            size[rb] += size[ra];
        } else {
            parent[rb] = ra;
            size[ra] += size[rb];
        }
    }
    free(parent);
    free(size);
    return out;
}

static int64_t seed = 684;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 100, n = 20000, rounds = 30;
    Edge **graphs = malloc((size_t)count * sizeof(Edge *));
    int64_t *name = malloc((size_t)n * sizeof(int64_t));
    int64_t *up = malloc((size_t)n * sizeof(int64_t));
    for (int64_t c = 0; c < count; c++) {
        for (int64_t v = 0; v < n; v++) {
            name[v] = v + 1;
        }
        for (int64_t i = n - 1; i > 0; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = name[i];
            name[i] = name[j];
            name[j] = t;
        }
        Edge *edges = malloc((size_t)n * sizeof(Edge));
        up[0] = 0;
        for (int64_t v = 1; v < n; v++) {
            up[v] = next_random() % v;
            edges[v - 1] = (Edge){name[up[v]], name[v]};
        }
        for (;;) {
            int64_t x = next_random() % n;
            int64_t y = next_random() % n;
            int64_t lo = x < y ? x : y, hi = x < y ? y : x;
            if (lo != hi && up[hi] != lo) {
                edges[n - 1] = (Edge){name[lo], name[hi]};
                break;
            }
        }
        for (int64_t k = n - 1; k > 0; k--) {
            int64_t j = next_random() % (k + 1);
            Edge t = edges[k];
            edges[k] = edges[j];
            edges[j] = t;
        }
        for (int64_t e = 0; e < n; e++) {
            if (next_random() % 2 == 0) {
                edges[e] = (Edge){edges[e].b, edges[e].a};
            }
        }
        graphs[c] = edges;
    }
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            Edge e = find_redundant_connection(graphs[c], n);
            sum = (sum * 31 + e.a * 20011 + e.b + r) % 1000000007;
        }
    }
    printf("%lld graphs answered, checksum %lld\n", (long long)(count * rounds), (long long)sum);
    for (int64_t c = 0; c < count; c++) {
        free(graphs[c]);
    }
    free(graphs);
    free(name);
    free(up);
    return 0;
}
