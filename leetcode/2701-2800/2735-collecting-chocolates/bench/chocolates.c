// LeetCode #2735: Collecting Chocolates -- the bench (chocolates.kara in
// C): each type's cheapest price within k turns, narrowed one turn at a
// time, and the least of k x plus their sum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t min_cost(const int64_t *nums, int64_t n, int64_t x, int64_t *cheapest) {
    memcpy(cheapest, nums, sizeof(int64_t) * n);
    int64_t best = 0;
    for (int64_t t = 0; t < n; t++) best += nums[t];
    for (int64_t k = 1; k < n; k++) {
        for (int64_t t = 0; t < n; t++) {
            int64_t v = nums[(t - k + n) % n];
            if (v < cheapest[t]) cheapest[t] = v;
        }
        int64_t total = 0;
        for (int64_t t = 0; t < n; t++) total += cheapest[t];
        if (k * x + total < best) best = k * x + total;
    }
    return best;
}

static int64_t seed = 2735;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int cases = 100, rounds = 3;
    const int64_t n = 1000;
    int64_t *nums = malloc(sizeof(int64_t) * n * cases);
    int64_t xs[100];
    for (int c = 0; c < cases; c++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t hi = next_random();
            nums[c * n + i] = (hi * 32768 + next_random()) % 1000000000 + 1;
        }
        int64_t hi = next_random();
        xs[c] = (hi * 32768 + next_random()) % 10000000 + 1;
    }
    int64_t *cheapest = malloc(sizeof(int64_t) * n);
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int c = 0; c < cases; c++) {
            int64_t cost = min_cost(nums + c * n, n, xs[c], cheapest);
            sum += cost;
            check = (check * 31 + cost + r) % 1000000007;
        }
    }
    printf("%d cases of %lld chocolates, %d rounds: costs sum to %lld, checksum %lld\n", cases, (long long)n, rounds, (long long)sum, (long long)check);
    free(nums); free(cheapest);
    return 0;
}
