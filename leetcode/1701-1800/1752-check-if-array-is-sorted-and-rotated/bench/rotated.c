// LeetCode #1752: Check if Array Is Sorted and Rotated -- the bench
// (rotated.kara in C): count the drops.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { COUNT = 100000, ROUNDS = 5, N = 100 };

static bool check_rotated(const int32_t *nums, int64_t n) {
    int64_t drops = 0;
    for (int64_t i = 0; i + 1 < n; i++)
        if (nums[i] > nums[i + 1]) drops++;
    int64_t wrap = nums[n - 1] > nums[0] ? 1 : 0;
    return drops + wrap <= 1;
}

static int64_t seed = 1752;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int ascending(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    static int32_t arrays[COUNT][N];
    for (int c = 0; c < COUNT; c++) {
        for (int64_t i = 0; i < N; i++) arrays[c][i] = (int32_t)(next_random() % 100 + 1);
        if (next_random() % 2 == 0) {
            qsort(arrays[c], N, sizeof(int32_t), ascending);
            int64_t k = next_random() % N;
            int32_t turned[N];
            for (int64_t i = 0; i < N; i++) turned[i] = arrays[c][(i + k) % N];
            memcpy(arrays[c], turned, sizeof(turned));
        }
    }
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            bool answer = check_rotated(arrays[c], N);
            if (answer) yes++;
            check = (check * 31 + (answer ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%d arrays of %d values, %d rounds: %lld sorted and rotated, checksum %lld\n", COUNT, N, ROUNDS, (long long)yes, (long long)check);
    return 0;
}
