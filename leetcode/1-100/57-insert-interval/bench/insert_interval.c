// Benchmark workload — Insert Interval (LeetCode #57).
// C mirror of bench/insert_interval.kara. Same M/N/K, LCG generator,
// cursor-based disjoint-sorted case builder, per-case new interval, linear
// three-phase insert, and sink — see that file's header for the rationale.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    int64_t start;
    int64_t end;
} Interval;

// Forces the result allocation to escape so clang can't elide the
// malloc/free pair as dead (the kara/rust mirrors genuinely allocate a Vec
// that escapes to the caller — this keeps the seq lane apples-to-apples).
static volatile int64_t g_sink;

// Materializes the insert result into a fresh heap array (matching the
// kara/rust mirrors' Vec allocation) and returns its length — the sink.
static int64_t insert_interval(const Interval *intervals, int64_t n,
                               int64_t new_start, int64_t new_end) {
    // Result is at most n + 1 intervals.
    Interval *result = (Interval *)malloc(sizeof(Interval) * (size_t)(n + 1));
    int64_t count = 0;
    int64_t i = 0;

    // Phase 1 — intervals entirely left of the new one.
    while (i < n && intervals[i].end < new_start) {
        result[count++] = intervals[i];
        i++;
    }
    // Phase 2 — absorb every overlapping/touching interval.
    while (i < n && intervals[i].start <= new_end) {
        if (intervals[i].start < new_start) new_start = intervals[i].start;
        if (intervals[i].end > new_end) new_end = intervals[i].end;
        i++;
    }
    result[count].start = new_start;
    result[count].end = new_end;
    count++;
    // Phase 3 — the untouched tail.
    while (i < n) {
        result[count++] = intervals[i];
        i++;
    }

    // Read from the materialized buffer through a volatile sink so the
    // allocation is observable and cannot be optimized away.
    g_sink = result[count - 1].end;
    free(result);
    return count;
}

// Overflow-free 31-bit LCG: 1103515245 * state + 12345 (mod 2^31).
static int64_t lcg_next(int64_t state) {
    return (1103515245LL * state + 12345LL) % 2147483648LL;
}

static Interval *build_case(int64_t seed, int64_t count) {
    Interval *v = (Interval *)malloc(sizeof(Interval) * (size_t)count);
    int64_t state = seed;
    int64_t cursor = 0;
    for (int64_t j = 0; j < count; j++) {
        state = lcg_next(state);
        int64_t gap = (state % 4) + 2;
        state = lcg_next(state);
        int64_t width = (state % 6) + 1;
        int64_t start = cursor + gap;
        int64_t end = start + width;
        v[j].start = start;
        v[j].end = end;
        cursor = end;
    }
    return v;
}

static void pick_new(const Interval *case_, int64_t m, int64_t count,
                     int64_t *out_start, int64_t *out_end) {
    int64_t half = count / 2;
    int64_t st = lcg_next(m * 7919 + 101);
    int64_t lo = st % half;
    st = lcg_next(st);
    int64_t span = st % half;
    int64_t hi = lo + 1 + span;
    if (hi > count - 1) hi = count - 1;
    *out_start = case_[lo].start;
    *out_end = case_[hi].end;
}

int main(void) {
    const int64_t m_cases = 8;
    const int64_t n_values = 16;
    const int64_t k_iters = 1000000;

    Interval **sets = (Interval **)malloc(sizeof(Interval *) * (size_t)m_cases);
    int64_t *ns = (int64_t *)malloc(sizeof(int64_t) * (size_t)m_cases);
    int64_t *ne = (int64_t *)malloc(sizeof(int64_t) * (size_t)m_cases);
    for (int64_t m = 0; m < m_cases; m++) {
        sets[m] = build_case(m * 1000003 + 12345, n_values);
        pick_new(sets[m], m, n_values, &ns[m], &ne[m]);
    }

    int64_t sum = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t idx = k % m_cases;
        sum += insert_interval(sets[idx], n_values, ns[idx], ne[idx]);
    }
    printf("%lld\n", (long long)sum);

    for (int64_t m = 0; m < m_cases; m++) free(sets[m]);
    free(sets);
    free(ns);
    free(ne);
    return 0;
}
