// LeetCode #1221 bench, C mirror of the Kāra ★ arm: walk the string keeping
// L's count less R's and count the returns to zero, over 2000 random
// balanced strings of 1000 letters drawn once, 20 passes; checksum of the
// answers.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t seed = 1221;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t balanced_string_split(const char *s) {
    int64_t balance = 0, pieces = 0;
    for (; *s; s++) {
        if (*s == 'L') {
            balance += 1;
        } else {
            balance -= 1;
        }
        if (balance == 0) {
            pieces += 1;
        }
    }
    return pieces;
}

int main(void) {
    char *strings[2000];
    for (int i = 0; i < 2000; i++) {
        char *letters = malloc(1001);
        for (int k = 0; k < 500; k++) {
            letters[2 * k] = 'L';
            letters[2 * k + 1] = 'R';
        }
        letters[1000] = 0;
        for (int64_t k = 999; k > 0; k--) {
            int64_t j = next_random() % (k + 1);
            char t = letters[k];
            letters[k] = letters[j];
            letters[j] = t;
        }
        strings[i] = letters;
    }
    int64_t total = 0, check = 0;
    for (int pass = 0; pass < 20; pass++) {
        for (int i = 0; i < 2000; i++) {
            int64_t answer = balanced_string_split(strings[i]);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    printf("2000 strings of 1000 letters, 20 passes: pieces total %lld, checksum %lld\n", (long long)total, (long long)check);
    for (int i = 0; i < 2000; i++) {
        free(strings[i]);
    }
    return 0;
}
