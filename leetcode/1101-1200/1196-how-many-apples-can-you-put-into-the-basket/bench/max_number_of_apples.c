// LeetCode #1196 bench: the ★ arm in C, over the same 200 baskets of 10^3
// apples and 200 rounds as the Kāra bench; each call copies its basket
// and sorts the copy with `qsort`.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int ascending(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t max_number_of_apples(const int64_t *basket, int64_t n, int64_t *weight) {
    memcpy(weight, basket, n * sizeof(int64_t));
    qsort(weight, n, sizeof(int64_t), ascending);
    int64_t load = 0;
    for (int64_t i = 0; i < n; i++) {
        load += weight[i];
        if (load > 5000) {
            return i;
        }
    }
    return n;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t lows[4] = {1, 1, 300, 1};
    int64_t highs[4] = {1000, 20, 1000, 100};
    int64_t seed = 1196;
    int64_t *baskets = malloc(200 * 1000 * sizeof(int64_t));
    int64_t *weight = malloc(1000 * sizeof(int64_t));
    for (int k = 0; k < 200; k++) {
        int64_t low = lows[k % 4], high = highs[k % 4];
        for (int j = 0; j < 1000; j++) {
            baskets[k * 1000 + j] = low + next_random(&seed) % (high - low + 1);
        }
    }
    int64_t check = 0;
    for (int r = 0; r < 200; r++) {
        for (int k = 0; k < 200; k++) {
            int64_t apples = max_number_of_apples(baskets + k * 1000, 1000, weight);
            check = (check * 131 + apples + 1) % 1000000007;
        }
    }
    printf("200 rounds of 200 baskets of 1000 apples: checksum %lld\n", (long long)check);
    free(weight);
    free(baskets);
    return 0;
}
