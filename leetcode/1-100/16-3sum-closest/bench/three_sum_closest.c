// Benchmark workload — 3Sum Closest (LeetCode #16).
// C mirror of bench/three_sum_closest.kara. Same M/N/K, LCG generator,
// per-case target bag, sort + two-pointer body, and sink — see that file's
// header for the rationale.
//
// Unlike kata 15's C mirror, there's no nested-Vec output to track; the
// function returns a single int64 and the per-iter allocation profile is
// just the working-buffer copy + qsort that any sort-based mirror needs.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static inline int64_t abs_i64(int64_t x) {
    return x < 0 ? -x : x;
}

static int64_t three_sum_closest(const int64_t *nums, int64_t n, int64_t target) {
    int64_t *s = (int64_t *)malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t t = 0; t < n; t++) s[t] = nums[t];
    qsort(s, (size_t)n, sizeof(int64_t), cmp_i64);

    int64_t best = s[0] + s[1] + s[2];
    int64_t i = 0;
    while (i < n - 2) {
        int64_t lo = i + 1, hi = n - 1;
        while (lo < hi) {
            int64_t sum = s[i] + s[lo] + s[hi];
            if (sum == target) {
                free(s);
                return sum;
            }
            if (abs_i64(sum - target) < abs_i64(best - target)) {
                best = sum;
            }
            if (sum < target) {
                lo++;
            } else {
                hi--;
            }
        }
        i++;
    }
    free(s);
    return best;
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
static int64_t lcg_next(int64_t state) {
    return (1103515245LL * state + 12345LL) % 2147483648LL;
}

static int64_t *build_case(int64_t seed, int64_t count) {
    int64_t *v = (int64_t *)malloc(sizeof(int64_t) * (size_t)count);
    int64_t state = seed;
    for (int64_t j = 0; j < count; j++) {
        state = lcg_next(state);
        v[j] = (state % 21) - 10;
    }
    return v;
}

static int64_t target_for(int64_t idx) {
    static const int64_t bag[8] = { -12, -6, -1, 0, 1, 5, 11, 19 };
    return bag[idx];
}

int main(void) {
    const int64_t m_cases = 8;
    const int64_t n_values = 16;
    const int64_t k_iters = 1000000;

    int64_t **sets = (int64_t **)malloc(sizeof(int64_t *) * (size_t)m_cases);
    for (int64_t m = 0; m < m_cases; m++) {
        sets[m] = build_case(m * 1000003 + 12345, n_values);
    }

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % m_cases;
        sum += three_sum_closest(sets[idx], n_values, target_for(idx));
    }
    printf("%lld\n", (long long)sum);

    for (int64_t m = 0; m < m_cases; m++) free(sets[m]);
    free(sets);
    return 0;
}
