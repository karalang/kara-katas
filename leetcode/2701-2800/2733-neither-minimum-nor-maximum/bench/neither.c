// LeetCode #2733: Neither Minimum nor Maximum -- the bench (neither.kara
// in C): the least and the greatest in one pass, then the first number
// that is neither.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_non_min_or_max(const int64_t *nums, int64_t n) {
    int64_t low = nums[0], high = nums[0];
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] < low) low = nums[i];
        if (nums[i] > high) high = nums[i];
    }
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] != low && nums[i] != high) return nums[i];
    }
    return -1;
}

static int64_t seed = 2733;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 2000, rounds = 3000;
    int64_t *arrays = malloc(sizeof(int64_t) * count * 100);
    int64_t *lens = malloc(sizeof(int64_t) * count);
    for (int k = 0; k < count; k++) {
        int64_t n = next_random() % 100 + 1;
        int64_t *all = arrays + (int64_t)k * 100;
        for (int i = 0; i < 100; i++) all[i] = i + 1;
        for (int64_t i = 99; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = all[i]; all[i] = all[j]; all[j] = t;
        }
        lens[k] = n;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t answer = find_non_min_or_max(arrays + (int64_t)k * 100, lens[k]);
            sum += answer;
            check = (check * 31 + answer + 1 + r) % 1000000007;
        }
    }
    printf("%d arrays, %d rounds: answers sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(arrays); free(lens);
    return 0;
}
