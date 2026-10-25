// Benchmark: LeetCode #1000 Minimum Cost to Merge Stones -- the ★ arm,
// an interval table by length, on rows of up to 30 piles, LeetCode's
// largest. Mirrors merge_stones.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t merge_stones(const int64_t *stones, int64_t n, int64_t k) {
    if ((n - 1) % (k - 1) != 0) return -1;
    int64_t *prefix = calloc((size_t)n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) prefix[i + 1] = prefix[i] + stones[i];
    int64_t **dp = malloc(sizeof(int64_t *) * (size_t)n);
    for (int64_t i = 0; i < n; i++) dp[i] = calloc((size_t)n, sizeof(int64_t));
    for (int64_t length = k; length <= n; length++) {
        for (int64_t i = 0; i + length <= n; i++) {
            int64_t j = i + length - 1, best = (int64_t)1 << 60;
            for (int64_t m = i; m < j; m += k - 1) {
                int64_t c = dp[i][m] + dp[m + 1][j];
                if (c < best) best = c;
            }
            if ((length - 1) % (k - 1) == 0) best += prefix[j + 1] - prefix[i];
            dp[i][j] = best;
        }
    }
    int64_t answer = dp[0][n - 1];
    for (int64_t i = 0; i < n; i++) free(dp[i]);
    free(dp);
    free(prefix);
    return answer;
}

static int64_t seed = 1000;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 5000;
    // 20 rows, k from 2 to 11 twice over, each with as many piles of 1 to
    // 100 stones, up to 30, as k can merge down to one pile
    int64_t rows[20][30], ns[20], ks[20];
    for (int t = 0; t < 20; t++) {
        int64_t k = 2 + t % 10;
        int64_t n = 1 + 29 / (k - 1) * (k - 1);
        for (int64_t i = 0; i < n; i++) rows[t][i] = 1 + next_random() % 100;
        ns[t] = n;
        ks[t] = k;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 20; i++) {
            int64_t t = (r + i) % 20;
            int64_t got = merge_stones(rows[t], ns[t], ks[t]);
            total += got;
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    printf("%lld rounds over 20 rows of up to 30 piles: cost %lld, checksum %lld\n",
           (long long)rounds, (long long)total, (long long)check);
    return 0;
}
