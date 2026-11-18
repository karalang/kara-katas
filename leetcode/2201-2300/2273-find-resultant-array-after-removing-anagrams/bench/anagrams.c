// LeetCode #2273: Find Resultant Array After Removing Anagrams -- the
// bench, the ★ arm. Words are heap strings, and each word's sorted
// letters a fresh key, as in the other languages.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int by_char(const void *a, const void *b) { return *(const char *)a - *(const char *)b; }

static char *sorted_letters(const char *w) {
    size_t n = strlen(w);
    char *k = malloc(n + 1);
    memcpy(k, w, n + 1);
    qsort(k, n, 1, by_char);
    return k;
}

// the kept words, as copies, in `out`; returns how many
static int64_t remove_anagrams(char **words, int64_t m, char **out) {
    int64_t kept = 0;
    char *last = NULL;
    for (int64_t i = 0; i < m; i++) {
        char *key = sorted_letters(words[i]);
        if (kept == 0 || strcmp(key, last) != 0) out[kept++] = strdup(words[i]);
        free(last);
        last = key;
    }
    free(last);
    return kept;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2273;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    char *words[100], *out[100];
    int64_t check = 0;
    for (int t = 0; t < 20000; t++) {
        for (int i = 0; i < 100; i++) {
            words[i] = malloc(11);
            if (i > 0 && next_random() % 2 == 0) {
                memcpy(words[i], words[i - 1], 11);
                for (int64_t j = 9; j >= 1; j--) {
                    int64_t r = next_random() % (j + 1);
                    char c = words[i][j];
                    words[i][j] = words[i][r];
                    words[i][r] = c;
                }
            } else {
                for (int j = 0; j < 10; j++) words[i][j] = (char)('a' + next_random() % 4);
                words[i][10] = 0;
            }
        }
        int64_t kept = remove_anagrams(words, 100, out);
        check = (check * 31 + kept * 1000 + out[kept - 1][0]) % 1000000007;
        for (int64_t i = 0; i < kept; i++) free(out[i]);
        for (int i = 0; i < 100; i++) free(words[i]);
    }
    printf("20000 lists of 100: checksum %lld\n", (long long)check);
    return 0;
}
