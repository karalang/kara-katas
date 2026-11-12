// LeetCode #1135: Connecting Cities With Minimum Cost -- the bench in C, the
// same algorithm and workload as minimum_cost.kara: each road its own
// allocation of three values, the roads copied one by one and sorted with
// `qsort` in every call, the same 8 networks and 50 rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int by_cost(const void *a, const void *b) {
    int64_t x = (*(int64_t *const *)a)[2], y = (*(int64_t *const *)b)[2];
    return (x > y) - (x < y);
}

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int64_t minimum_cost(int64_t n, int64_t **connections, int64_t m) {
    int64_t **roads = malloc(m * sizeof(int64_t *));
    for (int64_t i = 0; i < m; i++) {
        roads[i] = malloc(3 * sizeof(int64_t));
        roads[i][0] = connections[i][0];
        roads[i][1] = connections[i][1];
        roads[i][2] = connections[i][2];
    }
    qsort(roads, m, sizeof(int64_t *), by_cost);
    int64_t *parent = malloc((n + 1) * sizeof(int64_t));
    int64_t *size = malloc((n + 1) * sizeof(int64_t));
    for (int64_t i = 0; i <= n; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    int64_t total = 0, joined = 1;
    for (int64_t i = 0; i < m; i++) {
        int64_t a = find(parent, roads[i][0]);
        int64_t b = find(parent, roads[i][1]);
        if (a != b) {
            if (size[a] < size[b]) {
                int64_t t = a;
                a = b;
                b = t;
            }
            parent[b] = a;
            size[a] += size[b];
            total += roads[i][2];
            joined += 1;
        }
    }
    for (int64_t i = 0; i < m; i++) free(roads[i]);
    free(roads);
    free(parent);
    free(size);
    return joined == n ? total : -1;
}

static int64_t seed = 1135;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t **networks[8];
    for (int j = 0; j < 8; j++) {
        networks[j] = malloc(10000 * sizeof(int64_t *));
        for (int i = 0; i < 10000; i++) {
            int64_t *road = malloc(3 * sizeof(int64_t));
            road[0] = next_random() % 1000 + 1;
            road[1] = next_random() % 999 + 1;
            if (road[1] >= road[0]) road[1] += 1;
            int64_t high = next_random();
            road[2] = (high * 32768 + next_random()) % 100000 + 1;
            networks[j][i] = road;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 50; round++) {
        for (int64_t j = 0; j < 8; j++) {
            int64_t at = (round * 7919 + j * 104729) % 10000;
            networks[j][at][2] = (networks[j][at][2] * 7 + 13) % 100000 + 1;
            int64_t r = minimum_cost(1000, networks[j], 10000);
            total += r;
            check = (check * 31 + r + 1) % 1000000007;
        }
    }
    printf("50 rounds over 8 networks of 1000 cities and 10000 roads: costs total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int j = 0; j < 8; j++) {
        for (int i = 0; i < 10000; i++) free(networks[j][i]);
        free(networks[j]);
    }
    return 0;
}
