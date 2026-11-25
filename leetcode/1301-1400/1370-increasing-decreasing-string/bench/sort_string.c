// LeetCode #1370 bench -- C: the letters counted, then sweeps up from a to
// z and down from z to a, each taking one of every letter still left,
// until none is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LEN 500

static char *sort_string(const char *s) {
    int64_t counts[26] = {0};
    size_t n = strlen(s);
    for (size_t k = 0; k < n; k++) counts[s[k] - 'a'] += 1;
    char *out = malloc(n + 1);
    size_t len = 0;
    int64_t left = (int64_t)n;
    while (left > 0) {
        for (int i = 0; i < 26; i++) {
            if (counts[i] > 0) {
                out[len++] = (char)('a' + i);
                counts[i] -= 1;
                left -= 1;
            }
        }
        for (int i = 25; i >= 0; i--) {
            if (counts[i] > 0) {
                out[len++] = (char)('a' + i);
                counts[i] -= 1;
                left -= 1;
            }
        }
    }
    out[len] = '\0';
    return out;
}

static int64_t seed = 1370;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char strings[20][LEN + 1];

int main(void) {
    // 20 strings of 500 letters, the constraints' most, each from the
    // first 2 to 26 letters of the alphabet, built once; then 60000
    // rounds, each changing one letter of one string and sorting that
    // string, all drawn from the checksum so far
    for (int64_t k = 0; k < 20; k++) {
        int64_t letters = 2 + k * 24 / 19;
        for (int j = 0; j < LEN; j++) strings[k][j] = (char)('a' + next_random() % letters);
        strings[k][LEN] = '\0';
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 60000; r++) {
        int64_t i = check % 20;
        int64_t at = (check / 20) % LEN;
        strings[i][at] = (char)('a' + (check / 10000) % 26);
        char *sorted = sort_string(strings[i]);
        for (size_t k = 0; sorted[k]; k++) check = (check * 31 + (unsigned char)sorted[k]) % 1000000007;
        free(sorted);
        check = (check + r) % 1000000007;
    }
    printf("60000 rounds over 20 strings of 500 letters: checksum %lld\n", (long long)check);
    return 0;
}
