// LeetCode #1653: Minimum Deletions to Make String Balanced -- the bench's
// C mirror: the ★ arm on 500 random strings of 100000 a's and b's, each
// with its own chance of a b, all drawn first.

#include <stdint.h>
#include <stdio.h>

#define STRINGS 500
#define LENGTH 100000

static int64_t minimum_deletions(const char *s, size_t n) {
    int64_t deletions = 0, bs = 0;
    for (size_t i = 0; i < n; i++) {
        if (s[i] == 'b') {
            bs += 1;
        } else {
            deletions = deletions + 1 < bs ? deletions + 1 : bs;
        }
    }
    return deletions;
}

static int64_t seed = 1653;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char strings[STRINGS][LENGTH];
    for (int k = 0; k < STRINGS; k++) {
        int64_t percent = next_random() % 101;
        for (int i = 0; i < LENGTH; i++) strings[k][i] = next_random() % 100 < percent ? 'b' : 'a';
    }
    int64_t check = 0, total = 0;
    for (int k = 0; k < STRINGS; k++) {
        int64_t deletions = minimum_deletions(strings[k], LENGTH);
        total += deletions;
        check = (check * 31 + deletions + 1) % 1000000007;
    }
    printf("500 strings of 100000 letters: deletions sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
