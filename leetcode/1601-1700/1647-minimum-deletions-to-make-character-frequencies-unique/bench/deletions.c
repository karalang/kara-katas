// LeetCode #1647: Minimum Deletions to Make Character Frequencies Unique
// -- the bench's C mirror: the ★ arm on 500 random strings of 100000
// letters, each from the first 1 to 26 of the alphabet, all drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define STRINGS 500
#define LENGTH 100000

static int descending(const void *a, const void *b) {
    int32_t x = *(const int32_t *)a, y = *(const int32_t *)b;
    return (x < y) - (x > y);
}

static int32_t min_deletions(const char *s, size_t n) {
    int32_t counts[26] = {0};
    for (size_t i = 0; i < n; i++) counts[s[i] - 'a'] += 1;
    qsort(counts, 26, sizeof counts[0], descending);
    int32_t deletions = 0;
    int32_t cap = counts[0];
    for (int i = 0; i < 26; i++) {
        int32_t keep = counts[i] < cap ? counts[i] : cap;
        deletions += counts[i] - keep;
        cap = keep - 1 > 0 ? keep - 1 : 0;
    }
    return deletions;
}

static int64_t seed = 1647;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char strings[STRINGS][LENGTH];
    for (int k = 0; k < STRINGS; k++) {
        int64_t letters = next_random() % 26 + 1;
        for (int i = 0; i < LENGTH; i++) strings[k][i] = (char)('a' + next_random() % letters);
    }
    int64_t check = 0, total = 0;
    for (int k = 0; k < STRINGS; k++) {
        int64_t deletions = min_deletions(strings[k], LENGTH);
        total += deletions;
        check = (check * 31 + deletions + 1) % 1000000007;
    }
    printf("500 strings of 100000 letters: deletions sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
