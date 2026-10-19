// LeetCode 797 — All Paths From Source to Target: the bench, in C.
// Mirrors all_paths_source_target.kara: a depth first search keeping the
// path so far, copying it into a fresh allocation at node n - 1.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t *v; int64_t len; } Path;
typedef struct { Path *p; int64_t len, cap; } Paths;
typedef struct { int64_t next[15][15]; int64_t deg[15]; int64_t n; } Graph;

static void walk(const Graph *g, int64_t node, int64_t *path, int64_t len, Paths *out) {
    if (node == g->n - 1) {
        if (out->len == out->cap) {
            out->cap = out->cap ? out->cap * 2 : 4;
            out->p = realloc(out->p, out->cap * sizeof(Path));
        }
        int64_t *copy = malloc(len * sizeof(int64_t));
        memcpy(copy, path, len * sizeof(int64_t));
        out->p[out->len++] = (Path){copy, len};
        return;
    }
    for (int64_t k = 0; k < g->deg[node]; k++) {
        int64_t next = g->next[node][k];
        path[len] = next;
        walk(g, next, path, len + 1, out);
    }
}

static Paths all_paths_source_target(const Graph *g) {
    Paths out = {NULL, 0, 0};
    int64_t path[15];
    path[0] = 0;
    walk(g, 0, path, 1, &out);
    return out;
}

static int64_t seed = 797;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 15;
    static Graph graphs[1024];
    for (int g = 0; g < 1024; g++) {
        int64_t order[15];
        order[0] = 0;
        for (int64_t i = 1; i < n - 1; i++) order[i] = i;
        for (int64_t i = 2; i < n - 1; i++) {
            int64_t j = 1 + next_random() % i;
            int64_t t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        order[n - 1] = n - 1;
        int64_t chance = 1 + next_random() % 4;
        graphs[g].n = n;
        memset(graphs[g].deg, 0, sizeof graphs[g].deg);
        for (int64_t a = 0; a < n; a++)
            for (int64_t b = a + 1; b < n; b++)
                if (next_random() % 5 < chance) {
                    int64_t u = order[a];
                    graphs[g].next[u][graphs[g].deg[u]++] = order[b];
                }
    }
    const int64_t rounds = 40960;
    int64_t count = 0, nodes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        Paths paths = all_paths_source_target(&graphs[r % 1024]);
        count += paths.len;
        for (int64_t k = 0; k < paths.len; k++) {
            nodes += paths.p[k].len;
            int64_t h = 0;
            for (int64_t i = 0; i < paths.p[k].len; i++) h = (h * 31 + paths.p[k].v[i] + 1) % 1000000007;
            check = (check + h) % 1000000007;
            free(paths.p[k].v);
        }
        free(paths.p);
    }
    printf("%lld graphs: %lld paths through %lld nodes, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)nodes, (long long)check);
    return 0;
}
