// LeetCode #1589: Maximum Sum Obtained of Any Permutation -- the bench in
// C, mirroring max_sum.kara. Each request is its own malloc; the sorts are
// qsort's.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int cmp32(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x > y) - (x < y);
}

static int32_t max_sum_range_query(const int32_t *nums, int64_t n, int32_t **requests, int64_t m) {
    int64_t *asked = calloc(n + 1, sizeof(int64_t));
    for (int64_t k = 0; k < m; k++) {
        asked[requests[k][0]] += 1;
        asked[requests[k][1] + 1] -= 1;
    }
    for (int64_t i = 1; i < n; i++) asked[i] += asked[i - 1];
    qsort(asked, n, sizeof(int64_t), cmp64);
    int32_t *values = malloc(n * sizeof(int32_t));
    memcpy(values, nums, n * sizeof(int32_t));
    qsort(values, n, sizeof(int32_t), cmp32);
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total = (total + asked[i] * values[i]) % 1000000007;
    free(asked);
    free(values);
    return (int32_t)total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t a = next_random(seed);
    return a * 32768 + next_random(seed);
}

int main(void) {
    int64_t seed = 1589;
    const int64_t n = 100000, m = 100000;
    int32_t *nums[20];
    int32_t **requests[20];
    for (int p = 0; p < 20; p++) {
        nums[p] = malloc(n * sizeof(int32_t));
        for (int64_t i = 0; i < n; i++) nums[p][i] = (int32_t)(wide(&seed) % 100001);
        requests[p] = malloc(m * sizeof(int32_t *));
        for (int64_t k = 0; k < m; k++) {
            int64_t a = wide(&seed) % n;
            int64_t b = wide(&seed) % n;
            int32_t *r = malloc(2 * sizeof(int32_t));
            r[0] = (int32_t)(a < b ? a : b);
            r[1] = (int32_t)(a < b ? b : a);
            requests[p][k] = r;
        }
    }
    int64_t check = 0;
    for (int p = 0; p < 20; p++) {
        check = (check * 31 + max_sum_range_query(nums[p], n, requests[p], m) + 1) % 1000000007;
    }
    printf("20 problems of 100000 values and 100000 requests: checksum %lld\n", (long long)check);
    return 0;
}
