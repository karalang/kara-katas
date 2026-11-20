// LeetCode #1289 bench, in C: the ★ arm (the row above's two smallest path
// sums) on 100 grids of 200 by 200, built once, 300 rounds, every answer
// folded into a checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 200

static int64_t min_falling_path_sum(int64_t grid[N][N], int64_t n) {
    int64_t first = 0, first_col = -1, second = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t next_first = INT64_MAX, next_col = -1, next_second = INT64_MAX;
        for (int64_t j = 0; j < n; j++) {
            int64_t sum = grid[i][j] + (j == first_col ? second : first);
            if (sum < next_first) {
                next_second = next_first;
                next_first = sum;
                next_col = j;
            } else if (sum < next_second) {
                next_second = sum;
            }
        }
        first = next_first;
        first_col = next_col;
        second = next_second;
    }
    return first;
}

static int64_t seed;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    seed = 1289;
    int64_t (*grids)[N][N] = malloc(100 * sizeof(int64_t[N][N]));
    for (int k = 0; k < 100; k++)
        for (int i = 0; i < N; i++)
            for (int j = 0; j < N; j++) grids[k][i][j] = next_random() % 199 - 99;
    int64_t check = 0;
    for (int64_t round = 0; round < 300; round++)
        for (int k = 0; k < 100; k++)
            check = (check * 131 + min_falling_path_sum(grids[k], N) + round + 1000000) % 1000000007;
    printf("300 rounds of 100 grids of 200 by 200: checksum %lld\n", (long long)check);
    return 0;
}
