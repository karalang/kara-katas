// LeetCode 750 — Number Of Corner Rectangles, bench: the ★ arm (pairs
// of rows) on a 200 x 200 grid that keeps changing.
// Mirrors count_corner_rectangles.kara.
#include <stdint.h>
#include <stdio.h>

#define M 200
#define N 200

static int64_t count_corner_rectangles(const int64_t grid[M][N]) {
    int64_t total = 0;
    for (int a = 0; a < M; a++) {
        for (int b = a + 1; b < M; b++) {
            int64_t k = 0;
            for (int c = 0; c < N; c++)
                if (grid[a][c] == 1 && grid[b][c] == 1) k++;
            total += k * (k - 1) / 2;
        }
    }
    return total;
}

static int64_t seed = 750;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 100;
    static int64_t grid[M][N];
    for (int r = 0; r < M; r++)
        for (int c = 0; c < N; c++) grid[r][c] = next_random() % 2;
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int k = 0; k < 50; k++) {
            int64_t r = next_random() % 200;
            int64_t c = next_random() % 200;
            grid[r][c] = next_random() % 2;
        }
        int64_t k = count_corner_rectangles(grid);
        total += k;
        check = (check * 31 + k) % 1000000007;
    }
    printf("%lld grids of 200 x 200: %lld rectangles in all, checksum %lld\n", (long long)rounds, (long long)total, (long long)check);
    return 0;
}
