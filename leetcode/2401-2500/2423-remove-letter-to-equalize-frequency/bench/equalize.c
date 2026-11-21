// LeetCode #2423: Remove Letter To Equalize Frequency -- the bench, the ★
// arm: the 26 letter counts, each held letter taken away once in turn and
// the counts left that are not zero compared.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WORDS 10000

static int64_t seed = 2423;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int equal_frequency(const unsigned char *word, int64_t n) {
    int64_t count[26] = {0};
    for (int64_t i = 0; i < n; i++) count[word[i] - 'a']++;
    for (int c = 0; c < 26; c++) {
        if (count[c] == 0) continue;
        count[c]--;
        int64_t want = 0;
        int equal = 1;
        for (int k = 0; k < 26; k++) {
            if (count[k] > 0) {
                if (want == 0) want = count[k];
                else if (count[k] != want) equal = 0;
            }
        }
        count[c]++;
        if (equal) return 1;
    }
    return 0;
}

int main(void) {
    static unsigned char words[WORDS][128];
    static int64_t lens[WORDS];
    for (int w = 0; w < WORDS; w++) {
        int64_t kinds = 1 + next_random() % 20;
        int64_t times = 1 + next_random() % 5;
        unsigned char *b = words[w];
        int64_t n = 0;
        for (int64_t k = 0; k < kinds; k++)
            for (int64_t t = 0; t < times; t++) b[n++] = (unsigned char)('a' + k);
        if (next_random() % 2 == 0) {
            b[n++] = (unsigned char)('a' + next_random() % 26);
        } else {
            int64_t at = next_random() % n;
            memmove(b + at, b + at + 1, n - at - 1);
            n--;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            unsigned char t = b[i];
            b[i] = b[j];
            b[j] = t;
        }
        while (n < 2) b[n++] = 'a';
        lens[w] = n;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 200; p++)
        for (int w = 0; w < WORDS; w++) check = (check * 3 + equal_frequency(words[w], lens[w]) + p) % 1000000007;
    printf("200 passes over 10^4 words: checksum %lld\n", (long long)check);
    return 0;
}
