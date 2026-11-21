// LeetCode #2414: Length of the Longest Alphabetical Continuous Substring
// -- the bench, the ★ arm in C: one scan, the run growing while each
// letter follows the one before, the longest run kept.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN 100000

static int64_t longest_continuous_substring(const unsigned char *b, int64_t n) {
    int64_t run = 1, best = 1;
    for (int64_t i = 1; i < n; i++) {
        if (b[i] == b[i - 1] + 1) {
            run++;
            if (run > best) best = run;
        } else {
            run = 1;
        }
    }
    return best;
}

static int64_t seed = 2414;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    unsigned char *strings[10];
    for (int64_t i = 0; i < 10; i++) {
        unsigned char *b = malloc(LEN);
        for (int64_t j = 0; j < LEN; j++) {
            if (j > 0 && b[j - 1] < 'z' && next_random() % (i + 2) != 0)
                b[j] = b[j - 1] + 1;
            else
                b[j] = 'a' + next_random() % 26;
        }
        strings[i] = b;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 200; p++)
        for (int i = 0; i < 10; i++) check = (check * 31 + longest_continuous_substring(strings[i], LEN) + p) % 1000000007;
    printf("200 passes over 10 strings of 10^5 letters: checksum %lld\n", (long long)check);
    for (int i = 0; i < 10; i++) free(strings[i]);
    return 0;
}
