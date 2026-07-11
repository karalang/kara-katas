/*
 * Benchmark workload — Subsets (LeetCode #78).
 * C mirror of bench/subsets.kara. Emit-at-every-node backtracking that ENUMERATES
 * the power set of [1..16] (2^16 subsets) and folds each node's path into a threaded
 * accumulator (no storage), K=300 iterations seeded by the iteration index. The path
 * is a small stack buffer indexed by depth (equivalent to Kara's reused Vec
 * push/pop). The DFS recursion is the measured work. See ../README.md.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t enumerate(const int64_t *nums, int64_t n, int64_t start,
                        int64_t *path, int64_t depth, int64_t acc) {
    int64_t a = acc;
    a = (a * 131 + (depth + 1)) % 1000000007;
    for (int64_t p = 0; p < depth; p++)
        a = (a * 131 + path[p]) % 1000000007;
    for (int64_t i = start; i < n; i++) {
        path[depth] = nums[i];
        a = enumerate(nums, n, i + 1, path, depth + 1, a);
    }
    return a;
}

int main(void) {
    const int64_t n = 16, total = 300, modulus = 1000000007;
    int64_t nums[16];
    for (int64_t i = 0; i < n; i++) nums[i] = i + 1;
    int64_t path[64];
    int64_t sum = 0;
    for (int64_t iter = 0; iter < total; iter++) {
        int64_t r = enumerate(nums, n, 0, path, 0, iter);
        sum = (sum + r) % modulus;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
