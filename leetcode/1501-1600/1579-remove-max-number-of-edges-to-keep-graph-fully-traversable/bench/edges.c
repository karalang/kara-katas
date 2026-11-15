// LeetCode #1579 bench: the same two union-find structs, in C. Each edge is
// its own allocation and each graph's edge list grows by doubling, as the
// Kara Vec[Vec[i64]] does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *parent;
    int64_t *size;
    int64_t parts;
} Dsu;

static Dsu dsu_new(int64_t n) {
    Dsu d = {malloc((n + 1) * sizeof(int64_t)), malloc((n + 1) * sizeof(int64_t)), n};
    for (int64_t i = 0; i <= n; i++) {
        d.parent[i] = i;
        d.size[i] = 1;
    }
    return d;
}

static int64_t dsu_find(Dsu *d, int64_t x) {
    while (d->parent[x] != x) {
        d->parent[x] = d->parent[d->parent[x]];
        x = d->parent[x];
    }
    return x;
}

static int dsu_join(Dsu *d, int64_t a, int64_t b) {
    int64_t ra = dsu_find(d, a), rb = dsu_find(d, b);
    if (ra == rb) return 0;
    int64_t big = ra, small = rb;
    if (d->size[ra] < d->size[rb]) {
        big = rb;
        small = ra;
    }
    d->parent[small] = big;
    d->size[big] += d->size[small];
    d->parts -= 1;
    return 1;
}

static int64_t max_num_edges_to_remove(int64_t n, int64_t **edges, int64_t m) {
    Dsu alice = dsu_new(n), bob = dsu_new(n);
    int64_t kept = 0;
    for (int64_t i = 0; i < m; i++) {
        int64_t *e = edges[i];
        if (e[0] == 3) {
            int a = dsu_join(&alice, e[1], e[2]);
            int b = dsu_join(&bob, e[1], e[2]);
            if (a || b) kept++;
        }
    }
    for (int64_t i = 0; i < m; i++) {
        int64_t *e = edges[i];
        if (e[0] == 1 && dsu_join(&alice, e[1], e[2])) kept++;
        if (e[0] == 2 && dsu_join(&bob, e[1], e[2])) kept++;
    }
    int64_t result = (alice.parts != 1 || bob.parts != 1) ? -1 : m - kept;
    free(alice.parent);
    free(alice.size);
    free(bob.parent);
    free(bob.size);
    return result;
}

static int64_t seed = 1579;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

typedef struct {
    int64_t n, m;
    int64_t **edges;
} Graph;

int main(void) {
    Graph graphs[40];
    for (int g = 0; g < 40; g++) {
        int64_t n = 13000, m = 0, cap = 4;
        int64_t **edges = malloc(cap * sizeof(int64_t *));
        for (int64_t u = 1; u < n; u++) {
            int64_t draws = next_random() % 8 + 4;
            for (int64_t t = 0; t < draws; t++) {
                int64_t r = next_random() % 4;
                int64_t kind = (r < 2 ? r : 2) + 1;
                int64_t v = u + 1 + next_random() % 12;
                if (v > n) v = n;
                int64_t *e = malloc(3 * sizeof(int64_t));
                e[0] = kind;
                e[1] = u;
                e[2] = v;
                if (m == cap) edges = realloc(edges, (cap *= 2) * sizeof(int64_t *));
                edges[m++] = e;
            }
        }
        for (int64_t i = m - 1; i > 0; i--) {
            int64_t j = (next_random() * 32768 + next_random()) % (i + 1);
            int64_t *t = edges[i];
            edges[i] = edges[j];
            edges[j] = t;
        }
        graphs[g] = (Graph){n, m, edges};
    }
    int64_t check = 0, total = 0, stuck = 0;
    for (int g = 0; g < 40; g++) {
        int64_t removed = max_num_edges_to_remove(graphs[g].n, graphs[g].edges, graphs[g].m);
        if (removed < 0)
            stuck++;
        else
            total += removed;
        check = mix(check, removed + 1);
    }
    printf("40 graphs of 13000 nodes: %lld not traversable, edges removed %lld, checksum %lld\n", (long long)stuck,
           (long long)total, (long long)check);
    for (int g = 0; g < 40; g++) {
        for (int64_t i = 0; i < graphs[g].m; i++) free(graphs[g].edges[i]);
        free(graphs[g].edges);
    }
    return 0;
}
