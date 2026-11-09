// LeetCode #2038: Remove Colored Pieces if Both Neighbors are the Same
// Color -- the ★ arm in C, the same algorithm and workload as colors.kara:
// each row written out as a fresh string, its pieces copied into a char
// array, each player's moves counted, Alice winning with more.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int winner_of_game(const char *colors) {
    size_t n = strlen(colors);
    char *c = malloc(n);
    memcpy(c, colors, n);
    int64_t alice = 0, bob = 0;
    for (size_t i = 1; i + 1 < n; i++) {
        if (c[i - 1] == c[i] && c[i] == c[i + 1]) {
            if (c[i] == 'A') alice++;
            else bob++;
        }
    }
    free(c);
    return alice > bob;
}

static int64_t seed = 2038;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { N = 100000 };
    static char rows[4][N];
    const int64_t stays[4] = {2, 3, 50, 1000};
    for (int r = 0; r < 4; r++) {
        char c = next_random() % 2 == 0 ? 'A' : 'B';
        for (int i = 0; i < N; i++) {
            if (next_random() % stays[r] == 0) c = c == 'A' ? 'B' : 'A';
            rows[r][i] = c;
        }
    }
    int64_t calls = 0, wins = 0, check = 0;
    char *colors = malloc(N + 1);
    for (int64_t round = 0; round < 100; round++) {
        for (int64_t r = 0; r < 4; r++) {
            int64_t at = (round * 7919 + r * 104729) % N;
            rows[r][at] = rows[r][at] == 'A' ? 'B' : 'A';
            memcpy(colors, rows[r], N);
            colors[N] = 0;
            int64_t bit = winner_of_game(colors);
            calls++;
            wins += bit;
            check = (check * 3 + bit + 1) % 1000000007;
        }
    }
    free(colors);
    printf("%lld calls: Alice wins %lld, checksum %lld\n", (long long)calls, (long long)wins, (long long)check);
    return 0;
}
