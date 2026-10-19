// LeetCode 789 — Escape The Ghosts: the bench, in C.
// Mirrors escape_ghosts.kara: every ghost's distance to the target
// against yours, stopping at the first that is no farther.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t iabs(int64_t v) { return v < 0 ? -v : v; }

static int escape_ghosts(const int64_t (*ghosts)[2], int64_t count, const int64_t target[2]) {
    int64_t mine = iabs(target[0]) + iabs(target[1]);
    for (int64_t i = 0; i < count; i++) {
        if (iabs(ghosts[i][0] - target[0]) + iabs(ghosts[i][1] - target[1]) <= mine) return 0;
    }
    return 1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 789;
    static int64_t boards[64][100][2];
    for (int b = 0; b < 64; b++) {
        for (int i = 0; i < 100; i++) {
            boards[b][i][0] = next_random(&seed) % 20001 - 10000;
            boards[b][i][1] = next_random(&seed) % 20001 - 10000;
        }
    }
    int64_t rounds = 10000000, escapes = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t target[2];
        target[0] = next_random(&seed) % 2001 - 1000;
        target[1] = next_random(&seed) % 2001 - 1000;
        if (escape_ghosts((const int64_t (*)[2])boards[r % 64], 100, target)) {
            escapes++;
            check = (check * 31 + r % 1000) % 1000000007;
        }
    }
    printf("%lld rounds of 100-ghost boards: %lld escapes, checksum %lld\n", (long long)rounds, (long long)escapes,
           (long long)check);
    return 0;
}
