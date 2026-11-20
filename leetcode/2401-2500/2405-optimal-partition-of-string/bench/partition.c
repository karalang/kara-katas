// LeetCode #2405: Optimal Partition of String -- the bench, the ★ arm in
// C: greedy with a bitmask, a letter already in the current part starting
// the next one.

#include <stdint.h>
#include <stdio.h>

#define LEN 100000

static int64_t seed = 2405;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t partition_string(const unsigned char *s, int64_t n) {
    int64_t parts = 1, seen = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t bit = (int64_t)1 << (s[i] - 'a');
        if (seen & bit) {
            parts++;
            seen = 0;
        }
        seen |= bit;
    }
    return parts;
}

int main(void) {
    static unsigned char strings[26][LEN];
    for (int i = 0; i < 26; i++)
        for (int j = 0; j < LEN; j++) strings[i][j] = (unsigned char)('a' + next_random() % (i + 1));
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++)
        for (int i = 0; i < 26; i++) check = (check * 31 + partition_string(strings[i], LEN) + p) % 1000000007;
    printf("50 passes over 26 strings of 10^5 letters: checksum %lld\n", (long long)check);
    return 0;
}
