// LeetCode #2245: Maximum Trailing Zeros in a Cornered Path -- the
// benchmark's C mirror of zeros.kara: prefix sums of the twos and fives
// of each row and column, in flat arrays, every cell tried as the
// corner.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define M 250
#define N 400

static int64_t grid[M][N];
static int64_t row_twos[M][N + 1], row_fives[M][N + 1];
static int64_t col_twos[M + 1][N], col_fives[M + 1][N];

static int64_t count_factor(int64_t v, int64_t p) {
    int64_t count = 0;
    while (v % p == 0) {
        v /= p;
        count++;
    }
    return count;
}

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t max_trailing_zeros(int m, int n) {
    for (int i = 0; i < m; i++) row_twos[i][0] = row_fives[i][0] = 0;
    for (int j = 0; j < n; j++) col_twos[0][j] = col_fives[0][j] = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            int64_t t = count_factor(grid[i][j], 2);
            int64_t f = count_factor(grid[i][j], 5);
            row_twos[i][j + 1] = row_twos[i][j] + t;
            row_fives[i][j + 1] = row_fives[i][j] + f;
            col_twos[i + 1][j] = col_twos[i][j] + t;
            col_fives[i + 1][j] = col_fives[i][j] + f;
        }
    }
    int64_t best = 0;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            int64_t ht[2] = {row_twos[i][j + 1], row_twos[i][n] - row_twos[i][j]};
            int64_t hf[2] = {row_fives[i][j + 1], row_fives[i][n] - row_fives[i][j]};
            int64_t vt[2] = {col_twos[i][j], col_twos[m][j] - col_twos[i + 1][j]};
            int64_t vf[2] = {col_fives[i][j], col_fives[m][j] - col_fives[i + 1][j]};
            for (int a = 0; a < 2; a++)
                for (int b = 0; b < 2; b++) {
                    int64_t z = min64(ht[a] + vt[b], hf[a] + vf[b]);
                    if (z > best) best = z;
                }
        }
    }
    return best;
}

static int64_t seed = 2245;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int g = 0; g < 40; g++) {
        for (int i = 0; i < M; i++)
            for (int j = 0; j < N; j++) grid[i][j] = next_random() % 1000 + 1;
        check = (check * 31 + max_trailing_zeros(M, N) + 1) % 1000000007;
    }
    printf("40 grids of 250 x 400: checksum %lld\n", (long long)check);
    return 0;
}
