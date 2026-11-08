// LeetCode #1510: Stone Game IV -- the bench: 40 piles of 50000 to 100000
// stones, each answered by the ★ arm.
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

static bool winner_square_game(long n) {
    bool *wins = calloc(n + 1, sizeof(bool));
    for (long pile = 1; pile <= n; pile++) {
        for (long k = 1; k * k <= pile; k++) {
            if (!wins[pile - k * k]) {
                wins[pile] = true;
                break;
            }
        }
    }
    bool w = wins[n];
    free(wins);
    return w;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    long seed = 1510, wins = 0, check = 0;
    for (int i = 0; i < 40; i++) {
        long hi = next_random(&seed) * 32768;
        long n = 50000 + (hi + next_random(&seed)) % 50001;
        bool w = winner_square_game(n);
        if (w) wins++;
        check = (check * 31 + (w ? n : 0) + 1) % 1000000007;
    }
    printf("40 piles of 50000 to 100000 stones: Alice wins %ld, checksum %ld\n", wins, check);
    return 0;
}
