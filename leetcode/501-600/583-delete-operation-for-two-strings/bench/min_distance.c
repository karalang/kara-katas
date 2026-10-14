// Benchmark for #583: C mirror of the ★ arm (the longest common
// subsequence); see min_distance.kara. Each call copies both words into
// fresh arrays of code points (the words are ASCII, one byte each) and
// allocates the table as an array of row pointers, one row per prefix
// of word1, and frees it all.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t min_distance(const char *word1, const char *word2) {
    int64_t m = (int64_t)strlen(word1);
    int64_t n = (int64_t)strlen(word2);
    uint32_t *a = malloc(sizeof(uint32_t) * (m ? m : 1));
    uint32_t *b = malloc(sizeof(uint32_t) * (n ? n : 1));
    for (int64_t i = 0; i < m; i++) a[i] = (unsigned char)word1[i];
    for (int64_t j = 0; j < n; j++) b[j] = (unsigned char)word2[j];
    int64_t **lcs = malloc(sizeof(int64_t *) * (m + 1));
    for (int64_t i = 0; i <= m; i++) lcs[i] = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = 1; i <= m; i++) {
        for (int64_t j = 1; j <= n; j++) {
            if (a[i - 1] == b[j - 1]) {
                lcs[i][j] = lcs[i - 1][j - 1] + 1;
            } else {
                int64_t up = lcs[i - 1][j], left = lcs[i][j - 1];
                lcs[i][j] = up > left ? up : left;
            }
        }
    }
    int64_t answer = m + n - 2 * lcs[m][n];
    for (int64_t i = 0; i <= m; i++) free(lcs[i]);
    free(lcs);
    free(a);
    free(b);
    return answer;
}

// ---- benchmark --------------------------------------------------------------

static int64_t seed = 583;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *word(int64_t len, int64_t letters) {
    char *s = malloc(len + 1);
    for (int64_t i = 0; i < len; i++) s[i] = (char)('a' + next_random() % letters);
    s[len] = 0;
    return s;
}

int main(void) {
    int64_t count = 40, rounds = 30;
    char *firsts[40], *seconds[40];
    for (int64_t g = 0; g < count; g++) {
        int64_t letters = 2 + next_random() % 25;
        firsts[g] = word(500, letters);
        seconds[g] = word(500, letters);
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int64_t got = min_distance(firsts[p], seconds[p]);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    printf("%lld pairs of 500 letters, %lld rounds: %lld deletions, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        free(firsts[g]);
        free(seconds[g]);
    }
    return 0;
}
