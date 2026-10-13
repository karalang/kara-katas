// Benchmark for #520: C mirror of the ★ arm (count the capitals); see
// detect_capital_use.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool detect_capital_use(const char *word, int64_t len) {
    int64_t capitals = 0;
    for (int64_t i = 0; i < len; i++)
        if (word[i] >= 'A' && word[i] <= 'Z') capitals++;
    return capitals == 0 || capitals == len || (capitals == 1 && word[0] >= 'A' && word[0] <= 'Z');
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char upper(char c) { return c >= 'a' && c <= 'z' ? c - 32 : c; }
static char lower(char c) { return c >= 'A' && c <= 'Z' ? c + 32 : c; }

// A random word of 1 to 100 letters: all capitals, all lower case, a
// capital then lower case, any mix, or one of the first three with one
// letter's case turned.
static char *random_word(int64_t *seed, int64_t *out_len) {
    int64_t len = 1 + next_random(seed) % 100;
    int64_t kind = next_random(seed) % 5;
    int64_t shape = kind == 4 ? next_random(seed) % 3 : kind;
    char *w = malloc(len + 1);
    for (int64_t i = 0; i < len; i++) {
        char c = (char)(97 + next_random(seed) % 26);
        bool capital = shape == 0 ? true : shape == 1 ? false : shape == 2 ? i == 0 : next_random(seed) % 2 == 0;
        w[i] = capital ? upper(c) : c;
    }
    if (kind == 4) {
        int64_t at = next_random(seed) % len;
        w[at] = w[at] >= 'A' && w[at] <= 'Z' ? lower(w[at]) : upper(w[at]);
    }
    w[len] = 0;
    *out_len = len;
    return w;
}

int main(void) {
    // 20,000 random words made once, then every word checked in each of
    // 200 rounds.
    int64_t seed = 520, n = 20000;
    char **words = malloc(n * sizeof(char *));
    int64_t *lens = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) words[i] = random_word(&seed, &lens[i]);
    int64_t right = 0, checksum = 0;
    for (int64_t round = 0; round < 200; round++)
        for (int64_t i = 0; i < n; i++)
            if (detect_capital_use(words[i], lens[i])) {
                right++;
                checksum = (checksum + (round + 1) * (i + 1)) % 1000000007;
            }
    printf("20000 words, 200 rounds: %lld right, checksum %lld\n", (long long)right, (long long)checksum);
    for (int64_t i = 0; i < n; i++) free(words[i]);
    free(words);
    free(lens);
    return 0;
}
