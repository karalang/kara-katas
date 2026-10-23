// LeetCode #870: Advantage Shuffle -- C mirror of the bench program (the
// ★ arm, greedy from the largest). qsort is not stable, so the indices
// are ordered by value descending and then by index, the order a stable
// sort gives.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t *key_nums2;

static int cmp_i64(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int cmp_order(const void *x, const void *y) {
    int64_t i = *(const int64_t *)x, j = *(const int64_t *)y;
    int64_t a = key_nums2[i], b = key_nums2[j];
    if (a != b) return (a < b) - (a > b);
    return (i > j) - (i < j);
}

static void advantage_count(const int64_t *nums1, const int64_t *nums2, int64_t n, int64_t *result) {
    int64_t *sorted = malloc(n * sizeof(int64_t));
    int64_t *order = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        sorted[i] = nums1[i];
        order[i] = i;
    }
    qsort(sorted, n, sizeof(int64_t), cmp_i64);
    key_nums2 = nums2;
    qsort(order, n, sizeof(int64_t), cmp_order);
    int64_t lo = 0, hi = n - 1;
    for (int64_t k = 0; k < n; k++) {
        int64_t i = order[k];
        if (sorted[hi] > nums2[i]) {
            result[i] = sorted[hi--];
        } else {
            result[i] = sorted[lo++];
        }
    }
    free(sorted);
    free(order);
}

static int64_t seed = 870;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void random_vec(int64_t *v, int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        int64_t hi = next_random();
        int64_t lo = next_random();
        v[i] = (hi * 32768 + lo) % 1000000001;
    }
}

int main(void) {
    const int64_t n = 100000;
    int64_t *nums1 = malloc(n * sizeof(int64_t));
    int64_t *nums2 = malloc(n * sizeof(int64_t));
    int64_t *result = malloc(n * sizeof(int64_t));
    int64_t wins = 0, check = 0;
    for (int r = 0; r < 20; r++) {
        random_vec(nums1, n);
        random_vec(nums2, n);
        advantage_count(nums1, nums2, n, result);
        for (int64_t i = 0; i < n; i++) {
            if (result[i] > nums2[i]) wins++;
            check = (check + result[i] * (i + 1)) % 1000000007;
        }
    }
    printf("20 pairs of 100000 values: %lld wins, checksum %lld\n", (long long)wins, (long long)check);
    free(nums1);
    free(nums2);
    free(result);
    return 0;
}
