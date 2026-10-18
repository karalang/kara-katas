// LeetCode #712: Minimum ASCII Delete Sum for Two Strings -- a table
// of prefixes.
// Benchmark mirror of the Kara star arm: cost[i][j] is the least ASCII
// sum deleted to make the first i bytes of s1 equal to the first j of
// s2, in a table of rows allocated per call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t minimum_delete_sum(const char *a, const char *b) {
    int64_t m = strlen(a), n = strlen(b);
    int64_t **cost = malloc((m + 1) * sizeof(int64_t *));
    for (int64_t i = 0; i <= m; i++) cost[i] = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 1; i <= m; i++) cost[i][0] = cost[i - 1][0] + (unsigned char)a[i - 1];
    for (int64_t j = 1; j <= n; j++) cost[0][j] = cost[0][j - 1] + (unsigned char)b[j - 1];
    for (int64_t i = 1; i <= m; i++) {
        for (int64_t j = 1; j <= n; j++) {
            if (a[i - 1] == b[j - 1]) {
                cost[i][j] = cost[i - 1][j - 1];
            } else {
                int64_t drop_a = cost[i - 1][j] + (unsigned char)a[i - 1];
                int64_t drop_b = cost[i][j - 1] + (unsigned char)b[j - 1];
                cost[i][j] = drop_a < drop_b ? drop_a : drop_b;
            }
        }
    }
    int64_t out = cost[m][n];
    for (int64_t i = 0; i <= m; i++) free(cost[i]);
    free(cost);
    return out;
}

int main(void) {
    int64_t seed = 712;
    char *words[20];
    for (int w = 0; w < 20; w++) {
        words[w] = malloc(1001);
        for (int i = 0; i < 1000; i++) words[w][i] = (char)(97 + next_random(&seed) % 26);
        words[w][1000] = 0;
    }
    int64_t sum = 0;
    for (int round = 0; round < 10; round++) {
        for (int p = 0; p < 10; p++) sum += minimum_delete_sum(words[2 * p], words[2 * p + 1]);
    }
    for (int w = 0; w < 20; w++) free(words[w]);
    printf("10 rounds of 10 pairs of 1000 letters: sum %lld\n", (long long)sum);
    return 0;
}
