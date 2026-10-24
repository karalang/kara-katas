// Benchmark: LeetCode #980 Unique Paths III -- the ★ arm, backtracking
// on the grid, on every start and end of an open 4 x 5 grid, LeetCode's
// largest. Mirrors unique_paths_iii.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>

#define ROWS 4
#define COLS 5

static int64_t walk(int64_t grid[ROWS][COLS], int64_t r, int64_t c, int64_t left) {
    if (r < 0 || c < 0 || r >= ROWS || c >= COLS || grid[r][c] == -1) return 0;
    if (grid[r][c] == 2) return left == 0 ? 1 : 0;
    grid[r][c] = -1;
    int64_t paths = walk(grid, r + 1, c, left - 1) + walk(grid, r - 1, c, left - 1) +
                    walk(grid, r, c + 1, left - 1) + walk(grid, r, c - 1, left - 1);
    grid[r][c] = 0;
    return paths;
}

static int64_t unique_paths_iii(int64_t grid[ROWS][COLS]) {
    int64_t g[ROWS][COLS];
    int64_t sr = 0, sc = 0, left = 0;
    for (int r = 0; r < ROWS; r++) {
        for (int c = 0; c < COLS; c++) {
            g[r][c] = grid[r][c];
            if (g[r][c] == 1) {
                sr = r;
                sc = c;
            } else if (g[r][c] != -1) {
                left++;
            }
        }
    }
    g[sr][sc] = 0;
    return walk(g, sr, sc, left);
}

int main(void) {
    int rounds = 20;
    int64_t total = 0, check = 0;
    for (int round = 0; round < rounds; round++) {
        for (int s = 0; s < ROWS * COLS; s++) {
            for (int e = 0; e < ROWS * COLS; e++) {
                if (s == e) continue;
                int64_t grid[ROWS][COLS] = {{0}};
                grid[s / COLS][s % COLS] = 1;
                grid[e / COLS][e % COLS] = 2;
                int64_t p = unique_paths_iii(grid);
                total += p;
                check = (check * 31 + p + s) % 1000000007;
            }
        }
    }
    printf("%d rounds over 380 starts and ends of a 4 x 5 grid: %lld paths, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
