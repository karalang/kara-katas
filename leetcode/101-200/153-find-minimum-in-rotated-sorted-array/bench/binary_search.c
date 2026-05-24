/*
 * LeetCode 153 — binary-search find-min on a rotated sorted array, bench mirror in C.
 *
 * Algorithmic mirror of bench/binary_search.{kara,rs,py}. N=2_000_000,
 * pivot R=666_666, K=2_000_000 outer iterations. Stdout sink: 2000000.
 *
 * black_box_slice keeps LLVM from hoisting the pure find_min call out of the
 * K loop (mirrors Rust's std::hint::black_box).
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define N 2000000
#define R 666666
#define K 2000000

static const int64_t *black_box_slice(const int64_t *p) {
#if defined(__GNUC__) || defined(__clang__)
    __asm__ volatile("" : "+r"(p) :: "memory");
#endif
    return p;
}

static int64_t find_min(const int64_t *nums, size_t len) {
    size_t lo = 0;
    size_t hi = len - 1;
    while (lo < hi) {
        size_t mid = lo + (hi - lo) / 2;
        if (nums[mid] > nums[hi]) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return nums[lo];
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
