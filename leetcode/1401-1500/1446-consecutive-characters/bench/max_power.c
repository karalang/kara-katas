// LeetCode #1446 Consecutive Characters: the bench, a mirror of
// max_power.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int max_power(const char *s, int n) {
    // the length of the run the letter so far ends, and the longest run
    int best = 0;
    int run = 0;
    char last = ' ';
    for (int i = 0; i < n; i++) {
        char ch = s[i];
        if (ch == last) {
            run += 1;
        } else {
            run = 1;
            last = ch;
        }
        if (run > best) best = run;
    }
    return best;
}

int main(void) {
    // 200 strings of 10^5 letters, each drawn from the first 2 to 4 of the
    // alphabet, each string's power asked 10 times, the powers folded to a
    // checksum
    enum { COUNT = 200, LEN = 100000 };
    int64_t seed = 1446;
    char **strings = malloc(COUNT * sizeof *strings);
    for (int j = 0; j < COUNT; j++) {
        int64_t k = 2 + j % 3;
        strings[j] = malloc(LEN);
        for (int i = 0; i < LEN; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            strings[j][i] = (char)('a' + seed / 65536 % k);
        }
    }
    int64_t check = 0;
    for (int r = 0; r < 10; r++) {
        for (int j = 0; j < COUNT; j++) {
            check = (check * 131 + max_power(strings[j], LEN)) % 1000000007;
        }
    }
    printf("2000 strings of 10^5 letters: checksum %lld\n", (long long)check);
    for (int j = 0; j < COUNT; j++) free(strings[j]);
    free(strings);
    return 0;
}
