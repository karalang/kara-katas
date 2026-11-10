// LeetCode #2098: Subsequence of Size K With the Largest Even Sum -- C
// mirror of the ★ arm's benchmark (even_sum.kara): the same 200 lists of
// 100000 numbers, each sorted largest first with `qsort` and given the
// better swap.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int larger_first(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x < y) - (x > y);
}

static int64_t largest_even_sum(const int64_t *nums, int64_t n, int64_t k, int64_t *sorted) {
    memcpy(sorted, nums, (size_t)n * sizeof(int64_t));
    qsort(sorted, (size_t)n, sizeof(int64_t), larger_first);
    int64_t sum = 0;
    for (int64_t i = 0; i < k; i++) sum += sorted[i];
    if (sum % 2 == 0) return sum;
    int64_t taken_odd = -1, taken_even = -1, left_odd = -1, left_even = -1;
    for (int64_t i = 0; i < k; i++) {
        int64_t x = sorted[i];
        if (x % 2 == 1 && (taken_odd < 0 || x < taken_odd)) taken_odd = x;
        if (x % 2 == 0 && (taken_even < 0 || x < taken_even)) taken_even = x;
    }
    for (int64_t i = k; i < n; i++) {
        int64_t x = sorted[i];
        if (x % 2 == 1 && x > left_odd) left_odd = x;
        if (x % 2 == 0 && x > left_even) left_even = x;
    }
    int64_t best = -1;
    if (taken_odd >= 0 && left_even >= 0 && sum - taken_odd + left_even > best) best = sum - taken_odd + left_even;
    if (taken_even >= 0 && left_odd >= 0 && sum - taken_even + left_odd > best) best = sum - taken_even + left_odd;
    return best;
}

static int64_t seed = 2098;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

int main(void) {
    const int64_t n = 100000;
    int64_t *nums = malloc((size_t)n * sizeof(int64_t));
    int64_t *sorted = malloc((size_t)n * sizeof(int64_t));
    int64_t total = 0, check = 0;
    for (int r = 0; r < 200; r++) {
        for (int64_t i = 0; i < n; i++) nums[i] = wide_random() % 100001;
        int64_t k = wide_random() % 100000 + 1;
        int64_t got = largest_even_sum(nums, n, k, sorted);
        total += got;
        check = (check * 31 + got + 1) % 1000000007;
    }
    printf("200 answers: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(nums);
    free(sorted);
    return 0;
}
