// LeetCode #691: Stickers to Spell Word -- bench program, C mirror of the ★ arm.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long seed = 691;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_word(char *w, int len, int alphabet) {
    for (int i = 0; i < len; i++) w[i] = (char)('a' + next_random() % alphabet);
    w[len] = 0;
}

static long long min_stickers(char stickers[][16], int n, const char *target) {
    int m = (int)strlen(target);
    int full = (1 << m) - 1;
    long long (*counts)[26] = calloc(n, sizeof *counts);
    for (int s = 0; s < n; s++)
        for (const char *p = stickers[s]; *p; p++) counts[s][*p - 'a']++;
    long long *dp = malloc(sizeof(long long) * (full + 1));
    for (int i = 0; i <= full; i++) dp[i] = -1;
    dp[0] = 0;
    long long left[26];
    for (int mask = 0; mask <= full; mask++) {
        if (dp[mask] < 0) continue;
        for (int s = 0; s < n; s++) {
            for (int k = 0; k < 26; k++) left[k] = counts[s][k];
            int next = mask;
            for (int i = 0; i < m; i++) {
                int k = target[i] - 'a';
                if ((next & (1 << i)) == 0 && left[k] > 0) {
                    left[k]--;
                    next |= 1 << i;
                }
            }
            if (next != mask && (dp[next] < 0 || dp[mask] + 1 < dp[next])) dp[next] = dp[mask] + 1;
        }
    }
    long long r = dp[full];
    free(dp);
    free(counts);
    return r;
}

int main(void) {
    int problems = 160;
    long long total = 0, checksum = 0;
    static char stickers[50][16];
    char target[16];
    for (int p = 0; p < problems; p++) {
        for (int s = 0; s < 50; s++) random_word(stickers[s], 10, 12);
        random_word(target, 15, 12);
        long long r = min_stickers(stickers, 50, target);
        total += r;
        checksum = (checksum * 31 + r + 2) % 1000000007;
    }
    printf("%d problems of 50 stickers and a 15-letter target: %lld stickers in all, checksum %lld\n", problems, total, checksum);
    return 0;
}
