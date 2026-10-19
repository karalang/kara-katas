// LeetCode 787 — Cheapest Flights Within K Stops: the bench, in C.
// Mirrors find_cheapest_price.kara: Bellman-Ford for k + 1 rounds, each
// round reading a fresh copy of the costs, over the same 64 networks.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t from, to, price;
} Flight;

static int64_t find_cheapest_price(int64_t n, const Flight *flights, int64_t count, int64_t src, int64_t dst,
                                   int64_t k) {
    const int64_t unreached = INT64_MAX;
    int64_t *cost = malloc(n * sizeof *cost);
    for (int64_t i = 0; i < n; i++) cost[i] = unreached;
    cost[src] = 0;
    for (int64_t round = 0; round < k + 1; round++) {
        int64_t *before = malloc(n * sizeof *before);
        memcpy(before, cost, n * sizeof *before);
        for (int64_t i = 0; i < count; i++) {
            const Flight *f = &flights[i];
            if (before[f->from] != unreached && before[f->from] + f->price < cost[f->to]) {
                cost[f->to] = before[f->from] + f->price;
            }
        }
        free(before);
    }
    int64_t answer = cost[dst] == unreached ? -1 : cost[dst];
    free(cost);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 787;
    static Flight networks[64][1000];
    for (int net = 0; net < 64; net++) {
        static char taken[10000];
        memset(taken, 0, sizeof taken);
        int count = 0;
        while (count < 1000) {
            int64_t from = next_random(&seed) % 100;
            int64_t to = next_random(&seed) % 100;
            if (from != to && !taken[from * 100 + to]) {
                taken[from * 100 + to] = 1;
                networks[net][count++] = (Flight){from, to, 1 + next_random(&seed) % 10000};
            }
        }
    }
    int64_t rounds = 20000, found = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t src = next_random(&seed) % 100;
        int64_t dst = (src + 1 + next_random(&seed) % 99) % 100;
        int64_t k = next_random(&seed) % 100;
        int64_t answer = find_cheapest_price(100, networks[r % 64], 1000, src, dst, k);
        if (answer != -1) found++;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("%lld rounds of 100-city networks: %lld with a way, checksum %lld\n", (long long)rounds, (long long)found,
           (long long)check);
    return 0;
}
