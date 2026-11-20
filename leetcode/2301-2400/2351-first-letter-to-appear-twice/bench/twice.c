// LeetCode #2351: First Letter to Appear Twice -- the bench, the ★ arm in
// C: a table of 26 marks, one per letter, the first letter already marked
// is the answer.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char repeated_character(const char *s) {
    bool seen[26];
    memset(seen, 0, sizeof seen);
    for (; *s; s++) {
        int i = *s - 'a';
        if (seen[i]) {
            return *s;
        }
        seen[i] = true;
    }
    return ' ';
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // string t is the first 2 to 26 letters of the alphabet shuffled, then
    // one of them again
    int64_t seed = 2351;
    char (*strings)[28] = malloc(100000 * sizeof *strings);
    for (int t = 0; t < 100000; t++) {
        int64_t k = 2 + next_random(&seed) % 25;
        char *letters = strings[t];
        for (int64_t i = 0; i < k; i++) {
            letters[i] = (char)(97 + i);
        }
        for (int64_t i = k - 1; i >= 1; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            char x = letters[i];
            letters[i] = letters[j];
            letters[j] = x;
        }
        letters[k] = letters[next_random(&seed) % k];
        letters[k + 1] = 0;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int t = 0; t < 100000; t++) {
            check = (check * 31 + repeated_character(strings[t]) + p) % 1000000007;
        }
    }
    printf("50 passes over 10^5 strings: checksum %lld\n", (long long)check);
    free(strings);
    return 0;
}
