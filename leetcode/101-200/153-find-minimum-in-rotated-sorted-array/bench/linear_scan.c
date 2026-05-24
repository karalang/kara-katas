/*
 * LeetCode 153 — linear-scan find-min on a rotated sorted array, bench mirror in C.
 *
 * Algorithmic mirror of bench/linear_scan.{kara,rs,py}. N=2_000_000,
 * pivot R=666_666, K=10 outer iterations. Stdout sink: 10.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define N 2000000
#define R 666666
#define K 10

static const int64_t *black_box_slice(const int64_t *p) {
#if defined(__GNUC__) || defined(__clang__)
    __asm__ volatile("" : "+r"(p) :: "memory");
#endif
    return p;
}

static int64_t find_min(const int64_t *nums, size_t len) {
    int64_t m = nums[0];
    for (size_t i = 1; i < len; i++) {
        if (nums[i] < m) {
            m = nums[i];
        }
    }
    return m;
}

int main(void) {
    int64_t *data = (int64_t *)malloc((size_t)N * sizeof(int64_t));
    if (!data) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }
    for (size_t i = 0; i < (size_t)N; i++) {
        data[i] = (int64_t)(((i + R) % N) + 1);
    }

    int64_t sum = 0;
    for (int k = 0; k < K; k++) {
        sum += find_min(black_box_slice(data), (size_t)N);
    }
    printf("%lld\n", (long long)sum);
    free(data);
    return 0;
}
