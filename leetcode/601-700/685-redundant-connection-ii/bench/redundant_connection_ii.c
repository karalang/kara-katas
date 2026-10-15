// LeetCode #685: Redundant Connection II -- union-find and two
// candidates. Bench.
//
// 100 random rooted trees of 20,000 vertices, each with one more directed
// edge, are built once; then 30 rounds answer every graph.

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

static Edge find_redundant_directed_connection(const Edge *edges, int64_t n) {
    int64_t *into = malloc((size_t)(n + 1) * sizeof(int64_t));
    for (int64_t v = 0; v <= n; v++) {
        into[v] = -1;
    }
    int64_t first = -1, second = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t b = edges[i].b;
        if (into[b] == -1) {
            into[b] = i;
        } else {
            first = into[b];
            second = i;
        }
    }
    int64_t *parent = malloc((size_t)(n + 1) * sizeof(int64_t));
    for (int64_t v = 0; v <= n; v++) {
        parent[v] = v;
    }
    Edge out = second >= 0 ? edges[second] : (Edge){0, 0};
    for (int64_t i = 0; i < n; i++) {
        if (i != second) {
            int64_t ra = find(parent, edges[i].a);
            int64_t rb = find(parent, edges[i].b);
            if (ra == rb) {
                out = first == -1 ? edges[i] : edges[first];
                break;
            }
            parent[rb] = ra;
        }
    }
    free(into);
    free(parent);
    return out;
}

static int64_t seed = 685;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 100, n = 20000, rounds = 30;
    Edge **graphs = malloc((size_t)count * sizeof(Edge *));
    int64_t *name = malloc((size_t)n * sizeof(int64_t));
    int64_t *up = malloc((size_t)(n + 1) * sizeof(int64_t));
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
        for (int64_t v = 0; v <= n; v++) {
            up[v] = 0;
        }
        Edge *edges = malloc((size_t)n * sizeof(Edge));
        for (int64_t v = 1; v < n; v++) {
            int64_t a = name[next_random() % v];
            up[name[v]] = a;
            edges[v - 1] = (Edge){a, name[v]};
        }
        for (;;) {
            int64_t a = 1 + next_random() % n;
            int64_t b = 1 + next_random() % n;
            if (a != b && up[b] != a) {
                edges[n - 1] = (Edge){a, b};
                break;
            }
        }
        for (int64_t k = n - 1; k > 0; k--) {
            int64_t j = next_random() % (k + 1);
            Edge t = edges[k];
            edges[k] = edges[j];
            edges[j] = t;
        }
        graphs[c] = edges;
    }
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            Edge e = find_redundant_directed_connection(graphs[c], n);
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
