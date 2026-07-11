/*
 * Benchmark workload — Combinations (LeetCode #77).
 * C mirror of bench/combinations.kara. Start-indexed pruned backtracking that
 * ENUMERATES all C(16,8)=12870 combinations and folds each leaf's values into a
 * threaded accumulator (no storage), K=1500 iterations seeded by the iteration
 * index. The path is a small stack buffer indexed by depth (equivalent to Kara's
 * reused Vec push/pop). The DFS recursion is the measured work. See ../README.md.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t enumerate(int64_t n, int64_t k, int64_t start,
                         int64_t *path, int64_t depth, int64_t acc) {
    if (depth == k) {
        int64_t a = acc;
        for (int64_t j = 0; j < k; j++)
            a = (a * 131 + path[j]) % 1000000007;
        return a;
    }
    int64_t need = k - depth;
    int64_t limit = n - need + 1;
    int64_t a = acc;
    for (int64_t i = start; i <= limit; i++) {
        path[depth] = i;
        a = enumerate(n, k, i + 1, path, depth + 1, a);
    }
    return a;
}

int main(void) {
    const int64_t n = 16, k = 8, total = 1500, modulus = 1000000007;
    int64_t path[64];
    int64_t sum = 0;
    for (int64_t iter = 0; iter < total; iter++) {
        int64_t r = enumerate(n, k, 1, path, 0, iter);
        sum = (sum + r) % modulus;
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
