// LeetCode #2257: Count Unguarded Cells in the Grid -- the benchmark's C
// mirror of unguarded.kara: a grid of marks and a walk from every guard in
// each of the four directions until a wall, a guard or the edge.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define CELLS 100000
#define GUARDS 2000
#define WALLS 10000

static int8_t grid[CELLS];
static uint8_t taken[CELLS];
static int64_t cells[GUARDS + WALLS][2];

static const int64_t DR[4] = {-1, 1, 0, 0};
static const int64_t DC[4] = {0, 0, -1, 1};

// 0 empty, 1 seen, 2 guard, 3 wall; guards are cells[0..g), walls the rest
static int64_t count_unguarded(int64_t m, int64_t n, int64_t g, int64_t w) {
    memset(grid, 0, (size_t)(m * n));
    for (int64_t i = 0; i < g; i++) grid[cells[i][0] * n + cells[i][1]] = 2;
    for (int64_t i = g; i < g + w; i++) grid[cells[i][0] * n + cells[i][1]] = 3;
    for (int64_t i = 0; i < g; i++) {
        for (int d = 0; d < 4; d++) {
            int64_t r = cells[i][0] + DR[d], c = cells[i][1] + DC[d];
            while (r >= 0 && r < m && c >= 0 && c < n && grid[r * n + c] < 2) {
                grid[r * n + c] = 1;
                r += DR[d];
                c += DC[d];
            }
        }
    }
    int64_t count = 0;
    for (int64_t k = 0; k < m * n; k++) count += grid[k] == 0;
    return count;
}

static int64_t seed = 2257;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

static void place(int64_t m, int64_t n, int64_t total) {
    memset(taken, 0, (size_t)(m * n));
    int64_t len = 0;
    while (len < total) {
        int64_t k = wide_random() % (m * n);
        if (!taken[k]) {
            taken[k] = 1;
            cells[len][0] = k / n;
            cells[len][1] = k % n;
            len++;
        }
    }
}

int main(void) {
    static const int64_t shapes[3][2] = {{1, 100000}, {250, 400}, {100000, 1}};
    int64_t check = 0;
    for (int t = 0; t < 300; t++) {
        int64_t m = shapes[t % 3][0], n = shapes[t % 3][1];
        place(m, n, GUARDS + WALLS);
        check = (check * 31 + count_unguarded(m, n, GUARDS, WALLS) + 1) % 1000000007;
    }
    printf("300 grids of 10^5 cells: checksum %lld\n", (long long)check);
    return 0;
}
