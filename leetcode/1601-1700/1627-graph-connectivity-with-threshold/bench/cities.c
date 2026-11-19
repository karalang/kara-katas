// LeetCode #1627: Graph Connectivity With Threshold -- the bench's C
// mirror: the ★ arm on 100 problems of 10000 cities, thresholds 0 to 99,
// each asked the same 100000 queries, all drawn first.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t find(int32_t *parent, int32_t x) {
    int32_t root = x;
    while (parent[root] != root) root = parent[root];
    while (parent[x] != root) {
        int32_t next = parent[x];
        parent[x] = root;
        x = next;
    }
    return root;
}

static bool *are_connected(int32_t n, int32_t threshold, const int32_t (*queries)[2], int q) {
    int32_t *parent = malloc(sizeof(int32_t) * (size_t)(n + 1));
    for (int32_t i = 0; i <= n; i++) parent[i] = i;
    for (int32_t z = threshold + 1; z <= n; z++) {
        for (int32_t m = 2 * z; m <= n; m += z) {
            int32_t a = find(parent, z), b = find(parent, m);
            if (a != b) parent[b] = a;
        }
    }
    bool *answers = malloc(sizeof(bool) * (size_t)q);
    for (int i = 0; i < q; i++) answers[i] = find(parent, queries[i][0]) == find(parent, queries[i][1]);
    free(parent);
    return answers;
}

static int64_t seed = 1627;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { PROBLEMS = 100, Q = 100000 };
    const int64_t n = 10000;
    static int32_t thresholds[PROBLEMS];
    static int32_t queries[Q][2];
    for (int i = 0; i < PROBLEMS; i++) thresholds[i] = (int32_t)(next_random() % 100);
    for (int i = 0; i < Q; i++) {
        int64_t a = next_random() % n + 1;
        int64_t b = next_random() % n + 1;
        queries[i][0] = (int32_t)a;
        queries[i][1] = (int32_t)b;
    }
    int64_t check = 0, total = 0;
    for (int t = 0; t < PROBLEMS; t++) {
        bool *answers = are_connected((int32_t)n, thresholds[t], (const int32_t (*)[2])queries, Q);
        int64_t yes = 0;
        for (int i = 0; i < Q; i++)
            if (answers[i]) yes++;
        free(answers);
        total += yes;
        check = (check * 31 + yes + 1) % 1000000007;
    }
    printf("100 problems of 10000 cities and 100000 queries: %lld connected, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
