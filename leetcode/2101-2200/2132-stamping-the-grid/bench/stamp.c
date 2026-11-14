// LeetCode #2132: Stamping the Grid -- the benchmark, the same algorithm
// as stamp.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int possible_to_stamp(int64_t **grid, int64_t m, int64_t n, int64_t stamp_height, int64_t stamp_width) {
    int64_t w = n + 1;
    int64_t *full = calloc((size_t)((m + 1) * w), sizeof(int64_t));
    for (int64_t r = 0; r < m; r++)
        for (int64_t c = 0; c < n; c++)
            full[(r + 1) * w + c + 1] = grid[r][c] + full[r * w + c + 1] + full[(r + 1) * w + c] - full[r * w + c];
    int64_t *marks = calloc((size_t)((m + 1) * w), sizeof(int64_t));
    for (int64_t r = 0; r < m - stamp_height + 1; r++)
        for (int64_t c = 0; c < n - stamp_width + 1; c++) {
            int64_t r2 = r + stamp_height, c2 = c + stamp_width;
            if (full[r2 * w + c2] - full[r * w + c2] - full[r2 * w + c] + full[r * w + c] == 0) {
                marks[r * w + c] += 1;
                marks[r * w + c2] -= 1;
                marks[r2 * w + c] -= 1;
                marks[r2 * w + c2] += 1;
            }
        }
    int ok = 1;
    for (int64_t r = 0; r < m && ok; r++)
        for (int64_t c = 0; c < n; c++) {
            if (r > 0) marks[r * w + c] += marks[(r - 1) * w + c];
            if (c > 0) marks[r * w + c] += marks[r * w + c - 1];
            if (r > 0 && c > 0) marks[r * w + c] -= marks[(r - 1) * w + c - 1];
            if (grid[r][c] == 0 && marks[r * w + c] == 0) {
                ok = 0;
                break;
            }
        }
    free(full);
    free(marks);
    return ok;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2132;
    int64_t *grid[400];
    for (int r = 0; r < 400; r++) {
        grid[r] = malloc(500 * sizeof(int64_t));
        for (int c = 0; c < 500; c++) grid[r][c] = (r % 4 == 3 || c % 4 == 3) ? 1 : 0;
    }
    int64_t stamped = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        int64_t hi = next_random(&seed);
        int64_t at = (hi * 32768 + next_random(&seed)) % 200000;
        int64_t r = at / 500, c = at % 500;
        grid[r][c] = 1 - grid[r][c];
        int64_t h = next_random(&seed) % 3 + 1;
        int64_t w = next_random(&seed) % 3 + 1;
        int64_t fits = possible_to_stamp(grid, 400, 500, h, w);
        grid[r][c] = 1 - grid[r][c];
        stamped += fits;
        check = (check * 31 + fits + at + round) % 1000000007;
    }
    printf("100 solves: %lld stamped, checksum %lld\n", (long long)stamped, (long long)check);
    for (int r = 0; r < 400; r++) free(grid[r]);
    return 0;
}
