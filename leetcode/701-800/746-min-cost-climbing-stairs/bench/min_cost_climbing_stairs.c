// LeetCode 746 — Min Cost Climbing Stairs, bench: the ★ arm (two running
// totals) on a staircase of 1000 steps whose costs keep changing.
// Mirrors min_cost_climbing_stairs.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t min_cost_climbing_stairs(const int64_t *cost, int64_t n) {
    int64_t before = 0, here = 0;
    for (int64_t i = 2; i <= n; i++) {
        int64_t next = before + cost[i - 2] < here + cost[i - 1] ? before + cost[i - 2] : here + cost[i - 1];
        before = here;
        here = next;
    }
    return here;
}

static int64_t seed = 746;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 300000, n = 1000;
    int64_t cost[1000];
    for (int64_t i = 0; i < n; i++) cost[i] = next_random() % 1000;
    int64_t total = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < 5; c++) {
            int64_t i = next_random() % n;
            cost[i] = next_random() % 1000;
        }
        total += min_cost_climbing_stairs(cost, n);
    }
    printf("%lld rounds on 1000 steps: least costs sum to %lld\n", (long long)rounds, (long long)total);
    return 0;
}
