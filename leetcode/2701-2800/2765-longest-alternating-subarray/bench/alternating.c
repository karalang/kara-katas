// LeetCode #2765: Longest Alternating Subarray -- the bench
// (alternating.kara in C): one pass with the length of the alternating
// run ending at each number.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2765;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t alternating_subarray(const int64_t *nums, int64_t n) {
    int64_t best = -1, run = 1;
    for (int64_t i = 1; i < n; i++) {
        if (run >= 2 && nums[i] == nums[i - 2]) run++;
        else if (nums[i] - nums[i - 1] == 1) run = 2;
        else run = 1;
        if (run >= 2 && run > best) best = run;
    }
    return best;
}

int main(void) {
    const int count = 100000, rounds = 10;
    int64_t *nums = malloc(sizeof(int64_t) * count * 100);
    for (int k = 0; k < count; k++) {
        int64_t top = next_random() % 4 + 2;
        for (int i = 0; i < 100; i++) nums[(int64_t)k * 100 + i] = next_random() % top + 1;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < count; k++) {
            int64_t length = alternating_subarray(nums + (int64_t)k * 100, 100);
            sum += length;
            check = (check * 31 + length + 1 + r) % 1000000007;
        }
    printf("%d arrays of 100, %d rounds: lengths sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(nums);
    return 0;
}
