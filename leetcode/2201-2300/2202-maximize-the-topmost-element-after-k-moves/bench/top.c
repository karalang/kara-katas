// benchmark's C mirror of top.kara (LeetCode #2202, the ★ arm): the first
// k - 1 numbers and the one at index k.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t maximum_top(const int64_t *nums, int64_t n, int64_t k) {
    if (n == 1) return k % 2 == 1 ? -1 : nums[0];
    int64_t best = -1;
    int64_t reach = k - 1 < n ? k - 1 : n;
    for (int64_t i = 0; i < reach; i++)
        if (nums[i] > best) best = nums[i];
    if (k < n && nums[k] > best) best = nums[k];
    return best;
}

static int64_t seed = 2202;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

int main(void) {
    static int64_t piles[10][100000];
    int64_t ks[10][10];
    for (int p = 0; p < 10; p++) {
        for (int i = 0; i < 100000; i++) piles[p][i] = wide_random() % 1000000001;
        for (int j = 0; j < 10; j++) ks[p][j] = wide_random() % 100002;
    }
    int64_t check = 0;
    for (int pass = 0; pass < 50; pass++)
        for (int p = 0; p < 10; p++)
            for (int j = 0; j < 10; j++)
                check = (check * 31 + maximum_top(piles[p], 100000, ks[p][j]) + 1) % 1000000007;
    printf("50 passes over 10 piles: checksum %lld\n", (long long)check);
    return 0;
}
