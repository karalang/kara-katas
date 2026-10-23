// LeetCode #892 bench: the ★ arm (six faces a cube, less the shared ones)
// on 400 random grids of 50 by 50, built once; then 80 passes, each
// raising one tower of every grid by a cube and measuring every grid
// again. The same algorithm as surface_area.kara.
#include <stdint.h>
#include <stdio.h>

#define N 50
#define GRIDS 400

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t surface_area(int64_t grid[N][N], int64_t n) {
    int64_t area = 0;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = 0; j < n; j++) {
            int64_t v = grid[i][j];
            if (v > 0) area += 4 * v + 2;
            if (i + 1 < n) area -= 2 * min64(v, grid[i + 1][j]);
            if (j + 1 < n) area -= 2 * min64(v, grid[i][j + 1]);
        }
    }
    return area;
}

static int64_t seed = 892;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t grids[GRIDS][N][N];

int main(void) {
    for (int g = 0; g < GRIDS; g++)
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++) grids[g][i][j] = next_random() % 51;
    int64_t total = 0, check = 0;
    for (int64_t pass = 0; pass < 80; pass++) {
        for (int64_t g = 0; g < GRIDS; g++) {
            int64_t i = (pass * 7 + g) % 50;
            int64_t j = (pass * 13 + g * 3) % 50;
            grids[g][i][j] += 1;
            int64_t got = surface_area(grids[g], N);
            total += got;
            check = (check * 131 + got) % 1000000007;
        }
    }
    printf("32000 measurements of 400 grids of 50 by 50: surface area %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
