// Benchmark workload — Merge Intervals (LeetCode #56).
// C mirror of bench/merge_intervals.kara. Same M/N/K, LCG generator,
// per-case (start, end) shape, sort-by-first-component + sweep, and sink
// — see that file's header for the rationale.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    int64_t start;
    int64_t end;
} Interval;

static int cmp_interval(const void *a, const void *b) {
    int64_t xa = ((const Interval *)a)->start;
    int64_t xb = ((const Interval *)b)->start;
    return (xa > xb) - (xa < xb);
}

static int64_t merge_intervals(const Interval *intervals, int64_t n) {
    Interval *s = (Interval *)malloc(sizeof(Interval) * (size_t)n);
    for (int64_t t = 0; t < n; t++) s[t] = intervals[t];
    qsort(s, (size_t)n, sizeof(Interval), cmp_interval);

    Interval *result = (Interval *)malloc(sizeof(Interval) * (size_t)n);
    int64_t count = 0;

    if (n == 0) {
        free(result);
        free(s);
        return 0;
    }

    int64_t cur_start = s[0].start, cur_end = s[0].end;
    for (int64_t i = 1; i < n; i++) {
        if (s[i].start <= cur_end) {
            if (s[i].end > cur_end) cur_end = s[i].end;
        } else {
            result[count].start = cur_start;
            result[count].end = cur_end;
            count++;
            cur_start = s[i].start;
            cur_end = s[i].end;
        }
    }
    result[count].start = cur_start;
    result[count].end = cur_end;
    count++;

    free(result);
    free(s);
    return count;
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
static int64_t lcg_next(int64_t state) {
    return (1103515245LL * state + 12345LL) % 2147483648LL;
}

static Interval *build_case(int64_t seed, int64_t count) {
    Interval *v = (Interval *)malloc(sizeof(Interval) * (size_t)count);
    int64_t state = seed;
    for (int64_t j = 0; j < count; j++) {
        state = lcg_next(state);
        int64_t start = state % 51;
        state = lcg_next(state);
        int64_t width = (state % 10) + 1;
        v[j].start = start;
        v[j].end = start + width;
    }
    return v;
}

int main(void) {
    const int64_t m_cases = 8;
    const int64_t n_values = 16;
    const int64_t k_iters = 1000000;

    Interval **sets = (Interval **)malloc(sizeof(Interval *) * (size_t)m_cases);
    for (int64_t m = 0; m < m_cases; m++) {
        sets[m] = build_case(m * 1000003 + 12345, n_values);
    }

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % m_cases;
        sum += merge_intervals(sets[idx], n_values);
    }
    printf("%lld\n", (long long)sum);

    for (int64_t m = 0; m < m_cases; m++) free(sets[m]);
    free(sets);
    return 0;
}
