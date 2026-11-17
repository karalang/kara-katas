// LeetCode #2218: Maximum Value of K Coins From Piles -- bench mirror of
// coins.kara: a knapsack over the piles, best[j] the most j coins are
// worth so far, each pile tried at every count of its top coins with j
// running down.
#include <stdio.h>
#include <stdlib.h>

#define S 20
#define P 100
#define L 10

static long max_value_of_coins(long piles[P][L], long k) {
    long *best = calloc(k + 1, sizeof(long));
    for (int i = 0; i < P; i++) {
        long prefix[L + 1];
        prefix[0] = 0;
        for (int t = 0; t < L; t++) prefix[t + 1] = prefix[t] + piles[i][t];
        for (long j = k; j >= 1; j--) {
            long most = j < L ? j : L;
            for (long t = 1; t <= most; t++) {
                long v = best[j - t] + prefix[t];
                if (v > best[j]) best[j] = v;
            }
        }
    }
    long answer = best[k];
    free(best);
    return answer;
}

static long seed = 2218;
static long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// a draw of 30 bits, since one draw stops at 32767
static long wide_random(void) {
    long high = next_random();
    return high * 32768 + next_random();
}

static long chests[S][P][L];

int main(void) {
    // 100 piles of 10 coins worth up to 10^5
    for (int a = 0; a < S; a++)
        for (int i = 0; i < P; i++)
            for (int t = 0; t < L; t++) chests[a][i][t] = wide_random() % 100000 + 1;
    long check = 0;
    for (int a = 0; a < S; a++)
        for (int r = 0; r < 4; r++) {
            // punch: one coin is drawn again before each answer
            chests[a][r * 31 % 100][r] = wide_random() % 100000 + 1;
            check = (check * 31 + max_value_of_coins(chests[a], 600)) % 1000000007;
        }
    printf("20 sets of 100 piles of 10, k = 600, 4 punches: checksum %ld\n", check);
    return 0;
}
