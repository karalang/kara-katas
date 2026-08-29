/* Benchmark mirror of bullscore.kara — LeetCode #299, Bulls and Cows.
 * Same algorithm: build boards once, then 12 scoring passes over a flat digit
 * array. See ../README.md § Benchmarks. */
#include <stdio.h>
#include <stdlib.h>

#define N_PAIRS  400000
#define PASSES   12
#define WIDTH    4
#define ALPHABET 4

static long lcg(long state) {
    return (state * 1103515245 + 12345) & 0x7fffffff;
}

int main(void) {
    long total = (long)N_PAIRS * WIDTH;
    long *secrets = malloc(sizeof(long) * total);
    long *guesses = malloc(sizeof(long) * total);
    if (!secrets || !guesses) return 1;

    long state = 20299;
    for (long i = 0; i < total; i++) {
        state = lcg(state);
        secrets[i] = (state / 65536) % ALPHABET;
        state = lcg(state);
        guesses[i] = (state / 65536) % ALPHABET;
    }

    long checksum = 0;
    for (int pass = 0; pass < PASSES; pass++) {
        for (long p = 0; p < N_PAIRS; p++) {
            long base = p * WIDTH;
            long s_left[ALPHABET] = {0};
            long g_left[ALPHABET] = {0};
            long bulls = 0, cows = 0;

            for (int k = 0; k < WIDTH; k++) {
                long sd = secrets[base + k], gd = guesses[base + k];
                if (sd == gd) {
                    bulls++;
                } else {
                    s_left[sd]++;
                    g_left[gd]++;
                }
            }
            for (int d = 0; d < ALPHABET; d++)
                cows += s_left[d] < g_left[d] ? s_left[d] : g_left[d];

            checksum = (checksum * 31 + bulls * 7 + cows) % 1000000007;
        }
    }

    printf("pairs %d passes %d checksum %ld\n", N_PAIRS, PASSES, checksum);
    free(secrets);
    free(guesses);
    return 0;
}
