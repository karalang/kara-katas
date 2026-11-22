// LeetCode #2900: Longest Unequal Adjacent Groups Subsequence I -- the
// bench's C mirror (words.kara): each chosen word copied into a fresh
// allocation, as the other languages' clones are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { COUNT = 10000, ROUNDS = 20, N = 100 };

static int64_t seed = 2900;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char words[COUNT][N][4];
static int64_t groups[COUNT][N];

static char **get_longest_subsequence(char (*w)[4], const int64_t *g, int64_t n, int64_t *len) {
    char **chosen = malloc(sizeof(char *) * n);
    int64_t m = 0;
    for (int64_t i = 0; i < n; i++)
        if (i == 0 || g[i] != g[i - 1]) {
            size_t l = strlen(w[i]);
            chosen[m] = malloc(l + 1);
            memcpy(chosen[m], w[i], l + 1);
            m++;
        }
    *len = m;
    return chosen;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) {
            words[c][i][0] = letters[next_random() % 26];
            words[c][i][1] = letters[i % 26];
            words[c][i][2] = letters[i / 26];
            words[c][i][3] = 0;
        }
        int len = 0;
        int64_t group = next_random() % 2;
        while (len < N) {
            int64_t run = next_random() % 5 + 1;
            for (int64_t t = 0; t < run; t++)
                if (len < N) groups[c][len++] = group;
            group = 1 - group;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            int64_t len;
            char **chosen = get_longest_subsequence(words[c], groups[c], N, &len);
            total += len;
            check = (check * 31 + len + r) % 1000000007;
            for (int64_t i = 0; i < len; i++) check = (check * 31 + (int64_t)strlen(chosen[i])) % 1000000007;
            check = (check * 31 + (unsigned char)chosen[len - 1][0]) % 1000000007;
            for (int64_t i = 0; i < len; i++) free(chosen[i]);
            free(chosen);
        }
    printf("%d cases of %d, %d rounds: %lld words chosen, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)check);
    return 0;
}
