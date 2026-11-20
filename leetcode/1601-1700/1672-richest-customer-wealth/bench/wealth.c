// LeetCode #1672: Richest Customer Wealth -- the bench's C mirror: the ★ arm
// on 4000 grids of 50 customers by 50 banks, up to 100 in each account,
// all drawn first, each answered 100 times.

#include <stdint.h>
#include <stdio.h>

#define GRIDS 4000
#define SIDE 50
#define ROUNDS 100

static int32_t maximum_wealth(int32_t accounts[SIDE][SIDE], int m, int n) {
    int32_t richest = 0;
    for (int i = 0; i < m; i++) {
        int32_t wealth = 0;
        for (int j = 0; j < n; j++) wealth += accounts[i][j];
        if (i == 0 || wealth > richest) richest = wealth;
    }
    return richest;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1672;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t all[GRIDS][SIDE][SIDE];
    for (int g = 0; g < GRIDS; g++)
        for (int i = 0; i < SIDE; i++)
            for (int j = 0; j < SIDE; j++) all[g][i][j] = (int32_t)(next_random() % 100 + 1);
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int g = 0; g < GRIDS; g++) {
            int64_t richest = maximum_wealth(all[g], SIDE, SIDE);
            total += richest;
            check = (check * 31 + richest + r) % 1000000007;
        }
    }
    printf("%d grids of %d by %d, %d rounds: answers sum to %lld, checksum %lld\n", GRIDS, SIDE, SIDE, ROUNDS, (long long)total, (long long)check);
    return 0;
}
