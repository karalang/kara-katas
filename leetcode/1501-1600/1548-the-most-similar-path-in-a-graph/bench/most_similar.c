// LeetCode #1548: The Most Similar Path in a Graph -- bench: the ★ arm (a
// DP over the target's places) over 100 connected graphs of 50 to 100
// cities named from up to 26 names, each with a target of 100 names, built
// once, each asked 20 times. C mirror of most_similar.kara: the neighbour
// lists, cost and from tables are flat heap arrays, built on every call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char s[4]; } Name;

static int64_t *most_similar(int64_t n, int64_t m, const int64_t *roads, const Name *names,
                             int64_t length, const Name *target) {
    int64_t *degree = calloc(n + 1, sizeof(int64_t));
    for (int64_t r = 0; r < m; r++) {
        degree[roads[2 * r] + 1]++;
        degree[roads[2 * r + 1] + 1]++;
    }
    for (int64_t v = 0; v < n; v++) degree[v + 1] += degree[v];
    int64_t *fill = malloc(n * sizeof(int64_t));
    memcpy(fill, degree, n * sizeof(int64_t));
    int64_t *next_to = malloc(2 * m * sizeof(int64_t));
    for (int64_t r = 0; r < m; r++) {
        int64_t a = roads[2 * r], b = roads[2 * r + 1];
        next_to[fill[a]++] = b;
        next_to[fill[b]++] = a;
    }
    int64_t *cost = malloc(length * n * sizeof(int64_t));
    int64_t *from = calloc(length * n, sizeof(int64_t));
    for (int64_t i = 0; i < length * n; i++) cost[i] = INT64_MAX;
    for (int64_t v = 0; v < n; v++) cost[v] = strcmp(names[v].s, target[0].s) == 0 ? 0 : 1;
    for (int64_t t = 1; t < length; t++) {
        for (int64_t v = 0; v < n; v++) {
            int64_t miss = strcmp(names[v].s, target[t].s) == 0 ? 0 : 1;
            for (int64_t e = degree[v]; e < degree[v + 1]; e++) {
                int64_t u = next_to[e];
                if (cost[(t - 1) * n + u] + miss < cost[t * n + v]) {
                    cost[t * n + v] = cost[(t - 1) * n + u] + miss;
                    from[t * n + v] = u;
                }
            }
        }
    }
    int64_t last = 0;
    for (int64_t v = 1; v < n; v++)
        if (cost[(length - 1) * n + v] < cost[(length - 1) * n + last]) last = v;
    int64_t *path = malloc(length * sizeof(int64_t));
    path[length - 1] = last;
    for (int64_t t = length - 1; t >= 1; t--) path[t - 1] = from[t * n + path[t]];
    free(degree); free(fill); free(next_to); free(cost); free(from);
    return path;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static Name name_of(int64_t i) {
    Name name;
    name.s[0] = 'A' + i / 676 % 26;
    name.s[1] = 'A' + i / 26 % 26;
    name.s[2] = 'A' + i % 26;
    name.s[3] = 0;
    return name;
}

typedef struct {
    int64_t n, m;
    int64_t *roads;
    Name *names, target[100];
} Graph;

int main(void) {
    int64_t seed = 1548;
    static Graph graphs[100];
    static char joined[100][100];
    for (int g = 0; g < 100; g++) {
        Graph *G = &graphs[g];
        int64_t n = next_random(&seed) % 51 + 50;
        int64_t own = next_random(&seed) % 26 + 1;
        G->n = n;
        G->names = malloc(n * sizeof(Name));
        for (int64_t v = 0; v < n; v++) G->names[v] = name_of(next_random(&seed) % own);
        memset(joined, 0, sizeof joined);
        G->roads = malloc(2 * (n - 1 + 4 * n) * sizeof(int64_t));
        G->m = 0;
        for (int64_t v = 1; v < n; v++) {
            int64_t u = next_random(&seed) % v;
            joined[u][v] = joined[v][u] = 1;
            G->roads[2 * G->m] = v;
            G->roads[2 * G->m + 1] = u;
            G->m++;
        }
        int64_t extra = next_random(&seed) % (4 * n);
        for (int64_t k = 0; k < extra; k++) {
            int64_t a = next_random(&seed) % n;
            int64_t b = next_random(&seed) % n;
            if (a != b && !joined[a][b]) {
                joined[a][b] = joined[b][a] = 1;
                G->roads[2 * G->m] = a;
                G->roads[2 * G->m + 1] = b;
                G->m++;
            }
        }
        for (int t = 0; t < 100; t++) G->target[t] = name_of(next_random(&seed) % (own + 1));
    }
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 20; pass++) {
        for (int g = 0; g < 100; g++) {
            Graph *G = &graphs[g];
            int64_t *path = most_similar(G->n, G->m, G->roads, G->names, 100, G->target);
            int64_t distance = 0;
            for (int t = 0; t < 100; t++) {
                check = mix(check, path[t]);
                if (strcmp(G->names[path[t]].s, G->target[t].s) != 0) distance++;
            }
            total += distance;
            free(path);
        }
    }
    printf("20 passes over 100 graphs of up to 100 cities: distance %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
