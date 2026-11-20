// LeetCode #1262 bench, in C: the ★ arm (the best sum with each remainder
// modulo 3, in an array of three copied before each number) on 100 random
// lists of 4 * 10^4 numbers from 1 to 10^4 built once, 30 rounds; every
// answer folded into a checksum.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t max_sum_div_three(const int64_t *nums, int64_t n) {
    // -1 marks a remainder no sum has reached yet.
    int64_t best[3] = {0, -1, -1};
    for (int64_t i = 0; i < n; i++) {
        int64_t before[3];
        memcpy(before, best, sizeof best);
        for (int r = 0; r < 3; r++) {
            if (before[r] >= 0) {
                int64_t sum = before[r] + nums[i];
                if (sum > best[sum % 3]) best[sum % 3] = sum;
            }
        }
    }
    return best[0];
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1262;
    int64_t *lists[100];
    for (int l = 0; l < 100; l++) {
        lists[l] = malloc(40000 * sizeof(int64_t));
        for (int i = 0; i < 40000; i++) lists[l][i] = next_random(&seed) % 10000 + 1;
    }
    int64_t check = 0;
    for (int64_t round = 0; round < 30; round++)
        for (int l = 0; l < 100; l++) {
            int64_t best = max_sum_div_three(lists[l], 40000);
            check = (check * 131 + best + round) % 1000000007;
        }
    printf("30 rounds of 100 lists of 40000: checksum %lld\n", (long long)check);
    for (int l = 0; l < 100; l++) free(lists[l]);
    return 0;
}
