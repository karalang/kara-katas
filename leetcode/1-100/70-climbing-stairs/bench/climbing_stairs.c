/*
 * Benchmark workload — Climbing Stairs (LeetCode #70).
 * C mirror of bench/climbing_stairs.kara. The ★'s two-counter Fibonacci
 * recurrence run K=30_000_000 times over a sweep of n = 1 + k%45, folding each
 * result into a rolling polynomial hash. No allocation — a pure integer-add /
 * branch benchmark of the recurrence loop. See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t climb(int64_t n) {
    if (n <= 2) return n;
    int64_t a = 1, b = 2;
    for (int64_t i = 3; i <= n; i++) {
        int64_t next = a + b;
        a = b;
        b = next;
    }
    return b;
}

int main(void) {
    const int64_t total = 30000000;
    const int64_t modulus = 1000000007;
    const int64_t span = 45;

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t n = 1 + (k % span);
        acc = (acc * 131 + climb(n)) % modulus;
    }
    printf("%lld\n", (long long)acc);
    return 0;
}
