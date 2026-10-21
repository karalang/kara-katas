// Benchmark for #840: Magic Squares In Grid -- the ★ arm (the centre first).
//
// Mirrors magic_squares_in_grid.kara: each 3 by 3 window is looked at
// only if its centre is 5; then its nine numbers must be 1 to 9, each
// once, kept as bits of a mask, its rows and columns must add up to 15,
// and each diagonal's two corners to 10.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

enum { COUNT = 64, N = 10 };

static bool is_magic(int64_t grid[N][N], int64_t r, int64_t c) {
    if (grid[r + 1][c + 1] != 5) return false;
    int64_t mask = 0;
    for (int64_t i = r; i < r + 3; i++) {
        for (int64_t j = c; j < c + 3; j++) {
            int64_t v = grid[i][j];
            if (v < 1 || v > 9) return false;
            mask |= (int64_t)1 << v;
        }
    }
    if (mask != 1022) return false;
    for (int64_t k = 0; k < 3; k++) {
        if (grid[r + k][c] + grid[r + k][c + 1] + grid[r + k][c + 2] != 15) return false;
        if (grid[r][c + k] + grid[r + 1][c + k] + grid[r + 2][c + k] != 15) return false;
    }
    return grid[r][c] + grid[r + 2][c + 2] == 10 && grid[r][c + 2] + grid[r + 2][c] == 10;
}

static int64_t num_magic_squares_inside(int64_t grid[N][N], int64_t rows, int64_t cols) {
    int64_t count = 0;
    for (int64_t r = 0; r < rows - 2; r++)
        for (int64_t c = 0; c < cols - 2; c++)
            if (is_magic(grid, r, c)) count += 1;
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 64 grids drawn once, each LeetCode's largest, 10 by 10, of numbers
    // 0 to 15 with 12 squares of 3 by 3 stamped on it: the Lo Shu turned
    // or mirrored, a square of 5s, or the Lo Shu with 1 added to every
    // number. Each round changes one cell of the next grid and counts its
    // magic squares.
    const int64_t rounds = 14000000;
    static const int64_t lo_shu[3][3] = {{4, 9, 2}, {3, 5, 7}, {8, 1, 6}};
    int64_t seed = 840;
    static int64_t grids[COUNT][N][N];
    for (int64_t g = 0; g < COUNT; g++) {
        for (int64_t i = 0; i < N; i++)
            for (int64_t j = 0; j < N; j++) grids[g][i][j] = next_random(&seed) % 16;
        for (int64_t p = 0; p < 12; p++) {
            int64_t turn = next_random(&seed) % 8;
            int64_t kind = next_random(&seed) % 3;
            int64_t r = next_random(&seed) % 8;
            int64_t c = next_random(&seed) % 8;
            for (int64_t i = 0; i < 3; i++) {
                for (int64_t j = 0; j < 3; j++) {
                    int64_t a = i, b = turn >= 4 ? 2 - j : j;
                    for (int64_t t = 0; t < turn % 4; t++) {
                        int64_t s = a;
                        a = 2 - b;
                        b = s;
                    }
                    grids[g][r + i][c + j] = kind == 1 ? 5 : lo_shu[a][b] + kind / 2;
                }
            }
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % COUNT;
        int64_t cell = round * 7 % 100;
        grids[g][cell / 10][cell % 10] = round % 16;
        int64_t magic = num_magic_squares_inside(grids[g], N, N);
        total += magic;
        checksum = (checksum * 31 + magic + round) % 1000000007;
    }
    printf("%lld rounds of %d grids: %lld magic squares, checksum %lld\n", (long long)rounds, COUNT, (long long)total,
           (long long)checksum);
    return 0;
}
