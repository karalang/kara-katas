// LeetCode #2270: Number of Ways to Split Array -- the bench, the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t ways_to_split_array(const int64_t *nums, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    int64_t left = 0, ways = 0;
    for (int64_t i = 0; i < n - 1; i++) {
        left += nums[i];
        if (left >= total - left) ways++;
    }
    return ways;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2270;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 100; t++) {
        int64_t *nums = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) nums[i] = next_random() % 200001 - 100000;
        check = (check * 31 + ways_to_split_array(nums, 100000)) % 1000000007;
        free(nums);
    }
    printf("100 arrays of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
