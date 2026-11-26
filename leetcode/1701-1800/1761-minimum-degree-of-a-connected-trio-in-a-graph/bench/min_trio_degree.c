// LeetCode #1761: Minimum Degree of a Connected Trio in a Graph -- the bench
// in C, mirroring min_trio_degree.kara: an adjacency matrix, the degrees,
// and every edge (u, v) with each w above v.
#include <limits.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PAIRS (400 * 399 / 2)

static int min_trio_degree(int n, int (*edges)[2], int m) {
    bool *joined = calloc((size_t)(n + 1) * (n + 1), sizeof(bool));
    int *degree = calloc(n + 1, sizeof(int));
    for (int i = 0; i < m; i++) {
        int u = edges[i][0], v = edges[i][1];
        joined[u * (n + 1) + v] = joined[v * (n + 1) + u] = true;
        degree[u]++;
        degree[v]++;
    }
    int best = INT_MAX;
    for (int u = 1; u <= n; u++)
        for (int v = u + 1; v <= n; v++) {
            if (!joined[u * (n + 1) + v]) continue;
            for (int w = v + 1; w <= n; w++)
                if (joined[u * (n + 1) + w] && joined[v * (n + 1) + w]) {
                    int d = degree[u] + degree[v] + degree[w] - 6;
                    if (d < best) best = d;
                }
        }
    free(joined);
    free(degree);
    return best == INT_MAX ? -1 : best;
}

int main(void) {
    int64_t seed = 1761;
    static int pu[PAIRS], pv[PAIRS];
    static int64_t pw[PAIRS];
    static int edges[PAIRS][2];
    int k = 0;
    for (int u = 1; u < 401; u++)
        for (int v = u + 1; v < 401; v++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            pu[k] = u;
            pv[k] = v;
            pw[k] = seed / 65536 % 1000;
            k++;
        }
    int64_t check = 0;
    for (int64_t call = 0; call < 40; call++) {
        int64_t threshold = 300 + (check + call * 7919) % 500;
        int m = 0;
        for (int i = 0; i < PAIRS; i++)
            if (pw[i] < threshold) {
                edges[m][0] = pu[i];
                edges[m][1] = pv[i];
                m++;
            }
        check = (check * 31 + min_trio_degree(400, edges, m) + 1) % 1000000007;
    }
    printf("40 calls on 400 nodes: checksum %lld\n", (long long)check);
    return 0;
}
