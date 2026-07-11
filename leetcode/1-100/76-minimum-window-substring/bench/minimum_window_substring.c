/*
 * Benchmark workload — Minimum Window Substring (LeetCode #76).
 * C mirror of bench/minimum_window_substring.kara. Sliding-window need/have
 * algorithm over a fixed n=50000 sequence (alphabet {0,1,2,3}) built once, K=5000
 * iterations against a k-cycled 3-symbol target, folding (start, len) into a
 * rolling hash. The O(n) window scan is the measured work. See ../README.md.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define N 50000

static void min_window(const int64_t *s, int64_t n, const int64_t *t, int64_t m,
                       int64_t *out_start, int64_t *out_len) {
    if (m > n) { *out_start = -1; *out_len = 0; return; }
    int64_t need[4] = {0, 0, 0, 0};
    int64_t required = 0;
    for (int64_t j = 0; j < m; j++) {
        int64_t c = t[j];
        if (need[c] == 0) required++;
        need[c]++;
    }
    int64_t have[4] = {0, 0, 0, 0};
    int64_t formed = 0, l = 0, best_start = -1, best_len = 0;
    for (int64_t r = 0; r < n; r++) {
        int64_t cr = s[r];
        have[cr]++;
        if (have[cr] == need[cr]) formed++;
        while (formed == required) {
            int64_t win = r - l + 1;
            if (best_start == -1 || win < best_len) { best_start = l; best_len = win; }
            int64_t cl = s[l];
            have[cl]--;
            if (have[cl] < need[cl]) formed--;
            l++;
        }
    }
    *out_start = best_start;
    *out_len = best_len;
}

int main(void) {
    const int64_t total = 5000, modulus = 1000000007;
    int64_t *s = (int64_t *)malloc(sizeof(int64_t) * N);
    for (int64_t i = 0; i < N; i++) s[i] = (i * 7) % 4;
    int64_t targets[6][3] = {
        {0, 1, 2}, {1, 2, 3}, {2, 3, 0}, {3, 0, 1}, {0, 2, 3}, {1, 3, 0},
    };

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t start, len;
        min_window(s, N, targets[k % 6], 3, &start, &len);
        acc = (acc * 131 + (start + 1)) % modulus;
        acc = (acc * 131 + len) % modulus;
    }
    printf("%lld\n", (long long)acc);
    free(s);
    return 0;
}
