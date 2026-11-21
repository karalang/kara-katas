// LeetCode #2477: Minimum Fuel Cost to Report to the Capital -- the bench,
// the ★ arm in C: a breadth-first order from the capital, walked
// backwards, gives each city its subtree's size, and the road out of it
// carries `ceil(size / seats)` cars. The neighbours are kept as
// compressed rows, one malloc'd array of every road's two ends.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimum_fuel_cost(const int64_t (*roads)[2], int64_t m, int64_t seats) {
    int64_t n = m + 1;
    int64_t *start = calloc(n + 1, sizeof(int64_t));
    int64_t *ends = malloc(sizeof(int64_t) * 2 * m);
    for (int64_t r = 0; r < m; r++) {
        start[roads[r][0] + 1]++;
        start[roads[r][1] + 1]++;
    }
    for (int64_t i = 0; i < n; i++) start[i + 1] += start[i];
    int64_t *fill = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) fill[i] = start[i];
    for (int64_t r = 0; r < m; r++) {
        ends[fill[roads[r][0]]++] = roads[r][1];
        ends[fill[roads[r][1]]++] = roads[r][0];
    }
    int64_t *parent = malloc(sizeof(int64_t) * n);
    int64_t *order = malloc(sizeof(int64_t) * n);
    int64_t *size = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) parent[i] = -1, size[i] = 1;
    parent[0] = 0;
    order[0] = 0;
    int64_t len = 1;
    for (int64_t next = 0; next < len; next++) {
        int64_t city = order[next];
        for (int64_t e = start[city]; e < start[city + 1]; e++) {
            int64_t other = ends[e];
            if (parent[other] < 0) {
                parent[other] = city;
                order[len++] = other;
            }
        }
    }
    int64_t fuel = 0;
    for (int64_t k = n - 1; k >= 1; k--) {
        int64_t city = order[k];
        fuel += (size[city] + seats - 1) / seats;
        size[parent[city]] += size[city];
    }
    free(start);
    free(ends);
    free(fill);
    free(parent);
    free(order);
    free(size);
    return fuel;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2477;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

#define N 10000

static int64_t trees[20][N - 1][2];

static void random_roads(int64_t (*roads)[2]) {
    for (int64_t k = 1; k < N; k++) {
        int64_t other = wide_random() % k;
        if (next_random() % 2 == 0) {
            roads[k - 1][0] = k;
            roads[k - 1][1] = other;
        } else {
            roads[k - 1][0] = other;
            roads[k - 1][1] = k;
        }
    }
    for (int64_t i = N - 2; i > 0; i--) {
        int64_t j = wide_random() % (i + 1);
        int64_t a = roads[i][0], b = roads[i][1];
        roads[i][0] = roads[j][0];
        roads[i][1] = roads[j][1];
        roads[j][0] = a;
        roads[j][1] = b;
    }
}

int main(void) {
    // 20 random trees of 10^4 cities built once; then 60 passes, each
    // answering every tree with 1 to 50 seats chosen by the checksum so
    // far, folding the fuel plus the pass into the checksum
    for (int t = 0; t < 20; t++) random_roads(trees[t]);
    int64_t check = 0;
    for (int64_t p = 0; p < 60; p++) {
        for (int t = 0; t < 20; t++) {
            int64_t seats = 1 + check % 50;
            check = (check * 31 + minimum_fuel_cost((const int64_t (*)[2])trees[t], N - 1, seats) + p) % 1000000007;
        }
    }
    printf("60 passes over 20 trees of 10^4: checksum %lld\n", (long long)check);
    return 0;
}
