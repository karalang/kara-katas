// LeetCode #2379: Minimum Recolors to Get K Consecutive Black Blocks --
// the bench, the ★ arm in C: the whites of the first window counted, then
// the window slid along one block at a time.

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int64_t minimum_recolors(const char *b, int64_t k) {
    int64_t n = (int64_t)strlen(b);
    int64_t whites = 0;
    for (int64_t i = 0; i < k; i++) {
        if (b[i] == 'W') {
            whites++;
        }
    }
    int64_t fewest = whites;
    for (int64_t i = k; i < n; i++) {
        if (b[i] == 'W') {
            whites++;
        }
        if (b[i - k] == 'W') {
            whites--;
        }
        if (whites < fewest) {
            fewest = whites;
        }
    }
    return fewest;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char strings[1000][101];

int main(void) {
    // 1000 strings of 100 blocks, string s white with a chance of s % 10
    // in 10; pass p asks string s for k = 1 + (7 p + s) % 100
    int64_t seed = 2379;
    for (int64_t s = 0; s < 1000; s++) {
        for (int i = 0; i < 100; i++) {
            strings[s][i] = next_random(&seed) % 10 < s % 10 ? 'W' : 'B';
        }
        strings[s][100] = 0;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int64_t s = 0; s < 1000; s++) {
            int64_t k = 1 + (7 * p + s) % 100;
            check = (check * 31 + minimum_recolors(strings[s], k) + p) % 1000000007;
        }
    }
    printf("500 passes over 1000 strings of 100 blocks: checksum %lld\n", (long long)check);
    return 0;
}
