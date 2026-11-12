// LeetCode #1128: Number of Equivalent Domino Pairs -- the bench in C, the
// ★ arm over LeetCode's `int **dominoes` with an array of 100 counts, the
// same 16 sets and 300 rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t num_equiv_domino_pairs(int **dominoes, int n) {
    int64_t count[100] = {0};
    int64_t pairs = 0;
    for (int i = 0; i < n; i++) {
        int a = dominoes[i][0], b = dominoes[i][1];
        int key = (a < b ? a : b) * 10 + (a < b ? b : a);
        pairs += count[key];
        count[key]++;
    }
    return pairs;
}

static int64_t seed = 1128;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { SETS = 16, N = 40000 };
    int **sets[SETS];
    for (int s = 0; s < SETS; s++) {
        sets[s] = malloc(N * sizeof(int *));
        for (int i = 0; i < N; i++) {
            int64_t a = next_random() % 9 + 1;
            int64_t b = next_random() % 9 + 1;
            sets[s][i] = malloc(2 * sizeof(int));
            sets[s][i][0] = (int)a;
            sets[s][i][1] = (int)b;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 300; round++) {
        for (int64_t j = 0; j < SETS; j++) {
            int64_t at = (round * 7919 + j * 104729) % N;
            int side = (int)(round % 2);
            sets[j][at][side] = sets[j][at][side] % 9 + 1;
            int64_t answer = num_equiv_domino_pairs(sets[j], N);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    printf("300 rounds over 16 sets of 4 * 10^4 dominoes: pairs total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int s = 0; s < SETS; s++) {
        for (int i = 0; i < N; i++) free(sets[s][i]);
        free(sets[s]);
    }
    return 0;
}
