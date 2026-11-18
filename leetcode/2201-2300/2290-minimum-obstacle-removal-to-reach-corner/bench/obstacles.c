// LeetCode #2290: Minimum Obstacle Removal to Reach Corner -- the bench,
// the ★ arm in C. A 0-1 breadth-first search over a ring-buffer deque: a
// step onto an empty cell to the front, one onto an obstacle to the back.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { GRIDS = 10, M = 200, N = 200 };

static int64_t minimum_obstacles(const int64_t *grid, int m, int n, int64_t *cost, int64_t *best, int64_t *ring, int cap) {
    for (int i = 0; i < m * n; i++) {
        cost[i] = -1;
        best[i] = INT64_MAX;
    }
    int head = 0, len = 0;
    best[0] = 0;
    ring[0] = 0;
    len = 1;
    static const int moves[4][2] = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
    while (len > 0) {
        int64_t at = ring[head];
        head = (head + 1) % cap;
        len--;
        int r = (int)(at / n), c = (int)(at % n);
        if (cost[at] >= 0) continue;
        int64_t here = best[at];
        cost[at] = here;
        if (r == m - 1 && c == n - 1) return here;
        for (int k = 0; k < 4; k++) {
            int nr = r + moves[k][0], nc = c + moves[k][1];
            if (nr < 0 || nc < 0 || nr >= m || nc >= n) continue;
            int64_t to = (int64_t)nr * n + nc;
            int64_t step = grid[to];
            if (here + step < best[to]) {
                best[to] = here + step;
                if (step == 0) {
                    head = (head - 1 + cap) % cap;
                    ring[head] = to;
                } else {
                    ring[(head + len) % cap] = to;
                }
                len++;
            }
        }
    }
    return best[m * n - 1];
}

static int64_t seed = 2290;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t grids[GRIDS][M * N];
    for (int g = 0; g < GRIDS; g++) {
        for (int i = 0; i < M * N; i++) grids[g][i] = next_random() % 10 < 4 ? 1 : 0;
        grids[g][0] = 0;
        grids[g][M * N - 1] = 0;
    }
    // each cell is pushed at most once per neighbour that lowers it
    int cap = 4 * M * N + 1;
    int64_t *cost = malloc(sizeof(int64_t) * M * N);
    int64_t *best = malloc(sizeof(int64_t) * M * N);
    int64_t *ring = malloc(sizeof(int64_t) * cap);
    int64_t check = 0;
    for (int p = 0; p < 5; p++) {
        int64_t total = 0;
        for (int g = 0; g < GRIDS; g++) total += minimum_obstacles(grids[g], M, N, cost, best, ring, cap);
        check = (check * 31 + total) % 1000000007;
    }
    printf("5 passes over 10 grids of 200x200: checksum %lld\n", (long long)check);
    free(cost);
    free(best);
    free(ring);
    return 0;
}
