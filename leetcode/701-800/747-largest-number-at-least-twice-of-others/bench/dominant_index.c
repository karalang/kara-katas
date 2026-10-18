// LeetCode 747 — Largest Number At Least Twice of Others, bench: the ★
// arm (one pass) on millions of 50-value lists cut from a random pool.
// Mirrors dominant_index.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t dominant_index(const int64_t *nums, int64_t n) {
    int64_t best = 0, second = -1;
    for (int64_t i = 1; i < n; i++) {
        if (nums[i] > nums[best]) {
            second = nums[best];
            best = i;
        } else if (nums[i] > second) {
            second = nums[i];
        }
    }
    return nums[best] >= 2 * second ? best : -1;
}

static int64_t seed = 747;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t queries = 2000000, pool_len = 100000, n = 50;
    int64_t *pool = malloc(pool_len * sizeof(int64_t));
    for (int64_t i = 0; i < pool_len; i++) pool[i] = next_random() % 52;
    int64_t *nums = malloc(n * sizeof(int64_t));
    int64_t found = 0, total = 0;
    for (int64_t q = 0; q < queries; q++) {
        int64_t start = next_random() % (pool_len - n);
        for (int64_t j = 0; j < n; j++) nums[j] = pool[start + j];
        nums[q % n] = 100;
        int64_t got = dominant_index(nums, n);
        if (got != -1) { found++; total += got; }
    }
    printf("%lld lists of 50 values: %lld have a dominant value, indices sum to %lld\n",
           (long long)queries, (long long)found, (long long)total);
    free(pool);
    free(nums);
    return 0;
}
