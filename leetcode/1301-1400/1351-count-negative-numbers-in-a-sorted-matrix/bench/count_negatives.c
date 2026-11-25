// LeetCode #1351 bench -- C: a staircase walk from the bottom-left corner.
#include <stdio.h>

static int grids[50][100][100];

static int count_negatives(int grid[100][100], int m, int n) {
    int row = m - 1, col = 0, count = 0;
    while (row >= 0 && col < n) {
        if (grid[row][col] < 0) {
            count += n - col;
            row--;
        } else {
            col++;
        }
    }
    return count;
}

int main(void) {
    long long seed = 1351;
    for (int k = 0; k < 50; k++)
        for (int i = 0; i < 100; i++)
            for (int j = 0; j < 100; j++) {
                int v = 60;
                if (i > 0 && grids[k][i - 1][j] < v) v = grids[k][i - 1][j];
                if (j > 0 && grids[k][i][j - 1] < v) v = grids[k][i][j - 1];
                if (i + j > 0) {
                    seed = (seed * 1103515245 + 12345) % 2147483648LL;
                    v -= (int)((seed / 65536) % 2);
                }
                grids[k][i][j] = v < -100 ? -100 : v;
            }
    long long check = 0;
    for (long long r = 0; r < 300000; r++) {
        int k = check % 50, i = (check / 50) % 100, j = (check / 5000) % 100;
        int v;
        if (check % 2 == 0) {
            v = 100;
            if (i > 0 && grids[k][i - 1][j] < v) v = grids[k][i - 1][j];
            if (j > 0 && grids[k][i][j - 1] < v) v = grids[k][i][j - 1];
        } else {
            v = -100;
            if (i < 99 && grids[k][i + 1][j] > v) v = grids[k][i + 1][j];
            if (j < 99 && grids[k][i][j + 1] > v) v = grids[k][i][j + 1];
        }
        grids[k][i][j] = v;
        check = (check * 31 + count_negatives(grids[k], 100, 100) + r) % 1000000007;
    }
    printf("300000 rounds over 50 grids of 100 by 100: checksum %lld\n", check);
    return 0;
}
