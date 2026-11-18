// LeetCode #1624: Largest Substring Between Two Equal Characters -- the
// bench in C, mirroring gap.kara: one pass, the first index of each
// letter, and at every later sight the gap back to it. The strings are
// ASCII, so a byte is a character.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int32_t max_length_between_equal_characters(const char *s, int64_t n) {
    int64_t first[26];
    for (int k = 0; k < 26; k++) first[k] = -1;
    int64_t best = -1;
    for (int64_t i = 0; i < n; i++) {
        int letter = s[i] - 'a';
        if (first[letter] == -1) {
            first[letter] = i;
        } else if (i - first[letter] - 1 > best) {
            best = i - first[letter] - 1;
        }
    }
    return (int32_t)best;
}

static int64_t seed = 1624;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 100000 };
    char **strings = malloc(sizeof(char *) * COUNT);
    int64_t *lengths = malloc(sizeof(int64_t) * COUNT);
    for (int k = 0; k < COUNT; k++) {
        int64_t n = next_random() % 300 + 1;
        char *s = malloc((size_t)n + 1);
        for (int64_t i = 0; i < n; i++) s[i] = (char)('a' + next_random() % 26);
        s[n] = '\0';
        strings[k] = s;
        lengths[k] = n;
    }
    int64_t check = 0, total = 0;
    for (int k = 0; k < COUNT; k++) {
        int64_t got = max_length_between_equal_characters(strings[k], lengths[k]);
        total += got;
        check = (check * 31 + got + 1) % 1000000007;
    }
    for (int k = 0; k < COUNT; k++) free(strings[k]);
    free(strings);
    free(lengths);
    printf("100000 random strings: answers sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
