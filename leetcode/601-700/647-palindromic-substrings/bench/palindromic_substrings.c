// LeetCode #647: Palindromic Substrings -- C mirror of the Kāra bench.
//
// The ★ arm over the same texts and rounds: from each of the 2n - 1
// centers, the window widened while its two ends match, over a char
// array.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_substrings(const char *s, int64_t n) {
    int64_t count = 0;
    for (int64_t center = 0; center < 2 * n - 1; center++) {
        int64_t lo = center / 2;
        int64_t hi = lo + center % 2;
        while (lo >= 0 && hi < n && s[lo] == s[hi]) {
            count++;
            lo--;
            hi++;
        }
    }
    return count;
}

static int64_t seed = 647;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { INPUTS = 20, ROUNDS = 300, LENGTH = 2000 };
    char *texts[INPUTS];
    for (int i = 0; i < INPUTS; i++) {
        int64_t letters = 1 + next_random() % 3;
        texts[i] = malloc(LENGTH);
        for (int j = 0; j < LENGTH; j++) {
            texts[i][j] = (char)(97 + next_random() % letters);
        }
    }
    int64_t sum = 0, checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t c = count_substrings(texts[(r * 7) % INPUTS], LENGTH);
        sum += c;
        checksum = (checksum * 31 + c) % 1000000007;
    }
    printf("%d inputs, %d rounds: total %lld, checksum %lld\n", INPUTS, ROUNDS, (long long)sum, (long long)checksum);
    for (int i = 0; i < INPUTS; i++) free(texts[i]);
    return 0;
}
