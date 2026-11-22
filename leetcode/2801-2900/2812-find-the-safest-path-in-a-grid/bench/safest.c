// LeetCode #2812: Find the Safest Path in a Grid -- the bench in C: the ★
// arm over 10 grids of 400 by 400, a thief in about one cell of 2000, all
// drawn first, then each answered 3 times. The queues are arrays of n * n
// cells, each cell entering a search once.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 400
#define COUNT 10

static const int DR[4] = {0, 1, 0, -1};
static const int DC[4] = {1, 0, -1, 0};

static int64_t seed = 2812;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t grids[COUNT][N][N];
static int64_t dist[N][N];
static char seen[N][N];
static int64_t queue_r[N * N], queue_c[N * N];

static void thief_distances(int64_t (*grid)[N], int64_t n) {
    int64_t head = 0, tail = 0;
    for (int64_t r = 0; r < n; r++)
        for (int64_t c = 0; c < n; c++) {
            dist[r][c] = -1;
            if (grid[r][c] == 1) {
                dist[r][c] = 0;
                queue_r[tail] = r;
                queue_c[tail++] = c;
            }
        }
    while (head < tail) {
        int64_t r = queue_r[head], c = queue_c[head++];
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + DR[d], nc = c + DC[d];
            if (nr >= 0 && nr < n && nc >= 0 && nc < n && dist[nr][nc] == -1) {
                dist[nr][nc] = dist[r][c] + 1;
                queue_r[tail] = nr;
                queue_c[tail++] = nc;
            }
        }
    }
}

static int reachable(int64_t n, int64_t s) {
    if (dist[0][0] < s) return 0;
    memset(seen, 0, sizeof seen);
    seen[0][0] = 1;
    int64_t head = 0, tail = 0;
    queue_r[tail] = 0;
    queue_c[tail++] = 0;
    while (head < tail) {
        int64_t r = queue_r[head], c = queue_c[head++];
        if (r == n - 1 && c == n - 1) return 1;
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + DR[d], nc = c + DC[d];
            if (nr >= 0 && nr < n && nc >= 0 && nc < n && !seen[nr][nc] && dist[nr][nc] >= s) {
                seen[nr][nc] = 1;
                queue_r[tail] = nr;
                queue_c[tail++] = nc;
            }
        }
    }
    return 0;
}

static int64_t maximum_safeness_factor(int64_t (*grid)[N], int64_t n) {
    thief_distances(grid, n);
    int64_t lo = 0;
    int64_t hi = dist[0][0] < dist[n - 1][n - 1] ? dist[0][0] : dist[n - 1][n - 1];
    while (lo < hi) {
        int64_t mid = (lo + hi + 1) / 2;
        if (reachable(n, mid))
            lo = mid;
        else
            hi = mid - 1;
    }
    return lo;
}

int main(void) {
    int rounds = 3;
    for (int g = 0; g < COUNT; g++) {
        for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++) grids[g][r][c] = next_random() % 2000 == 0 ? 1 : 0;
        int64_t r = next_random() % N;
        int64_t c = next_random() % N;
        grids[g][r][c] = 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int g = 0; g < COUNT; g++) {
            int64_t a = maximum_safeness_factor(grids[g], N);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    printf("%d grids of %d, %d rounds: safeness sums to %lld, checksum %lld\n", COUNT, N, rounds, (long long)total, (long long)check);
    return 0;
}
