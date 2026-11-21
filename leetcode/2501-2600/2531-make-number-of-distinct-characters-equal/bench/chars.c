// LeetCode #2531: Make Number of Distinct Characters Equal -- C mirror of
// the benchmark (chars.kara): the same pairs, passes, order and checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t distinct(const int64_t *counts) {
    int64_t d = 0;
    for (int i = 0; i < 26; i++) d += counts[i] > 0;
    return d;
}

static int is_it_possible(const char *word1, const char *word2) {
    int64_t one[26] = {0}, two[26] = {0};
    for (const char *c = word1; *c; c++) one[*c - 'a']++;
    for (const char *c = word2; *c; c++) two[*c - 'a']++;
    for (int a = 0; a < 26; a++)
        for (int b = 0; b < 26; b++) {
            if (one[a] > 0 && two[b] > 0) {
                one[a]--; one[b]++; two[b]--; two[a]++;
                int equal = distinct(one) == distinct(two);
                one[a]++; one[b]--; two[b]++; two[a]--;
                if (equal) return 1;
            }
        }
    return 0;
}

static int64_t seed = 2531;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *random_word(int64_t length, int64_t letters) {
    char *w = malloc(length + 1);
    for (int64_t i = 0; i < length; i++) w[i] = (char)('a' + next_random() % letters);
    w[length] = 0;
    return w;
}

static char *words1[1000], *words2[1000];

int main(void) {
    for (int t = 0; t < 1000; t++) {
        int64_t l1 = next_random() % 1000 + 1;
        int64_t k1 = next_random() % 26 + 1;
        words1[t] = random_word(l1, k1);
        int64_t l2 = next_random() % 1000 + 1;
        int64_t k2 = next_random() % 26 + 1;
        words2[t] = random_word(l2, k2);
    }
    const int passes = 24;
    int64_t check = 0;
    for (int p = 0; p < passes; p++) {
        int64_t start = check % 1000;
        for (int64_t i = 0; i < 1000; i++) {
            int64_t at = (start + i) % 1000;
            int answer = is_it_possible(words1[at], words2[at]);
            check = (check * 31 + (answer ? 2 : 1) + p) % 1000000007;
        }
    }
    printf("%d passes over 1000 pairs of words: checksum %lld\n", passes, (long long)check);
    return 0;
}
