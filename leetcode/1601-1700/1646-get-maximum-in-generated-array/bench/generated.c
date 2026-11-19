// LeetCode #1646: Get Maximum in Generated Array -- the bench's C mirror:
// the ★ arm on 4000000 random n from 0 to 100, all drawn first. The array
// is allocated per call, as the other languages do.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CASES 4000000

static int32_t get_maximum_generated(int32_t n) {
    if (n == 0) return 0;
    int32_t *nums = calloc((size_t)n + 1, sizeof *nums);
    nums[1] = 1;
    int32_t best = 1;
    for (int32_t i = 2; i <= n; i++) {
        nums[i] = i % 2 == 0 ? nums[i / 2] : nums[i / 2] + nums[i / 2 + 1];
        if (nums[i] > best) best = nums[i];
    }
    free(nums);
    return best;
}

static int64_t seed = 1646;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t ns[CASES];
    for (int c = 0; c < CASES; c++) ns[c] = (int32_t)(next_random() % 101);
    int64_t check = 0, total = 0;
    for (int c = 0; c < CASES; c++) {
        int64_t found = get_maximum_generated(ns[c]);
        total += found;
        check = (check * 31 + found + 1) % 1000000007;
    }
    printf("%d random n up to 100: maxima sum to %lld, checksum %lld\n", CASES, (long long)total, (long long)check);
    return 0;
}
