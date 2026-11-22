// LeetCode #2762: Continuous Subarrays -- the bench (continuous.kara in
// C): a window with two deques of indices, each an array with a head and
// a tail, whose fronts are its least and greatest, shrunk from the left
// while those lie more than 2 apart.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2762;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t continuous_subarrays(const int64_t *nums, int64_t n, int64_t *lows, int64_t *highs) {
    int64_t lo_head = 0, lo_tail = 0, hi_head = 0, hi_tail = 0;
    int64_t left = 0, count = 0;
    for (int64_t right = 0; right < n; right++) {
        int64_t v = nums[right];
        while (lo_tail > lo_head && nums[lows[lo_tail - 1]] > v) lo_tail--;
        while (hi_tail > hi_head && nums[highs[hi_tail - 1]] < v) hi_tail--;
        lows[lo_tail++] = right;
        highs[hi_tail++] = right;
        while (nums[highs[hi_head]] - nums[lows[lo_head]] > 2) {
            left++;
            if (lows[lo_head] < left) lo_head++;
            if (highs[hi_head] < left) hi_head++;
        }
        count += right - left + 1;
    }
    return count;
}

int main(void) {
    const int count = 20, rounds = 10, n = 100000;
    int64_t *nums = malloc(sizeof(int64_t) * count * n);
    int64_t *lows = malloc(sizeof(int64_t) * n);
    int64_t *highs = malloc(sizeof(int64_t) * n);
    for (int k = 0; k < count; k++) {
        int64_t value = 500000000;
        for (int i = 0; i < n; i++) {
            value += next_random() % 5 - 2;
            nums[(int64_t)k * n + i] = value;
        }
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < count; k++) {
            int64_t found = continuous_subarrays(nums + (int64_t)k * n, n, lows, highs);
            sum += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    printf("%d walks of %d, %d rounds: subarrays sum to %lld, checksum %lld\n", count, n, rounds, (long long)sum, (long long)check);
    free(nums); free(lows); free(highs);
    return 0;
}
