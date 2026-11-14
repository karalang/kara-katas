// LeetCode #1563: Stone Game V -- bench: the ★ arm (every stretch,
// shortest first, every split) over 5 rows of 400 stones of 1 to 10^6,
// built once, each asked twice.
// C mirror of stones.kara; the table is one block of n * n, freed per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static int64_t stone_game_v(const int64_t *row, int64_t n) {
    int64_t *prefix = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) prefix[i + 1] = prefix[i] + row[i];
    int64_t *best = calloc(n * n, sizeof(int64_t));
    for (int64_t length = 2; length <= n; length++) {
        for (int64_t i = 0; i <= n - length; i++) {
            int64_t j = i + length - 1, most = 0;
            for (int64_t k = i; k < j; k++) {
                int64_t left = prefix[k + 1] - prefix[i];
                int64_t right = prefix[j + 1] - prefix[k + 1];
                if (left < right)
                    most = max64(most, left + best[i * n + k]);
                else if (left > right)
                    most = max64(most, right + best[(k + 1) * n + j]);
                else
                    most = max64(most, left + max64(best[i * n + k], best[(k + 1) * n + j]));
            }
            best[i * n + j] = most;
        }
    }
    int64_t answer = best[n - 1];
    free(prefix);
    free(best);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1563;
    static int64_t rows[5][400];
    for (int r = 0; r < 5; r++)
        for (int i = 0; i < 400; i++) {
            int64_t v = next_random(&seed) * 32768;
            rows[r][i] = (v + next_random(&seed)) % 1000000 + 1;
        }
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 2; pass++)
        for (int r = 0; r < 5; r++) {
            int64_t score = stone_game_v(rows[r], 400);
            total += score;
            check = mix(check, score);
        }
    printf("2 passes over 5 rows of 400 stones: %lld points, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
