/*
 * Benchmark workload — Subsets II (LeetCode #90).
 * C mirror of bench/subsets_ii.kara. Enumerate-and-fold over the emit-at-node dedup
 * backtracking of a sorted multiset (8 distinct values x2 => 3^8 unique subsets). The
 * path is a stack buffer indexed by depth (equivalent to Kara's reused Vec push/pop),
 * folded into a threaded accumulator, K=2700 iterations seeded by the index.
 * See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t enumerate(const int64_t *nums, int64_t n, int64_t start,
                         int64_t *path, int64_t depth, int64_t acc) {
    int64_t a = (acc * 131 + (depth + 1)) % 1000000007;
    for (int64_t p = 0; p < depth; p++)
        a = (a * 131 + (path[p] + 1)) % 1000000007;
    for (int64_t i = start; i < n; i++) {
        if (i == start || nums[i] != nums[i - 1]) {
            path[depth] = nums[i];
            a = enumerate(nums, n, i + 1, path, depth + 1, a);
        }
    }
    return a;
}

int main(void) {
    const int64_t d = 8, r = 2, total = 2700, modulus = 1000000007;
    int64_t nums[64];
    int64_t n = 0;
    for (int64_t v = 0; v < d; v++)
        for (int64_t c = 0; c < r; c++)
            nums[n++] = v;
    int64_t path[64];
    int64_t sum = 0;
    for (int64_t iter = 0; iter < total; iter++) {
        int64_t rr = enumerate(nums, n, 0, path, 0, iter);
        sum = (sum * 131 + rr) % modulus;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
