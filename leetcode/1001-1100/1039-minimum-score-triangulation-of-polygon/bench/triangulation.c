// LeetCode #1039: Minimum Score Triangulation of Polygon -- bench
// Mirrors ../triangulation.kara; see ../README.md § Benchmarks. The
// table is allocated per call, as the Vec of rows is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_score_triangulation(const int64_t *values, int64_t n) {
    int64_t *best = calloc(n * n, sizeof(int64_t));
    for (int64_t len = 2; len < n; len++) {
        for (int64_t i = 0; i < n - len; i++) {
            int64_t j = i + len;
            int64_t least = INT64_MAX;
            for (int64_t k = i + 1; k < j; k++) {
                int64_t score = best[i * n + k] + best[k * n + j] + values[i] * values[k] * values[j];
                if (score < least) least = score;
            }
            best[i * n + j] = least;
        }
    }
    int64_t answer = best[n - 1];
    free(best);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 2000, rounds = 10;
    int64_t seed = 1039;
    int64_t *polygons = malloc(count * 50 * sizeof(int64_t));
    for (int64_t p = 0; p < count; p++)
        for (int64_t i = 0; i < 50; i++) polygons[p * 50 + i] = next_random(&seed) % 100 + 1;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t p = 0; p < count; p++) {
            int64_t score = min_score_triangulation(&polygons[p * 50], 50);
            total += score;
            check = (check * 131 + score) % 1000000007;
        }
    }
    printf("%lld polygons of 50 vertices, %lld rounds: total %lld, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)total, (long long)check);
    free(polygons);
    return 0;
}
