/*
 * LeetCode 1 — brute-force O(n²) Two Sum, bench mirror in C.
 *
 * Algorithmic mirror of bench/brute_force.kara and bench/brute_force.rs.
 * Same N=5000, K=10, sentinel target=-1 (no pair sums to -1, so every
 * call walks the full N*(N-1)/2 = 12,497,500 comparisons and returns
 * -1, -1). Stdout sink: K * (-1 + -1) = -20.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>

#define N 5000

/* Returns true with (*oi, *oj) populated if a pair is found; false otherwise. */
static int two_sum(const int64_t *nums, int64_t target, size_t *oi, size_t *oj) {
    for (size_t i = 0; i < N; i++) {
        for (size_t j = i + 1; j < N; j++) {
            if (nums[i] + nums[j] == target) {
                *oi = i;
                *oj = j;
                return 1;
            }
        }
    }
    return 0;
}

int main(void) {
    int64_t data[N];
    for (size_t i = 0; i < N; i++) {
        data[i] = ((int64_t)i * 7) % 1000;
    }

    const int64_t target = -1;
    int64_t sum = 0;
    for (int k = 0; k < 10; k++) {
        size_t i, j;
        if (two_sum(data, target, &i, &j)) {
            sum += (int64_t)i + (int64_t)j;
        } else {
            sum += -2;
        }
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
