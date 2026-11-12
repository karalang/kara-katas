// LeetCode #1140: Stone Game II -- the bench in C, the ★ arm's algorithm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t stone_game_ii(const int64_t *piles, int64_t n) {
    int64_t *left = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) left[i] = left[i + 1] + piles[i];
    int64_t **best = malloc((n + 1) * sizeof(int64_t *));
    for (int64_t i = 0; i <= n; i++) best[i] = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        for (int64_t m = 1; m <= n; m++) {
            if (i + 2 * m >= n) {
                best[i][m] = left[i];
            } else {
                int64_t most = 0;
                for (int64_t x = 1; x <= 2 * m; x++) {
                    int64_t mm = m > x ? m : x;
                    int64_t v = left[i] - best[i + x][mm];
                    if (v > most) most = v;
                }
                best[i][m] = most;
            }
        }
    }
    int64_t answer = best[0][1];
    for (int64_t i = 0; i <= n; i++) free(best[i]);
    free(best);
    free(left);
    return answer;
}

static int64_t seed = 1140;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t rows[20][100];
    for (int r = 0; r < 20; r++)
        for (int i = 0; i < 100; i++) rows[r][i] = next_random() % 10000 + 1;
    int64_t total = 0, check = 0;
    for (int round = 0; round < 100; round++) {
        for (int r = 0; r < 20; r++) {
            int64_t at = next_random() % 100;
            rows[r][at] = next_random() % 10000 + 1;
            int64_t answer = stone_game_ii(rows[r], 100);
            total += answer;
            check = (check * 131 + answer + 1) % 1000000007;
        }
    }
    printf("100 rounds over 20 rows of 100 piles: answers total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
