// LeetCode #1755: Closest Subsequence Sum -- the bench (closest.kara in C):
// meet in the middle with binary search.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { COUNT = 8, N = 40 };

static int32_t *subset_sums(const int32_t *values, int64_t n) {
    int64_t count = (int64_t)1 << n;
    int32_t *sums = calloc(count, sizeof(int32_t));
    for (int64_t mask = 1; mask < count; mask++)
        sums[mask] = sums[mask & (mask - 1)] + values[__builtin_ctzll(mask)];
    return sums;
}

static int ascending(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static int32_t min_abs_difference(const int32_t *nums, int64_t n, int32_t goal) {
    int64_t half = n / 2;
    int32_t *left = subset_sums(nums, half);
    int32_t *right = subset_sums(nums + half, n - half);
    int64_t left_count = (int64_t)1 << half, right_count = (int64_t)1 << (n - half);
    qsort(right, right_count, sizeof(int32_t), ascending);
    int32_t best = INT32_MAX;
    for (int64_t k = 0; k < left_count; k++) {
        int32_t rest = goal - left[k];
        int64_t lo = 0, hi = right_count;
        while (lo < hi) {
            int64_t mid = (lo + hi) / 2;
            if (right[mid] < rest) lo = mid + 1;
            else hi = mid;
        }
        if (lo < right_count && right[lo] - rest < best) best = right[lo] - rest;
        if (lo > 0 && rest - right[lo - 1] < best) best = rest - right[lo - 1];
    }
    free(left);
    free(right);
    return best;
}

static int64_t seed = 1755;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    static int32_t nums[COUNT][N];
    int32_t goals[COUNT];
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) nums[c][i] = (int32_t)(wide() % 20000001 - 10000000);
        goals[c] = (int32_t)(wide() % 200000001 - 100000000);
    }
    int64_t sum = 0, check = 0;
    for (int c = 0; c < COUNT; c++) {
        int64_t answer = min_abs_difference(nums[c], N, goals[c]);
        sum += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    printf("%d problems of %d values: differences add to %lld, checksum %lld\n", COUNT, N, (long long)sum, (long long)check);
    return 0;
}
