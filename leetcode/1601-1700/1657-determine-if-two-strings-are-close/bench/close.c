// LeetCode #1657: Determine if Two Strings Are Close -- the bench's C
// mirror: the ★ arm on 400 random pairs of words of 100000 letters, each
// pair from the first 1 to 26 of the alphabet, half of the second words
// made close by construction, all drawn first.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PAIRS 400
#define LENGTH 100000

static int ascending(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static bool close_strings(const char *word1, const char *word2, size_t n) {
    int64_t count1[26] = {0}, count2[26] = {0};
    for (size_t i = 0; i < n; i++) count1[word1[i] - 'a'] += 1;
    for (size_t i = 0; i < n; i++) count2[word2[i] - 'a'] += 1;
    for (int i = 0; i < 26; i++)
        if ((count1[i] == 0) != (count2[i] == 0)) return false;
    qsort(count1, 26, sizeof count1[0], ascending);
    qsort(count2, 26, sizeof count2[0], ascending);
    return memcmp(count1, count2, sizeof count1) == 0;
}

static int64_t seed = 1657;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char word1[PAIRS][LENGTH], word2[PAIRS][LENGTH];
    for (int p = 0; p < PAIRS; p++) {
        int64_t alphabet = next_random() % 26 + 1;
        for (int i = 0; i < LENGTH; i++) word1[p][i] = (char)('a' + next_random() % alphabet);
        if (next_random() % 2 == 0) {
            for (int i = 0; i < LENGTH; i++) word2[p][i] = (char)('a' + next_random() % alphabet);
        } else {
            char a = (char)('a' + next_random() % alphabet);
            char b = (char)('a' + next_random() % alphabet);
            for (int i = 0; i < LENGTH; i++) {
                char c = word1[p][LENGTH - 1 - i];
                word2[p][i] = c == a ? b : c == b ? a : c;
            }
        }
    }
    int64_t check = 0, close = 0;
    for (int p = 0; p < PAIRS; p++) {
        bool answer = close_strings(word1[p], word2[p], LENGTH);
        if (answer) close += 1;
        check = (check * 31 + (answer ? 2 : 1)) % 1000000007;
    }
    printf("400 pairs of 100000 letters: %lld close, checksum %lld\n", (long long)close, (long long)check);
    return 0;
}
