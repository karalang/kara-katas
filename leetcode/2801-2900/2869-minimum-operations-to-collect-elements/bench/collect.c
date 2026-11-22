// LeetCode #2869: Minimum Operations to Collect Elements -- the bench,
// as collect.kara: 50000 arrays of 50 values, each answered 20 times by
// the bit-mask arm.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_operations(const int64_t *nums, int64_t n, int64_t k) {
    int64_t full = ((int64_t)1 << k) - 1, mask = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        if (nums[i] <= k) mask |= (int64_t)1 << (nums[i] - 1);
        if (mask == full) return n - i;
    }
    return n;
}

static int64_t seed = 2869;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static bool contains(const int64_t *nums, int64_t n, int64_t v) {
    for (int64_t i = 0; i < n; i++)
        if (nums[i] == v) return true;
    return false;
}

int main(void) {
    const int64_t count = 50000, rounds = 20, n = 50;
    int64_t *all = malloc(count * n * sizeof *all), *ks = malloc(count * sizeof *ks);
    for (int64_t c = 0; c < count; c++) {
        int64_t *nums = all + c * n;
        for (int64_t i = 0; i < n; i++) nums[i] = next_random() % n + 1;
        nums[next_random() % n] = 1;
        int64_t reach = 1;
        while (contains(nums, n, reach + 1)) reach++;
        ks[c] = next_random() % reach + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t ops = min_operations(all + c * n, n, ks[c]);
            total += ops;
            check = (check * 31 + ops + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: %lld operations, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(all);
    free(ks);
    return 0;
}
