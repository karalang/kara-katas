// LeetCode #2508: Add Edges to Make Degrees of All Nodes Even -- C
// mirror of the benchmark (even.kara): the same graphs, passes and
// checksum, the edges held in an open-addressed table of 2^18 slots
// probed linearly, cleared on every ask.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS (1 << 18)
static int64_t table[SLOTS];

static uint64_t slot_of(int64_t code) {
    return (uint64_t)code * 0x9E3779B97F4A7C15ULL >> 46;
}

static void insert(int64_t code) {
    uint64_t s = slot_of(code);
    while (table[s] != 0 && table[s] != code) s = (s + 1) & (SLOTS - 1);
    table[s] = code;
}

static int contains(int64_t code) {
    uint64_t s = slot_of(code);
    while (table[s] != 0) {
        if (table[s] == code) return 1;
        s = (s + 1) & (SLOTS - 1);
    }
    return 0;
}

static int64_t code_of(int64_t n, int64_t a, int64_t b) {
    return (a < b ? a : b) * (n + 1) + (a < b ? b : a);
}

#define FREE(a, b) (!contains(code_of(n, (a), (b))))

typedef struct { int64_t a, b; } Edge;

static int is_possible(int64_t n, const Edge *edges, int64_t m) {
    int64_t *degree = calloc(n + 1, sizeof *degree);
    memset(table, 0, sizeof table);
    for (int64_t i = 0; i < m; i++) {
        degree[edges[i].a]++;
        degree[edges[i].b]++;
        insert(code_of(n, edges[i].a, edges[i].b));
    }
    int64_t odd[5], k = 0;
    for (int64_t v = 1; v <= n; v++)
        if (degree[v] % 2 == 1) {
            if (k < 5) odd[k] = v;
            k++;
        }
    free(degree);
    if (k == 0) return 1;
    if (k == 2) {
        int64_t a = odd[0], b = odd[1];
        if (FREE(a, b)) return 1;
        for (int64_t c = 1; c <= n; c++)
            if (c != a && c != b && FREE(a, c) && FREE(b, c)) return 1;
        return 0;
    }
    if (k == 4) {
        int64_t a = odd[0], b = odd[1], c = odd[2], d = odd[3];
        return (FREE(a, b) && FREE(c, d)) || (FREE(a, c) && FREE(b, d)) || (FREE(a, d) && FREE(b, c));
    }
    return 0;
}

typedef struct { int64_t n, m; Edge *edges; } Graph;

static Graph ring_of(int64_t n, int64_t step) {
    Graph g = {n, n, malloc(n * sizeof(Edge))};
    for (int64_t v = 1; v <= n; v++) g.edges[v - 1] = (Edge){v, (v + step - 1) % n + 1};
    return g;
}

static Graph joined_ring(int64_t spare) {
    Graph g = {33000, 0, malloc(100000 * sizeof(Edge))};
    for (int64_t v = 3; v < 33000; v++) g.edges[g.m++] = (Edge){v, v + 1};
    g.edges[g.m++] = (Edge){33000, 3};
    g.edges[g.m++] = (Edge){1, 2};
    for (int64_t v = 3; v <= 33000; v++)
        if (v != spare)
            for (int64_t h = 1; h <= 2; h++) g.edges[g.m++] = (Edge){h, v};
    return g;
}

int main(void) {
    const int64_t passes = 90;
    Graph graphs[4] = {ring_of(100000, 1), ring_of(100000, 2), joined_ring(0), joined_ring(17000)};
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int i = 0; i < 4; i++) {
            Graph *g = &graphs[i];
            int64_t at = check % g->m;
            Edge taken = g->edges[at];
            g->edges[at] = g->edges[g->m - 1];
            g->m--;
            int64_t answer = is_possible(g->n, g->edges, g->m) ? 2 : 1;
            check = (check * 31 + answer + p) % 1000000007;
            g->edges[g->m] = g->edges[at];
            g->edges[at] = taken;
            g->m++;
        }
    }
    printf("%lld passes over 4 graphs: checksum %lld\n", (long long)passes, (long long)check);
    for (int i = 0; i < 4; i++) free(graphs[i].edges);
    return 0;
}
