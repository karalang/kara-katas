// LeetCode #1162: As Far from Land as Possible -- C mirror of the Kāra ★
// arm: a breadth-first search from every land cell at once, over a flat
// distance array and a queue of cell indices.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100

static int64_t dist[N * N];
static int64_t queue[N * N];

static int64_t max_distance(int64_t n, int64_t grid[N][N]) {
    int64_t len = 0;
    for (int64_t i = 0; i < n * n; i++) dist[i] = -1;
    for (int64_t i = 0; i < n; i++)
        for (int64_t j = 0; j < n; j++)
            if (grid[i][j] == 1) {
                dist[i * n + j] = 0;
                queue[len++] = i * n + j;
            }
    if (len == 0 || len == n * n) return -1;
    static const int64_t di[4] = {-1, 1, 0, 0}, dj[4] = {0, 0, -1, 1};
    int64_t head = 0, far = 0;
    while (head < len) {
        int64_t cell = queue[head++];
        int64_t i = cell / n, j = cell % n;
        far = dist[cell];
        for (int k = 0; k < 4; k++) {
            int64_t a = i + di[k], b = j + dj[k];
            if (a >= 0 && a < n && b >= 0 && b < n && dist[a * n + b] < 0) {
                dist[a * n + b] = far + 1;
                queue[len++] = a * n + b;
            }
        }
    }
    return far;
}

static int64_t seed = 1162;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t grids[16][N][N];

int main(void) {
    static const int64_t odds[8] = {1, 2, 5, 10, 50, 200, 500, 900};
    for (int k = 0; k < 16; k++) {
        int64_t o = odds[k % 8];
        for (int a = 0; a < N; a++)
            for (int b = 0; b < N; b++) grids[k][a][b] = next_random() % 1000 < o ? 1 : 0;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 300; r++)
        for (int k = 0; k < 16; k++) {
            int64_t a = next_random() % 100;
            int64_t b = next_random() % 100;
            grids[k][a][b] = 1 - grids[k][a][b];
            int64_t d = max_distance(N, grids[k]);
            total += d;
            check = (check * 31 + d + 1) % 1000000007;
        }
    printf("300 rounds over 16 grids of 100 by 100: total %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
