// LeetCode #2444: Count Subarrays With Fixed Bounds -- the bench, the ★
// arm: one pass keeping the last value outside the bounds, the last
// `min_k` and the last `max_k`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_subarrays(const int64_t *nums, int64_t n, int64_t min_k, int64_t max_k) {
    int64_t count = 0, bad = -1, last_min = -1, last_max = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (x < min_k || x > max_k) bad = i;
        if (x == min_k) last_min = i;
        if (x == max_k) last_max = i;
        int64_t start = last_min < last_max ? last_min : last_max;
        if (start > bad) count += start - bad;
    }
    return count;
}

static int64_t seed = 2444;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *arrays[10];
    for (int c = 0; c < 10; c++) {
        arrays[c] = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) arrays[c][i] = 1 + next_random() % 20;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++)
        for (int64_t c = 0; c < 10; c++) {
            int64_t at = (p * 7919 + c * 104729) % 100000;
            arrays[c][at] = 1 + next_random() % 20;
            check = (check * 31 + count_subarrays(arrays[c], 100000, 3, 17) + p) % 1000000007;
        }
    printf("100 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int c = 0; c < 10; c++) free(arrays[c]);
    return 0;
}
