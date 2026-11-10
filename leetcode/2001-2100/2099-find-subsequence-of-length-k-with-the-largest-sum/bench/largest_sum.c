// LeetCode #2099: Find Subsequence of Length K With the Largest Sum -- C
// mirror of the ★ arm's benchmark (largest_sum.kara): the same 20000 lists
// of 1000 numbers, the positions sorted by value with `qsort` (the
// position breaking ties, so the order is the ★ arm's) and the chosen put
// back in order.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t *values;

static int by_value(const void *pa, const void *pb) {
    int64_t a = *(const int64_t *)pa, b = *(const int64_t *)pb;
    if (values[a] != values[b]) return values[a] > values[b] ? -1 : 1;
    return (a > b) - (a < b);
}

static int by_position(const void *pa, const void *pb) {
    int64_t a = *(const int64_t *)pa, b = *(const int64_t *)pb;
    return (a > b) - (a < b);
}

static void max_subsequence(const int64_t *nums, int64_t n, int64_t k, int64_t *order, int64_t *out) {
    for (int64_t i = 0; i < n; i++) order[i] = i;
    values = nums;
    qsort(order, (size_t)n, sizeof(int64_t), by_value);
    qsort(order, (size_t)k, sizeof(int64_t), by_position);
    for (int64_t j = 0; j < k; j++) out[j] = nums[order[j]];
}

static int64_t seed = 2099;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

int main(void) {
    int64_t nums[1000], order[1000], out[1000];
    int64_t total = 0, check = 0;
    for (int r = 0; r < 20000; r++) {
        for (int i = 0; i < 1000; i++) nums[i] = wide_random() % 200001 - 100000;
        int64_t k = next_random() % 1000 + 1;
        max_subsequence(nums, 1000, k, order, out);
        total += k;
        for (int64_t j = 0; j < k; j++) check = (check * 31 + out[j] + 100000) % 1000000007;
    }
    printf("20000 answers: %lld numbers, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
