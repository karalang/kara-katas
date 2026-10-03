// Benchmark workload for LeetCode #330 — mirrors patching_array.kara.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define LEN 100000
#define PUNCHES 1500
#define MODULUS 1073741789LL

static int64_t seed = 330;

static int64_t next(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t min_patches(const int64_t *nums, int64_t len, int64_t n) {
    int64_t miss = 1, i = 0, patches = 0;
    while (miss <= n) {
        if (i < len && nums[i] <= miss) {
            miss += nums[i];
            i += 1;
        } else {
            miss += miss;
            patches += 1;
        }
    }
    return patches;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    int64_t *nums = malloc(sizeof(int64_t) * LEN);
    int64_t total = 0;
    for (int64_t k = 0; k < LEN; k++) {
        int64_t v = next() % 1001 + 50;
        nums[k] = v;
        total += v;
    }
    qsort(nums, LEN, sizeof(int64_t), cmp);
    int64_t sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        int64_t hi = next();
        int64_t lo = next();
        int64_t n = (hi * 32768 + lo) % (2 * total) + 1;
        int64_t answer = min_patches(nums, LEN, n);
        sink = (sink * 1000003 + answer * 64 + n % 64) % MODULUS;
    }
    printf("%lld\n", (long long)sink);
    free(nums);
    return 0;
}
