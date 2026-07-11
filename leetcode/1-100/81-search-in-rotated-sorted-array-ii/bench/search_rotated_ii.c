/*
 * Benchmark workload — Search in Rotated Sorted Array II (LeetCode #81).
 * C mirror of bench/search_rotated_ii.kara. Build-once + punch: one rotated sorted
 * array with duplicates (each value 0..M appears twice, M=1000, rotated) built once,
 * then searched K=17,000,000 times for targets sweeping present/absent values, each
 * boolean folded through a rolling polynomial hash. The duplicate-aware rotated
 * binary search's branch loop is the measured work. See ../README.md.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int search(const int64_t *nums, int64_t len, int64_t target) {
    int64_t lo = 0, hi = len - 1;
    while (lo <= hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (nums[mid] == target) return 1;
        if (nums[lo] == nums[mid] && nums[mid] == nums[hi]) {
            lo++;
            hi--;
        } else if (nums[lo] <= nums[mid]) {
            if (nums[lo] <= target && target < nums[mid]) hi = mid - 1;
            else lo = mid + 1;
        } else {
            if (nums[mid] < target && target <= nums[hi]) lo = mid + 1;
            else hi = mid - 1;
        }
    }
    return 0;
}

/* 1D heap array (malloc'd int64_t*) — the same layout kara's Vec[i64] uses. */
static int64_t *build(int64_t m, int64_t dup, int64_t rot, int64_t *out_n) {
    int64_t n = m * dup;
    int64_t *base = malloc(n * sizeof(int64_t));
    int64_t pos = 0;
    for (int64_t v = 0; v < m; v++)
        for (int64_t d = 0; d < dup; d++)
            base[pos++] = v;
    int64_t *arr = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++)
        arr[i] = base[(i + rot) % n];
    free(base);
    *out_n = n;
    return arr;
}

int main(void) {
    const int64_t m = 1000, dup = 2, total = 17000000, modulus = 1000000007;
    int64_t n;
    int64_t *arr = build(m, dup, (m * dup) / 3, &n);
    int64_t span = m + 50;
    int64_t sum = 0;
    for (int64_t iter = 0; iter < total; iter++) {
        int64_t target = iter % span;
        int found = search(arr, n, target);
        int64_t bit = found ? 1 : 0;
        sum = (sum * 131 + bit + 1) % modulus;
    }
    printf("%lld\n", (long long)sum);
    free(arr);
    return 0;
}
