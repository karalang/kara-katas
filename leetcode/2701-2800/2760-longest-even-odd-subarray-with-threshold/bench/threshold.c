// LeetCode #2760: Longest Even Odd Subarray With Threshold -- the bench
// (threshold.kara in C): one pass with the length of the good run ending
// at each number.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t longest_alternating_subarray(const int64_t *nums, int n, int64_t threshold) {
    int64_t best = 0, run = 0;
    for (int i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (x > threshold) run = 0;
        else if (run > 0 && x % 2 != nums[i - 1] % 2) run++;
        else if (x % 2 == 0) run = 1;
        else run = 0;
        if (run > best) best = run;
    }
    return best;
}

static int64_t seed = 2760;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 100000, rounds = 10;
    int64_t *nums = malloc(sizeof(int64_t) * count * 100);
    int64_t *thresholds = malloc(sizeof(int64_t) * count);
    for (int k = 0; k < count; k++) {
        for (int i = 0; i < 100; i++) nums[(int64_t)k * 100 + i] = next_random() % 100 + 1;
        thresholds[k] = next_random() % 100 + 1;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < count; k++) {
            int64_t length = longest_alternating_subarray(nums + (int64_t)k * 100, 100, thresholds[k]);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    printf("%d arrays of 100, %d rounds: lengths sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(nums); free(thresholds);
    return 0;
}
