// LeetCode #2316: Count Unreachable Pairs of Nodes in an Undirected
// Graph -- the bench, the ★ arm in C. Union-find with union by size and
// path halving, then each set's root, met in order, pairs its size with
// every node of the sets before it.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { N = 100000, GRAPHS = 10 };

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int64_t count_pairs(int64_t n, const int64_t (*edges)[2], int64_t m) {
    int64_t *parent = malloc(sizeof(int64_t) * (size_t)n);
    int64_t *size = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t x = 0; x < n; x++) {
        parent[x] = x;
        size[x] = 1;
    }
    for (int64_t k = 0; k < m; k++) {
        int64_t ra = find(parent, edges[k][0]);
        int64_t rb = find(parent, edges[k][1]);
        if (ra != rb) {
            if (size[ra] < size[rb]) {
                int64_t t = ra;
                ra = rb;
                rb = t;
            }
            parent[rb] = ra;
            size[ra] += size[rb];
        }
    }
    int64_t before = 0, pairs = 0;
    for (int64_t x = 0; x < n; x++) {
        if (parent[x] == x) {
            pairs += size[x] * before;
            before += size[x];
        }
    }
    free(parent);
    free(size);
    return pairs;
}

static int64_t seed = 2316;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t edges[GRAPHS][N][2];
    static int64_t counts[GRAPHS];
    for (int64_t g = 0; g < GRAPHS; g++) {
        counts[g] = 0;
        for (int64_t i = 1; i < N; i++) {
            if (next_random() % (g + 3) != 0) {
                int64_t hi = next_random();
                int64_t j = (hi * 32768 + next_random()) % i;
                edges[g][counts[g]][0] = i;
                edges[g][counts[g]][1] = j;
                counts[g]++;
            }
        }
    }
    int64_t check = 0;
    for (int p = 0; p < 50; p++)
        for (int a = 0; a < GRAPHS; a++) {
            int g = (a + p) % GRAPHS;
            check = (check * 31 + count_pairs(N, (const int64_t (*)[2])edges[g], counts[g]) % 1000000007) % 1000000007;
        }
    printf("50 passes over 10 graphs of 10^5 nodes: checksum %lld\n", (long long)check);
    return 0;
}
