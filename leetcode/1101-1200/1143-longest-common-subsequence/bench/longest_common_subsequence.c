// LeetCode #1143: Longest Common Subsequence -- the bench in C, the ★ arm's
// algorithm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t longest_common_subsequence(const char *a, const char *b) {
    int64_t m = (int64_t)strlen(a), n = (int64_t)strlen(b);
    int64_t **best = malloc((m + 1) * sizeof(int64_t *));
    for (int64_t i = 0; i <= m; i++) best[i] = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 1; i <= m; i++) {
        for (int64_t j = 1; j <= n; j++) {
            if (a[i - 1] == b[j - 1]) {
                best[i][j] = best[i - 1][j - 1] + 1;
            } else {
                int64_t up = best[i - 1][j], back = best[i][j - 1];
                best[i][j] = up > back ? up : back;
            }
        }
    }
    int64_t answer = best[m][n];
    for (int64_t i = 0; i <= m; i++) free(best[i]);
    free(best);
    return answer;
}

static int64_t seed = 1143;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char letters[] = "abcd";
    static char texts[20][1001];
    for (int t = 0; t < 20; t++) {
        for (int i = 0; i < 1000; i++) texts[t][i] = letters[next_random() % 4];
        texts[t][1000] = 0;
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 10; round++) {
        for (int p = 0; p < 10; p++) {
            for (int t = 2 * p; t <= 2 * p + 1; t++) {
                int64_t at = next_random() % 1000;
                texts[t][at] = letters[next_random() % 4];
            }
            int64_t answer = longest_common_subsequence(texts[2 * p], texts[2 * p + 1]);
            total += answer;
            check = (check * 131 + answer + 1) % 1000000007;
        }
    }
    printf("10 rounds over 10 pairs of 1000 letters: answers total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
