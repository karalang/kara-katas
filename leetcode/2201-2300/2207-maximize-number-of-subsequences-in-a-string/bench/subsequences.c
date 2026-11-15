// benchmark's C mirror of subsequences.kara (LeetCode #2207, the ★ arm):
// one pass counting the first letter so far, each second letter adding
// that count, then the more common letter added. The text is a byte
// string, its letters all ASCII.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t maximum_subsequence_count(const char *text, int64_t n, const char *pattern) {
    char first = pattern[0], second = pattern[1];
    int64_t firsts = 0, seconds = 0, pairs = 0;
    for (int64_t i = 0; i < n; i++) {
        char ch = text[i];
        if (ch == second) {
            pairs += firsts;
            seconds++;
        }
        if (ch == first) firsts++;
    }
    return pairs + (firsts > seconds ? firsts : seconds);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2207;
    static const int64_t sizes[3] = {2, 3, 26};
    char *texts[12];
    for (int t = 0; t < 12; t++) {
        texts[t] = malloc(100000);
        for (int i = 0; i < 100000; i++) texts[t][i] = (char)(97 + next_random(&seed) % sizes[t % 3]);
    }
    // each pass asks every text about its own pattern
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int64_t t = 0; t < 12; t++) {
            int64_t letters = sizes[t % 3];
            char pattern[2] = {(char)(97 + p % letters), (char)(97 + (p * 7 + t) % letters)};
            check = (check * 31 + maximum_subsequence_count(texts[t], 100000, pattern)) % 1000000007;
        }
    }
    printf("50 passes over 12 texts: checksum %lld\n", (long long)check);
    for (int t = 0; t < 12; t++) free(texts[t]);
    return 0;
}
