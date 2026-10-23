// LeetCode #916: Word Subsets -- bench: C mirror of every word of words2
// folded into one need in word_subsets.kara. The result holds copies of
// the universal words, as the Kara and Rust versions clone them.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void counts(const char *word, int64_t *count) {
    for (int c = 0; c < 26; c++)
        count[c] = 0;
    for (const char *p = word; *p; p++)
        count[*p - 'a']++;
}

// Returns the number of universal words, copied into `universal`.
static int64_t word_subsets(char **words1, int64_t n1, char **words2, int64_t n2, char **universal) {
    int64_t need[26] = {0};
    int64_t count[26];
    for (int64_t i = 0; i < n2; i++) {
        counts(words2[i], count);
        for (int c = 0; c < 26; c++)
            if (count[c] > need[c])
                need[c] = count[c];
    }
    int64_t kept = 0;
    for (int64_t i = 0; i < n1; i++) {
        counts(words1[i], count);
        int all = 1;
        for (int c = 0; c < 26; c++)
            if (count[c] < need[c])
                all = 0;
        if (all)
            universal[kept++] = strdup(words1[i]);
    }
    return kept;
}

static int64_t seed = 916;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char *random_word(int64_t len, int64_t letters) {
    char *w = malloc(len + 1);
    for (int64_t i = 0; i < len; i++)
        w[i] = (char)(97 + next_random() % letters);
    w[len] = 0;
    return w;
}

int main(void) {
    int64_t rounds = 200;
    int64_t n = 50000;
    char **words1 = malloc(sizeof(char *) * n);
    for (int64_t i = 0; i < n; i++)
        words1[i] = random_word(10, 8);
    char **universal = malloc(sizeof(char *) * n);
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        char *words2[3];
        for (int j = 0; j < 3; j++) {
            int64_t len = 1 + next_random() % 3;
            words2[j] = random_word(len, 8);
        }
        int64_t kept = word_subsets(words1, n, words2, 3, universal);
        total += kept;
        for (int64_t i = 0; i < kept; i++) {
            for (const char *p = universal[i]; *p; p++)
                check = (check * 31 + (unsigned char)*p) % 1000000007;
            free(universal[i]);
        }
        for (int j = 0; j < 3; j++)
            free(words2[j]);
    }
    printf("%lld rounds over %lld words: %lld universal, checksum %lld\n", (long long)rounds, (long long)n,
           (long long)total, (long long)check);
    for (int64_t i = 0; i < n; i++)
        free(words1[i]);
    free(words1);
    free(universal);
    return 0;
}
