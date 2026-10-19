// LeetCode 764 — Largest Plus Sign: benchmark, the ★ arm in C.
// 300 random grids of 500 x 500 with 5,000 mines each.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 500

static int64_t order_of_largest_plus_sign(int n, int (*mines)[2], int count) {
    static int64_t grid[N][N];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) grid[i][j] = n;
    for (int m = 0; m < count; m++) grid[mines[m][0]][mines[m][1]] = 0;
    for (int i = 0; i < n; i++) {
        int64_t left = 0, right = 0, up = 0, down = 0;
        for (int j = 0; j < n; j++) {
            left = grid[i][j] == 0 ? 0 : left + 1;
            if (left < grid[i][j]) grid[i][j] = left;
            int k = n - 1 - j;
            right = grid[i][k] == 0 ? 0 : right + 1;
            if (right < grid[i][k]) grid[i][k] = right;
            up = grid[j][i] == 0 ? 0 : up + 1;
            if (up < grid[j][i]) grid[j][i] = up;
            down = grid[k][i] == 0 ? 0 : down + 1;
            if (down < grid[k][i]) grid[k][i] = down;
        }
    }
    int64_t best = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (grid[i][j] > best) best = grid[i][j];
    return best;
}

static int64_t seed = 764;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 300, n = N;
    int64_t total = 0, check = 0;
    static char taken[N * N];
    static int mines[5000][2];
    for (int round = 0; round < rounds; round++) {
        memset(taken, 0, sizeof taken);
        int count = 0;
        while (count < 5000) {
            int r = (int)(next_random() % n);
            int c = (int)(next_random() % n);
            if (!taken[r * n + c]) {
                taken[r * n + c] = 1;
                mines[count][0] = r;
                mines[count][1] = c;
                count++;
            }
        }
        int64_t order = order_of_largest_plus_sign(n, mines, count);
        total += order;
        check = (check * 31 + order) % 1000000007;
    }
    printf("%d grids of 500 x 500 with 5000 mines: orders adding up to %lld, checksum %lld\n", rounds, (long long)total, (long long)check);
    return 0;
}
