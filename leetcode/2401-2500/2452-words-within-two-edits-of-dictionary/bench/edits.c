// LeetCode #2452: Words Within Two Edits of Dictionary -- the bench, the
// ★ arm: each query against each word, the differing places counted
// until a third rules the word out.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LEN 100

static int within_two(const char *a, const char *b) {
    int differ = 0;
    for (int j = 0; j < LEN; j++)
        if (a[j] != b[j] && ++differ > 2) return 0;
    return 1;
}

// the kept queries, copied as each arm's vector of strings is; returns
// how many
static int64_t two_edit_words(char **queries, char **dictionary, int64_t q, int64_t d, char **answers) {
    int64_t kept = 0;
    for (int64_t i = 0; i < q; i++)
        for (int64_t k = 0; k < d; k++)
            if (within_two(queries[i], dictionary[k])) {
                answers[kept++] = strdup(queries[i]);
                break;
            }
    return kept;
}

static int64_t seed = 2452;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char words[100][100][LEN + 1];
    static char asks[100][100][LEN + 1];
    char **dictionaries[100];
    for (int c = 0; c < 100; c++) {
        for (int i = 0; i < 100; i++) {
            for (int j = 0; j < LEN; j++) words[c][i][j] = (char)(97 + next_random() % 4);
            words[c][i][LEN] = 0;
        }
        for (int i = 0; i < 100; i++) {
            memcpy(asks[c][i], words[c][next_random() % 100], LEN + 1);
            int64_t changes = next_random() % 5;
            for (int64_t t = 0; t < changes; t++) {
                int64_t place = next_random() % 100;
                asks[c][i][place] = (char)(97 + next_random() % 4);
            }
        }
        dictionaries[c] = malloc(100 * sizeof(char *));
        for (int i = 0; i < 100; i++) dictionaries[c][i] = strdup(words[c][i]);
    }
    int64_t check = 0;
    char *queries[100], *answers[100];
    for (int64_t p = 0; p < 45; p++)
        for (int c = 0; c < 100; c++) {
            int64_t place = next_random() % 100;
            asks[c][p % 100][place] = (char)(97 + next_random() % 4);
            for (int i = 0; i < 100; i++) queries[i] = strdup(asks[c][i]);
            int64_t kept = two_edit_words(queries, dictionaries[c], 100, 100, answers);
            check = (check * 31 + kept + p) % 1000000007;
            for (int64_t i = 0; i < kept; i++) free(answers[i]);
            for (int i = 0; i < 100; i++) free(queries[i]);
        }
    printf("45 passes over 100 cases of 100 queries: checksum %lld\n", (long long)check);
    for (int c = 0; c < 100; c++) {
        for (int i = 0; i < 100; i++) free(dictionaries[c][i]);
        free(dictionaries[c]);
    }
    return 0;
}
