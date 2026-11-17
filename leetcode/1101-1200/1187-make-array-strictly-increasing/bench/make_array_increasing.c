// LeetCode #1187: Make Array Strictly Increasing -- the ★ arm in C: for each
// count k of replacements so far, the least value the prefix can end on,
// over the same pairs as the Kāra bench.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 2000

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t make_array_increasing(const int64_t *arr1, size_t n, const int64_t *arr2, size_t m) {
    int64_t *spare = malloc(m * sizeof(int64_t));
    memcpy(spare, arr2, m * sizeof(int64_t));
    qsort(spare, m, sizeof(int64_t), cmp_i64);
    size_t len = 0;
    for (size_t i = 0; i < m; i++) {
        if (len == 0 || spare[len - 1] != spare[i]) spare[len++] = spare[i];
    }
    const int64_t none = INT64_MAX;
    int64_t *end = malloc((n + 1) * sizeof(int64_t));
    for (size_t k = 0; k <= n; k++) end[k] = none;
    end[0] = INT64_MIN;
    for (size_t i = 0; i < n; i++) {
        int64_t a = arr1[i];
        int64_t *next = malloc((n + 1) * sizeof(int64_t));
        for (size_t k = 0; k <= n; k++) next[k] = none;
        for (size_t k = 0; k <= n; k++) {
            if (end[k] != none && a > end[k]) next[k] = a;
            if (k > 0 && end[k - 1] != none) {
                // partition point: the first spare value above end[k - 1]
                size_t lo = 0, hi = len;
                while (lo < hi) {
                    size_t mid = lo + (hi - lo) / 2;
                    if (spare[mid] <= end[k - 1]) lo = mid + 1; else hi = mid;
                }
                if (lo < len && spare[lo] < next[k]) next[k] = spare[lo];
            }
        }
        free(end);
        end = next;
    }
    int64_t answer = -1;
    for (size_t k = 0; k <= n; k++) {
        if (end[k] != none) { answer = (int64_t)k; break; }
    }
    free(end);
    free(spare);
    return answer;
}

static int64_t seed = 1187;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void values(int64_t *out, size_t n, int64_t span) {
    for (size_t i = 0; i < n; i++) {
        int64_t hi = next_random();
        out[i] = (hi * 32768 + next_random()) % span;
    }
}

int main(void) {
    static int64_t firsts[4][N], seconds[4][N];
    values(firsts[0], N, 1000000001);
    values(seconds[0], N, 1000000001);
    for (int64_t i = 0; i < N; i++) firsts[1][i] = i % 40 == 39 ? 0 : i * 500000;
    values(seconds[1], N, 1000000001);
    values(firsts[2], N, 4000);
    values(seconds[2], N, 4000);
    for (int64_t i = 0; i < N; i++) firsts[3][i] = (N - i) * 1000;
    values(seconds[3], N, 1000000001);
    int64_t rounds = 6, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int p = 0; p < 4; p++) {
            int64_t ops = make_array_increasing(firsts[p], N, seconds[p], N);
            check = (check * 131 + ops + 2 + round) % 1000000007;
        }
    }
    printf("%lld rounds of 4 pairs of 2000 values: checksum %lld\n", (long long)rounds, (long long)check);
    return 0;
}
