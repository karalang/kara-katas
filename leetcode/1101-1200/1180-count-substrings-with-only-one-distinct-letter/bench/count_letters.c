// LeetCode #1180: Count Substrings with Only One Distinct Letter -- the ★
// arm's bench in C: one pass, the run of equal letters ending at each
// position added at every step. The same strings and the same 100 rounds.
#include <stdio.h>
#include <stdlib.h>

static long count_letters(const char *s) {
    long total = 0, run = 0;
    char last = 0;
    for (; *s; s++) {
        if (*s == last) {
            run += 1;
        } else {
            run = 1;
            last = *s;
        }
        total += run;
    }
    return total;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long seed = 1180;
    char **strings = malloc(sizeof(char *) * 1000);
    for (int i = 0; i < 1000; i++) {
        long m = 1 + next_random(&seed) % 4;
        strings[i] = malloc(1001);
        for (int j = 0; j < 1000; j++) {
            strings[i][j] = (char)('a' + next_random(&seed) % m);
        }
        strings[i][1000] = 0;
    }
    long rounds = 100;
    long check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int i = 0; i < 1000; i++) {
            check = (check * 131 + count_letters(strings[i])) % 1000000007;
        }
    }
    printf("%ld rounds of 1000 strings: checksum %ld\n", rounds, check);
    return 0;
}
