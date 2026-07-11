/*
 * Benchmark workload — Scramble String (LeetCode #87), SEQ lane.
 * C mirror of bench/scramble_string.kara. Each iteration builds a length-12 string and
 * a coprime-step permutation of it, runs the O(n^4) top-down memoized scramble, and
 * folds the filled memo state into a work-sensitive checksum added to an associative
 * sum. Same len/K. The scramble_string_par.c sibling parallelises with pthreads.
 * See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int scramble(const uint8_t *s1, int64_t i1, const uint8_t *s2, int64_t i2,
                    int64_t len, int64_t *memo, int64_t n) {
    if (len == 0) return 1;
    int64_t key = (i1 * n + i2) * (n + 1) + len;
    if (memo[key] != -1) return memo[key] == 1;
    int equal = 1;
    for (int64_t k = 0; k < len; k++) {
        if (s1[i1 + k] != s2[i2 + k]) { equal = 0; break; }
    }
    if (equal) { memo[key] = 1; return 1; }
    int64_t counts[26] = {0};
    for (int64_t k = 0; k < len; k++) {
        counts[s1[i1 + k] - 97]++;
        counts[s2[i2 + k] - 97]--;
    }
    for (int c = 0; c < 26; c++) {
        if (counts[c] != 0) { memo[key] = 0; return 0; }
    }
    for (int64_t split = 1; split < len; split++) {
        if (scramble(s1, i1, s2, i2, split, memo, n)
            && scramble(s1, i1 + split, s2, i2 + split, len - split, memo, n)) {
            memo[key] = 1;
            return 1;
        }
        if (scramble(s1, i1, s2, i2 + len - split, split, memo, n)
            && scramble(s1, i1 + split, s2, i2, len - split, memo, n)) {
            memo[key] = 1;
            return 1;
        }
    }
    memo[key] = 0;
    return 0;
}

static int64_t one(int64_t len, int64_t seed) {
    uint8_t *s1 = malloc(len * sizeof(uint8_t));
    uint8_t *s2 = malloc(len * sizeof(uint8_t));
    for (int64_t j = 0; j < len; j++)
        s1[j] = (uint8_t)(97 + (j % 8));
    for (int64_t j = 0; j < len; j++)
        s2[j] = s1[(j * 5 + seed) % len];
    int64_t cells = len * len * (len + 1);
    int64_t *memo = malloc(cells * sizeof(int64_t));
    for (int64_t i = 0; i < cells; i++) memo[i] = -1;
    int64_t r = scramble(s1, 0, s2, 0, len, memo, len) ? 1 : 0;
    int64_t h = r;
    for (int64_t i = 0; i < cells; i++)
        h = (h * 131 + (memo[i] + 2)) % 1000000007;
    free(s1);
    free(s2);
    free(memo);
    return h;
}

int main(void) {
    const int64_t len = 12, total = 60000;
    int64_t sum = 0;
    for (int64_t k = 0; k < total; k++)
        sum += one(len, k);
    printf("%lld\n", (long long)sum);
    return 0;
}
