// Benchmark for #644: mirror of max_average_ii.kara (the ★ arm: binary
// search on the average) on the same workload.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// The start and end of a subarray of `k` or more values averaging at
// least `m`; returns 0 if there is none.
static int reaches(const int64_t *prefix, int64_t len, int64_t k, double m, int64_t *start, int64_t *end_out) {
    int64_t lowest = 0;
    for (int64_t end = k; end < len; end++) {
        int64_t c = end - k;
        if ((double)(prefix[c] - prefix[lowest]) < m * (double)(c - lowest)) {
            lowest = c;
        }
        if ((double)(prefix[end] - prefix[lowest]) >= m * (double)(end - lowest)) {
            *start = lowest;
            *end_out = end;
            return 1;
        }
    }
    return 0;
}

static double find_max_average(const int64_t *nums, int64_t n, int64_t k) {
    int64_t *prefix = malloc((size_t)(n + 1) * sizeof(int64_t));
    prefix[0] = 0;
    for (int64_t i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    double lo = (double)nums[0];
    double hi = (double)nums[0];
    for (int64_t i = 0; i < n; i++) {
        double x = (double)nums[i];
        lo = x < lo ? x : lo;
        hi = x > hi ? x : hi;
    }
    int64_t best_start = 0, best_end = n;
    for (int it = 0; it < 100; it++) {
        double mid = (lo + hi) / 2.0;
        int64_t start, end;
        if (!reaches(prefix, n + 1, k, mid, &start, &end)) {
            hi = mid;
        } else {
            lo = mid;
            best_start = start;
            best_end = end;
        }
    }
    double answer = (double)(prefix[best_end] - prefix[best_start]) / (double)(best_end - best_start);
    free(prefix);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 644;
    int64_t n = 100000;
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        arrays[a] = malloc((size_t)n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            arrays[a][i] = next_random(&seed) % 20001 - 10000;
        }
    }
    int64_t rounds = 40;
    double total = 0.0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = 1 + (r * 7919) % 100000;
        total += find_max_average(arrays[r % 20], n, k);
    }
    printf("%lld rounds over 20 arrays of 100000 values: answers adding to %.5f\n", (long long)rounds, total);
    for (int a = 0; a < 20; a++) {
        free(arrays[a]);
    }
    return 0;
}
