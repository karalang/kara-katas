// LeetCode #1685: Sum of Absolute Differences in a Sorted Array -- the
// bench's C mirror: the ★ arm on 50 random sorted arrays of 100000 values,
// all drawn first, each answered 20 times. Each answer is malloc'd, as the
// other languages build a new vector.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 50
#define SIZE 100000
#define ROUNDS 20

static int32_t *sum_differences(const int32_t *nums, int64_t n) {
    int32_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    int32_t before = 0;
    int32_t *result = malloc((size_t)n * sizeof *result);
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        int64_t after = total - before - x;
        result[i] = (int32_t)(x * i - before + after - x * (n - 1 - i));
        before += (int32_t)x;
    }
    return result;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1685;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int compare(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

int main(void) {
    static int32_t arrays[COUNT][SIZE];
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < SIZE; i++) arrays[c][i] = (int32_t)(next_random() % 10000 + 1);
        qsort(arrays[c], SIZE, sizeof(int32_t), compare);
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int32_t *answer = sum_differences(arrays[c], SIZE);
            int64_t first = answer[0], middle = answer[SIZE / 2], last = answer[SIZE - 1];
            total += middle;
            check = (check * 31 + first + middle + last + r) % 1000000007;
            free(answer);
        }
    }
    printf("%d arrays of %d values, %d rounds: middles sum to %lld, checksum %lld\n", COUNT, SIZE, ROUNDS, (long long)total, (long long)check);
    return 0;
}
