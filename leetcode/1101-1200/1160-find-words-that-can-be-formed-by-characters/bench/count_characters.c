// LeetCode #1160 bench: the ★ arm's counts of each letter, the same
// workload as count_characters.kara. Words are NUL-terminated strings.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t count_characters(char **words, int64_t n, const char *chars) {
    int64_t have[26] = {0};
    for (const char *c = chars; *c; c++) have[*c - 'a']++;
    int64_t total = 0;
    for (int64_t k = 0; k < n; k++) {
        int64_t need[26] = {0};
        int good = 1;
        int64_t len = 0;
        for (const char *c = words[k]; *c; c++, len++) {
            if (++need[*c - 'a'] > have[*c - 'a']) {
                good = 0;
                break;
            }
        }
        if (good) total += len;
    }
    return total;
}

static int64_t seed = 1160;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *word(int64_t len, int64_t k) {
    char *w = malloc(len + 1);
    for (int64_t i = 0; i < len; i++) w[i] = (char)('a' + next_random() % k);
    w[len] = 0;
    return w;
}

int main(void) {
    const int64_t passes = 1500;
    char **words[12];
    char *chars[12];
    for (int p = 0; p < 12; p++) {
        int kind = p % 3;
        chars[p] = word(100, kind == 1 ? 4 : 26);
        words[p] = malloc(1000 * sizeof(char *));
        for (int i = 0; i < 1000; i++) {
            if (kind == 0) {
                int64_t len = 1 + next_random() % 100;
                words[p][i] = word(len, 26);
            } else if (kind == 1) {
                int64_t len = 1 + next_random() % 30;
                words[p][i] = word(len, 4);
            } else {
                char *b = malloc(103);
                int64_t m = 0;
                for (int j = 0; j < 100; j++)
                    if (next_random() % 2 == 0) b[m++] = chars[p][j];
                if (i % 2 == 1) {
                    char x = b[next_random() % m];
                    b[m++] = x;
                }
                b[m] = 0;
                words[p][i] = b;
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++)
        for (int k = 0; k < 12; k++)
            check = (check * 31 + count_characters(words[k], 1000, chars[k]) + p) % 1000000007;
    printf("%lld passes over 12 problems of 1000 words: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
