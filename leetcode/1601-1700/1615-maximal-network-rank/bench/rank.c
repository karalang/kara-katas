// LeetCode #1615: Maximal Network Rank -- the bench in C, mirroring
// rank.kara: each city's degree and a table of which pairs share a road,
// then every pair's rank.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NETWORKS 2000
#define N 100

typedef struct {
    int32_t (*roads)[2];
    int64_t len;
} Network;

static int32_t maximal_network_rank(int n, const int32_t (*roads)[2], int64_t m) {
    int32_t *degree = calloc(n, sizeof(int32_t));
    bool *joined = calloc((size_t)n * n, sizeof(bool));
    for (int64_t i = 0; i < m; i++) {
        int a = roads[i][0], b = roads[i][1];
        degree[a]++;
        degree[b]++;
        joined[a * n + b] = true;
        joined[b * n + a] = true;
    }
    int32_t best = 0;
    for (int a = 0; a < n; a++)
        for (int b = a + 1; b < n; b++) {
            int32_t rank = degree[a] + degree[b] - (joined[a * n + b] ? 1 : 0);
            if (rank > best) best = rank;
        }
    free(degree);
    free(joined);
    return best;
}

static int64_t seed = 1615;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    Network *networks = malloc(NETWORKS * sizeof(Network));
    for (int k = 0; k < NETWORKS; k++) {
        networks[k].roads = malloc(N * (N - 1) / 2 * sizeof(int32_t[2]));
        networks[k].len = 0;
        for (int a = 0; a < N; a++)
            for (int b = a + 1; b < N; b++)
                if (next_random() % 4 == 0) {
                    networks[k].roads[networks[k].len][0] = a;
                    networks[k].roads[networks[k].len][1] = b;
                    networks[k].len++;
                }
    }
    int64_t check = 0, roads_seen = 0;
    for (int k = 0; k < NETWORKS; k++) {
        check = (check * 31 + maximal_network_rank(N, (const int32_t(*)[2])networks[k].roads, networks[k].len) + 1) %
                1000000007;
        roads_seen += networks[k].len;
    }
    printf("2000 networks of 100 cities: %lld roads, checksum %lld\n", (long long)roads_seen, (long long)check);
    for (int k = 0; k < NETWORKS; k++) free(networks[k].roads);
    free(networks);
    return 0;
}
