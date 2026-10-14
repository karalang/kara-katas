// LeetCode #628: Maximum Product of Three Numbers -- C mirror of the
// Kāra bench.
//
// The ★ arm's one pass over the same inputs and rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t maximum_product(const int64_t *nums, int64_t n) {
    int64_t max1 = INT64_MIN, max2 = INT64_MIN, max3 = INT64_MIN;
    int64_t min1 = INT64_MAX, min2 = INT64_MAX;
    for (int64_t i = 0; i < n; i++) {
        int64_t v = nums[i];
        if (v > max1) {
            max3 = max2;
            max2 = max1;
            max1 = v;
        } else if (v > max2) {
            max3 = max2;
            max2 = v;
        } else if (v > max3) {
            max3 = v;
        }
        if (v < min1) {
            min2 = min1;
            min1 = v;
        } else if (v < min2) {
            min2 = v;
        }
    }
    int64_t top = max1 * max2 * max3;
    int64_t ends = max1 * min1 * min2;
    return top > ends ? top : ends;
}

static int64_t seed = 628;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { INPUTS = 20, ROUNDS = 20000, COUNT = 10000 };
    int64_t *all[INPUTS];
    for (int i = 0; i < INPUTS; i++) {
        int64_t spread = 1 + next_random() % 1000;
        all[i] = malloc(COUNT * sizeof(int64_t));
        for (int j = 0; j < COUNT; j++) {
            all[i][j] = next_random() % (2 * spread + 1) - spread;
        }
    }
    int64_t checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t p = maximum_product(all[(r * 7) % INPUTS], COUNT);
        checksum = (checksum * 31 + p % 1000000007 + 1000000007) % 1000000007;
    }
    printf("%d inputs, %d rounds: checksum %lld\n", INPUTS, ROUNDS, (long long)checksum);
    for (int i = 0; i < INPUTS; i++) free(all[i]);
    return 0;
}
