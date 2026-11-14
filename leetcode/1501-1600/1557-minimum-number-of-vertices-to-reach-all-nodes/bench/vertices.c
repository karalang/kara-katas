// LeetCode #1557: Minimum Number of Vertices to Reach All Nodes -- bench:
// the ★ arm (the nodes no edge ends at) over 20 acyclic graphs of 100000
// nodes and up to 300000 edges, built once, each asked 20 times. C mirror of vertices.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t *find_smallest_set_of_vertices(int64_t n, const int64_t *edges, int64_t m,
                                              int64_t *count) {
    char *reached = calloc(n, 1);
    for (int64_t e = 0; e < m; e++) reached[edges[2 * e + 1]] = 1;
    int64_t *sources = malloc(n * sizeof(int64_t));
    int64_t k = 0;
    for (int64_t v = 0; v < n; v++)
        if (!reached[v]) sources[k++] = v;
    free(reached);
    *count = k;
    return sources;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1557;
    static int64_t order[N];
    static int64_t *graphs[20];
    static int64_t sizes[20];
    for (int g = 0; g < 20; g++) {
        for (int64_t i = 0; i < N; i++) order[i] = i;
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t j = (next_random(&seed) * 32768 + next_random(&seed)) % (i + 1);
            int64_t t = order[i];
            order[i] = order[j];
            order[j] = t;
        }
        graphs[g] = malloc(2 * 300000 * sizeof(int64_t));
        int64_t m = 0;
        for (int e = 0; e < 300000; e++) {
            int64_t a = (next_random(&seed) * 32768 + next_random(&seed)) % N;
            int64_t b = (next_random(&seed) * 32768 + next_random(&seed)) % N;
            if (a < b) {
                graphs[g][2 * m] = order[a];
                graphs[g][2 * m + 1] = order[b];
                m++;
            }
        }
        sizes[g] = m;
    }
    int64_t check = 0, total = 0;
    for (int64_t pass = 0; pass < 20; pass++) {
        for (int64_t g = 0; g < 20; g++) {
            int64_t count;
            int64_t *sources = find_smallest_set_of_vertices(N, graphs[g], sizes[g], &count);
            total += count;
            check = mix(check, sources[(pass * 7 + g) % count]);
            free(sources);
        }
    }
    printf("20 passes over 20 graphs of 100000 nodes: %lld sources, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
