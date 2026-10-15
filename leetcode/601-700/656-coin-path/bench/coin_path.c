// Benchmark for #656: cheapest cost to the end, worked backwards, as the
// Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define UNREACHABLE INT64_MAX

static int64_t *cheapest_jump(const int64_t *coins, int64_t n, int64_t max_jump, int64_t *len) {
    int64_t *cost = malloc(n * sizeof *cost);
    int64_t *next = malloc(n * sizeof *next);
    for (int64_t i = 0; i < n; i++) {
        cost[i] = UNREACHABLE;
        next[i] = -1;
    }
    if (coins[n - 1] != -1) cost[n - 1] = coins[n - 1];
    for (int64_t i = n - 2; i >= 0; i--) {
        if (coins[i] == -1) continue;
        int64_t last = i + max_jump < n - 1 ? i + max_jump : n - 1;
        for (int64_t j = i + 1; j <= last; j++) {
            if (cost[j] != UNREACHABLE && coins[i] + cost[j] < cost[i]) {
                cost[i] = coins[i] + cost[j];
                next[i] = j;
            }
        }
    }
    int64_t *path = malloc(n * sizeof *path);
    *len = 0;
    if (cost[0] != UNREACHABLE) {
        for (int64_t at = 0; at != -1; at = next[at]) path[(*len)++] = at + 1;
    }
    free(cost);
    free(next);
    return path;
}

static int64_t seed = 656;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int inputs = 8, rounds = 40;
    int64_t n = 100000;
    int64_t *rows[8];
    for (int k = 0; k < inputs; k++) {
        rows[k] = malloc(n * sizeof **rows);
        for (int64_t i = 0; i < n; i++) {
            if (i > 0 && next_random() % 10 == 0) rows[k][i] = -1;
            else rows[k][i] = next_random() % 101;
        }
    }
    int64_t steps = 0, checksum = 0;
    for (int r = 0; r < rounds; r++) {
        const int64_t *coins = rows[(r * 3) % inputs];
        int64_t len;
        int64_t *path = cheapest_jump(coins, n, 100, &len);
        int64_t cost = 0;
        for (int64_t k = 0; k < len; k++) {
            cost += coins[path[k] - 1];
            checksum = (checksum * 31 + path[k]) % 1000000007;
        }
        steps += len;
        checksum = (checksum * 31 + cost) % 1000000007;
        free(path);
    }
    printf("%d rows of %lld, %d rounds: %lld steps, checksum %lld\n", inputs, (long long)n, rounds,
           (long long)steps, (long long)checksum);
    for (int k = 0; k < inputs; k++) free(rows[k]);
    return 0;
}
