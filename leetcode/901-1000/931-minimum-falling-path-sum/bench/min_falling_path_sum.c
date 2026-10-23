// LeetCode #931: Minimum Falling Path Sum -- bench: one row of sums at a
// time. Mirrors min_falling_path_sum.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t min_falling_path_sum(int64_t **matrix, int64_t n) {
    int64_t *prev = malloc(n * sizeof(int64_t));
    int64_t *cur = malloc(n * sizeof(int64_t));
    memcpy(prev, matrix[0], n * sizeof(int64_t));
    for (int64_t r = 1; r < n; r++) {
        for (int64_t c = 0; c < n; c++) {
            int64_t best = prev[c];
            if (c > 0 && prev[c - 1] < best) best = prev[c - 1];
            if (c + 1 < n && prev[c + 1] < best) best = prev[c + 1];
            cur[c] = matrix[r][c] + best;
        }
        int64_t *t = prev;
        prev = cur;
        cur = t;
    }
    int64_t answer = prev[0];
    for (int64_t c = 1; c < n; c++)
        if (prev[c] < answer) answer = prev[c];
    free(prev);
    free(cur);
    return answer;
}

static int64_t seed = 931;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 150, count = 100, n = 100;
    // count matrices of n x n values from -100 to 100, built once
    int64_t ***matrices = malloc(count * sizeof(int64_t **));
    for (int64_t g = 0; g < count; g++) {
        matrices[g] = malloc(n * sizeof(int64_t *));
        for (int64_t i = 0; i < n; i++) {
            matrices[g][i] = malloc(n * sizeof(int64_t));
            for (int64_t j = 0; j < n; j++) matrices[g][i][j] = next_random() % 201 - 100;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round visits every matrix, starting from a different one
        for (int64_t i = 0; i < count; i++) {
            int64_t a = min_falling_path_sum(matrices[(r + i) % count], n);
            total += a;
            check = (check * 1000003 + a + 1000000) % 1000000007;
        }
    }
    printf("%lld rounds over %lld matrices of %lld x %lld: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)n, (long long)total, (long long)check);
    for (int64_t g = 0; g < count; g++) {
        for (int64_t i = 0; i < n; i++) free(matrices[g][i]);
        free(matrices[g]);
    }
    free(matrices);
    return 0;
}
