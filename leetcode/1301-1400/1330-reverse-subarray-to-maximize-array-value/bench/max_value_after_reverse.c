// LeetCode #1330 bench, C mirror of the Kāra bench: the ★ arm (the prefix,
// suffix and inside reversals' best gains in one pass) on 20 arrays of
// 3 * 10^4 values, the constraints' longest, within 30000 of 0, built once.
// Then 75 passes, each setting one value of every array from the checksum
// so far, answering it and folding the answer plus the pass into the
// checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t max32(int32_t a, int32_t b) { return a > b ? a : b; }
static int32_t min32(int32_t a, int32_t b) { return a < b ? a : b; }

static int32_t max_value_after_reverse(const int32_t *nums, int64_t n) {
    int32_t total = 0, gain = 0, high_low = INT32_MIN, low_high = INT32_MAX;
    for (int64_t i = 0; i < n - 1; i++) {
        int32_t a = nums[i], b = nums[i + 1];
        int32_t d = abs(a - b);
        total += d;
        gain = max32(gain, abs(nums[0] - b) - d);
        gain = max32(gain, abs(nums[n - 1] - a) - d);
        high_low = max32(high_low, min32(a, b));
        low_high = min32(low_high, max32(a, b));
    }
    if (n > 1) gain = max32(gain, 2 * (high_low - low_high));
    return total + gain;
}

static int64_t seed = 1330;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 30000;
    static int32_t arrays[20][30000];
    for (int t = 0; t < 20; t++)
        for (int64_t i = 0; i < n; i++) arrays[t][i] = (int32_t)(next_random() % 60001 - 30000);
    int64_t check = 0;
    for (int64_t pass = 0; pass < 75; pass++) {
        for (int t = 0; t < 20; t++) {
            arrays[t][check % n] = (int32_t)((check / 7) % 60001 - 30000);
            int32_t got = max_value_after_reverse(arrays[t], n);
            check = (check * 31 + got + pass) % 1000000007;
        }
    }
    printf("75 passes over 20 arrays of 3 * 10^4: checksum %lld\n", (long long)check);
    return 0;
}
