// LeetCode #1547: Minimum Cost to Cut a Stick -- bench: the ★ arm (interval
// DP) over 100 sticks of 2 to 1000000 with 1 to 100 distinct cuts, built
// once, each asked 4 times. C mirror of cut.kara: the table is a fresh
// heap block per call, as the Kāra arm's nested Vec is.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t min_cost(int64_t n, const int64_t *cuts, int64_t c) {
    int64_t m = c + 2;
    int64_t *points = malloc(m * sizeof(int64_t));
    memcpy(points, cuts, c * sizeof(int64_t));
    points[c] = 0;
    points[c + 1] = n;
    qsort(points, m, sizeof(int64_t), cmp);
    int64_t *cost = calloc(m * m, sizeof(int64_t));
    for (int64_t gap = 2; gap < m; gap++) {
        for (int64_t i = 0; i + gap < m; i++) {
            int64_t j = i + gap;
            int64_t best = INT64_MAX;
            for (int64_t k = i + 1; k < j; k++) {
                int64_t here = cost[i * m + k] + cost[k * m + j];
                if (here < best) best = here;
            }
            cost[i * m + j] = best + points[j] - points[i];
        }
    }
    int64_t answer = cost[m - 1];
    free(points);
    free(cost);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1547;
    int64_t ns[100], counts[100];
    int64_t *cutss[100];
    for (int s = 0; s < 100; s++) {
        int64_t a = next_random(&seed);
        int64_t n = (a * 32768 + next_random(&seed)) % 999999 + 2;
        int64_t want = next_random(&seed) % 100 + 1;
        if (want > n - 1) want = n - 1;
        int64_t *cuts = malloc(want * sizeof(int64_t));
        int64_t have = 0;
        while (have < want) {
            int64_t b = next_random(&seed);
            int64_t c = (b * 32768 + next_random(&seed)) % (n - 1) + 1;
            bool seen = false;
            for (int64_t i = 0; i < have; i++) seen |= cuts[i] == c;
            if (!seen) cuts[have++] = c;
        }
        ns[s] = n;
        counts[s] = want;
        cutss[s] = cuts;
    }
    int64_t check = 0;
    for (int p = 0; p < 4; p++) {
        for (int s = 0; s < 100; s++) check = mix(check, min_cost(ns[s], cutss[s], counts[s]));
    }
    for (int s = 0; s < 100; s++) free(cutss[s]);
    printf("4 passes over 100 sticks of up to 1000000 with up to 100 cuts: checksum %lld\n", (long long)check);
    return 0;
}
