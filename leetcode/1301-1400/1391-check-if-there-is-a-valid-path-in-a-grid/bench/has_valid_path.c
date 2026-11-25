// LeetCode #1391 bench, C mirror of the ★ arm: the queue a ring of cell
// pairs as large as the grid.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { M = 299, N = 300 };

static const int64_t WAYS[7][2][2] = {
    {{0, 0}, {0, 0}},   {{0, -1}, {0, 1}}, {{-1, 0}, {1, 0}}, {{0, -1}, {1, 0}},
    {{0, 1}, {1, 0}},   {{0, -1}, {-1, 0}}, {{0, 1}, {-1, 0}},
};
static const int WAY_COUNT[7] = {0, 2, 2, 2, 2, 2, 2};

static bool opens(int street, int64_t dr, int64_t dc) {
    for (int k = 0; k < WAY_COUNT[street]; k++)
        if (WAYS[street][k][0] == dr && WAYS[street][k][1] == dc) return true;
    return false;
}

static int32_t grid[M][N];
static bool seen[M * N];
static int64_t queue[M * N][2];

static bool has_valid_path(int64_t m, int64_t n) {
    for (int64_t k = 0; k < m * n; k++) seen[k] = false;
    int64_t head = 0, tail = 0;
    queue[tail][0] = 0;
    queue[tail][1] = 0;
    tail++;
    seen[0] = true;
    while (head < tail) {
        int64_t r = queue[head][0], c = queue[head][1];
        head++;
        if (r == m - 1 && c == n - 1) return true;
        int street = grid[r][c];
        for (int k = 0; k < WAY_COUNT[street]; k++) {
            int64_t dr = WAYS[street][k][0], dc = WAYS[street][k][1];
            int64_t nr = r + dr, nc = c + dc;
            if (nr < 0 || nr >= m || nc < 0 || nc >= n || seen[nr * n + nc]) continue;
            if (opens(grid[nr][nc], -dr, -dc)) {
                seen[nr * n + nc] = true;
                queue[tail][0] = nr;
                queue[tail][1] = nc;
                tail++;
            }
        }
    }
    return false;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    for (int r = 0; r < M; r++)
        for (int c = 0; c < N; c++) grid[r][c] = 1;
    for (int r = 0; r < M - 1; r++) {
        if (r % 2 == 0) {
            grid[r][N - 1] = 3;
            grid[r + 1][N - 1] = 5;
        } else {
            grid[r][0] = 4;
            grid[r + 1][0] = 6;
        }
    }
    int64_t seed = 1391, check = 0;
    bool whole = has_valid_path(M, N);
    for (int round = 0; round < 3000; round++) {
        seed = (seed + check) % 2147483648LL;
        int64_t cell = next_random(&seed) % (M * N);
        int64_t r = cell / N, c = cell % N;
        int32_t street = grid[r][c];
        grid[r][c] = street % 6 + 1;
        bool got = has_valid_path(M, N);
        grid[r][c] = street;
        check = (check * 131 + (got ? 2 : 1) * (cell + 1)) % 1000000007;
    }
    printf("3000 rounds over a 299 by 300 snake, whole %s: checksum %lld\n", whole ? "true" : "false",
           (long long)check);
    return 0;
}
