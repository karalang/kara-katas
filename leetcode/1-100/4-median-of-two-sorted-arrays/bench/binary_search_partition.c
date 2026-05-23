/*
 * LeetCode 4 — binary-search-partition O(log min(m, n)) Median of Two
 * Sorted Arrays, bench mirror in C.
 *
 * Algorithmic mirror of bench/binary_search_partition.{kara,rs,py}. Same
 * M = N = 1_000_000, R = 1_000, K = 10_000_000 rotated-input workload.
 * Per-iter `off = k % R`; per-iter contribution to the sink is
 * 4*off + (2M - 1); aggregate sink = 20_019_970_000_000.
 *
 * No allocator surface in the inner loop — same shape Kara/Rust hit: two
 * `int64_t*` buffers (M + R elements each) built once, then 10M
 * `middle_pair_off(base_a, off, M, base_b, off, N)` calls. Each call does
 * ~log2(M) ≈ 20 partition cross-checks; the rotation `off = k % R`
 * defeats the cross-iteration CSE that would hoist the call out of the
 * loop.
 *
 * See ../README.md § Benchmarks for what the numbers mean.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct { int64_t lower, upper; } Pair;

static inline int64_t i64_min(int64_t a, int64_t b) { return a < b ? a : b; }
static inline int64_t i64_max(int64_t a, int64_t b) { return a > b ? a : b; }

static Pair middle_pair_off(const int64_t *a, int64_t a_off, int64_t a_len,
                            const int64_t *b, int64_t b_off, int64_t b_len) {
    if (a_len > b_len) {
        return middle_pair_off(b, b_off, b_len, a, a_off, a_len);
    }
    int64_t half = (a_len + b_len + 1) / 2;
    int64_t lo = 0, hi = a_len;
    while (lo <= hi) {
        int64_t i = (lo + hi) / 2;
        int64_t j = half - i;
        int64_t left_a  = (i > 0)     ? a[a_off + i - 1] : INT64_MIN;
        int64_t right_a = (i < a_len) ? a[a_off + i]     : INT64_MAX;
        int64_t left_b  = (j > 0)     ? b[b_off + j - 1] : INT64_MIN;
        int64_t right_b = (j < b_len) ? b[b_off + j]     : INT64_MAX;
        if (left_a > right_b) {
            hi = i - 1;
        } else if (left_b > right_a) {
            lo = i + 1;
        } else {
            int64_t lower = i64_max(left_a, left_b);
            if ((a_len + b_len) % 2 == 1) {
                return (Pair){lower, lower};
            }
            int64_t upper = i64_min(right_a, right_b);
            return (Pair){lower, upper};
        }
    }
    __builtin_unreachable();
}

int main(void) {
    const int64_t M = 1000000;
    const int64_t N = 1000000;
    const int64_t R = 1000;
    const int64_t K = 10000000;

    int64_t *base_a = (int64_t *)malloc(sizeof(int64_t) * (size_t)(M + R));
    int64_t *base_b = (int64_t *)malloc(sizeof(int64_t) * (size_t)(N + R));
    for (int64_t p = 0; p < M + R; p++) base_a[p] = 2 * p;
    for (int64_t p = 0; p < N + R; p++) base_b[p] = 2 * p + 1;

    int64_t sum = 0;
    for (int64_t k = 0; k < K; k++) {
        int64_t off = k % R;
        Pair p = middle_pair_off(base_a, off, M, base_b, off, N);
        sum += p.lower + p.upper;
    }
    printf("%lld\n", (long long)sum);

    free(base_a);
    free(base_b);
    return 0;
}
