// LeetCode #2267: Check if There Is a Valid Parentheses String Path -- C
// mirror of the ★ arm (path.kara): a table reach[i][j][b] of the balances
// some path to (i, j) can end with, one calloc'd block per call. Output
// is byte-identical to path.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool has_valid_path(char grid[100][99], int m, int n) {
    if ((m + n - 1) % 2 == 1 || grid[0][0] == ')' || grid[m - 1][n - 1] == '(') return false;
    int most = (m + n) / 2 + 1;
    int w = most + 1;
    bool *reach = calloc((size_t)m * n * w, sizeof(bool));
#define R(i, j, b) reach[((size_t)(i) * n + (j)) * w + (b)]
    R(0, 0, 1) = true;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (i == 0 && j == 0) continue;
            int step = grid[i][j] == '(' ? 1 : -1;
            for (int b = 0; b <= most; b++) {
                int from = b - step;
                if (from < 0 || from > most) continue;
                if ((i > 0 && R(i - 1, j, from)) || (j > 0 && R(i, j - 1, from))) R(i, j, b) = true;
            }
        }
    }
    bool answer = R(m - 1, n - 1, 0);
#undef R
    free(reach);
    return answer;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2267;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char grid[100][99];
    int found = 0;
    int64_t check = 0;
    for (int t = 0; t < 20; t++) {
        int open = 50 + t;
        for (int i = 0; i < 100; i++)
            for (int j = 0; j < 99; j++) grid[i][j] = next_random() % 100 < open ? '(' : ')';
        grid[0][0] = '(';
        grid[99][98] = ')';
        bool valid = has_valid_path(grid, 100, 99);
        if (valid) found++;
        check = (check * 31 + (valid ? 2 : 1)) % 1000000007;
    }
    printf("20 grids of 100 by 99: %d with a path, checksum %lld\n", found, (long long)check);
    return 0;
}
