// LeetCode 795 — Number of Subarrays with Bounded Maximum: the bench, in
// C. Mirrors num_subarray_bounded_max.kara: one pass, keeping the last
// place of a number above right and of one in range.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_subarray_bounded_max(const int64_t *nums, int64_t n, int64_t left, int64_t right) {
    int64_t too_big = -1, in_range = -1, count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] > right)
            too_big = i;
        else if (nums[i] >= left)
            in_range = i;
        if (in_range > too_big) count += in_range - too_big;
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t big_random(int64_t *seed) {
    int64_t a = next_random(seed);
    int64_t b = next_random(seed);
    return (a * 32768 + b) % 1000000001;
}

int main(void) {
    int64_t seed = 795;
    int64_t *arrays[16];
    for (int k = 0; k < 16; k++) {
        arrays[k] = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) arrays[k][i] = big_random(&seed);
    }
    int64_t rounds = 8000, total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t a = big_random(&seed);
        int64_t b = big_random(&seed);
        int64_t count = num_subarray_bounded_max(arrays[r % 16], 100000, a < b ? a : b, a < b ? b : a);
        total += count;
        check = (check * 131 + count % 1000000007) % 1000000007;
    }
    printf("%lld rounds of 100000 numbers: %lld subarrays, checksum %lld\n", (long long)rounds, (long long)total,
           (long long)check);
    return 0;
}
