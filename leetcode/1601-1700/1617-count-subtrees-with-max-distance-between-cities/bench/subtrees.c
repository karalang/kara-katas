// LeetCode #1617: Count Subtrees With Max Distance Between Cities -- the
// bench in C, mirroring subtrees.kara: all pair distances by
// Floyd-Warshall, then every mask of two or more cities that holds one
// road fewer than it has cities, its largest distance counted.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define TREES 400
#define N 15

static void count_subgraphs_for_each_diameter(int n, const int32_t (*edges)[2], int32_t *answer) {
    int64_t far = n + 1;
    int64_t dist[N][N];
    int64_t ea[N], eb[N];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) dist[i][j] = i == j ? 0 : far;
    for (int e = 0; e < n - 1; e++) {
        int64_t a = edges[e][0] - 1, b = edges[e][1] - 1;
        dist[a][b] = dist[b][a] = 1;
        ea[e] = a;
        eb[e] = b;
    }
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (dist[i][k] + dist[k][j] < dist[i][j]) dist[i][j] = dist[i][k] + dist[k][j];
    for (int d = 0; d < n - 1; d++) answer[d] = 0;
    for (int64_t mask = 1; mask < (1LL << n); mask++) {
        int64_t size = __builtin_popcountll(mask);
        if (size < 2) continue;
        int64_t roads = 0;
        for (int e = 0; e < n - 1; e++)
            if ((mask >> ea[e] & 1) == 1 && (mask >> eb[e] & 1) == 1) roads++;
        if (roads != size - 1) continue;
        int64_t widest = 0;
        for (int i = 0; i < n; i++)
            if ((mask >> i & 1) == 1)
                for (int j = i + 1; j < n; j++)
                    if ((mask >> j & 1) == 1 && dist[i][j] > widest) widest = dist[i][j];
        answer[widest - 1]++;
    }
}

static int64_t seed = 1617;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static void random_tree(int n, int32_t (*edges)[2]) {
    int32_t name[N];
    for (int c = 0; c < n; c++) name[c] = c + 1;
    for (int i = n - 1; i >= 1; i--) {
        int64_t j = next_random() % (i + 1);
        int32_t t = name[i];
        name[i] = name[j];
        name[j] = t;
    }
    for (int c = 1; c < n; c++) {
        int64_t p = next_random() % c;
        edges[c - 1][0] = name[c];
        edges[c - 1][1] = name[p];
    }
}

int main(void) {
    static int32_t trees[TREES][N - 1][2];
    for (int t = 0; t < TREES; t++) random_tree(N, trees[t]);
    int64_t check = 0, subtrees = 0;
    int32_t answer[N - 1];
    for (int t = 0; t < TREES; t++) {
        count_subgraphs_for_each_diameter(N, trees[t], answer);
        for (int d = 0; d < N - 1; d++) {
            check = mix(check, answer[d]);
            subtrees += answer[d];
        }
    }
    printf("%d trees of %d cities: %lld subtrees, checksum %lld\n", TREES, N, (long long)subtrees, (long long)check);
    return 0;
}
