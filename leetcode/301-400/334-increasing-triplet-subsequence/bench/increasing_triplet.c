// Benchmark workload for LeetCode #334 — C mirror of increasing_triplet.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define VALUES 1000000
#define PUNCHES 100
#define MODULUS 1073741789LL

static int increasing_triplet(const int64_t *nums, int64_t n) {
    int has_first = 0, has_second = 0;
    int64_t first = 0, second = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (has_second && x > second) return 1;
        if (has_first && x > first) {
            second = x;
            has_second = 1;
        } else {
            first = x;
            has_first = 1;
        }
    }
    return 0;
}

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = next(seed);
    return hi * 32768 + next(seed);
}

int main(void) {
    int64_t *nums = malloc(sizeof(int64_t) * VALUES);
    int64_t n = 0, top = 2LL * VALUES;
    for (int64_t k = 0; k < VALUES / 2; k++) {
        nums[n++] = top - 1;
        nums[n++] = top;
        top -= 2;
    }
    int64_t seed = 334, sink = 0;
    for (int64_t p = 0; p < PUNCHES; p++) {
        int64_t at = 2 + 2 * (wide(&seed) % (VALUES / 2 - 1));
        int64_t old = nums[at];
        if (p % 2 == 0) nums[at] = nums[at - 1] + 1;
        int64_t answer = increasing_triplet(nums, n);
        nums[at] = old;
        sink = (sink * 1000003 + answer * 2000003 + at) % MODULUS;
    }
    printf("%lld\n", (long long)sink);
    free(nums);
    return 0;
}
